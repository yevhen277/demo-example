import flet as ft
from config import * 

class FolderCard(ft.UserControl):
    def __init__(self, folder_name, folder_path, tags=None, note="", alias="", time_str="", size_str="", on_edit_click=None, on_click=None):
        super().__init__()
        self.folder_name = folder_name
        self.folder_path = folder_path
        self.tags = tags if tags else [] 
        self.note = note
        self.alias = alias
        self.time_str = time_str
        self.size_str = size_str
        self.on_edit_click = on_edit_click
        self.on_click = on_click

    def build(self):
        # 显示名称：如果有别名则显示别名，否则显示文件夹原名
        display_name = self.alias if self.alias else self.folder_name
        
        # 1. 顶部：图标 + 文件夹名 + 日期 + 编辑按钮
        header = ft.Row(
            controls=[
                ft.Icon(ft.icons.FOLDER, size=16, color=PRIMARY_COLOR),
                ft.Text(display_name, size=16, weight="bold", color=TEXT_PRIMARY, font_family=FONT_FAMILY),
                ft.Container(expand=True),
                ft.Text(f"   {self.time_str}", size=12, color=TEXT_SECONDARY, font_family=FONT_FAMILY),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )

        # 2. 第二行：路径
        path_row = ft.Text(
            value=self.folder_path,
            size=12,
            color=TEXT_SECONDARY,
            font_family=FONT_FAMILY,
            selectable=True
        )

        # 3. 中部：中文备注
        note_text = self.note if self.note else "暂无备注"
        content_row = ft.Text(
            value=note_text,
            size=14,
            color=TEXT_SECONDARY,
            font_family=FONT_FAMILY,
            max_lines=2,
            overflow=ft.TextOverflow.ELLIPSIS,
        )

        # 4. 底部：标签 + 统计信息
        # 标签
        tag_views = []
        for tag in self.tags:
            tag_views.append(
                ft.Container(
                    content=ft.Text(f"# {tag}", size=10, color=TAG_TEXT, weight="bold", font_family=FONT_FAMILY),
                    bgcolor=TAG_BG, 
                    padding=ft.padding.symmetric(horizontal=6, vertical=2),
                    border_radius=4, 
                )
            )
        
        # 统计信息 (放在最右边)
        stats_text = ft.Text(f"   {self.size_str}", size=11, color=TEXT_SECONDARY, font_family=FONT_FAMILY)

        footer = ft.Row(
            controls=[
                *tag_views, 
                ft.Container(expand=True), # 占位，把统计信息顶到最右边
                stats_text
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )

        # --- 组装 ---
        card_content = ft.Column(
            controls=[
                header,
                path_row,             # 路径移到了第二行
                ft.Container(height=4),
                content_row,
                ft.Container(height=8),
                footer
            ],
            spacing=2
        )

        card_container = ft.Container(
            content=card_content,
            padding=15,
            bgcolor=CARD_BG, 
            border=ft.border.all(1, ACCENT_COLOR), 
            border_radius=8,
            on_hover=self.on_hover, 
            animate=ft.animation.Animation(200, "easeOut"),
        )
        
        # 如果传入了 on_click，包装一个 GestureDetector
        if self.on_click:
            return ft.GestureDetector(
                content=card_container,
                on_tap=self._handle_click,
            )
        return card_container

    def on_hover(self, e):
        e.control.bgcolor = HOVER_COLOR if e.data == "true" else CARD_BG
        e.control.update()

    def _handle_edit_click(self, e):
        """处理编辑按钮点击，调用外部传入的回调"""
        if self.on_edit_click:
            self.on_edit_click({
                "folder_path": self.folder_path,
                "folder_name": self.folder_name,
                "alias": self.alias,
                "note": self.note,
                "tags": self.tags
            })

    def _handle_click(self, e):
        """处理卡片点击，调用外部传入的回调"""
        if self.on_click:
            self.on_click(e)