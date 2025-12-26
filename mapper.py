import pygame
import os
import json
import re

# --- Konfigurace ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
UI_HEIGHT = 120
MAP_FILE = "data/mapa.json"
IMG_FOLDER = "obrazky_stylizovane" if os.path.exists("obrazky_stylizovane") else "obrazky_hra"

def extract_number(filename):
    match = re.search(r'(\d+)', filename)
    return int(match.group(1)) if match else 0

# --- Inicializace ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + UI_HEIGHT))
pygame.display.set_caption("MAPPER - Přesné umisťování tlačítek")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20, bold=True)
font_big = pygame.font.SysFont("Arial", 28, bold=True)

# --- Načtení dat ---
if os.path.exists(MAP_FILE):
    with open(MAP_FILE, "r", encoding="utf-8") as f:
        story_map = json.load(f)
else:
    story_map = {}

image_files = sorted([f for f in os.listdir(IMG_FOLDER) if f.endswith(".png")], key=extract_number)
images = [pygame.transform.scale(pygame.image.load(os.path.join(IMG_FOLDER, f)), (SCREEN_WIDTH, SCREEN_HEIGHT)) for f in image_files]

current_page_idx = 0
drag_start = None
current_rect = None
input_active = False
input_text = ""
selected_choice_idx = -1

def save_map():
    # Sort map keys numerically
    sorted_map = {k: story_map[k] for k in sorted(story_map.keys(), key=int)}
    with open(MAP_FILE, "w", encoding="utf-8") as f:
        json.dump(sorted_map, f, ensure_ascii=False, indent=4)
    print("Disk: mapa.json uložen.")

running = True
while running:
    current_page_id = str(current_page_idx + 1)
    if current_page_id not in story_map:
        story_map[current_page_id] = {"choices": [], "dice": {}}
    page_data = story_map[current_page_id]

    mx, my = pygame.mouse.get_pos()
    hovered_idx = -1
    if not input_active and my < SCREEN_HEIGHT:
        for i, choice in enumerate(page_data["choices"]):
            x1, y1, x2, y2 = choice["area"]
            if x1 <= mx <= x2 and y1 <= my <= y2:
                hovered_idx = i

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Left click
                if my < SCREEN_HEIGHT and not input_active:
                    drag_start = (mx, my)
                elif my > SCREEN_HEIGHT:
                    if 700 < mx < 790 and SCREEN_HEIGHT + 10 < my < SCREEN_HEIGHT + 50:
                        save_map()
            elif event.button == 3: # Right click to delete
                if hovered_idx != -1:
                    page_data["choices"].pop(hovered_idx)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drag_start and not input_active:
                x1, y1 = drag_start
                x2, y2 = mx, my
                rx1, rx2 = min(x1, x2), max(x1, x2)
                ry1, ry2 = min(y1, y2), max(y1, y2)
                if rx2 - rx1 > 5 and ry2 - ry1 > 5:
                    current_rect = [rx1, ry1, rx2, ry2]
                    input_active = True
                    input_text = ""
                drag_start = None

        elif event.type == pygame.KEYDOWN:
            if input_active:
                if event.key == pygame.K_RETURN:
                    if input_text.isdigit():
                        page_data["choices"].append({
                            "area": current_rect,
                            "goto": int(input_text)
                        })
                    input_active = False
                    current_rect = None
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_ESCAPE:
                    input_active = False
                    current_rect = None
                else:
                    input_text += event.unicode
            else:
                if event.key == pygame.K_RIGHT:
                    current_page_idx = (current_page_idx + 1) % len(images)
                elif event.key == pygame.K_LEFT:
                    current_page_idx = (current_page_idx - 1) % len(images)
                elif event.key == pygame.K_s:
                    save_map()
                elif event.key == pygame.K_c: # CLEAR page
                    page_data["choices"] = []
                    print(f"Strana {current_page_id} vyčištěna.")
                elif event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                    if page_data["choices"]:
                        page_data["choices"].pop()

    # --- Vykreslování ---
    screen.fill((40, 40, 45))
    screen.blit(images[current_page_idx], (0, 0))

    # Kreslení oblastí
    for i, choice in enumerate(page_data["choices"]):
        x1, y1, x2, y2 = choice["area"]
        is_hovered = (i == hovered_idx)
        color = (255, 255, 0) if is_hovered else (0, 255, 0)
        width = 3 if is_hovered else 2
        
        pygame.draw.rect(screen, color, (x1, y1, x2-x1, y2-y1), width)
        
        # Label s cílem
        lbl = font.render(f"GOTO: {choice['goto']}", True, (255, 255, 255))
        lbl_bg = pygame.Surface((lbl.get_width()+4, lbl.get_height()+2))
        lbl_bg.fill((0, 100, 0) if not is_hovered else (100, 100, 0))
        screen.blit(lbl_bg, (x1, y1 - 22))
        screen.blit(lbl, (x1 + 2, y1 - 21))

    # Kreslení aktuálního tažení
    if drag_start:
        x1, y1 = drag_start
        pygame.draw.rect(screen, (255, 255, 255), (x1, y1, mx-x1, my-y1), 1)

    # UI Panel
    pygame.draw.rect(screen, (20, 20, 25), (0, SCREEN_HEIGHT, SCREEN_WIDTH, UI_HEIGHT))
    pygame.draw.line(screen, (100, 100, 100), (0, SCREEN_HEIGHT), (SCREEN_WIDTH, SCREEN_HEIGHT), 2)

    info_str = f"STRANA: {current_page_id} / {len(images)} | OBLASTÍ: {len(page_data['choices'])}"
    screen.blit(font_big.render(info_str, True, (220, 220, 220)), (20, SCREEN_HEIGHT + 15))
    
    hint1 = font.render("LEVÉ MYŠÍTKO: Kreslit oblast | PRAVÉ MYŠÍTKO: Smazat oblast", True, (200, 200, 200))
    hint2 = font.render("C: VYČISTIT STRANU | S: ULOŽIT | ŠIPKY: Listování", True, (150, 150, 150))
    screen.blit(hint1, (20, SCREEN_HEIGHT + 55))
    screen.blit(hint2, (20, SCREEN_HEIGHT + 85))

    # Tlačítko ULOŽIT v UI
    save_btn_rect = pygame.Rect(700, SCREEN_HEIGHT + 15, 80, 40)
    pygame.draw.rect(screen, (40, 80, 40), save_btn_rect, border_radius=5)
    screen.blit(font.render("ULOŽIT", True, (255, 255, 255)), (712, SCREEN_HEIGHT + 24))

    # Input Overlay pro cílovou stranu
    if input_active:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT + UI_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0,0))
        
        # Okénko zadávání
        input_box = pygame.Rect(SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 - 50, 300, 100)
        pygame.draw.rect(screen, (50, 50, 60), input_box, border_radius=10)
        pygame.draw.rect(screen, (200, 200, 255), input_box, 2, border_radius=10)
        
        prompt = font.render("CÍLOVÁ STRANA (ČÍSLO):", True, (255, 255, 0))
        screen.blit(prompt, (input_box.x + 45, input_box.y + 20))
        
        txt = font_big.render(input_text + "|", True, (255, 255, 255))
        screen.blit(txt, (input_box.centerx - txt.get_width()//2, input_box.y + 50))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
