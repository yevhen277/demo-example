import flet as ft

# === 视觉风格配置 ===

# 1. 背景色系 (从深到浅)
BG_COLOR = "#111111"       # 整体大背景 (极深)
SIDEBAR_BG = "#181818"     # 侧边栏背景
CARD_BG = "#1F1F1F"        # 卡片背景 (稍微亮一点)
HOVER_COLOR = "#2A2A2A"    # 鼠标悬停时的颜色
SETTINGS_BTN_BG = "#181818" # 系统设置按钮背景

# 2. 文字颜色
TEXT_PRIMARY = "#E0E0E0"   # 主要文字 (白灰)
TEXT_SECONDARY = "#858585" # 次要文字 (深灰)
TEXT_WHITE = "#FFFFFF"     # 白色文字
ACCENT_COLOR = "#3A3A3A"   # 装饰性边框/分割线颜色

# 3. 强调色 (克制的蓝色) - 使用可变字典以便动态切换
theme_state = {
    "primary_color": "#3794FF",
}

def get_primary_color():
    return theme_state["primary_color"]

def set_primary_color(color):
    theme_state["primary_color"] = color

PRIMARY_COLOR = "#3794FF"  # 默认值，实际使用时应该通过 get_primary_color() 获取
TAG_BG = "#263238"         # 标签背景色 (深蓝灰)
TAG_TEXT = "#80CBC4"       # 标签文字色 (清新的青色)

# 4. 状态颜色
ERROR_COLOR = "#EF5350"    # 错误/警告颜色 (红色)
SUCCESS_COLOR = "#4CAF50"  # 成功颜色 (绿色)

FONT_FAMILY = "Microsoft YaHei UI"