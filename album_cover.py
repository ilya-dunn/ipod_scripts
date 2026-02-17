import os
import requests
from PIL import Image
from io import BytesIO
import time
import re

# ===== Настройки =====
ROOT_DIR = r"D:\Bladee\Albums"        # Папка с альбомами
DEFAULT_ARTIST = "Bladee"     # Артист по умолчанию
HEADERS = {"User-Agent": "AlbumCoverDownloader/1.0"}
TIMEOUT = 15                   # Таймаут для сети

# ===== поиск через iTunes =====
def search_itunes(artist, album):
    url = "https://itunes.apple.com/search"
    params = {
        "term": f"{artist} {album}",
        "entity": "album",
        "limit": 1
    }

    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=TIMEOUT)
        data = r.json()
    except:
        return None

    if data["resultCount"] == 0:
        return None

    # artworkUrl100 -> заменяем на большой размер
    art = data["results"][0]["artworkUrl100"]
    art = art.replace("100x100bb.jpg", "1400x1400bb.jpg")
    return art

# ===== скачивание и ресайз =====
def download_cover(url, folder):
    if not url:
        return False

    path = os.path.join(folder, "cover.jpg")
    if os.path.exists(path):
        print("Уже есть:", folder)
        return True

    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        img = Image.open(BytesIO(r.content)).convert("RGB")

        # делаем 500x500
        img = img.resize((500, 500), Image.LANCZOS)
        img.save(path, "JPEG", quality=95)

        print("Скачано:", folder)
        return True

    except Exception as e:
        print("Ошибка:", e)
        return False

# ===== очистка названия альбома =====
def clean_album_name(name):
    # удаляем дату в начале (например "2014 gluee" -> "gluee")
    return re.sub(r"^\d+\s+-", "", name).strip()

# ===== основной цикл =====
def process_library(root):
    for folder in os.listdir(root):
        full = os.path.join(root, folder)
        if not os.path.isdir(full):
            continue

        album_name = clean_album_name(folder)
        artist = DEFAULT_ARTIST

        print(f"\nПоиск: {artist} — {album_name}")

        url = search_itunes(artist, album_name)
        if not url:
            print("Не найдено")
            continue

        download_cover(url, full)
        time.sleep(0.3)  # небольшая пауза для API

if __name__ == "__main__":
    process_library(ROOT_DIR)
