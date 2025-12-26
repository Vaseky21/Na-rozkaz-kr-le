import pygame
import os

pygame.init()

def create_button(text, size=(150, 40), color_schemes="gold"):
    # Create surface with per-pixel alpha
    surface = pygame.Surface(size, pygame.SRCALPHA)
    
    # Colors matching the premium frame
    gold = (212, 175, 55)
    dark_gold = (130, 100, 40)
    blue_stone = (25, 35, 50)
    gem_blue = (0, 180, 255)
    
    # 1. Hexagonal Shape (Shield Style)
    h = size[1]
    w = size[0]
    side = 20 # Smaller side for small button
    pts = [(side, 0), (w-side, 0), (w, h//2), (w-side, h), (side, h), (0, h//2)]
    
    # Fill with stone texture
    pygame.draw.polygon(surface, blue_stone, pts)
    for i in range(400): # Fewer pixels
        rx, ry = random.randint(0, w-1), random.randint(0, h-1)
        if surface.get_at((rx, ry))[3] > 0:
            noise = random.randint(-10, 10)
            c = surface.get_at((rx, ry))
            surface.set_at((rx, ry), (max(0, min(255, c[0]+noise)), 
                                      max(0, min(255, c[1]+noise)), 
                                      max(0, min(255, c[2]+noise))))

    # 2. Ornate Gold Border
    pygame.draw.polygon(surface, dark_gold, pts, 4)
    pygame.draw.polygon(surface, gold, pts, 1)
    
    # Decorative inner line
    inner_pts = [(side+4, 4), (w-side-4, 4), (w-4, h//2), (w-side-4, h-4), (side+4, h-4), (4, h//2)]
    pygame.draw.polygon(surface, gold, inner_pts, 1)
    
    # 3. Corner Gems
    gem_pos = [(0, h//2), (w, h//2)]
    for gx, gy in gem_pos:
        # Glow
        for r in range(6, 0, -1):
            alpha = int(100 * (1 - r/6))
            pygame.draw.circle(surface, (*gem_blue, alpha), (gx, gy), r)
        pygame.draw.circle(surface, (200, 240, 255), (gx, gy), 2)
    
    # 4. Text
    font = pygame.font.SysFont("Verdana", 18, bold=True)
    
    # Text Shadow
    for ox, oy in [(-1,-1), (1,-1), (-1,1), (1,1)]:
        text_surf_glow = font.render(text, True, (0, 50, 100))
        text_rect = text_surf_glow.get_rect(center=(w//2 + ox, h//2 + oy))
        surface.blit(text_surf_glow, text_rect)
        
    # Text Primary
    text_surf = font.render(text, True, highlight_color if 'highlight_color' in locals() else (255, 220, 100))
    text_rect = text_surf.get_rect(center=(w//2, h//2))
    surface.blit(text_surf, text_rect)
    
    return surface

import random
highlight_color = (255, 215, 0)

# Save buttons
os.makedirs("assets", exist_ok=True)
btn_roll = create_button("HOD KOSTKOU")
pygame.image.save(btn_roll, "assets/btn_roll.png")

btn_continue = create_button("POKRAČOVAT")
pygame.image.save(btn_continue, "assets/btn_continue.png")

print("Premium buttons saved to assets/ folder!")
pygame.quit()
