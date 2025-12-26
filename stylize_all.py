from PIL import Image, ImageChops, ImageEnhance, ImageDraw, ImageOps
import os
import re

def extract_number(filename):
    match = re.search(r'(\d+)', filename)
    return int(match.group(1)) if match else 0

def create_soft_vignette(size, margin=60):
    # Create a soft vignette mask
    width, height = size
    mask = Image.new('L', size, 255)
    draw = ImageDraw.Draw(mask)
    
    # Draw a gradient by nesting rectangles with decreasing alpha
    for i in range(margin):
        alpha = int(255 * (i / margin))
        draw.rectangle([i, i, width - i, height - i], outline=alpha)
    
    # Soften the mask further
    # mask = mask.filter(ImageFilter.GaussianBlur(10)) # Needs ImageFilter
    return mask

def stylize_page(original_path, texture_path, output_path):
    # Load original page and texture
    original = Image.open(original_path).convert("RGBA")
    texture = Image.open(texture_path).convert("RGBA")
    
    # Resize texture to match original
    texture = texture.resize(original.size, Image.Resampling.LANCZOS)
    
    # Enhance original: increase contrast to make text "popping"
    enhancer = ImageEnhance.Contrast(original)
    enhanced = enhancer.enhance(1.6)
    
    # Multiply the color images
    result_rgb = ImageChops.multiply(texture.convert("RGB"), enhanced.convert("RGB"))
    
    # Convert back to RGBA
    result = result_rgb.convert("RGBA")
    
    # Add Soft Shadow Vignette (to blend with the frame)
    vignette_mask = create_soft_vignette(result.size, margin=40)
    shadow = Image.new('RGBA', result.size, (0, 0, 0, 255))
    # In PIL composite: 1st image where mask is 255, 2nd where mask is 0.
    # Our mask is 255 in middle, 0 at edges.
    # So we want result where 255, shadow where 0.
    result = Image.composite(result, shadow, vignette_mask) 
    
    result.save(output_path)

def main():
    input_dir = "obrazky_hra"
    output_dir = "obrazky_stylizovane"
    texture_path = r"C:\Users\vacla\.gemini\antigravity\brain\45a580f5-fa1c-4608-b7f6-4794ca5059ea\fantasy_parchment_light_1766413742068.png"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    files = [f for f in os.listdir(input_dir) if f.endswith(".png")]
    files.sort(key=extract_number)

    total = len(files)
    print(f"Starting stylization of {total} files...")

    for i, filename in enumerate(files):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)
        
        try:
            stylize_page(input_path, texture_path, output_path)
            if (i + 1) % 10 == 0:
                print(f"Processed {i + 1}/{total}...")
        except Exception as e:
            print(f"Error processing {filename}: {e}")

    print("Stylization complete!")

if __name__ == "__main__":
    main()
