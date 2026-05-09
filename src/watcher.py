import os
import time

SOURCE_DIR = r"C:\Users\finnr\Videos\Source"

def get_new_files(processed_list):
    """
    Scans the source directory and returns files that haven't been processed.
    """
    if not os.path.exists(SOURCE_DIR):
        print(f"Watcher: Source directory not found: {SOURCE_DIR}")
        return []

    all_files = [f for f in os.listdir(SOURCE_DIR) if f.lower().endswith(('.mp4', '.mov', '.mkv'))]
    new_files = [os.path.join(SOURCE_DIR, f) for f in all_files if f not in processed_list]

    return new_files

def wait_for_file_ready(filepath, timeout=30):
    """
    Ensures the file is fully copied/rendered by checking size stability.
    """
    last_size = -1
    start_time = time.time()
    while time.time() - start_time < timeout:
        current_size = os.path.getsize(filepath)
        if current_size == last_size:
            return True
        last_size = current_size
        time.sleep(2)
    return False
