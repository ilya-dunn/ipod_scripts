import os
from mutagen.id3 import ID3, TIT2, TPE1, TALB, ID3NoHeaderError

MUSIC_DIR = r"G:\Scrim\A man rose from the dead"

ARTIST_NAME = "scrim"
ALBUM_NAME = "A man rose from the dead"


def clean_tags(mp3_path):
    filename = os.path.basename(mp3_path)
    title = os.path.splitext(filename)[0]

    try:
        tags = ID3(mp3_path)
    except ID3NoHeaderError:
        tags = ID3()

    # --- ПОЛНАЯ ОЧИСТКА ТЕГОВ ---
    tags.clear()

    # --- НОВЫЕ ЧИСТЫЕ ТЕГИ ---
    tags.add(TIT2(encoding=3, text=title))        # Title
    tags.add(TPE1(encoding=3, text=ARTIST_NAME))  # Artist
    tags.add(TALB(encoding=3, text=ALBUM_NAME))   # Album

    tags.save(mp3_path)
    print(f"OK: {filename}")


def process_folder(folder):
    for file in os.listdir(folder):
        if file.lower().endswith(".mp3"):
            full_path = os.path.join(folder, file)
            clean_tags(full_path)


if __name__ == "__main__":
    process_folder(MUSIC_DIR)
