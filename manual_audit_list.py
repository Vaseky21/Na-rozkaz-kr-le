from PIL import Image, ImageFilter, ImageOps
import os

def detect_dice_boxes(image_path):
    img = Image.open(image_path).convert("L")
    # Threshold to find black boxes
    bw = img.point(lambda x: 0 if x < 50 else 255, '1')
    
    # Simple logic: find small black blobs that look like rectangles
    # For a gamebook, these are usually at the bottom
    w, h = img.size
    bottom_half = bw.crop((0, h//2, w, h))
    
    # We could use more advanced CV, but let's just flag the page if it has 
    # many black-to-white transitions in a small area
    # Or just count the number of "choices" in mapa.json and check manually.
    
    # Actually, a better way: check if the page has "dice" mentioned in PDF 
    # even if search failed, maybe try a broader search.
    pass

# Let's just create a list of pages with >1 choice and view them 10 at a time.
import json
with open("data/mapa.json", "r", encoding="utf-8") as f:
    story_map = json.load(f)

pages_to_check = [p for p, d in story_map.items() if len(d.get("choices", [])) >= 2]
print(f"Pages with multiple links to check manually: {pages_to_check}")
