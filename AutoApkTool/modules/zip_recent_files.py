import os
import time
import zipfile
import shutil

def zip_and_delete_subfolders(parent_path, days=7, log_callback=None):
    """
    将指定文件夹中最近 N 天内修改过的文件打包。
    如果未指定压缩包名称，默认使用源文件夹名称命名。

    参数:
    parent_path (str): 要扫描的源文件夹路径。
    days (int): 筛选最近多少天的文件，默认为7天。
    log_callback (callable): 用于将日志回显到 UI 的回调函数。
    """

    if log_callback:
        log_callback(f"[*] Scanning the directory: {parent_path}\n")
    
    time_threshold = time.time() - (days * 24 * 60 * 60)

    processed_count = 0

    # 1. 遍历父目录下的所有内容
    for item in os.listdir(parent_path):
        item_path = os.path.join(parent_path, item)

        if os.path.isdir(item_path):
            folder_ctime = os.path.getctime(item_path)
            if folder_ctime <= time_threshold:

                zip_path = f"{item_path}.zip"
                try:
                    if log_callback:
                        log_callback(f"[*] Packing: {item}\n")

                    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                        for root, dirs, files in os.walk(item_path):
                            for file in files:
                                file_path = os.path.join(root, file)
                                arcname = os.path.relpath(file_path, item_path)
                                zipf.write(file_path, arcname)

                    # 使用 shutil.rmtree 删除整个目录树
                    shutil.rmtree(item_path)

                    if log_callback:
                        log_callback(f"[OK] Success: {item} -> {item}.zip\n")
                    processed_count += 1

                except Exception as e:
                    if log_callback:
                        log_callback(f"[Error] Processing {item} failed: {e}\n")
            else:
                if log_callback:
                    log_callback(f"[Warning] ⏭️ Skip {item}\n")