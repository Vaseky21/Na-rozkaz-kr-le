import pygame
import os

pygame.init()

def create_scroll_button(text, size=(240, 60)):
    surface = pygame.Surface(size, pygame.SRCALPHA)
    # Light parchment colors
    bg_color = (230, 210, 180)
    border_color = (139, 69, 19) # SaddleBrown
    
    # Base
    pygame.draw.rect(surface, bg_color, (10, 5, size[0]-20, size[1]-10), border_radius=5)
    # Scroll ends
    pygame.draw.ellipse(surface, bg_color, (0, 0, 20, size[1]))
    pygame.draw.ellipse(surface, bg_color, (size[0]-20, 0, 20, size[1]))
    # Border
    pygame.draw.rect(surface, border_color, (10, 5, size[0]-20, size[1]-10), 2, border_radius=5)
    pygame.draw.arc(surface, border_color, (0, 0, 20, size[1]), 0.5, 3.14*1.5, 2)
    pygame.draw.arc(surface, border_color, (size[0]-20, 0, 20, size[1]), 3.14*1.5, 0.5, 2)
    
    font = pygame.font.SysFont("Verdana", 24, bold=True)
    text_surf = font.render(text, True, (60, 30, 0))
    text_rect = text_surf.get_rect(center=(size[0]//2, size[1]//2))
    surface.blit(text_surf, text_rect)
    return surface

def create_shield_button(text, size=(240, 60)):
    surface = pygame.Surface(size, pygame.SRCALPHA)
    # Shield colors (matches frame)
    gold = (212, 175, 55)
    blue_stone = (20, 40, 60)
    
    # Hexagon points
    pts = [(30, 0), (size[0]-30, 0), (size[0], size[1]//2), (size[0]-30, size[1]), (30, size[1]), (0, size[1]//2)]
    pygame.draw.polygon(surface, blue_stone, pts)
    pygame.draw.polygon(surface, gold, pts, 3)
    
    # Gems in points
    pygame.draw.circle(surface, (0, 200, 255), (0, size[1]//2), 5)
    pygame.draw.circle(surface, (0, 200, 255), (size[0], size[1]//2), 5)
    
    font = pygame.font.SysFont("Verdana", 24, bold=True)
    text_surf = font.render(text, True, gold)
    surface.blit(text_surf, text_surf.get_rect(center=(size[0]//2, size[1]//2)))
    return surface

def create_stone_button(text, size=(240, 60)):
    surface = pygame.Surface(size, pygame.SRCALPHA)
    dark_gray = (40, 40, 45)
    glow = (0, 150, 255)
    
    # Octagon points
    o = 15
    pts = [(o, 0), (size[0]-o, 0), (size[0], o), (size[0], size[1]-o), (size[0]-o, size[1]), (o, size[1]), (0, size[1]-o), (0, o)]
    pygame.draw.polygon(surface, dark_gray, pts)
    pygame.draw.polygon(surface, (80, 80, 90), pts, 2)
    
    font = pygame.font.SysFont("Verdana", 24, bold=True)
    # Glow effect
    for i in range(3, 0, -1):
        surf = font.render(text, True, (*glow, 100))
        surface.blit(surf, surf.get_rect(center=(size[0]//2, size[1]//2)))
        
    text_surf = font.render(text, True, (200, 230, 255))
    surface.blit(text_surf, text_surf.get_rect(center=(size[0]//2, size[1]//2)))
    return surface

os.makedirs("assets/previews", exist_ok=True)
pygame.image.save(create_scroll_button("HOD KOSTKOU"), "assets/previews/preview_scroll.png")
pygame.image.save(create_shield_button("HOD KOSTKOU"), "assets/previews/preview_shield.png")
pygame.image.save(create_stone_button("HOD KOSTKOU"), "assets/previews/preview_stone.png")

print("Previews created!")
pygame.quit()
