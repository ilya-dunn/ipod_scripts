import os
from PIL import Image

ROOT = r"D:\Платина"  # путь к библиотеке
SIZE = (500, 500)
QUALITY = 92

IMAGE_EXT = (".png", ".jpg", ".jpeg", ".webp", ".bmp")


def create_cover_500(source_img, folder):
    """Создаёт cover.jpeg 500x500"""
    cover_path = os.path.join(folder, "cover.jpeg")
    try:
        with Image.open(source_img) as img:
            # прозрачность
            if img.mode in ("RGBA", "LA", "P"):
                bg = Image.new("RGB", img.size, (255, 255, 255))
                bg.paste(img, mask=img.split()[-1] if img.mode != "RGB" else None)
                img = bg
            else:
                img = img.convert("RGB")

            # уменьшение
            img.thumbnail(SIZE, Image.LANCZOS)
            canvas = Image.new("RGB", SIZE, (255, 255, 255))
            offset = ((SIZE[0] - img.size[0]) // 2, (SIZE[1] - img.size[1]) // 2)
            canvas.paste(img, offset)
            canvas.save(cover_path, "JPEG", quality=QUALITY, subsampling=0)
            print(f"✔ created {cover_path}")
    except Exception as e:
        print(f"✖ Ошибка создания {cover_path}: {e}")


def process_folder(folder):
    images = [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.lower().endswith(IMAGE_EXT)
    ]

    if not images:
        return

    cover_jpg = os.path.join(folder, "cover.jpg")
    cover_jpeg = os.path.join(folder, "cover.jpeg")

    # выбираем первую картинку для нового cover.jpeg
    first_img = images[0]

    # создаём cover.jpeg только если cover.jpg уже есть
    if os.path.exists(cover_jpg):
        create_cover_500(first_img, folder)
    else:
        # если cover.jpg нет, создаём cover.jpg из первой картинки
        try:
            with Image.open(first_img) as img:
                if img.mode in ("RGBA", "LA", "P"):
                    bg = Image.new("RGB", img.size, (255, 255, 255))
                    bg.paste(img, mask=img.split()[-1] if img.mode != "RGB" else None)
                    img = bg
                else:
                    img = img.convert("RGB")

                img.thumbnail(SIZE, Image.LANCZOS)
                canvas = Image.new("RGB", SIZE, (255, 255, 255))
                offset = ((SIZE[0] - img.size[0]) // 2, (SIZE[1] - img.size[1]) // 2)
                canvas.paste(img, offset)
                canvas.save(cover_jpg, "JPEG", quality=QUALITY, subsampling=0)
                print(f"✔ created {cover_jpg}")
        except Exception as e:
            print(f"✖ Ошибка создания {cover_jpg}: {e}")

    # удаляем все остальные картинки, кроме cover.jpg и cover.jpeg
    for img in images:
        if os.path.abspath(img) not in [os.path.abspath(cover_jpg), os.path.abspath(cover_jpeg)]:
            try:
                os.remove(img)
            except:
                pass


def scan(root):
    for path, dirs, files in os.walk(root):
        process_folder(path)


if __name__ == "__main__":
    scan(ROOT)
    print("Готово — все папки теперь имеют cover.jpg и/или cover.jpeg 500x500")
