import os
import shutil
import time

MAX_CACHE_DAYS = 7
MAX_CACHE_SIZE_MB = 500
CACHE_DIR = "./chroma_db"

def get_folder_size_mb(path: str) -> float:
    total = sum(
        os.path.getsize(os.path.join(dirpath, f))
        for dirpath, _, files in os.walk(path)
        for f in files
    )
    return total / (1024 * 1024)

def cleanup_cache():
    if not os.path.exists(CACHE_DIR):
        return

    folders = [
        (f, os.path.getmtime(os.path.join(CACHE_DIR, f)))
        for f in os.listdir(CACHE_DIR)
    ]

    now = time.time()
    for folder, mtime in folders:
        age_days = (now - mtime) / 86400
        if age_days > MAX_CACHE_DAYS:
            shutil.rmtree(os.path.join(CACHE_DIR, folder))
            print(f"Deleted old cache: {folder}")

    while get_folder_size_mb(CACHE_DIR) > MAX_CACHE_SIZE_MB:
        folders = sorted(
            [(f, os.path.getmtime(os.path.join(CACHE_DIR, f)))
             for f in os.listdir(CACHE_DIR)],
            key=lambda x: x[1]
        )
        if not folders:
            break
        shutil.rmtree(os.path.join(CACHE_DIR, folders[0][0]))
        print(f"Deleted oldest cache: {folders[0][0]}")