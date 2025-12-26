import fitz  # PyMuPDF
import os

pdf_path = "na_rozkaz_krale_2021_v3-01_medium.pdf"
output_folder = "obrazky_hra"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

doc = fitz.open(pdf_path)
print(f"Celkem stran: {len(doc)}")

for page_num in range(len(doc)):
    page = doc.load_page(page_num)
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # Higher resolution (2x zoom)
    output_filename = os.path.join(output_folder, f"page_{page_num + 1:03d}.png")
    pix.save(output_filename)
    if (page_num + 1) % 10 == 0:
        print(f"Exportováno {page_num + 1} stran...")

print("Hotovo! Všechny strany byly uloženy do složky 'obrazky_hra'.")
doc.close()
