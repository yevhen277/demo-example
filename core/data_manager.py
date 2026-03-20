import json
import os
import sys
from datetime import datetime, date

def get_app_path():
    """获取应用根目录（兼容开发环境和打包后）"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class DataManager:
    def __init__(self):
        app_root = get_app_path()
        self.data_dir = os.path.join(app_root, "data")
        self.data_file = os.path.join(self.data_dir, "metadata.json")
        self.data = {}
        self._load_data()
        self._init_install_date()

    def _load_data(self):
        """内部方法：加载 JSON 数据"""
        # 如果目录不存在，创建目录
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        
        # 如果文件不存在，初始化为空字典
        if not os.path.exists(self.data_file):
            self.data = {}
            self._save_data()
        else:
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            except Exception as e:
                print(f"读取数据失败: {e}")
                self.data = {}

    def _save_data(self):
        """内部方法：保存 JSON 数据"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存数据失败: {e}")

    def _init_install_date(self):
        """初始化安装日期，如果没有则写入今天"""
        config = self.get_config()
        if "install_date" not in config:
            self.update_config("install_date", date.today().isoformat())

    def get_install_days(self):
        """获取从安装到今天的天数"""
        config = self.get_config()
        install_date_str = config.get("install_date")
        if not install_date_str:
            return 0
        try:
            install_date = datetime.strptime(install_date_str, "%Y-%m-%d").date()
            return (date.today() - install_date).days
        except ValueError:
            return 0

    def get_notes_count(self):
        """获取已备注的文件夹数量（跳过 __config__ 等配置项）"""
        count = 0
        for key, value in self.data.items():
            if key.startswith("__"):
                continue
            if isinstance(value, dict) and (value.get("note") or value.get("alias")):
                count += 1
        return count

    def get_tags_count(self):
        """获取所有标签的去重总数（跳过 __config__ 等配置项）"""
        all_tags = set()
        for key, value in self.data.items():
            if key.startswith("__"):
                continue
            if isinstance(value, dict) and "tags" in value:
                all_tags.update(value["tags"])
        return len(all_tags)

    def get_info(self, folder_path):
        """
        获取某个文件夹的信息
        :param folder_path: 文件夹绝对路径 (作为 Key)
        :return: 字典 {'alias': '...', 'note': '...', 'tags': [...], 'hidden': False}
        """
        norm_path = os.path.normpath(folder_path)
        info = self.data.get(norm_path, {"alias": "", "note": "", "tags": [], "hidden": False})
        if "alias" not in info:
            info["alias"] = ""
        if "hidden" not in info:
            info["hidden"] = False
        return info
    
    def is_hidden(self, folder_path):
        """
        检查某个文件夹是否被隐藏
        :param folder_path: 文件夹绝对路径
        :return: True 如果隐藏，False 如果显示
        """
        norm_path = os.path.normpath(folder_path)
        if norm_path not in self.data:
            return False
        return self.data[norm_path].get("hidden", False)
    
    def set_hidden(self, folder_path, hidden=True):
        """
        设置文件夹的隐藏状态
        :param folder_path: 文件夹绝对路径
        :param hidden: True 隐藏，False 显示
        """
        norm_path = os.path.normpath(folder_path)
        if norm_path not in self.data:
            self.data[norm_path] = {"alias": "", "note": "", "tags": [], "hidden": False}
        
        self.data[norm_path]["hidden"] = hidden
        self._save_data()

    def update_note(self, folder_path, note):
        """更新备注"""
        norm_path = os.path.normpath(folder_path)
        if norm_path not in self.data:
            self.data[norm_path] = {"alias": "", "note": "", "tags": [], "hidden": False}
        
        self.data[norm_path]["note"] = note
        self._save_data()

    def update_alias(self, folder_path, alias):
        """更新别名"""
        norm_path = os.path.normpath(folder_path)
        if norm_path not in self.data:
            self.data[norm_path] = {"alias": "", "note": "", "tags": [], "hidden": False}
        
        self.data[norm_path]["alias"] = alias
        self._save_data()

    def update_tags(self, folder_path, tags):
        """更新标签列表"""
        norm_path = os.path.normpath(folder_path)
        if norm_path not in self.data:
            self.data[norm_path] = {"alias": "", "note": "", "tags": [], "hidden": False}
        
        self.data[norm_path]["tags"] = tags
        self._save_data()

    def get_all_tags(self):
        """获取所有已存在的标签（去重，跳过配置项）"""
        all_tags = set()
        for key, folder_data in self.data.items():
            if key.startswith("__"):
                continue
            if isinstance(folder_data, dict) and "tags" in folder_data:
                all_tags.update(folder_data["tags"])
        return sorted(list(all_tags))
    
    def get_folders_by_tag(self, tag):
        """
        获取包含指定标签的所有文件夹路径列表
        :param tag: 标签名称
        :return: 包含该标签的文件夹路径列表
        """
        folders = []
        for path, info in self.data.items():
            if path.startswith("__"):
                continue
            if isinstance(info, dict) and "tags" in info:
                if tag in info["tags"] and not info.get("hidden", False):
                    folders.append(path)
        return folders
    
    def get_hidden_folders(self):
        """
        获取所有被隐藏的文件夹列表
        :return: 列表，每项为 {'path': '...', 'alias': '...', 'note': '...', 'tags': [...]}
        """
        hidden_list = []
        for path, info in self.data.items():
            if path == "__config__":
                continue
            if info.get("hidden", False):
                hidden_list.append({
                    "path": path,
                    "alias": info.get("alias", ""),
                    "note": info.get("note", ""),
                    "tags": info.get("tags", []),
                })
        hidden_list.sort(key=lambda x: x.get("alias") or os.path.basename(x["path"]))
        return hidden_list
    
    def get_config(self):
        """获取应用配置"""
        config = self.data.get("__config__", {})
        return config
    
    def update_config(self, key, value):
        """更新应用配置"""
        if "__config__" not in self.data:
            self.data["__config__"] = {}
        self.data["__config__"][key] = value
        self._save_data()

# 创建一个全局单例，方便其他文件调用
data_manager = DataManager()