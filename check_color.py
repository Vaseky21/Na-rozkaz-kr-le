from PIL import Image
import os

def check_color(path):
    img = Image.open(path)
    if img.mode == 'RGB' or img.mode == 'RGBA':
        # Check if R, G, B channels are significantly different
        # A simple check: get some pixels and check variance
        extrema = img.getextrema()
        print(f"File: {os.path.basename(path)}, Mode: {img.mode}, Extrema: {extrema}")
    else:
        print(f"File: {os.path.basename(path)}, Mode: {img.mode}")

check_color(r"c:\Users\vacla\.gemini\antigravity\playground\na-rozkaz-krale\obrazky_hra\page_001.png")
check_color(r"c:\Users\vacla\.gemini\antigravity\playground\na-rozkaz-krale\obrazky_hra\page_003.png")
