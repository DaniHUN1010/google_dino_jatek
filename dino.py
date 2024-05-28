import pygame
import random
import time
from itertools import cycle

# Pygame inicializálása
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Ablak mérete
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

# Háttérkép betöltése
BG = pygame.transform.scale(pygame.image.load("kepek/hatter.jpg"), (width, height))
bg_x = 0

# FPS osztály az FPS megjelenítéséhez
class FPS:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Calibri", 30, bold=True)

    def render(self, display):
        fps_text = self.font.render(f"FPS: {round(self.clock.get_fps(), 1)}", True, (255, 255, 255))
        display.blit(fps_text, (675, 10))

fps = FPS()

# Karakter adatai
rect_width, rect_height = 75, 85  # Sprite méret
rect_x, rect_y = width // 2 - rect_width // 2, height - rect_height
rect_speed = 5  # Vízszintes sebesség

# Karakter képek betöltése és méretezése
character_right = pygame.image.load("sprite/character/base_right.png").convert_alpha()
character_left = pygame.image.load("sprite/character/base_left.png").convert_alpha()
character_jump_right = pygame.image.load("sprite/character/jump/jump_right.png").convert_alpha()
character_jump_left = pygame.image.load("sprite/character/jump/jump_left.png").convert_alpha()
idle_right_images = [pygame.image.load("sprite/character/idle/idle_right1.png").convert_alpha()]
idle_left_images = [pygame.image.load("sprite/character/idle/idle_left1.png").convert_alpha()]

# Mozgás animáció képek betöltése
move_right_images = [pygame.image.load(f"sprite/character/move/move_right{i}.png").convert_alpha() for i in range(1, 6)]
move_left_images = [pygame.image.load(f"sprite/character/move/move_left{i}.png").convert_alpha() for i in range(1, 6)]

# Rugás animáció képek betöltése
kick_right_images = [pygame.image.load("sprite/character/kick/kick_right1.png").convert_alpha(),
                     pygame.image.load("sprite/character/kick/kick_right2.png").convert_alpha()]
kick_left_images = [pygame.image.load("sprite/character/kick/kick_left1.png").convert_alpha(),
                    pygame.image.load("sprite/character/kick/kick_left2.png").convert_alpha()]

# Karakter képek méretezése
character_right = pygame.transform.scale(character_right, (rect_width, rect_height))
character_left = pygame.transform.scale(character_left, (rect_width, rect_height))
character_jump_right = pygame.transform.scale(character_jump_right, (rect_width, rect_height))
character_jump_left = pygame.transform.scale(character_jump_left, (rect_width, rect_height))
idle_right_images = [pygame.transform.scale(img, (rect_width, rect_height)) for img in idle_right_images]
idle_left_images = [pygame.transform.scale(img, (rect_width, rect_height)) for img in idle_left_images]
move_right_images = [pygame.transform.scale(img, (rect_width, rect_height)) for img in move_right_images]
move_left_images = [pygame.transform.scale(img, (rect_width, rect_height)) for img in move_left_images]
kick_right_images = [pygame.transform.scale(img, (rect_width, rect_height)) for img in kick_right_images]
kick_left_images = [pygame.transform.scale(img, (rect_width, rect_height)) for img in kick_left_images]

current_character = character_right  # Kezdő nézet

# Ugrás változók
is_jumping = False
is_falling = False
jump_height = rect_height * 2  # Ugrási magasság
jump_speed = rect_speed * 2  # Ugrási sebesség növelése a gyors felugráshoz
fall_speed = jump_speed * 1  # Esési sebesség
initial_y = rect_y
max_jump_height = initial_y - jump_height

# Támadás változók
is_attacking = False
attack_start_time = 0
attack_duration = 0.4  # 0.4 másodperc (két képkocka 0.2 másodpercenként)
last_kick_time = 0
kick_cooldown = 1  # 1 másodperc

# Időszámláló
start_time = time.time()

# Betűtípus
font = pygame.font.Font(None, 36)

# Játék kezdőképernyője
show_start_message = True
show_easy_message = False
show_cancel_button = False

# Zene betöltése
start_sound = pygame.mixer.Sound("zenek/start.mp3")
elso_track = pygame.mixer.Sound("zenek/elso_track.wav")
masodik_track = pygame.mixer.Sound("zenek/masodik_track.wav")
harmadik_track = pygame.mixer.Sound("zenek/harmadik_track.mp3")

