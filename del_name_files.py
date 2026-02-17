import os
import re

root = r"C:\Users\volog\Downloads\A man rose from the dead"

patterns = [
    r'\[.*?\]',      # удаляет всё в квадратных скобках
    r'\(.*?\)',      # удаляет всё в круглых скобках
    r'Scrim - '
]

for name in os.listdir(root):
    old_path = os.path.join(root, name)

    # работаем только с файлами
    if os.path.isfile(old_path):

        # разделяем имя и расширение
        filename, ext = os.path.splitext(name)

        new_name = filename
        for pattern in patterns:
            new_name = re.sub(pattern, '', new_name)

        new_name = re.sub(r'\s+', ' ', new_name).strip()

        # возвращаем расширение
        new_name = new_name + ext

        new_path = os.path.join(root, new_name)

        if new_name != name:
            print(f"{name}  ->  {new_name}")
            os.rename(old_path, new_path)
