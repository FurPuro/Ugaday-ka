import pygame
import random
import os,sys

WORDS = []

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

with open(resource_path("assets/russian.txt"), "r", encoding="utf-8") as f:
    text = f.read()

    WORDS = [w.strip().upper() for w in text.split(',') if len(w.strip()) > 1]
    
pygame.init()
pygame.mixer.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Угадай-ка")

BG_COLOR = (240, 240, 240)
TEXT_COLOR = (50, 50, 50)
SUB_COLOR = (170, 170, 170)
BTN_COLOR = (100, 100, 100)

correctWord = pygame.mixer.Sound(resource_path("assets/correctWord.ogg"))
correctWord.set_volume(0.2)
incorrectWord = pygame.mixer.Sound(resource_path("assets/incorrectWord.mp3"))
incorrectWord.set_volume(0.1)
letter = pygame.mixer.Sound(resource_path("assets/А.ogg"))
letter.set_volume(0.1)

font_main = pygame.font.SysFont("Arial", 70, bold=True)
font_ui = pygame.font.SysFont("Arial", 24)

def reset_game():
    w = random.choice(WORDS).upper()
    wl = []
    for letter in w:
        if letter not in wl:
            wl.append(letter)
    return w, set(), [], 10, False, False, wl

def main():
    word, guessed, used, hp, game_over, win, wordletters = reset_game()
    btn_rect = pygame.Rect(WIDTH//2 - 100, 450, 200, 60)
    btn_rect2 = pygame.Rect(WIDTH//2 - 125, 450, 250, 60)

    running = True
    while running:
        if hp < 0:
            hp = 0

        if hp > 4:
            screen.fill(BG_COLOR)
        else:
            screen.fill((205+50-hp*10,
                         190+hp*10,
                         190+hp*10))
        
        display = " ".join([l if l in guessed else "_" for l in word])
        txt_surf = font_main.render(display, True, TEXT_COLOR)
        screen.blit(txt_surf, (WIDTH//2 - txt_surf.get_width()//2, 200))

        tut = font_ui.render("Чтобы начать играть, нажимайте клавиши на русской раскладке", True, TEXT_COLOR)
        hp_surf = font_ui.render(f"Осталось попыток: {hp} {"!!!" if hp < 5 else ""}", True, TEXT_COLOR)
        used_surf = font_ui.render(f"Использовано: {', '.join(used)}", True, SUB_COLOR)
        screen.blit(tut, (20, 20))
        screen.blit(hp_surf, (20, 60))
        screen.blit(used_surf, (20, 85))

        if game_over:
            msg = "ВЫ ПОБЕДИЛИ!" if win else f"НЕ ПОВЕЗЛО. СЛОВО: {word}"
            msg_surf = font_ui.render(msg, True, (30, 30, 30))
            screen.blit(msg_surf, (WIDTH//2 - msg_surf.get_width()//2, 350))
            
            pygame.draw.rect(screen, BTN_COLOR, btn_rect, border_radius=12)
            btn_txt = font_ui.render("ЕЩЁ РАЗ", True, (255, 255, 255))
            screen.blit(btn_txt, (btn_rect.centerx - btn_txt.get_width()//2, btn_rect.centery - btn_txt.get_height()//2))
        else:
            if hp > 2 and len(guessed) < len(wordletters)-2:
                pygame.draw.rect(screen, BTN_COLOR, btn_rect2, border_radius=12)
                btn_txt = font_ui.render("ПОМОЩЬ (-2 ПОПЫТКИ)", True, (255, 255, 255))
                screen.blit(btn_txt, (btn_rect2.centerx - btn_txt.get_width()//2, btn_rect2.centery - btn_txt.get_height()//2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN and not game_over:
                char = event.unicode.upper()
                if ('А' <= char <= 'Я' or char == 'Ё') and char not in used:
                    if os.path.exists(resource_path(f"assets/{char}.ogg")):
                        letter = pygame.mixer.Sound(resource_path(f"assets/{char}.ogg"))
                        letter.set_volume(0.1)
                        letter.play()
                    used.append(char)
                    if char in word:
                        guessed.add(char)
                    else: hp -= 1

            if event.type == pygame.MOUSEBUTTONDOWN and game_over:
                if btn_rect.collidepoint(event.pos):
                    word, guessed, used, hp, game_over, win, wordletters = reset_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if btn_rect2.collidepoint(event.pos):
                    if hp > 2 and len(guessed) < len(wordletters)-2:
                        ch = random.choice(word)
                        while ch in guessed:
                            ch = random.choice(word)
                        used.append(ch)
                        guessed.add(ch)
                        hp -= 2

        if not game_over:
            if all(l in guessed for l in word): 
                game_over, win = True, True
                pygame.mixer.stop()
                correctWord.play()
            elif hp <= 0: 
                game_over, win = True, False
                pygame.mixer.stop()
                incorrectWord.play()

        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()
