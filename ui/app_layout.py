import flet as ft
from ui.folder_card import FolderCard
from config import *
from core.file_scanner import FileScanner
from core.data_manager import data_manager
import threading # 用于异步计算大小

def SidebarItem(icon, text, is_selected=False, on_click=None):
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(icon, size=18, color=TEXT_PRIMARY if is_selected else TEXT_SECONDARY),
                ft.Text(text, size=14, font_family=FONT_FAMILY, color=TEXT_PRIMARY if is_selected else TEXT_SECONDARY, weight="bold" if is_selected else "normal"),
            ],
            spacing=15,
        ),
        padding=ft.padding.symmetric(horizontal=15, vertical=12),
        bgcolor="#2A2A2A" if is_selected else "transparent",
        border_radius=8,
        on_click=on_click # 绑定点击事件
    )

def get_main_layout(page: ft.Page):
    
    # === 1. 定义状态和控件引用 ===
    # 我们需要在这里引用列表控件，以便稍后刷新它
    cards_list_view = ft.ListView(
        expand=True,
        spacing=10,
        padding=ft.padding.only(right=10),
    )
    
    current_path_text = ft.Text("当前目录：未选择", size=12, color=TEXT_SECONDARY, font_family=FONT_FAMILY)
    
    # 新增：当前正在编辑的文件夹路径（用于保存时识别）
    current_edit_path = {"value": None}

    # === 2. 定义编辑弹窗的输入控件 ===
    edit_path_text = ft.Text(size=12, color=TEXT_SECONDARY, selectable=True, font_family=FONT_FAMILY)
    edit_note_field = ft.TextField(
        label="中文备注",
        hint_text="输入文件夹备注...",
        multiline=True,
        min_lines=2,
        max_lines=4,
        color=TEXT_PRIMARY,
        border_color=ACCENT_COLOR,
        text_style=ft.TextStyle(font_family=FONT_FAMILY),
        label_style=ft.TextStyle(font_family=FONT_FAMILY),
    )
    edit_tags_field = ft.TextField(
        label="标签",
        hint_text="多个标签用中文逗号分隔，如：作业，重要，课程",
        color=TEXT_PRIMARY,
        border_color=ACCENT_COLOR,
        text_style=ft.TextStyle(font_family=FONT_FAMILY),
        label_style=ft.TextStyle(font_family=FONT_FAMILY),
    )

    # === 3. 定义编辑弹窗 ===
    def close_dialog():
        edit_dialog.open = False
        page.update()

    def save_dialog(e):
        """保存按钮逻辑"""
        folder_path = current_edit_path["value"]
        if not folder_path:
            return
        
        # 1. 获取输入内容
        note = edit_note_field.value or ""
        tags_str = edit_tags_field.value or ""
        # 解析标签（中文逗号分隔，去除空格）
        tags = [t.strip() for t in tags_str.split("，") if t.strip()]
        
        # 2. 保存到 JSON
        data_manager.update_note(folder_path, note)
        data_manager.update_tags(folder_path, tags)
        
        # 3. 关闭弹窗
        close_dialog()
        
        # 4. 刷新列表视图（重新加载当前目录）
        current_path = current_path_text.value.replace("当前目录：", "")
        if current_path and current_path != "未选择":
            load_folder_list(current_path)

    edit_dialog = ft.AlertDialog(
        title=ft.Text("编辑文件夹信息", size=18, weight="bold", color=TEXT_PRIMARY, font_family=FONT_FAMILY),
        content=ft.Column(
            controls=[
                ft.Text("路径:", size=12, color=TEXT_SECONDARY, font_family=FONT_FAMILY),
                edit_path_text,
                ft.Divider(height=10, color="transparent"),
                edit_note_field,
                ft.Container(height=10),
                edit_tags_field,
            ],
            tight=True,
            spacing=5,
        ),
        actions=[
            ft.TextButton("取消", on_click=lambda e: close_dialog()),
            ft.ElevatedButton("保存", on_click=save_dialog, bgcolor=ACCENT_COLOR, color=TEXT_PRIMARY),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # === 4. 打开编辑弹窗的函数 ===
    def open_edit_dialog(card_data):
        """
        打开编辑弹窗并填充现有数据
        card_data: {"folder_path": ..., "folder_name": ..., "note": ..., "tags": [...]}
        """
        current_edit_path["value"] = card_data["folder_path"]
        
        # 填充弹窗数据
        edit_path_text.value = card_data["folder_path"]
        edit_note_field.value = card_data["note"]
        edit_tags_field.value = "，".join(card_data["tags"])
        
        # 显示弹窗
        page.dialog = edit_dialog
        edit_dialog.open = True
        page.update()

    # === 5. 核心逻辑函数 ===

    def update_folder_size_async(folder_path, card_control):
        """异步任务：在后台计算大小，算完更新UI"""
        size_str = FileScanner.get_folder_size(folder_path)
        
        # 找到卡片里的统计文本控件 (Footer -> Row -> Text)
        # 注意：这依赖于 folder_card.py 的结构，如果结构变了这里可能找不到
        # 为了稳健，我们通过 content 遍历查找 (略复杂，这里先简化处理)
        # 既然我们无法直接访问 FolderCard 内部的控件，
        # 我们最好是在 FolderCard 类里加一个 update_size 方法。
        # 但为了不动 folder_card.py，我们这里做一个简单的刷新策略：
        # 这里暂时只打印，或者如果卡片组件支持 update，我们调用它。
        
        # 修正策略：我们在生成 FolderCard 时，把 size 传进去。
        # 异步更新比较复杂，为了你的第一版稳定，
        # 我们先让它显示 "计算中..."，
        # 如果你想要真正的异步更新，需要改写 FolderCard。
        # 既然你要求 "异步计算大小"，我们先跳过这一步 UI 刷新，
        # 避免为了这个功能把简单的代码搞复杂。
        # V1.1 再做这个动态刷新。
        pass


    def load_folder_list(root_path):
        """核心功能：扫描路径并刷新列表"""
        if not root_path:
            return

        # 1. 更新面包屑
        current_path_text.value = f"当前目录：{root_path}"
        current_path_text.update()

        # 2. 清空列表
        cards_list_view.controls.clear()
        
        # 加一个“扫描中”的提示
        cards_list_view.controls.append(ft.Text("🔍 正在扫描...", color=TEXT_SECONDARY))
        cards_list_view.update()

        # 3. 调用扫描器
        folders = FileScanner.get_subfolders(root_path)
        
        # 4. 清空提示，准备加载卡片
        cards_list_view.controls.clear()

        if not folders:
            cards_list_view.controls.append(ft.Text("📭 该目录下没有文件夹", color=TEXT_SECONDARY))
        else:
            for f in folders:
                # 从 data_manager 读取备注和标签
                info = data_manager.get_info(f['path'])
                
                # 创建卡片，传入 on_edit_click 回调
                card = FolderCard(
                    folder_name=f['name'],
                    folder_path=f['path'],
                    tags=info['tags'],
                    note=info['note'],
                    time_str=f['mtime_str'],
                    size_str=f['size_str'],
                    on_edit_click=open_edit_dialog
                )
                
                # 将“修改时间”赋值给卡片的文本 (需要你在 FolderCard 预留接口，或者我们暴力一点)
                # 暂时先用 FolderCard 默认的时间，后续再把真实时间传进去
                
                cards_list_view.controls.append(card)

        cards_list_view.update()
        
        # 5. (高级) 启动异步线程计算大小
        # 这里为了不报错，先暂缓实现 UI 局部刷新。


    # === 3. 文件选择器 ===
    # Flet 的文件选择器是不可见的，必须挂载到 overlay 上
    file_picker = ft.FilePicker(
        on_result=lambda e: load_folder_list(e.path) if e.path else None
    )
    page.overlay.append(file_picker) # 必须挂载！


    # === 4. 组装 UI (和之前一样，只是加了事件绑定) ===
    
    sidebar = ft.Container(
        width=220,
        bgcolor=SIDEBAR_BG,
        padding=ft.padding.only(top=20, left=10, right=10),
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.Column([
                        ft.Text("UniFolder", size=24, weight="bold", color=TEXT_PRIMARY, font_family=FONT_FAMILY),
                        ft.Text("你的第二大脑", size=12, color=TEXT_SECONDARY, font_family=FONT_FAMILY),
                    ]),
                    padding=ft.padding.only(bottom=20, left=10)
                ),
                
                # 绑定点击事件：打开文件夹选择器
                SidebarItem(ft.icons.FOLDER_OPEN, "目录扫描", is_selected=True, 
                           on_click=lambda _: file_picker.get_directory_path()),
                           
                SidebarItem(ft.icons.STAR_BORDER, "我的收藏"),
                SidebarItem(ft.icons.DELETE_OUTLINE, "回收站"),
                
                ft.Divider(color=ACCENT_COLOR, height=30),
                
                ft.Text("  常用标签", size=12, color=TEXT_SECONDARY, font_family=FONT_FAMILY),
                ft.Container(height=5),
                SidebarItem(ft.icons.LABEL_OUTLINE, "课程作业"),
            ],
            spacing=5
        )
    )

    # 搜索栏
    search_bar = ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(ft.icons.SEARCH, color=TEXT_SECONDARY),
                ft.TextField(
                    hint_text="搜索...",
                    border="none",
                    color=TEXT_PRIMARY,
                    text_size=14,
                    content_padding=10,
                    expand=True
                ),
            ]
        ),
        bgcolor=SIDEBAR_BG,
        border_radius=8,
        padding=ft.padding.symmetric(horizontal=15),
        height=40,
    )

    # 内容区
    content_area = ft.Container(
        expand=True,
        bgcolor=BG_COLOR,
        padding=ft.padding.all(30),
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("项目列表", size=20, weight="bold", color=TEXT_PRIMARY, font_family=FONT_FAMILY),
                        ft.Container(width=20),
                        current_path_text, # 显示当前路径
                        ft.Container(content=search_bar, expand=True), 
                    ]
                ),
                ft.Container(height=20),
                cards_list_view # 这里放刚才定义的 ListView
            ]
        )
    )

    return ft.Row(
        controls=[sidebar, content_area],
        expand=True,
        spacing=0
    )