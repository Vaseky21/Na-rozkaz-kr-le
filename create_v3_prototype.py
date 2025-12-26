from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

def draw_styled_circle(draw, position, text, radius=30):
    # Colors matching the sample: uploaded_image_1766656800072.jpg
    gold_ring = (180, 150, 80)
    gold_highlight = (255, 230, 150)
    dark_inner = (40, 45, 55)
    text_color = (255, 220, 120)
    
    x, y = position
    
    # Ring
    draw.ellipse([x-radius, y-radius, x+radius, y+radius], fill=dark_inner, outline=gold_ring, width=4)
    draw.ellipse([x-radius+2, y-radius+2, x+radius-2, y+radius-2], outline=gold_highlight, width=1)
    
    # Text (try to find a nice serif font on Windows)
    font_paths = ["georgiab.ttf", "timesbd.ttf", "arial.ttf"]
    font = None
    for p in font_paths:
        try:
            full_path = os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts", p)
            font = ImageFont.truetype(full_path, 32)
            break
        except:
            continue
    if not font:
        font = ImageFont.load_default()
        
    # Center text
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((x - tw/2, y - th/2 - 4), text, fill=text_color, font=font)

def draw_dice_icon(draw, x, y, value, size=35):
    # Draw a clean d6 face
    draw.rounded_rectangle([x, y, x+size, y+size], radius=5, fill=(245, 235, 215), outline=(100, 90, 70), width=2)
    
    dot_r = 3
    center = size // 2
    margin = size // 4
    
    dots = {
        1: [(center, center)],
        2: [(margin, margin), (size-margin, size-margin)],
        3: [(margin, margin), (center, center), (size-margin, size-margin)],
        4: [(margin, margin), (size-margin, margin), (margin, size-margin), (size-margin, size-margin)],
        5: [(margin, margin), (size-margin, margin), (center, center), (margin, size-margin), (size-margin, size-margin)],
        6: [(margin, margin), (size-margin, margin), (margin, center), (size-margin, center), (margin, size-margin), (size-margin, size-margin)]
    }
    
    for dx, dy in dots.get(value, []):
        draw.ellipse([x+dx-dot_r, y+dy-dot_r, x+dx+dot_r, y+dy+dot_r], fill=(30, 30, 30))

def assemble_page_3():
    # Paths
    frame_path = r"C:\Users\vacla\.gemini\antigravity\brain\45a580f5-fa1c-4608-b7f6-4794ca5059ea\uploaded_image_1766497207934.jpg"
    parchment_path = r"C:\Users\vacla\.gemini\antigravity\brain\45a580f5-fa1c-4608-b7f6-4794ca5059ea\fantasy_parchment_light_1766413742068.png"
    output_path = r"C:\Users\vacla\.gemini\antigravity\brain\91b76dbe-4529-4f1a-b707-1d4d7a85a74d\page_003_v3_prototype.png"
    
    # Load assets
    frame = Image.open(frame_path).convert("RGBA")
    # Resize frame to 800x600 if needed (original is 640x640?)
    # Let's check frame size
    print(f"Frame size: {frame.size}")
    frame = frame.resize((800, 600), Image.Resampling.LANCZOS)
    
    # Create main surface
    canvas = frame.copy()
    draw = ImageDraw.Draw(canvas)
    
    # Add a parchment scroll overlay for the main text
    # Let's crop and shape the parchment like a scroll
    parchment = Image.open(parchment_path).convert("RGBA")
    scroll_w, scroll_h = 350, 400
    parchment = parchment.resize((scroll_w, scroll_h), Image.Resampling.LANCZOS)
    
    # Create a mask for the scroll (slightly rounded edges)
    mask = Image.new("L", (scroll_w, scroll_h), 0)
    d_mask = ImageDraw.Draw(mask)
    d_mask.rounded_rectangle([0, 0, scroll_w, scroll_h], radius=20, fill=255)
    
    # Paste scroll on the left
    canvas.paste(parchment, (60, 100), mask)
    
    # Draw ornate border for the scroll
    draw.rounded_rectangle([60, 100, 60+scroll_w, 100+scroll_h], radius=20, outline=(120, 100, 60), width=4)
    
    # Fonts
    font_path_bold = os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts", "georgiab.ttf")
    font_path_reg = os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts", "georgia.ttf")
    
    try:
        title_font = ImageFont.truetype(font_path_bold, 28)
        text_font = ImageFont.truetype(font_path_reg, 18)
        rules_font = ImageFont.truetype(font_path_reg, 16)
        gold_font = ImageFont.truetype(font_path_bold, 20)
    except:
        title_font = text_font = rules_font = gold_font = ImageFont.load_default()
    
    # 1. Scroll Text (Left side)
    draw.text((80, 120), "My, tvůj král,", fill=(50, 30, 10), font=title_font)
    
    body_text = (
        "z jehož rukou jsi přijal rytířské ostruhy,\n"
        "voláme tě k službě královské.\n\n"
        "Došla Nás zvěst, že na hradě rytíře\n"
        "Romualda se dějí podivné věci. Prý\n"
        "mince falešné tam razí, a lidé do\n"
        "hradu vejdoucí, tajemně mizí.\n\n"
        "Proto slyš a poslouchej Naší vůli.\n"
        "Jdi, zjisti a moudře jednej.\n"
        "Tento list ti dává právo zasáhnout.\n"
        "Jménem krále. I"
    )
    draw.text((80, 160), body_text, fill=(80, 50, 20), font=text_font)
    
    # 2. Right Side Content (Instructions and choices)
    # Background for choices (semi-transparent dark box)
    draw.rounded_rectangle([420, 100, 740, 500], radius=15, fill=(20, 20, 30, 150))
    
    rules_text = (
        "Chce to ovšem poctivou hru...\n"
        "Dobrodružství čeká jen toho,\n"
        "kdo neporuší jeho pravidla.\n\n"
        "Ty je neporušíš určitě. V erbu\n"
        "tvéhoprodu je heslo:\n"
        "ČEST JE MŮJ ŠTÍT."
    )
    draw.text((440, 120), rules_text, fill=(240, 220, 150), font=rules_font)
    
    # Choices
    y_off = 320
    draw.text((440, y_off), "Jak začít?", fill=(255, 215, 0), font=gold_font)
    
    choices = [
        ("a) moudrý astrolog", "11"),
        ("b) královská cesta", "20"),
        ("c) vniknout tajně", "31")
    ]
    
    for i, (txt, num) in enumerate(choices):
        draw.text((440, y_off + 40 + i*60), txt, fill=(200, 200, 200), font=rules_font)
        draw_styled_circle(draw, (700, y_off + 50 + i*60), num, radius=22)

    # Main Page Circle (Top Right)
    draw_styled_circle(draw, (740, 60), "1", radius=30)
    
    # Save
    canvas = canvas.convert("RGB") # Remove alpha for saving as PNG if needed, or keep RGBA
    canvas.save(output_path)
    print(f"Prototype saved to {output_path}")

if __name__ == "__main__":
    assemble_page_3()
