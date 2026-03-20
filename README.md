# 📂 UniFolder | 你的本地文件索引外脑

> **"不再面对满屏的 `CS101_Final_v2` 发呆。"**
> 一个极简、极客风的桌面文件管理工具，专为大学生和开发者设计。

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Flet](https://img.shields.io/badge/GUI-Flet-purple)
![License](https://img.shields.io/badge/License-MIT-green)

Created by 瓶盖

## 📖 痛点与解决方案

作为计算机相关学生，你的电脑里是否充斥着各种英文命名的课程作业、项目资料？
- ❌ **痛点**：文件夹名字太长、全是英文，过两个月就忘了里面是啥。
- ✅ **UniFolder**：不移动文件，只建立**索引**。给文件夹起中文“别名”，打上“标签”，实现毫秒级检索。

## ✨ 核心功能

- **🗂️ 虚拟别名系统**：给 `D:/Code/ProjectX` 起名为 `大二下-数据库课设`，直观易懂。
- **🏷️ 标签筛选**：支持多标签（如 `#紧急` `#复习` `#归档`），侧边栏一键过滤。
- **⚡ 极速启动**：双击卡片直接调用系统资源管理器打开目标路径。
- **🔒 数据安全**：纯本地 `JSON` 存储，无需联网，无需数据库，数据完全掌控在你手中。
- **🎨 极客 UI**：深色模式，无边框设计，专注沉浸式体验。（当然也有自定义颜色的调色盘）
<img width="2242" height="1389" alt="image" src="https://github.com/user-attachments/assets/904db637-1ff2-4723-8e61-30363f3c71c4" />

## 🛠️ 技术栈
- 语言：Python 3.10
- UI 框架：Flet (基于 Flutter)
- 数据存储：Native JSON (File-based)
- 打包工具：PyInstaller

## 📝 待办清单 (Roadmap)
- 基础列表与详情页 (V1.0已完成)
- 标签筛选与持久化存储 (V2.0已完成)
- 拖拽排序功能
- 全局快捷键呼出
- 数据导出与备份


## 📦 下载与安装

### 方式一：直接使用 (Windows)
前往 https://github.com/pinggai257/UniFolder/releases/tag/Unifolder 下载最新的 `UniFolder_v1.0.zip`。
1. 解压压缩包。
2. 确保 `UniFolder.exe` 同级目录下有 `data` 文件夹。
3. 双击运行即可。

### 方式二：源码运行
如果你想自己修改代码：
```bash
# 1. 克隆项目
git clone https://github.com/你的用户名/UniFolder.git

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行
python main.py

