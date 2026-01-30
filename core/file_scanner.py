import os
import time

class FileScanner:
    @staticmethod
    def get_subfolders(root_path):
        """
        扫描指定目录下的所有一级子文件夹
        :return: 列表，包含 [{'name': '...', 'path': '...', 'time': '...'}]
        """
        if not os.path.exists(root_path):
            return []

        folders = []
        try:
            # 获取该目录下所有内容
            with os.scandir(root_path) as entries:
                for entry in entries:
                    if entry.is_dir():
                        # 获取修改时间
                        mtime = entry.stat().st_mtime
                        time_str = FileScanner._format_time(mtime)
                        
                        folders.append({
                            "name": entry.name,
                            "path": entry.path,
                            "mtime_str": time_str,
                            # 注意：这里暂时不计算大小，因为太慢了，后续在 UI 里异步计算
                            "size_str": "计算中..." 
                        })
        except Exception as e:
            print(f"扫描出错: {e}")
            return []
        
        return folders

    @staticmethod
    def get_folder_size(folder_path):
        """
        【耗时操作】计算文件夹总大小
        :return: 格式化后的大小字符串 (如 '2.3 GB')
        """
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(folder_path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    # skip if it is symbolic link
                    if not os.path.islink(fp):
                        total_size += os.path.getsize(fp)
        except Exception:
            # 遇到权限问题跳过
            pass

        return FileScanner._format_size(total_size)

    @staticmethod
    def _format_time(timestamp):
        """将时间戳转为 '3天前' 或 '2023-10-01'"""
        # 简单实现，直接返回日期
        struct_time = time.localtime(timestamp)
        return time.strftime("%Y-%m-%d", struct_time)

    @staticmethod
    def _format_size(size_bytes):
        """将字节转为 GB/MB"""
        if size_bytes == 0:
            return "0 B"
        size_name = ("B", "KB", "MB", "GB", "TB")
        i = int(0)
        p = float(1024)
        s = float(size_bytes)
        while s >= p and i < len(size_name) - 1:
            s /= p
            i += 1
        return "{:.1f} {}".format(s, size_name[i])