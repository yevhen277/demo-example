import flet as ft
import os
from ui.folder_card import FolderCard
from config import *
from core.file_scanner import FileScanner
from core.data_manager import data_manager
import threading

def get_main_layout(page: ft.Page):
    
    saved_theme = data_manager.get_config().get("theme_color", PRIMARY_COLOR)
    from config import set_primary_color
    set_primary_color(saved_theme)
    current_primary_color = saved_theme
    
    # === 1. 定义状态和控件引用 ===
    cards_list_view = ft.ListView(
        expand=True,
        spacing=10,
        padding=ft.padding.only(right=10),
    )
    
    # 当前选中的文件夹路径和原始名称
    selected_folder_path = {"value": None}
    selected_folder_name = {"value": None}
    current_root_path = {"value": None}
    current_filter_tag = {"value": None}

    # === 2. 右侧面板控件定义（沉浸式编辑）===
    detail_path = ft.Text("", size=14, color=TEXT_SECONDARY, font_family=FONT_FAMILY, selectable=True)
    
    # 标题编辑框（沉浸式）
    detail_alias_field = ft.TextField(
        value="",
        text_style=ft.TextStyle(
            size=32,
            weight="bold",
            color=TEXT_PRIMARY,
            font_family=FONT_FAMILY,
        ),
        border="none",
        bgcolor="transparent",
        content_padding=ft.padding.all(0),
        hint_text="点击设置自定义名称",
        hint_style=ft.TextStyle(color=TEXT_SECONDARY, font_family=FONT_FAMILY),
        cursor_color=current_primary_color,
    )
    
    # 标签容器
    tags_container = ft.Row(spacing=8, wrap=True, scroll=ft.ScrollMode.AUTO)
    
    # 备注编辑框（沉浸式）
    detail_note_field = ft.TextField(
        value="",
        text_style=ft.TextStyle(
            size=14,
            color=TEXT_SECONDARY,
            font_family=FONT_FAMILY,
        ),
        border="none",
        bgcolor="transparent",
        multiline=True,
        min_lines=3,
        max_lines=10,
        content_padding=ft.padding.all(0),
        hint_text="这里可以写很长的备注...",
        hint_style=ft.TextStyle(color=TEXT_SECONDARY, font_family=FONT_FAMILY),
        cursor_color=current_primary_color,
    )
    
    # 默认提示控件
    empty_state_text = ft.Text("文件夹详情页", size=24, color=TEXT_SECONDARY, font_family=FONT_FAMILY, weight="bold")
    empty_state_container = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(expand=True),
                ft.Row(
                    controls=[
                        ft.Container(expand=True),
                        empty_state_text,
                        ft.Container(expand=True),
                    ]
                ),
                ft.Container(expand=True),
            ],
            expand=True,
        ),
        expand=True,
        alignment=ft.alignment.center,
    )
    
    # 当前标签列表
    current_tags = {"value": []}
    
    def open_folder_in_explorer(e):
        """打开文件夹按钮点击事件处理"""
        folder_path = selected_folder_path["value"]
        
        if not folder_path:
            show_snackbar("请先选择一个文件夹", error=True)
            return
        
        if not os.path.exists(folder_path):
            show_snackbar(f"文件夹不存在: {folder_path}", error=True)
            return
        
        try:
            import subprocess
            import platform
            
            system = platform.system()
            if system == "Windows":
                os.startfile(folder_path)
            elif system == "Darwin":
                subprocess.run(["open", folder_path], check=True)
            else:
                subprocess.run(["xdg-open", folder_path], check=True)
            
            show_snackbar(f"已打开文件夹: {os.path.basename(folder_path)}")
        except PermissionError:
            show_snackbar("权限不足，无法打开该文件夹", error=True)
        except FileNotFoundError:
            show_snackbar("找不到文件管理器", error=True)
        except subprocess.CalledProcessError:
            show_snackbar("打开文件夹失败", error=True)
        except Exception as ex:
            show_snackbar(f"打开文件夹时发生错误: {str(ex)}", error=True)
    
    def show_snackbar(message: str, error: bool = False):
        """显示提示消息"""
        snackbar = ft.SnackBar(
            content=ft.Text(
                message,
                color=TEXT_WHITE,
                font_family=FONT_FAMILY,
            ),
            bgcolor=ERROR_COLOR if error else current_primary_color,
            duration=3000,
        )
        page.snack_bar = snackbar
        snackbar.open = True
        page.update()

    def hide_current_folder(e):
        """隐藏当前选中的文件夹"""
        folder_path = selected_folder_path["value"]
        
        if not folder_path:
            show_snackbar("请先选择一个文件夹", error=True)
            return
        
        try:
            data_manager.set_hidden(folder_path, True)
            
            show_snackbar("已隐藏，可在「系统设置」中恢复")
            
            clear_detail_panel()
            
            if current_root_path["value"]:
                load_folder_list(current_root_path["value"])
                
        except Exception as ex:
            show_snackbar(f"隐藏失败: {str(ex)}", error=True)

    def clear_detail_panel():
        """清空右侧详情面板，恢复到未选中状态"""
        selected_folder_path["value"] = None
        selected_folder_name["value"] = None
        current_tags["value"] = []
        
        detail_alias_field.value = ""
        detail_path.value = ""
        detail_note_field.value = ""
        
        detail_content.visible = False
        empty_state_container.visible = True
        
        detail_alias_field.update()
        detail_path.update()
        detail_note_field.update()
        render_tags()
        detail_content.update()
        empty_state_container.update()

    stats_notes_text = ft.Text("0", size=24, weight="bold", color=TEXT_PRIMARY, font_family=FONT_FAMILY)
    stats_tags_text = ft.Text("0", size=24, weight="bold", color=TEXT_PRIMARY, font_family=FONT_FAMILY)
    stats_days_text = ft.Text("0天", size=24, weight="bold", color=TEXT_PRIMARY, font_family=FONT_FAMILY)

    def update_stats(refresh_ui=True):
        """更新统计数据"""
        notes_count = data_manager.get_notes_count()
        tags_count = data_manager.get_tags_count()
        install_days = data_manager.get_install_days()
        
        stats_notes_text.value = str(notes_count)
        stats_tags_text.value = str(tags_count)
        stats_days_text.value = f"{install_days}天"
        
        if refresh_ui:
            stats_notes_text.update()
            stats_tags_text.update()
            stats_days_text.update()

    def save_alias_on_blur(e):
        """标题失去焦点时自动保存"""
        folder_path = selected_folder_path["value"]
        if not folder_path:
            return
        alias = detail_alias_field.value.strip()
        data_manager.update_alias(folder_path, alias)
        update_stats()
        if current_root_path["value"]:
            load_folder_list(current_root_path["value"])
    
    def save_note_on_blur(e):
        """备注失去焦点时自动保存"""
        folder_path = selected_folder_path["value"]
        if not folder_path:
            return
        note = detail_note_field.value.strip()
        data_manager.update_note(folder_path, note)
        update_stats()
        if current_root_path["value"]:
            load_folder_list(current_root_path["value"])
    
    detail_alias_field.on_blur = save_alias_on_blur
    detail_note_field.on_blur = save_note_on_blur
    
    def render_tags():
        """渲染标签列表"""
        tags_container.controls.clear()
        for tag in current_tags["value"]:
            tag_chip = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text(f"# {tag}", size=11, color=TAG_TEXT, font_family=FONT_FAMILY),
                        ft.Container(
                            content=ft.IconButton(
                                icon=ft.icons.CLOSE,
                                icon_size=10,
                                icon_color=TAG_TEXT,
                                on_click=lambda e, t=tag: remove_tag(t),
                                width=20,
                                height=20,
                            ),
                            margin=ft.margin.only(left=2),
                        ),
                    ],
                    spacing=0,
                    alignment=ft.MainAxisAlignment.CENTER,
                    tight=True,
                ),
                bgcolor=TAG_BG,
                padding=ft.padding.only(left=8, right=2, top=2, bottom=2),
                border_radius=4,
            )
            tags_container.controls.append(tag_chip)
        
        # 添加标签按钮 - 使用简单的 IconButton
        add_tag_btn = ft.IconButton(
            icon=ft.icons.ADD,
            icon_color=current_primary_color,
            icon_size=20,
            tooltip="添加标签",
            on_click=lambda e: show_new_tag_dialog(),
        )
        tags_container.controls.append(add_tag_btn)
        tags_container.update()
    
    def add_tag(tag: str):
        """添加标签"""
        tag = tag.strip()
        if not tag or tag in current_tags["value"]:
            return
        current_tags["value"].append(tag)
        save_tags()
        render_tags()
    
    def remove_tag(tag: str):
        """删除标签"""
        if tag in current_tags["value"]:
            current_tags["value"].remove(tag)
            save_tags()
            render_tags()
    
    def build_tags_list():
        """构建标签列表控件（可点击筛选）"""
        all_tags = data_manager.get_all_tags()
        tag_controls = []
        for tag in all_tags:
            is_selected = current_filter_tag["value"] == tag
            tag_btn = ft.Container(
                content=ft.Text(f"# {tag}", size=14, color=TEXT_WHITE if is_selected else current_primary_color, font_family=FONT_FAMILY),
                bgcolor=current_primary_color if is_selected else "transparent",
                padding=ft.padding.only(left=8, right=8, top=4, bottom=4),
                border_radius=6,
                on_click=on_sidebar_tag_click,
                data=tag,
            )
            tag_controls.append(tag_btn)
        if not tag_controls:
            tag_controls.append(
                ft.Text("暂无标签", size=12, color=TEXT_SECONDARY, font_family=FONT_FAMILY)
            )
        return tag_controls

    def on_sidebar_tag_click(e):
        """侧边栏标签点击事件"""
        tag = e.control.data
        filter_by_tag(tag)

    show_all_btn = ft.TextButton(
        content=ft.Text("显示全部", size=12, color=current_primary_color, font_family=FONT_FAMILY),
        on_click=lambda e: clear_filter(),
        visible=False,
    )

    def filter_by_tag(tag: str):
        """按标签筛选文件夹"""
        current_filter_tag["value"] = tag
        show_all_btn.visible = True
        
        cards_list_view.controls.clear()
        
        folder_paths = data_manager.get_folders_by_tag(tag)
        
        if not folder_paths:
            cards_list_view.controls.append(ft.Text(f"没有标签为「{tag}」的文件夹", color=TEXT_SECONDARY, font_family=FONT_FAMILY))
        else:
            for folder_path in folder_paths:
                info = data_manager.get_info(folder_path)
                folder_name = os.path.basename(folder_path)
                
                try:
                    stat = os.stat(folder_path)
                    mtime_str = FileScanner._format_time(stat.st_mtime)
                    size_str = FileScanner._format_size(FileScanner._get_dir_size(folder_path))
                except:
                    mtime_str = ""
                    size_str = ""
                
                card = FolderCard(
                    folder_name=folder_name,
                    folder_path=folder_path,
                    tags=info['tags'],
                    note=info['note'],
                    alias=info.get('alias', ''),
                    time_str=mtime_str,
                    size_str=size_str,
                    on_edit_click=on_card_edit_click,
                    on_click=lambda e, fp=folder_path, fn=folder_name, al=info.get('alias', ''), ts=info['tags'], nt=info['note']: on_card_click(fp, fn, al, ts, nt)
                )
                cards_list_view.controls.append(card)
        
        refresh_tags_list()
        cards_list_view.update()
        show_all_btn.update()
    
    def clear_filter():
        """清除筛选，显示全部"""
        current_filter_tag["value"] = None
        show_all_btn.visible = False
        if current_root_path["value"]:
            load_folder_list(current_root_path["value"])
        refresh_tags_list()
        show_all_btn.update()

    def refresh_tags_list(refresh_ui=True):
        """刷新标签列表"""
        tags_list_column.controls.clear()
        tags_list_column.controls.extend(build_tags_list())
        if refresh_ui:
            tags_list_column.update()

    tags_list_column = ft.Column(
        controls=build_tags_list(),
        spacing=8,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    def save_tags():
        """保存标签到数据管理器"""
        folder_path = selected_folder_path["value"]
        if not folder_path:
            return
        data_manager.update_tags(folder_path, current_tags["value"])
        refresh_tags_list()
        if current_root_path["value"]:
            load_folder_list(current_root_path["value"])
    
    new_tag_field = ft.TextField(
        hint_text="输入新标签名称",
        text_style=ft.TextStyle(font_family=FONT_FAMILY),
        autofocus=True,
        width=300,
    )
    
    existing_tags_container = ft.Row(spacing=8, wrap=True, scroll=ft.ScrollMode.AUTO)
    
    def build_existing_tags_buttons():
        """构建已有标签按钮列表"""
        all_tags = data_manager.get_all_tags()
        existing_tags_container.controls.clear()
        for tag in all_tags:
            if tag not in current_tags["value"]:
                tag_btn = ft.Container(
                    content=ft.Text(f"# {tag}", size=12, color=TAG_TEXT, font_family=FONT_FAMILY),
                    bgcolor=TAG_BG,
                    padding=ft.padding.only(left=8, right=8, top=4, bottom=4),
                    border_radius=4,
                    on_click=lambda e, t=tag: select_existing_tag(t),
                )
                existing_tags_container.controls.append(tag_btn)
        if not existing_tags_container.controls:
            existing_tags_container.controls.append(
                ft.Text("暂无已有标签", size=11, color=TEXT_SECONDARY, font_family=FONT_FAMILY)
            )
    
    def select_existing_tag(tag: str):
        """选择已有标签"""
        add_tag(tag)
        close_new_tag_dialog()
    
    def close_new_tag_dialog(e=None):
        new_tag_dialog.open = False
        page.update()
    
    def confirm_new_tag(e):
        tag = new_tag_field.value.strip()
        if tag and tag not in current_tags["value"]:
            add_tag(tag)
            new_tag_field.value = ""
        close_new_tag_dialog()
    
    new_tag_dialog = ft.AlertDialog(
        title=ft.Text("添加标签", size=16, weight="bold", color=TEXT_PRIMARY, font_family=FONT_FAMILY),
        content=ft.Column(
            controls=[
                new_tag_field,
                ft.Container(height=10),
                ft.Text("或选择已有标签：", size=11, color=TEXT_SECONDARY, font_family=FONT_FAMILY),
                ft.Container(
                    content=existing_tags_container,
                    width=300,
                ),
            ],
            tight=True,
            spacing=5,
        ),
        actions=[
            ft.TextButton("取消", on_click=close_new_tag_dialog),
            ft.ElevatedButton("添加", on_click=confirm_new_tag, bgcolor=ACCENT_COLOR, color=TEXT_PRIMARY),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    
    def show_new_tag_dialog():
        new_tag_field.value = ""
        build_existing_tags_buttons()
        page.dialog = new_tag_dialog
        new_tag_dialog.open = True
        page.update()
    
    def update_detail_panel(folder_path, folder_name, alias, tags, note):
        """更新右侧面板内容"""
        selected_folder_path["value"] = folder_path
        selected_folder_name["value"] = folder_name
        current_tags["value"] = tags.copy() if tags else []
        
        # 更新标题：如果有别名显示别名，否则显示文件夹原名
        detail_alias_field.value = alias if alias else folder_name
        detail_path.value = folder_path
        detail_note_field.value = note if note else ""
        
        # 渲染标签
        render_tags()
        
        # 显示详情内容，隐藏空状态
        detail_content.visible = True
        empty_state_container.visible = False
        
        detail_alias_field.update()
        detail_path.update()
        detail_note_field.update()
        detail_content.update()
        empty_state_container.update()

    # === 3. 核心逻辑函数 ===
    def on_card_click(folder_path, folder_name, alias, tags, note):
        """卡片点击事件"""
        update_detail_panel(folder_path, folder_name, alias, tags, note)

    def on_card_edit_click(card_data):
        """卡片编辑按钮点击事件 - 选中文件夹"""
        folder_path = card_data["folder_path"]
        folder_name = card_data["folder_name"]
        alias = card_data.get("alias", "")
        tags = card_data["tags"]
        note = card_data["note"]
        update_detail_panel(folder_path, folder_name, alias, tags, note)

    def load_folder_list(root_path, refresh_ui=True):
        """加载文件夹列表"""
        if not root_path:
            return
        
        current_root_path["value"] = root_path
        current_filter_tag["value"] = None
        show_all_btn.visible = False
        current_path_display.value = root_path
        if refresh_ui:
            current_path_display.update()
            show_all_btn.update()
        refresh_tags_list(refresh_ui=refresh_ui)
        
        cards_list_view.controls.clear()
        cards_list_view.controls.append(ft.Text("正在扫描...", color=TEXT_SECONDARY, font_family=FONT_FAMILY))
        if refresh_ui:
            cards_list_view.update()

        folders = FileScanner.get_subfolders(root_path)
        cards_list_view.controls.clear()

        if not folders:
            cards_list_view.controls.append(ft.Text("该目录下没有文件夹", color=TEXT_SECONDARY, font_family=FONT_FAMILY))
        else:
            visible_count = 0
            for f in folders:
                info = data_manager.get_info(f['path'])
                
                if info.get('hidden', False):
                    continue
                
                visible_count += 1
                card = FolderCard(
                    folder_name=f['name'],
                    folder_path=f['path'],
                    tags=info['tags'],
                    note=info['note'],
                    alias=info.get('alias', ''),
                    time_str=f['mtime_str'],
                    size_str=f['size_str'],
                    on_edit_click=on_card_edit_click,
                    on_click=lambda e, fp=f['path'], fn=f['name'], al=info.get('alias', ''), ts=info['tags'], nt=info['note']: on_card_click(fp, fn, al, ts, nt)
                )
                cards_list_view.controls.append(card)
            
            if visible_count == 0:
                cards_list_view.controls.append(ft.Text("所有文件夹已隐藏", color=TEXT_SECONDARY, font_family=FONT_FAMILY))

        if refresh_ui:
            cards_list_view.update()

    # === 5. 文件选择器 ===
    file_picker = ft.FilePicker(
        on_result=lambda e: load_folder_list(e.path) if e.path else None
    )
    page.overlay.append(file_picker)

    # === 5.5 系统设置对话框 ===
    THEME_COLORS = [
        {"name": "蓝色", "color": "#3794FF"},
        {"name": "绿色", "color": "#58C28D"},
        {"name": "粉色", "color": "#DF95B8"},
        {"name": "橙色", "color": "#F0942B"},
        {"name": "浅蓝", "color": "#AFDBF2"},
        {"name": "浅绿", "color": "#B6E8C2"},
        {"name": "浅紫", "color": "#B880EC"},
        {"name": "浅粉", "color": "#FCDDE6"},
        {"name": "浅黄", "color": "#FCEDAB"},
    ]
    
    current_theme_color = {"value": data_manager.get_config().get("theme_color", PRIMARY_COLOR)}
    
    hidden_folders_list = ft.Column(
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
    )
    
    def build_hidden_folders_list():
        """构建隐藏文件夹列表"""
        hidden_folders_list.controls.clear()
        hidden_folders = data_manager.get_hidden_folders()
        
        if not hidden_folders:
            hidden_folders_list.controls.append(
                ft.Text("没有被隐藏的文件夹", color=TEXT_SECONDARY, font_family=FONT_FAMILY, size=13)
            )
        else:
            for folder in hidden_folders:
                display_name = folder.get("alias") or os.path.basename(folder["path"])
                folder_path = folder["path"]
                
                item = ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Text(display_name, size=14, color=TEXT_PRIMARY, font_family=FONT_FAMILY, weight="bold"),
                                    ft.Text(folder_path, size=11, color=TEXT_SECONDARY, font_family=FONT_FAMILY),
                                ],
                                spacing=2,
                                expand=True,
                            ),
                            ft.TextButton(
                                content=ft.Text("恢复显示", color=current_primary_color, font_family=FONT_FAMILY),
                                on_click=lambda e, p=folder_path: restore_folder(p),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    padding=ft.padding.all(10),
                    bgcolor=CARD_BG,
                    border_radius=8,
                )
                hidden_folders_list.controls.append(item)
    
    def restore_folder(folder_path):
        """恢复隐藏的文件夹"""
        data_manager.set_hidden(folder_path, False)
        build_hidden_folders_list()
        page.update()
        
        if current_root_path["value"]:
            parent_path = os.path.dirname(folder_path)
            if parent_path == current_root_path["value"]:
                load_folder_list(current_root_path["value"])
        
        show_snackbar("已恢复显示")
    
    def on_theme_color_select(color):
        """选择主题颜色"""
        from config import set_primary_color
        current_theme_color["value"] = color
        set_primary_color(color)
        data_manager.update_config("theme_color", color)
        print(f"主题颜色已选择: {color}")
        build_theme_colors()
        page.update()
        show_snackbar(f"主题颜色已保存，重启应用后生效")
    
    theme_colors_row = ft.Row(spacing=10)
    
    def build_theme_colors():
        """构建主题颜色选择区域"""
        theme_colors_row.controls.clear()
        for theme in THEME_COLORS:
            is_selected = current_theme_color["value"] == theme["color"]
            color_btn = ft.Container(
                content=ft.Container(
                    content=ft.Icon(
                        ft.icons.CHECK,
                        color=TEXT_WHITE,
                        size=16,
                    ) if is_selected else None,
                    alignment=ft.alignment.center,
                ),
                width=40,
                height=40,
                bgcolor=theme["color"],
                border_radius=8,
                border=ft.border.all(3, TEXT_WHITE) if is_selected else ft.border.all(1, ACCENT_COLOR),
                on_click=lambda e, c=theme["color"]: on_theme_color_select(c),
                ink=True,
            )
            theme_colors_row.controls.append(color_btn)
    
    settings_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("系统设置", size=20, weight="bold", color=TEXT_PRIMARY, font_family=FONT_FAMILY),
        content=ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("主题颜色", size=14, color=TEXT_SECONDARY, font_family=FONT_FAMILY),
                    theme_colors_row,
                    ft.Divider(height=20, color=ACCENT_COLOR),
                    ft.Text("隐藏文件夹管理", size=14, color=TEXT_SECONDARY, font_family=FONT_FAMILY),
                    ft.Container(
                        content=hidden_folders_list,
                        height=200,
                        width=400,
                    ),
                ],
                spacing=10,
            ),
            width=450,
        ),
        actions=[
            ft.TextButton(
                content=ft.Text("关闭", color=TEXT_PRIMARY, font_family=FONT_FAMILY),
                on_click=lambda e: close_settings_dialog()
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=lambda e: None,
    )
    
    def open_settings_dialog(e):
        """打开系统设置对话框"""
        build_theme_colors()
        build_hidden_folders_list()
        page.dialog = settings_dialog
        settings_dialog.open = True
        page.update()
    
    def close_settings_dialog():
        """关闭系统设置对话框"""
        settings_dialog.open = False
        page.update()

    sidebar = ft.Container(
        width=250,
        bgcolor=SIDEBAR_BG,
        padding=ft.padding.only(top=30, left=20, right=20, bottom=10),
        content=ft.Column(
            controls=[
                ft.Text("UniFolder", size=28, weight="bold", color=current_primary_color, font_family=FONT_FAMILY),
                ft.Container(height=30),
                
                ft.Row(
                    controls=[
                        ft.Column([
                            stats_notes_text,
                            ft.Text("已备注", size=10, color=TEXT_SECONDARY, font_family=FONT_FAMILY),
                        ], spacing=2),
                        ft.Container(width=20),
                        ft.Column([
                            stats_tags_text,
                            ft.Text("已有标签", size=10, color=TEXT_SECONDARY, font_family=FONT_FAMILY),
                        ], spacing=2),
                        ft.Container(width=20),
                        ft.Column([
                            stats_days_text,
                            ft.Text("已使用", size=10, color=TEXT_SECONDARY, font_family=FONT_FAMILY),
                        ], spacing=2),
                    ]
                ),
                ft.Container(height=30),
                
                ft.ElevatedButton(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.icons.FOLDER_OPEN, color=BG_COLOR),
                            ft.Text("打开目录", color=BG_COLOR, font_family=FONT_FAMILY),
                        ],
                        spacing=8,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    bgcolor=current_primary_color,
                    on_click=lambda _: file_picker.get_directory_path(),
                    width=210,
                    height=50,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                ),
                ft.Container(height=10),
                
                ft.OutlinedButton(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.icons.SETTINGS, color=current_primary_color),
                            ft.Text("系统设置", color=current_primary_color, font_family=FONT_FAMILY),
                        ],
                        spacing=8,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    on_click=open_settings_dialog,
                    width=210,
                    height=50,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        side=ft.BorderSide(1, current_primary_color),
                        bgcolor=SETTINGS_BTN_BG,
                    ),
                ),
                ft.Container(height=30),
                
                ft.Text("标签列表", size=12, color=TEXT_SECONDARY, font_family=FONT_FAMILY),
                ft.Container(height=10),
                show_all_btn,
                tags_list_column,
                
                ft.Container(height=10),
                ft.Text("Designed by 瓶盖", size=10, color="#555555", font_family=FONT_FAMILY),
            ],
            spacing=0,
            expand=True,
        )
    )

    # === 7. 中列：文件夹列表 ===
    # 当前路径显示
    current_path_display = ft.Text("", size=12, color=TEXT_SECONDARY, font_family=FONT_FAMILY, selectable=True)
    
    def go_to_parent(e):
        """返回上一级目录"""
        if current_root_path["value"]:
            parent_path = os.path.dirname(current_root_path["value"])
            # 检查是否已经是根目录（Windows下parent和current相同表示已到根）
            if parent_path and parent_path != current_root_path["value"]:
                load_folder_list(parent_path)
    
    middle_column = ft.Container(
        width=400,
        bgcolor=BG_COLOR,
        padding=ft.padding.all(20),
        content=ft.Column(
            controls=[
                # 标题
                ft.Text("文件夹列表", size=24, weight="bold", color=TEXT_PRIMARY, font_family=FONT_FAMILY),
                ft.Container(height=8),
                # 路径行（带返回按钮）
                ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.ARROW_UPWARD,
                            icon_color=TEXT_SECONDARY,
                            icon_size=16,
                            tooltip="返回上一级",
                            on_click=go_to_parent,
                        ),
                        current_path_display,
                    ],
                    spacing=0,
                ),
                ft.Container(height=20),
                cards_list_view,
            ]
        )
    )

    # === 8. 右列：详情面板（沉浸式编辑）===
    detail_content = ft.Column(
        controls=[
            # 标题编辑区
            detail_alias_field,
            ft.Container(height=8),
            # 路径行
            ft.Row(
                controls=[
                    ft.Icon(ft.icons.FOLDER, color=current_primary_color, size=18),
                    detail_path,
                    ft.IconButton(
                        icon=ft.icons.COPY,
                        icon_color=TEXT_SECONDARY,
                        icon_size=18,
                        tooltip="复制路径",
                        on_click=lambda e: page.set_clipboard(detail_path.value)
                    ),
                ],
                spacing=5,
            ),
            ft.Container(height=8),
            # 标签区
            tags_container,
            ft.Divider(height=40, color=ACCENT_COLOR),
            # 备注标题
            ft.Text("项目备注", size=12, color=TEXT_SECONDARY, font_family=FONT_FAMILY),
            ft.Container(height=10),
            # 备注编辑区
            detail_note_field,
            ft.Container(expand=True),
            # 底部按钮
            ft.Row(
                controls=[
                    ft.ElevatedButton(
                        content=ft.Row(
                            controls=[
                                ft.Icon(ft.icons.OPEN_IN_NEW, color=BG_COLOR, size=16),
                                ft.Text("打开文件夹", color=BG_COLOR, font_family=FONT_FAMILY),
                            ],
                            spacing=5,
                        ),
                        bgcolor=current_primary_color,
                        on_click=open_folder_in_explorer,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                    ),
                    ft.OutlinedButton(
                        content=ft.Row(
                            controls=[
                                ft.Icon(ft.icons.VISIBILITY_OFF, color="#FF5252", size=16),
                                ft.Text("不在此软件中显示", color="#FF5252", font_family=FONT_FAMILY),
                            ],
                            spacing=5,
                        ),
                        on_click=hide_current_folder,
                        style=ft.ButtonStyle(
                            side=ft.BorderSide(1, "#FF5252"),
                            bgcolor="transparent",
                            shape=ft.RoundedRectangleBorder(radius=8),
                        ),
                    ),
                ],
                spacing=10,
            ),
        ],
        visible=False,  # 默认隐藏
    )
    
    detail_panel = ft.Container(
        expand=True,
        bgcolor=BG_COLOR,
        padding=ft.padding.all(40),
        content=ft.Stack(
            controls=[
                empty_state_container,
                detail_content,
            ],
            expand=True,
        )
    )

    update_stats(refresh_ui=False)

    demo_root = os.getenv("UNIFOLDER_DEMO_ROOT")
    if demo_root and os.path.isdir(demo_root):
        load_folder_list(demo_root, refresh_ui=False)

    return ft.Row(
        controls=[sidebar, middle_column, detail_panel],
        expand=True,
        spacing=0,
    )
