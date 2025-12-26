import os
import json
from PIL import Image
import re
import random

# --- Konfigurace ---
# Nalezená správná složka s originály
IMG_FOLDER_ORIG = "obrazky_hra1" 
MAP_FILE = "data/mapa.json"
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

def extract_number(filename):
    match = re.search(r'(\d+)', filename)
    return int(match.group(1)) if match else 0

def find_blue_circles(img_path):
    img = Image.open(img_path).convert("RGBA")
    # Resize to 800x600 to match the game resolution
    img = img.resize((SCREEN_WIDTH, SCREEN_HEIGHT))
    w, h = img.size
    
    blobs = []
    # Vibrant blue in original is strictly like (0, 160, 230)
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            r, g, b, a = img.getpixel((x, y))
            # Strict blue filter
            if b > 180 and r < 80 and g > 100 and g < 200:
                blobs.append((x, y))
    
    if not blobs:
        return []
        
    # Clustering
    clusters = []
    for b in blobs:
        found = False
        for c in clusters:
            dist = ( (b[0]-c['x'])**2 + (b[1]-c['y'])**2 )**0.5
            if dist < 20:
                c['x'] = (c['x'] * c['n'] + b[0]) / (c['n'] + 1)
                c['y'] = (c['y'] * c['n'] + b[1]) / (c['n'] + 1)
                c['n'] += 1
                found = True
                break
        if not found:
            clusters.append({'x': b[0], 'y': b[1], 'n': 1})
            
    # Filter valid circles (size check)
    valid = []
    for c in clusters:
        # Expected radius ~15. Pixel count with 2x2 step ~175.
        if c['n'] > 40: 
            x, y = int(c['x']), int(c['y'])
            valid.append([x-22, y-22, x+22, y+22])
    
    # Sort circles logically: Top to bottom, then Left to right
    valid.sort(key=lambda b: (b[1] // 50, b[0]))
    return valid

# --- Main logic ---
if not os.path.exists(MAP_FILE):
    story_map = {}
else:
    with open(MAP_FILE, "r", encoding="utf-8") as f:
        story_map = json.load(f)

files = sorted([f for f in os.listdir(IMG_FOLDER_ORIG) if f.endswith(".png")], key=extract_number)

print(f"Začínám automatické mapování {len(files)} stran (Složka: {IMG_FOLDER_ORIG})...")

changes_made = 0
for file in files:
    page_id = str(extract_number(file))
    img_path = os.path.join(IMG_FOLDER_ORIG, file)
    
    detected = find_blue_circles(img_path)
    
    if page_id not in story_map:
        story_map[page_id] = {"choices": [], "dice": {}}
    
    page_data = story_map[page_id]
    existing_choices = page_data.get("choices", [])
    
    if len(detected) > 0:
        # Keep existing targets if count exactly matches
        new_choices = []
        for i in range(len(detected)):
            target = existing_choices[i]["goto"] if i < len(existing_choices) else 0
            new_choices.append({"area": detected[i], "goto": target})
        
        page_data["choices"] = new_choices
        changes_made += 1
        
        if len(detected) != len(existing_choices):
            print(f"Stran {page_id}: Detekováno {len(detected)} kroužků (v mapě bylo {len(existing_choices)}). Synchronizováno.")

# Sort map keys numerically
sorted_keys = sorted(story_map.keys(), key=int)
final_map = {k: story_map[k] for k in sorted_keys}

with open(MAP_FILE, "w", encoding="utf-8") as f:
    json.dump(final_map, f, ensure_ascii=False, indent=4)

print(f"Hotovo! Synchronizováno {changes_made} stránek v mapa.json.")
