from PIL import Image, ImageChops, ImageStat
import os

def check_for_dice_logic(img_path):
    img = Image.open(img_path).convert("L")
    w, h = img.size
    
    # We look at the bottom 40% of the image (where rolls usually are)
    cropped = img.crop((0, int(h * 0.6), w, h))
    
    # Use edge detection (very simple)
    # Find areas with many transitions
    # A dice box [1 2 3] has 10+ transitions in a small width
    data = list(cropped.getdata())
    cw, ch = cropped.size
    
    potential = False
    for y in range(0, ch, 10):
        transitions = 0
        last_val = data[y * cw]
        for x in range(cw):
            val = data[y * cw + x]
            if abs(val - last_val) > 100:
                transitions += 1
            last_val = val
        
        if transitions > 15: # High frequency of black/white
            potential = True
            break
            
    return potential

print("Scanning pages for potential dice rolls...")
dice_pages = []
for i in range(1, 88):
    path = f"obrazky_hra/page_{i:03d}.png"
    if os.path.exists(path):
        if check_for_dice_logic(path):
            dice_pages.append(i)

print(f"Found {len(dice_pages)} potential dice pages: {dice_pages}")
