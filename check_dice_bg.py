import pygame
import os

pygame.init()
DICE_SHEET_PATH = r"c:\Users\vacla\.gemini\antigravity\playground\na-rozkaz-krale\assets\dice_sheet.png"

if os.path.exists(DICE_SHEET_PATH):
    sheet = pygame.image.load(DICE_SHEET_PATH)
    w, h = sheet.get_size()
    corner_pixel = sheet.get_at((0, 0))
    print(f"Corner pixel at (0,0): {corner_pixel}")
    
    # Check middle of first cell
    mid_pixel = sheet.get_at((w//6, h//6))
    print(f"Mid cell early pixel: {mid_pixel}")
pygame.quit()
