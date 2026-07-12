import zipfile
import os

DATA_DIR = r"D:\alex's folder\code\mcproj\data"
OUT_DIR = os.path.join(DATA_DIR, "sword")

os.makedirs(OUT_DIR, exist_ok=True)

TARGET_SUFFIXES = [
    "assets/minecraft/textures/item/diamond_sword.png",
    "assets/minecraft/textures/items/diamond_sword.png",
]

for fname in os.listdir(DATA_DIR):
    if not fname.endswith(".zip"):
        continue

    pack_name = os.path.splitext(fname)[0]
    zip_path = os.path.join(DATA_DIR, fname)

    try:
        with zipfile.ZipFile(zip_path) as z:
            found = None
            for name in z.namelist():
                normalized = name.replace("\\", "/")
                for suffix in TARGET_SUFFIXES:
                    if normalized.lower().endswith(suffix.lower()):
                        found = name
                        break
                if found:
                    break

            if not found:
                print(f"[skip] {pack_name}: no diamond_sword.png found")
                continue

            out_path = os.path.join(OUT_DIR, f"{pack_name}.png")

            with z.open(found) as src, open(out_path, "wb") as dst:
                dst.write(src.read())

            print(f"[ok] {pack_name} -> sword\\{pack_name}.png")

    except zipfile.BadZipFile:
        print(f"[error] {pack_name}: not a valid zip")
    except Exception as e:
        print(f"[error] {pack_name}: {e}")