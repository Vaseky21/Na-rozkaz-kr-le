from PIL import Image
import os

def find_blue_blobs(img_path):
    img = Image.open(img_path).convert("RGBA")
    w, h = img.size
    
    # Blue in the original is like (0, 160, 230)
    blobs = []
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            r, g, b, a = img.getpixel((x, y))
            # Heuristic for blue circle
            if b > 150 and b > r + 50 and b > g + 20:
                blobs.append((x, y))
    
    # Cluster blobs to find circle centers
    if not blobs:
        return []
        
    clusters = []
    for b in blobs:
        found = False
        for c in clusters:
            dist = ( (b[0]-c['x'])**2 + (b[1]-c['y'])**2 )**0.5
            if dist < 30:
                c['x'] = (c['x'] * c['n'] + b[0]) / (c['n'] + 1)
                c['y'] = (c['y'] * c['n'] + b[1]) / (c['n'] + 1)
                c['n'] += 1
                found = True
                break
        if not found:
            clusters.append({'x': b[0], 'y': b[1], 'n': 1})
            
    return [c for c in clusters if c['n'] > 5]

page4 = "obrazky_hra/page_004.png"
if os.path.exists(page4):
    found = find_blue_blobs(page4)
    print(f"Found {len(found)} blue circles on Page 4:")
    for c in found:
        print(f"  Circle at ({int(c['x'])}, {int(c['y'])})")
else:
    print("Page 4 not found!")