# Ready és Go képek betöltése
ready_image = pygame.image.load("kepek/ready.png").convert_alpha()
go_image = pygame.image.load("kepek/go.png").convert_alpha()

# Zene késleltetési változók
play_track_delay = 1  # Másodperc
next_track_time = None
current_track_index = 0
tracks = [elso_track, masodik_track, harmadik_track]

def play_next_track():
    global current_track_index, next_track_time
    if current_track_index < len(tracks):
        tracks[current_track_index].play()
        next_track_time = time.time() + tracks[current_track_index].get_length() + play_track_delay
        current_track_index += 1

def start_game():
    global start_time
    start_time = time.time()
    play_next_track()

def show_ready_go():
    screen.fill((0, 0, 0))
    screen.blit(ready_image, (width // 2 - ready_image.get_width() // 2, height // 2 - ready_image.get_height() // 2))
    pygame.display.update()
    time.sleep(1)  # 1 másodperc várakozás

    screen.fill((0, 0, 0))
    screen.blit(go_image, (width // 2 - go_image.get_width() // 2, height // 2 - go_image.get_height() // 2))
    pygame.display.update()
    time.sleep(1)  # 1 másodperc várakozás

# Tégla méretek és pozíciók a nehézségi fokokhoz
button_width, button_height = 200, 50
easy_button_rect = pygame.Rect(width // 2 - button_width // 2, height // 2 - 100, button_width, button_height)
medium_button_rect = pygame.Rect(width // 2 - button_width // 2, height // 2, button_width, button_height)
hard_button_rect = pygame.Rect(width // 2 - button_width // 2, height // 2 + 100, button_width, button_height)
cancel_button_rect = pygame.Rect(10, height - 60, 100, 50)

# Színek
button_color = (70, 130, 180)
text_color = (255, 255, 255)

# Animációs vezérlés
idle_time = 2000  # Idő milliszekundumban, mielőtt az animáció elindul
idle_clock = pygame.time.get_ticks()
is_idle = False

# Képváltási időzítő
image_change_time = 100  # 0.1 másodperc képenként
image_change_clock = pygame.time.get_ticks()

# Képek ciklikus váltása
right_idle_cycle = cycle([character_right] + idle_right_images)
left_idle_cycle = cycle([character_left] + idle_left_images)
move_right_cycle = cycle(move_right_images)
move_left_cycle = cycle(move_left_images)
kick_right_cycle = cycle(kick_right_images)
kick_left_cycle = cycle(kick_left_images)

# Fő játékciklus
running = True
facing_right = True  # Jelenlegi nézési irány
is_moving = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if show_start_message:
                if easy_button_rect.collidepoint(mouse_pos):
                    show_start_message = False
                    show_easy_message = True
                    show_cancel_button = True
                elif medium_button_rect.collidepoint(mouse_pos) or hard_button_rect.collidepoint(mouse_pos):
                    show_start_message = False
                    start_sound.play()
                    show_ready_go()
                    start_game()
            elif show_easy_message and show_cancel_button:
                if cancel_button_rect.collidepoint(mouse_pos):
                    show_easy_message = False
                    show_start_message = True
                    show_cancel_button = False

    if show_start_message:
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, button_color, easy_button_rect)
        pygame.draw.rect(screen, button_color, medium_button_rect)
        pygame.draw.rect(screen, button_color, hard_button_rect)

        easy_text = font.render("Könnyű", True, text_color)
        medium_text = font.render("Közepes", True, text_color)
        hard_text = font.render("Nehéz", True, text_color)

        screen.blit(easy_text, (easy_button_rect.centerx - easy_text.get_width() // 2, easy_button_rect.centery - easy_text.get_height() // 2))
        screen.blit(medium_text, (medium_button_rect.centerx - medium_text.get_width() // 2, medium_button_rect.centery - medium_text.get_height() // 2))
        screen.blit(hard_text, (hard_button_rect.centerx - hard_text.get_width() // 2, hard_button_rect.centery - hard_text.get_height() // 2))

        pygame.display.update()

    elif show_easy_message:
        screen.fill((0, 0, 0))
        easy_message = font.render("Tudsz te ennél jobbat is!", True, text_color)
        screen.blit(easy_message, (width // 2 - easy_message.get_width() // 2, height // 2 - easy_message.get_height() // 2))

        if show_cancel_button:
            pygame.draw.rect(screen, button_color, cancel_button_rect)
            cancel_text = font.render("Mégse", True, text_color)
            screen.blit(cancel_text, (cancel_button_rect.centerx - cancel_text.get_width() // 2, cancel_button_rect.centery - cancel_text.get_height() // 2))

        pygame.display.update()

    else:
        if next_track_time and time.time() >= next_track_time:
            play_next_track()

        # Billentyűzet bemenetek kezelése
        keys = pygame.key.get_pressed()
        if any(keys) and not is_attacking:
            idle_clock = pygame.time.get_ticks()
            is_idle = False
            is_moving = True
            if keys[pygame.K_LEFT]:
                bg_x += rect_speed
                if pygame.time.get_ticks() - image_change_clock >= image_change_time:
                    image_change_clock = pygame.time.get_ticks()
                    current_character = next(move_left_cycle)
                facing_right = False
            if keys[pygame.K_RIGHT]:
                bg_x -= rect_speed
                if pygame.time.get_ticks() - image_change_clock >= image_change_time:
                    image_change_clock = pygame.time.get_ticks()
                    current_character = next(move_right_cycle)
                facing_right = True
            if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and not is_jumping and not is_falling:
                is_jumping = True
                if keys[pygame.K_LEFT]:
                    current_character = character_jump_left
                elif keys[pygame.K_RIGHT]:
                    current_character = character_jump_right
                else:
                    current_character = character_jump_left if current_character == character_left else character_jump_right
            if not (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and is_jumping:
                is_jumping = False
                is_falling = True
            if keys[pygame.K_x] and time.time() - last_kick_time >= kick_cooldown:  # Kick cooldown ellenőrzése
                is_attacking = True
                attack_start_time = time.time()
                last_kick_time = time.time()  # Utolsó rúgás időpontjának frissítése
                if facing_right:
                    attack_cycle = cycle(kick_right_images)
                else:
                    attack_cycle = cycle(kick_left_images)
        else:
            is_moving = False
            if pygame.time.get_ticks() - idle_clock >= idle_time:
                is_idle = True
                if pygame.time.get_ticks() - image_change_clock >= image_change_time*7:
                    image_change_clock = pygame.time.get_ticks()
                    if facing_right:
                        current_character = next(right_idle_cycle)
                    else:
                        current_character = next(left_idle_cycle)
            else:
                is_idle = False

        # Ha nincs mozgás, visszaáll az alapállapotba
        if not is_moving and not is_jumping and not is_falling and not is_idle and not is_attacking:
            current_character = character_right if facing_right else character_left

        # Támadás animáció kezelése
        if is_attacking:
            if time.time() - attack_start_time >= attack_duration:
                is_attacking = False
                current_character = character_right if facing_right else character_left
            else:
                if pygame.time.get_ticks() - image_change_clock >= image_change_time * 2:
                    image_change_clock = pygame.time.get_ticks()
                    current_character = next(attack_cycle)

        # Háttér mozgatása és ismétlése
        bg_x = bg_x % width  # A háttérkép folyamatos ismétlődésének biztosítása
        screen.blit(BG, (bg_x - width, 0))  # Háttérkép bal oldalon
        screen.blit(BG, (bg_x, 0))  # Háttérkép középen
        screen.blit(BG, (bg_x + width, 0))  # Háttérkép jobb oldalon

        # Ugrás kezelése
        if is_jumping:
            rect_y -= jump_speed
            if rect_y <= max_jump_height:
                rect_y = max_jump_height
                is_jumping = False
                is_falling = True

        # Esés kezelése
        if is_falling:
            rect_y += fall_speed
            if rect_y >= initial_y:
                rect_y = initial_y
                is_falling = False
                current_character = character_left if current_character == character_jump_left else character_right

        # Karakter kirajzolása
        screen.blit(current_character, (rect_x, rect_y))

        # FPS kirajzolása
        fps.render(screen)

        # Időszámláló kirajzolása
        elapsed_time = int(time.time() - start_time)
        time_text = font.render(f"Idő: {elapsed_time}", True, (255, 255, 255))
        screen.blit(time_text, (10, 10))

        # Képernyő frissítése
        pygame.display.update()

        # FPS szabályozása
        fps.clock.tick(75)

# Pygame leállítása
pygame.quit()
