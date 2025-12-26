import pygame
import os
import random
import json
import math
import asyncio
import sys
import re

def resource_path(relative_path):
    """ Získá absolutní cestu k prostředkům, funguje pro vývoj i pro PyInstaller balíček """
    try:
        # PyInstaller vytvoří dočasnou složku a uloží cestu do _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Konfigurace
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 30

# Cesty
IMG_FOLDER = resource_path("obrazky_optimalizovane")
DATA_PATH = resource_path("data/mapa.json")
UI_BG_PATH = resource_path("assets/ui_bg.png")
DICE_SHEET_PATH = resource_path("assets/dice_sheet.png")
MUSIC_PATH = resource_path("assets/music.mp3")

# Funkce pro extrakci čísel ze jména souboru (pro správné řazení)
def extract_number(filename):
    match = re.search(r'(\d+)', filename)
    return int(match.group(1)) if match else 0

# Funkce hodu kostkou
def throw_dice():
    return random.randint(1, 6)

# Inicializace
pygame.init()
pygame.mixer.init() # Explicitní inicializace pro zvuk
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME)
pygame.display.set_caption("Na rozkaz krále")
clock = pygame.time.Clock()

# Hudba na pozadí (načtení, ale spuštění až po assetech)
if os.path.exists(MUSIC_PATH):
    pygame.mixer.music.load(MUSIC_PATH)
    # play(-1) přesunuto níže

# Font pro text
font_small = pygame.font.SysFont("Verdana", 18, bold=True)
font_medium = pygame.font.SysFont("Verdana", 14, bold=True) # Zmenšeno o 50% z 28

# Načtení grafiky UI (vypnuto na žádost uživatele)
ui_frame = None

dice_images = []
for i in range(1, 7):
    path = resource_path(f"assets/dice/dice_{i}.png")
    if os.path.exists(path):
        img = pygame.image.load(path).convert_alpha()
        dice_images.append(pygame.transform.scale(img, (60, 60))) # Zmenšeno o 50% z 120
    else:
        print(f"[VAROVÁNÍ] Chybí kostka: {path}")

# Načtení tlačítek
btn_roll_img_path = resource_path("assets/btn_roll.png")
btn_roll_img = None
if os.path.exists(btn_roll_img_path):
    btn_roll_img = pygame.image.load(btn_roll_img_path).convert_alpha()

btn_continue_img_path = resource_path("assets/btn_continue.png")
btn_continue_img = None
if os.path.exists(btn_continue_img_path):
    btn_continue_img = pygame.image.load(btn_continue_img_path).convert_alpha()

# Načtení mapy větvení
if not os.path.exists(os.path.dirname(DATA_PATH)):
    os.makedirs(os.path.dirname(DATA_PATH))

if not os.path.exists(DATA_PATH):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump({}, f)

with open(DATA_PATH, "r", encoding="utf-8") as f:
    try:
        story_map = json.load(f)
    except json.JSONDecodeError:
        story_map = {}

# Načtení obrázků seřazených podle čísla
if not os.path.exists(IMG_FOLDER):
    os.makedirs(IMG_FOLDER)

images = []
image_files = sorted([f for f in os.listdir(IMG_FOLDER) if f.lower().endswith(".jpg")], key=extract_number)
total_files = len(image_files)

