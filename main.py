import flet as ft
import os
import sys
from ui.app_layout import get_main_layout

# --- 1. 获取 EXE 所在目录（用于读写 data/metadata.json）---
def get_app_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

# --- 2. 获取资源目录（用于图标，防止打包后找不到）---
def get_asset_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def main(page: ft.Page):
    page.title = "UniFolder | 文件夹别名索引"
    
    # 【修复 1】图标直接写文件名
    # 因为下面 ft.app 设了 assets_dir="assets"，Flet 会自动去 assets 文件夹找
    page.window_icon = "logo.png" 
    
    # 【修复 2】正确计算数据文件路径
    # 你的结构是：项目根目录/data/metadata.json
    app_root = get_app_path()
    data_dir = os.path.join(app_root, "data")
    
    # 确保 data 文件夹存在
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        
    # 最终的 json 路径
    json_path = os.path.join(data_dir, "metadata.json")

    print(f"Looking for data at: {json_path}") 

    # --- 【关键问题】 ---
    # 你这里算出了 json_path，但必须把它传给 layout 或者你的数据加载函数！
    # 如果你的 get_main_layout 里还是写的 open("data.json")，那这里算也是白算。
    # 假设你的布局函数支持传入路径（如果不支持，你需要去修改 app_layout.py）：
    # layout = get_main_layout(page, data_path=json_path) 
    
    # 暂时先用你的原样调用，但请去检查 ui/app_layout.py 里是怎么读文件的
    layout = get_main_layout(page) 
    
    page.window_width = 1132
    page.window_height = 700
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    
    page.add(layout)

if __name__ == "__main__":
    # 确保 assets 文件夹里有 logo.png
    ft.app(target=main, assets_dir="assets")