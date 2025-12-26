import pygame
import os
from collections import Counter

pygame.init()
DICE_SHEET_PATH = r"c:\Users\vacla\.gemini\antigravity\playground\na-rozkaz-krale\assets\dice_sheet.png"

if os.path.exists(DICE_SHEET_PATH):
    sheet = pygame.image.load(DICE_SHEET_PATH)
    w, h = sheet.get_size()
    
    # Sample edges for background colors
    colors = []
    for x in range(w):
        colors.append(tuple(sheet.get_at((x, 0))))
        colors.append(tuple(sheet.get_at((x, h-1))))
    for y in range(h):
        colors.append(tuple(sheet.get_at((0, y))))
        colors.append(tuple(sheet.get_at((w-1, y))))
        
    counts = Counter(colors)
    print("Most common edge colors (potential background):")
    for color, count in counts.most_common(10):
        print(f"Color {color}: {count} pixels")
        
pygame.quit()
