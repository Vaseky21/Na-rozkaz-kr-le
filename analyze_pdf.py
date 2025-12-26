import fitz
import re
import json

pdf_path = "na_rozkaz_krale_2021_v3-01_medium.pdf"
doc = fitz.open(pdf_path)

story_map = {}

# Regex to find "jdi na stranu X" or similar patterns
# Common Czech gamebook patterns: "Jdi na stranu X", "Pokračuj na straně X", "(X)"
patterns = [
    r'jdi na stranu\s*(\d+)',
    r'pokračuj na straně\s*(\d+)',
    r'na stranu\s*(\d+)',
    r'\((\d+)\)'
]

for page_num in range(len(doc)):
    page = doc.load_page(page_num)
    text = page.get_text().lower()
    
    page_id = str(page_num + 1)
    story_map[page_id] = {"choices": [], "dice": {}}
    
    # Try to find references to other pages
    found_pages = []
    for pattern in patterns:
        matches = re.finditer(pattern, text)
        for match in matches:
            target_page = int(match.group(1))
            if target_page not in found_pages and target_page <= len(doc):
                found_pages.append(target_page)
                # For now, we don't know the exact area, so we put a placeholder
                # or just record that this page has a link
                story_map[page_id]["choices"].append({
                    "area": [0, 0, 100, 100], # Placeholder area
                    "goto": target_page,
                    "text_found": match.group(0)
                })

# Save the draft map
with open("data/mapa_draft.json", "w", encoding="utf-8") as f:
    json.dump(story_map, f, ensure_ascii=False, indent=4)

print(f"Hotovo! Návrh mapy uložen do data/mapa_draft.json. Nalezeno {sum(len(v['choices']) for v in story_map.values())} odkazů.")
doc.close()
