import fitz
import json

pdf_path = "na_rozkaz_krale_2021_v3-01_medium.pdf"
doc = fitz.open(pdf_path)

story_map = {}

# PDF dimensions (usually 612x792 or similar)
# We need to map them to our screen size (800x600)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

for page_num in range(len(doc)):
    page = doc.load_page(page_num)
    links = page.get_links()
    
    page_id = str(page_num + 1)
    page_data = {"choices": [], "dice": {}}
    
    # PDF page size
    rect = page.rect
    pdf_w = rect.width
    pdf_h = rect.height
    
    for link in links:
        if link["kind"] == fitz.LINK_GOTO:
            # target page is link["page"] (0-indexed)
            target_page = link["page"] + 1
            
            # coords are in points (x0, y0, x1, y1)
            # Link rect is usually in "from" key
            l_rect = link["from"]
            
            # Scale coords to screen size
            x1 = int(l_rect.x0 * SCREEN_WIDTH / pdf_w)
            y1 = int(l_rect.y0 * SCREEN_HEIGHT / pdf_h)
            x2 = int(l_rect.x1 * SCREEN_WIDTH / pdf_w)
            y2 = int(l_rect.y1 * SCREEN_HEIGHT / pdf_h)
            
            page_data["choices"].append({
                "area": [x1, y1, x2, y2],
                "goto": target_page
            })
    
    # Sort choices by y1 top-to-bottom
    page_data["choices"].sort(key=lambda x: x["area"][1])
    
    if page_data["choices"]:
        story_map[page_id] = page_data

# Save to data/mapa.json
with open("data/mapa.json", "w", encoding="utf-8") as f:
    json.dump(story_map, f, ensure_ascii=False, indent=4)

print(f"Hotovo! Mapa uložena do data/mapa.json. Nalezeno celkem {sum(len(v['choices']) for v in story_map.values())} interaktivních oblastí na {len(story_map)} stranách.")
doc.close()
