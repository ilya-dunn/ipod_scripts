import os
from PIL import Image

ROOT = r"D:\Freddie Dredd\Singles"  # путь к твоей библиотеке
TARGET_SIZE = (500, 500)

COVER_NAMES = ("cover.jpg", "cover.jpeg")


def process_folder(folder):
    for name in COVER_NAMES:
        path = os.path.join(folder, name)
        if not os.path.isfile(path):
            continue

        try:
            with Image.open(path) as img:
                if img.size != TARGET_SIZE:
                    os.remove(path)
                    print(f"🗑 удалён {path} ({img.size[0]}x{img.size[1]})")
                else:
                    print(f"✔ {path} уже 500x500")
        except (PermissionError, OSError):
            print(f"⚠ пропущен заблокированный файл: {path}")


def scan(root):
    for path, dirs, files in os.walk(root):
        process_folder(path)


if __name__ == "__main__":
    scan(ROOT)
    print("Готово — все cover.jpg/jpeg проверены и неверного размера удалены")
