import fitz

pdf_path = "na_rozkaz_krale_2021_v3-01_medium.pdf"
doc = fitz.open(pdf_path)

for i in range(min(10, len(doc))):
    page = doc.load_page(i)
    print(f"--- PAGE {i+1} ---")
    print(page.get_text())

doc.close()
