import pygame
import os
import json
import re

# Konfigurace
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MAP_FILE = "data/mapa.json"
IMG_FOLDER = "obrazky_stylizovane" if os.path.exists("obrazky_stylizovane") else "obrazky_hra"

def extract_number(filename):
    match = re.search(r'(\d+)', filename)
    return int(match.group(1)) if match else 0

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + 100))
pygame.display.set_caption("HERNÍ EDITOR - Na rozkaz krále")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

# Načtení dat
if os.path.exists(MAP_FILE):
    with open(MAP_FILE, "r", encoding="utf-8") as f:
        story_map = json.load(f)
else:
    story_map = {}

image_files = sorted([f for f in os.listdir(IMG_FOLDER) if f.endswith(".png")], key=extract_number)
images = []
for file in image_files:
    img = pygame.image.load(os.path.join(IMG_FOLDER, file))
    img = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    images.append(img)

current_page_idx = 0
points = []
edit_mode = "CHOICES" # CHOICES, DICE
selected_dice_result = 1

def save_map():
    with open(MAP_FILE, "w", encoding="utf-8") as f:
        json.dump(story_map, f, ensure_ascii=False, indent=4)
    print("Změny uloženy!")

running = True
while running:
    current_page_id = str(current_page_idx + 1)
    if current_page_id not in story_map:
        story_map[current_page_id] = {"choices": [], "dice": {}}

    page_data = story_map[current_page_id]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                current_page_idx = (current_page_idx + 1) % len(images)
                points.clear()
            elif event.key == pygame.K_LEFT:
                current_page_idx = (current_page_idx - 1) % len(images)
                points.clear()
            elif event.key == pygame.K_s:
                save_map()
            elif event.key == pygame.K_m:
                 edit_mode = "DICE" if edit_mode == "CHOICES" else "CHOICES"
            elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6]:
                if edit_mode == "DICE":
                    selected_dice_result = int(event.unicode)
            elif event.key == pygame.K_d: # Smazat poslední oblast nebo dice roll
                if edit_mode == "CHOICES" and page_data["choices"]:
                    page_data["choices"].pop()
                elif edit_mode == "DICE" and str(selected_dice_result) in page_data["dice"]:
                    del page_data["dice"][str(selected_dice_result)]

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if y < SCREEN_HEIGHT: # Klik do obrázku
                if edit_mode == "CHOICES":
                    points.append((x, y))
                    if len(points) == 2:
                        target = input(f"Zadej cílovou stranu pro tuto oblast: ")
                        try:
                            goto_val = int(target)
                            page_data["choices"].append({
                                "area": [points[0][0], points[0][1], points[1][0], points[1][1]],
                                "goto": goto_val
                            })
                        except:
                            print("Neplatné číslo!")
                        points.clear()
                elif edit_mode == "DICE":
                    print(f"\n>>> NASTAVUJI HOD {selected_dice_result} PRO STRANU {current_page_id} <<<")
                    target = input(f"Zadej cílovou stranu pro hod {selected_dice_result} (v TERMINÁLU!): ")
                    try:
                        page_data["dice"][str(selected_dice_result)] = int(target)
                        print(f"Uloženo: Hod {selected_dice_result} -> Strana {target}")
                    except:
                        print("Neplatné číslo!")

    # Vykreslení
    screen.fill((50, 50, 50))
    screen.blit(images[current_page_idx], (0, 0))

    # Kreslení oblastí
    for choice in page_data["choices"]:
        x1, y1, x2, y2 = choice["area"]
        pygame.draw.rect(screen, (0, 255, 0), (x1, y1, x2-x1, y2-y1), 2)
        lbl = font.render(str(choice["goto"]), True, (0, 255, 0))
        screen.blit(lbl, (x1, y1 - 20))

    # Kreslení aktuálně tvořené oblasti
    for p in points:
        pygame.draw.circle(screen, (255, 0, 0), p, 5)

    # UI spodní panel
    pygame.draw.rect(screen, (30, 30, 30), (0, SCREEN_HEIGHT, SCREEN_WIDTH, 100))
    info = font.render(f"Strana: {current_page_id} | Mód: {edit_mode} | [M] Přepnout mód | [S] Uložit | [D] Smazat", True, (255, 255, 255))
    screen.blit(info, (10, SCREEN_HEIGHT + 10))

    if edit_mode == "DICE":
        # Seznam všech 6 kostek
        for i in range(1, 7):
            color = (255, 255, 0) if i == selected_dice_result else (150, 150, 150)
            status = "NASTAVENO" if str(i) in page_data["dice"] else "PRÁZDNÉ"
            target = page_data["dice"].get(str(i), "?")
            dice_lbl = font.render(f"Kostka [{i}]: {status} -> Strana {target}", True, color)
            screen.blit(dice_lbl, (10, SCREEN_HEIGHT + 40 + (i-1)*15))
        
        sel_info = font.render(f"VYBRÁN HOD: {selected_dice_result} | KLIKNI DO OBRAZU!", True, (255, 255, 0))
        screen.blit(sel_info, (300, SCREEN_HEIGHT + 40))
        
        hint = font.render("Stiskni 1-6 pro výběr kostky, pak klikni do obrazu.", True, (150, 150, 150))
        screen.blit(hint, (300, SCREEN_HEIGHT + 65))
    else:
        instr = font.render("Klikni 2x do obrazu pro vytvoření nové klikací oblasti", True, (200, 200, 200))
        screen.blit(instr, (10, SCREEN_HEIGHT + 40))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