# LOADING SCREEN
for idx, file in enumerate(image_files):
    # Vykreslení loading screenu
    screen.fill((20, 20, 30))
    progress = int((idx / total_files) * 100) if total_files > 0 else 100
    loading_text = font_medium.render(f"Načítání dobrodružství... {progress}%", True, (200, 200, 200))
    screen.blit(loading_text, (SCREEN_WIDTH // 2 - loading_text.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.flip()
    
    # Načtení a transformace
    img = pygame.image.load(os.path.join(IMG_FOLDER, file)).convert()
    img = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    images.append(img)
    
    # Ošetření eventů (aby okno nezamrzlo)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

# Spuštění hudby až po načtení všeho
if os.path.exists(MUSIC_PATH):
    pygame.mixer.music.play(-1)

# Placeholder if no images found
if not images:
    placeholder = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    placeholder.fill((30, 30, 40))
    images.append(placeholder)
    image_files = ["placeholder.png"]

# Aktuální stránka (indexujeme od 0)
current_page = 0 

# Pozice UI prvků (souřadnice levého horního rohu pro tlačítka)
dice_button_pos = (7, 553)
continue_button_pos = (7, 553) 
dice_result_pos = (SCREEN_WIDTH // 2 - 30, SCREEN_HEIGHT // 2 - 30) # Vycentrováno pro 60x60

page_dice_rolled = False # Sleduje, zda se na aktuální stránce už házelo

show_dice_result = False
dice_value = None
dice_button_active = False
continue_button_active = False
debug_mode = False

# Klikací oblasti pro tlačítka (vytvoříme globálně pro loop)
dice_button_click_rect = pygame.Rect(0,0,0,0)
continue_button_click_rect = pygame.Rect(0,0,0,0)

# Animace hodu
is_rolling = False
roll_start_time = 0
roll_duration = 1200 # mírně delší pro efekt

async def main():
    global current_page, page_dice_rolled, show_dice_result, dice_value, is_rolling, roll_start_time, debug_mode, \
           continue_button_active, continue_button_click_rect, dice_button_active, dice_button_click_rect
    running = True
    while running:
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    debug_mode = not debug_mode
                    print(f"[DEBUG] Režim ladění: {'ZAPNUT' if debug_mode else 'VYPNUT'}")
                elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                page_id = str(current_page + 1)
                
                if is_rolling:
                    continue

                # 1. Tlačítko hodu kostkou
                if dice_button_active and dice_button_click_rect.collidepoint(x, y):
                    is_rolling = True
                    roll_start_time = current_time
                    dice_button_active = False
                    print("[DEBUG] Hážu kostkou...")
                    continue

                # 2. Tlačítko pokračovat
                if continue_button_active and continue_button_click_rect.collidepoint(x, y):
                    if page_id in story_map and "dice" in story_map[page_id]:
                        dice_targets = story_map[page_id]["dice"]
                        target_page = None
                        
                        # 1. Přesná shoda (např. "4")
                        if str(dice_value) in dice_targets:
                            target_page = dice_targets[str(dice_value)]
                        else:
                            # 2. Rozsah (např. "1-3")
                            for key, val in dice_targets.items():
                                if "-" in key:
                                    try:
                                        start, end = map(int, key.split("-"))
                                        if start <= dice_value <= end:
                                            target_page = val
                                            break
                                    except: continue
                        
                        if target_page is not None:
                            goto_page = target_page - 1
                            if 0 <= goto_page < len(images):
                                current_page = goto_page
                                page_dice_rolled = False # Nová strana -> můžeme házet znovu (pokud tam hody jsou)
                                if current_page == 0 and os.path.exists(MUSIC_PATH):
                                    pygame.mixer.music.play(-1) # Restart od začátku
                        else:
                            # Pokud hod nevedl na novou stranu (např. str 54), označíme jako hozeno
                            page_dice_rolled = True
                            
                    show_dice_result = False
                    continue_button_active = False
                    continue

                # 3. Klikací oblasti na stránce (Zakázáno během hodu/výsledku)
                if not is_rolling and not show_dice_result:
                    rel_x = x
                    rel_y = y
                    
                    if page_id in story_map and "choices" in story_map[page_id]:
                        for choice in story_map[page_id]["choices"]:
                            x1, y1, x2, y2 = choice["area"]
                            if x1 <= rel_x <= x2 and y1 <= rel_y <= y2:
                                goto_page = choice["goto"] - 1
                                if 0 <= goto_page < len(images):
                                    current_page = goto_page
                                    if current_page == 0 and os.path.exists(MUSIC_PATH):
                                        pygame.mixer.music.play(-1) # Restart od začátku
                                    show_dice_result = False
                                    page_dice_rolled = False # Změna strany
                                    print(f"[DEBUG] Kliknuto na oblast -> Strana {choice['goto']}")
                                break

        # --- VYKRESLOVÁNÍ ---
        screen.fill((20, 20, 30)) # Tmavé pozadí pro jistotu

        # 1. Pozadí (můžeme nechat tmavé nebo nějakou texturu)
        screen.fill((20, 20, 30))

        # 2. Stránka knihy (přes celou obrazovku)
        if current_page < len(images):
            page_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
            screen.blit(images[current_page], (0, 0))

        page_id = str(current_page + 1)
        
        # --- LOGIKA A UI PRVKY ---
        
        # Animace hodu kostkou
        if is_rolling:
            elapsed = current_time - roll_start_time
            if elapsed < roll_duration:
                if dice_images:
                    pick = (current_time // 100) % len(dice_images)
                    screen.blit(dice_images[pick], dice_result_pos)
                else:
                    pygame.draw.rect(screen, (255, 255, 255), (dice_result_pos[0]-10, dice_result_pos[1]-5, 220, 50), border_radius=10)
                    text = font_medium.render("Hází se...", True, (50, 50, 50))
                    screen.blit(text, dice_result_pos)
            else:
                is_rolling = False
                dice_value = throw_dice()
                show_dice_result = True
                continue_button_active = True
                print(f"[DEBUG] Hozeno: {dice_value}")

        # Ladicí obdélníky
        if debug_mode:
            if page_id in story_map:
                for choice in story_map[page_id].get("choices", []):
                    rx1, ry1, rx2, ry2 = choice["area"]
                    pygame.draw.rect(screen, (255, 0, 0), (rx1, ry1, rx2-rx1, ry2-ry1), 2)
                    label = font_small.render(f"ID:{choice['goto']}", True, (255, 0, 0))
                    screen.blit(label, (rx1, ry1 - 25))
                
                if "dice" in story_map[page_id] and story_map[page_id]["dice"]:
                    dice_status = f"DICE: {story_map[page_id]['dice']}"
                    lbl = font_small.render(dice_status, True, (255, 255, 0))
                    screen.blit(lbl, (50, 50))

        # Tlačítko hodu
        has_dice = page_id in story_map and "dice" in story_map[page_id] and story_map[page_id]["dice"]
        if has_dice and not show_dice_result and not is_rolling and not page_dice_rolled:
            dice_button_active = True
            hover_offset = int(math.sin(current_time / 200) * 5)
            # Rozměr tlačítka je 150x40 (zmenšeno)
            bw, bh = 150, 40
            # Přesunuto na levý okraj dolů (7px od okraje)
            btn_rect = pygame.Rect(7, SCREEN_HEIGHT - bh - 7 + hover_offset, bw, bh)
            dice_button_click_rect = btn_rect 
            
            if btn_roll_img:
                screen.blit(btn_roll_img, btn_rect)
            else:
                pygame.draw.rect(screen, (139, 69, 19), btn_rect, border_radius=5)
                pygame.draw.rect(screen, (255, 215, 0), btn_rect, 2, border_radius=5)
                text = font_small.render("HOD KOSTKOU", True, (255, 215, 0))
                screen.blit(text, (btn_rect.x + (bw - text.get_width())//2, btn_rect.y + (bh - text.get_height())//2))
        else:
            dice_button_active = False
            dice_button_click_rect = pygame.Rect(0,0,0,0)

        # Výsledek hodu a tlačítko pokračovat
        if show_dice_result:
            if dice_images:
                dice_idx = (dice_value - 1) % len(dice_images)
                screen.blit(dice_images[dice_idx], dice_result_pos)
                
            res_text = font_medium.render(f"HOZENO: {dice_value}", True, (255, 255, 255))
            shadow = font_medium.render(f"HOZENO: {dice_value}", True, (0,0,0))
            text_x = SCREEN_WIDTH // 2 - res_text.get_width() // 2
            text_y = dice_result_pos[1] - 30
            screen.blit(shadow, (text_x + 1, text_y + 1))
            screen.blit(res_text, (text_x, text_y))
            
            bw, bh = 150, 40
            cont_rect = pygame.Rect(7, SCREEN_HEIGHT - bh - 7, bw, bh)
            continue_button_active = True
            continue_button_click_rect = cont_rect
            
            if btn_continue_img:
                screen.blit(btn_continue_img, cont_rect)
            else:
                pygame.draw.rect(screen, (34, 139, 34), cont_rect, border_radius=10)
                pygame.draw.rect(screen, (255, 255, 255), cont_rect, 2, border_radius=10)
                text = font_small.render("POKRAČOVAT", True, (255, 255, 255))
                screen.blit(text, (cont_rect.x + 20, cont_rect.y + 15))
        else:
            continue_button_click_rect = pygame.Rect(0,0,0,0)

        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(0) # Důležité pro webový prohlížeč (pygbag)

if __name__ == "__main__":
    asyncio.run(main())
