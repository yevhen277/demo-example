import json
import os

class DataManager:
    def __init__(self):
        # 数据文件存储路径：在项目根目录下的 data/metadata.json
        self.data_dir = "data"
        self.data_file = os.path.join(self.data_dir, "metadata.json")
        self.data = {}
        self._load_data()

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

    def get_info(self, folder_path):
        """
        获取某个文件夹的备注信息
        :param folder_path: 文件夹绝对路径 (作为 Key)
        :return: 字典 {'note': '...', 'tags': [...]}
        """
        # 统一把路径转为标准格式 (防止 / 和 \ 混用导致找不到)
        norm_path = os.path.normpath(folder_path)
        return self.data.get(norm_path, {"note": "", "tags": []})

    def update_note(self, folder_path, note):
        """更新备注"""
        norm_path = os.path.normpath(folder_path)
        if norm_path not in self.data:
            self.data[norm_path] = {"note": "", "tags": []}
        
        self.data[norm_path]["note"] = note
        self._save_data()

    def update_tags(self, folder_path, tags):
        """更新标签列表"""
        norm_path = os.path.normpath(folder_path)
        if norm_path not in self.data:
            self.data[norm_path] = {"note": "", "tags": []}
        
        self.data[norm_path]["tags"] = tags
        self._save_data()

# 创建一个全局单例，方便其他文件调用
data_manager = DataManager()