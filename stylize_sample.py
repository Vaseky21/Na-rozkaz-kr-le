from PIL import Image, ImageChops, ImageEnhance, ImageOps

def stylize_page_dark(original_path, texture_path, output_path):
    # Load original page and texture
    original = Image.open(original_path).convert("RGBA")
    texture = Image.open(texture_path).convert("RGBA")
    
    # Resize texture to match original
    texture = texture.resize(original.size, Image.Resampling.LANCZOS)
    
    # Pre-process original: 
    # 1. Convert to grayscale
    gray = original.convert("L")
    # 2. Invert (make text white, background black)
    inverted = ImageOps.invert(gray)
    # 3. Boost contrast to remove faint background noise
    enhancer = ImageEnhance.Contrast(inverted)
    inverted = enhancer.enhance(3.0)
    
    # Convert inverted back to RGB for blending
    inverted_rgb = inverted.convert("RGB")
    
    # Screen blend: keeps light parts (our text) and blends with texture
    result_rgb = ImageChops.screen(texture.convert("RGB"), inverted_rgb)
    
    # Convert back to RGBA and save
    result = result_rgb.convert("RGBA")
    result.save(output_path)
    print(f"Dark stylized page saved to {output_path}")

import os
# Test with Page 3
original_page = r"c:\Users\vacla\.gemini\antigravity\playground\na-rozkaz-krale\obrazky_hra\page_003.png"
texture_img = r"C:\Users\vacla\.gemini\antigravity\brain\45a580f5-fa1c-4608-b7f6-4794ca5059ea\fantasy_parchment_dark_premium_1766414021979.png"
output_sample = r"C:\Users\vacla\.gemini\antigravity\brain\45a580f5-fa1c-4608-b7f6-4794ca5059ea\stylized_page_003_prototype_v4.png"

if os.path.exists(original_page) and os.path.exists(texture_img):
    stylize_page_dark(original_page, texture_img, output_sample)
else:
    print("Files not found!")
