from PIL import Image, ImageChops, ImageEnhance, ImageDraw
import os

def create_vignette(size, color=(0, 0, 0, 255)):
    # Create a soft vignette mask
    mask = Image.new('L', size, 255)
    draw = ImageDraw.Draw(mask)
    
    # Draw a gradient rectangle
    width, height = size
    # Outer margin of shadow
    margin = 40
    for i in range(margin):
        alpha = int(255 * (i / margin))
        draw.rectangle([i, i, width - i, height - i], outline=alpha)
    
    return mask

def stylize_page_v5(original_path, texture_path, output_path):
    # Load original page and texture
    original = Image.open(original_path).convert("RGBA")
    texture = Image.open(texture_path).convert("RGBA")
    
    # Resize texture to match original
    texture = texture.resize(original.size, Image.Resampling.LANCZOS)
    
    # Enhance original
    enhancer = ImageEnhance.Contrast(original)
    enhanced = enhancer.enhance(1.6)
    
    # Multiply the color images
    result_rgb = ImageChops.multiply(texture.convert("RGB"), enhanced.convert("RGB"))
    
    # Convert back to RGBA
    result = result_rgb.convert("RGBA")
    
    # Add Vignette (Shadow at edges)
    vignette = create_vignette(result.size)
    shadow = Image.new('RGBA', result.size, (0, 0, 0, 255))
    result = Image.composite(shadow, result, ImageOps.invert(vignette)) # Shadows at edges
    
    result.save(output_path)
    print(f"Stylized page v5 saved to {output_path}")

from PIL import ImageOps
# Test
original_page = r"c:\Users\vacla\.gemini\antigravity\playground\na-rozkaz-krale\obrazky_hra\page_003.png"
texture_img = r"C:\Users\vacla\.gemini\antigravity\brain\45a580f5-fa1c-4608-b7f6-4794ca5059ea\fantasy_parchment_light_1766413742068.png"
output_sample = r"C:\Users\vacla\.gemini\antigravity\brain\45a580f5-fa1c-4608-b7f6-4794ca5059ea\stylized_page_003_prototype_v5.png"

if os.path.exists(original_page) and os.path.exists(texture_img):
    stylize_page_v5(original_page, texture_img, output_sample)
else:
    print("Files not found!")
