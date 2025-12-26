import fitz
import re

pdf_path = "na_rozkaz_krale_2021_v3-01_medium.pdf"
doc = fitz.open(pdf_path)

dice_keywords = ["kostk", "hoď", "hoďte", "padne", "součet"]
dice_pages = []

for page_num in range(len(doc)):
    page = doc.load_page(page_num)
    text = page.get_text().lower()
    
    found = False
    for kw in dice_keywords:
        if kw in text:
            found = True
            break
    
    if found:
        # Also look for dice results patterns like "1: jdi na", "1-3:", etc.
        results = re.findall(r'(\d)[-–]?(\d)?\s*[:\.]?\s*(?:jdi|pokračuj|na)?\s*stran[ua]\s*(\d+)', text)
        dice_pages.append({
            "page": page_num + 1,
            "patterns_found": results,
            "sample_text": text[:200].replace("\n", " ")
        })

print(f"Pages with potential dice rolls: {len(dice_pages)}")
for p in dice_pages:
    print(f"Page {p['page']}: {p['patterns_found']}")
    if not p['patterns_found']:
        print(f"  (Keyword found but no pattern: {p['sample_text']}...)")

doc.close()
