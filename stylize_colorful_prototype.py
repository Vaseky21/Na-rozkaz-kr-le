from PIL import Image, ImageChops, ImageEnhance, ImageOps, ImageDraw
import os

def create_colorful_overlay(size):
    # Create a vibrant colorful gradient overlay
    overlay = Image.new('RGB', size)
    draw = ImageDraw.Draw(overlay)
    
    # Draw a multi-directional gradient
    width, height = size
    for x in range(width):
        for y in range(height):
            # Complex color pattern
            r = int(127 + 127 * (x / width))
            g = int(127 + 127 * (y / height))
            b = int(127 + 127 * ((x + y) / (width + height)))
            overlay.putpixel((x, y), (r, g, b))
    
    # Smooth it out a bit
    overlay = ImageEnhance.Color(overlay).enhance(1.2)
    return overlay

def stylize_page_colorful(original_path, texture_path, output_path):
    # Load original page and texture
    original = Image.open(original_path).convert("RGBA")
    texture = Image.open(texture_path).convert("RGBA")
    
    # Resize texture to match original
    texture = texture.resize(original.size, Image.Resampling.LANCZOS)
    
    # Create a colorful overlay and blend it with the texture
    colorful_overlay = create_colorful_overlay(texture.size)
    # Blend texture with colorful overlay
    vibrant_texture = ImageChops.soft_light(texture.convert("RGB"), colorful_overlay)
    
    # Enhance original contrast to make text really black
    enhancer = ImageEnhance.Contrast(original)
    enhanced = enhancer.enhance(2.0)
    
    # Multiply to apply the colorful texture to the white background
    result_rgb = ImageChops.multiply(vibrant_texture, enhanced.convert("RGB"))
    
    # Convert back to RGBA
    result = result_rgb.convert("RGBA")
    
    # (Optional) Add vignette like in v5
    mask = Image.new('L', result.size, 255)
    draw = ImageDraw.Draw(mask)
    margin = 50
    for i in range(margin):
        alpha = int(255 * (i / margin))
        draw.rectangle([i, i, result.width - i, result.height - i], outline=alpha)
    
    shadow = Image.new('RGBA', result.size, (0, 0, 0, 255))
    result = Image.composite(shadow, result, ImageOps.invert(mask))
    
    result.save(output_path)
    print(f"Colorful stylized page saved to {output_path}")

# Test paths
original_page = r"c:\Users\vacla\.gemini\antigravity\playground\na-rozkaz-krale\obrazky_hra\page_003.png"
texture_img = r"C:\Users\vacla\.gemini\antigravity\brain\45a580f5-fa1c-4608-b7f6-4794ca5059ea\fantasy_parchment_light_1766413742068.png"
output_sample = r"C:\Users\vacla\.gemini\antigravity\brain\91b76dbe-4529-4f1a-b707-1d4d7a85a74d/stylized_page_003_colorful.png"

if os.path.exists(original_page) and os.path.exists(texture_img):
    stylize_page_colorful(original_page, texture_img, output_sample)
else:
    print("Files not found!")
