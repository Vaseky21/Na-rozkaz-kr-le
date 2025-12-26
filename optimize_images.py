import os
from PIL import Image

SRC_FOLDER = "obrazky_stylizovane"
DEST_FOLDER = "obrazky_optimalizovane"

if not os.path.exists(DEST_FOLDER):
    os.makedirs(DEST_FOLDER)

files = sorted([f for f in os.listdir(SRC_FOLDER) if f.lower().endswith(".png")])

print(f"Optimalizuji {len(files)} obrázků...")

for filename in files:
    src_path = os.path.join(SRC_FOLDER, filename)
    dest_filename = filename.replace(".png", ".jpg")
    dest_path = os.path.join(DEST_FOLDER, dest_filename)
    
    with Image.open(src_path) as img:
        # Převedeme na RGB (pro JPG)
        if img.mode in ("RGBA", "P"):
            rgb_img = img.convert("RGB")
        else:
            rgb_img = img
            
        # Uložíme s kompresí (kvalita 85 je skvělý poměr)
        rgb_img.save(dest_path, "JPEG", quality=85, optimize=True)
        
    print(f"Hotovo: {dest_filename} ({os.path.getsize(dest_path)//1024} KB)")

print("\nOptimalizace dokončena!")
