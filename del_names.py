import os
import re

root = r"C:\Users\volog\Downloads\A man rose from the dead"

patterns = [
    r'\[.*?\]',      # удаляет всё в квадратных скобках
    r'\(.*?\)',      # удаляет всё в круглых скобках
    # r'- '
]

for folder in os.listdir(root):
    old_path = os.path.join(root, folder)

    if os.path.isdir(old_path):
        new_name = folder

        for pattern in patterns:
            new_name = re.sub(pattern, '', new_name)

        new_name = re.sub(r'\s+', ' ', new_name).strip()
        new_path = os.path.join(root, new_name)

        if new_name != folder:
            print(f"{folder}  ->  {new_name}")
            os.rename(old_path, new_path)