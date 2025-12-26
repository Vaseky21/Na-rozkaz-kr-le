import pygame
import os

def create_dice():
    pygame.init()
    size = 256
    os.makedirs("assets/dice", exist_ok=True)
    
    # Colors
    BASE_COLOR = (245, 245, 220) # Parchment / Bone
    PIP_COLOR = (40, 40, 40)
    SHADOW_COLOR = (180, 180, 160)
    HIGHLIGHT_COLOR = (255, 255, 255)
    
    pip_radius = 25
    margin = 50
    center = size // 2
    
    # Pip positions for each value
    pip_map = {
        1: [(center, center)],
        2: [(margin, margin), (size-margin, size-margin)],
        3: [(margin, margin), (center, center), (size-margin, size-margin)],
        4: [(margin, margin), (size-margin, margin), (margin, size-margin), (size-margin, size-margin)],
        5: [(margin, margin), (size-margin, margin), (center, center), (margin, size-margin), (size-margin, size-margin)],
        6: [(margin, margin), (size-margin, margin), (margin, center), (size-margin, center), (margin, size-margin), (size-margin, size-margin)]
    }
    
    for i in range(1, 7):
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Body with rounding and bevel
        rect = pygame.Rect(10, 10, size-20, size-20)
        
        # Shadow/Bottom bevel
        pygame.draw.rect(surf, SHADOW_COLOR, rect.move(0, 8), border_radius=40)
        # Main body
        pygame.draw.rect(surf, BASE_COLOR, rect, border_radius=40)
        # Top highlight
        pygame.draw.rect(surf, HIGHLIGHT_COLOR, (15, 15, size-30, 10), border_radius=5)
        
        # Draw pips
        for pos in pip_map[i]:
            # Pip shadow
            pygame.draw.circle(surf, (100, 100, 100, 100), (pos[0], pos[1]+2), pip_radius)
            # Main pip
            pygame.draw.circle(surf, PIP_COLOR, pos, pip_radius)
            # Pip highlight
            pygame.draw.circle(surf, (80, 80, 80), (pos[0]-5, pos[1]-5), pip_radius//3)
            
        # Add a subtle border
        pygame.draw.rect(surf, (150, 140, 120), rect, 4, border_radius=40)
        
        pygame.image.save(surf, f"assets/dice/dice_{i}.png")
        print(f"Generated assets/dice/dice_{i}.png")

if __name__ == "__main__":
    create_dice()
