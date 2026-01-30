import flet as ft
from ui.app_layout import get_main_layout

def main(page: ft.Page):
    # 1. 基础设置
    page.title = "UniFolder - 大学生文件管理助手"
    page.window_width = 1000
    page.window_height = 700
    page.theme_mode = ft.ThemeMode.DARK # 强制深色模式
    page.padding = 0 # 移除页面默认边距，实现无缝布局
    
    # 2. 加载布局
    # 从 ui 包中获取主布局实例
    layout = get_main_layout(page)
    
    # 3. 添加到页面
    page.add(layout)

# 启动应用
if __name__ == "__main__":
    ft.app(target=main)