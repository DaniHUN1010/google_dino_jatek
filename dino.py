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
bg_speed_factor = 1.5  # Háttér sebesség faktor

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

# Elkerülés animáció képek betöltése
avoid_right_images = [pygame.image.load("sprite/character/avoid/avoid_right1.png").convert_alpha(),
                      pygame.image.load("sprite/character/avoid/avoid_right2.png").convert_alpha()]
avoid_left_images = [pygame.image.load("sprite/character/avoid/avoid_left1.png").convert_alpha(),
                     pygame.image.load("sprite/character/avoid/avoid_left2.png").convert_alpha()]

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
avoid_right_images = [pygame.transform.scale(img, (rect_width, rect_height)) for img in avoid_right_images]
avoid_left_images = [pygame.transform.scale(img, (rect_width, rect_height)) for img in avoid_left_images]

current_character = character_right  # Kezdő nézet

# Ugrás változók
is_jumping = False
is_falling = False
jump_height = rect_height * 2  # Ugrási magasság
jump_speed = rect_speed * 2  # Ugrási sebesség növelése a gyors felugráshoz
fall_speed = jump_speed  # Esési sebesség
initial_y = rect_y
max_jump_height = initial_y - jump_height

# Támadás változók
is_attacking = False
attack_start_time = 0
attack_duration = 0.4  # 0.4 másodperc (két képkocka 0.2 másodpercenként)
last_kick_time = 0
kick_cooldown = 1  # 1 másodperc

# Elkerülés változók
is_avoiding = False
avoid_start_time = 0
avoid_duration = 0.2  # 0.2 másodperc
last_avoid_time = 0
avoid_cooldown = 1  # 1 másodperc

# Időszámláló
start_time = time.time()

# Betűtípus
font = pygame.font.Font(None, 36)

# Játék kezdőképernyője
show_start_message = True

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
avoid_right_cycle = cycle(avoid_right_images)
avoid_left_cycle = cycle(avoid_left_images)

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
                start_sound.play()
                show_start_message = False
                show_ready_go()
                start_game()

    if show_start_message:
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 60)
        start_text = font.render("Nyomd meg a gombot a kezdéshez!", True, (255, 255, 255))
        screen.blit(start_text, (width // 2 - start_text.get_width() // 2, height // 2 - start_text.get_height() // 2))
        pygame.display.update()
        continue

    keys = pygame.key.get_pressed()
    if not is_attacking and not is_avoiding:
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and rect_x > 0:
            rect_x -= rect_speed
            current_character = next(move_left_cycle)
            facing_right = False
            is_moving = True
            idle_clock = pygame.time.get_ticks()
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and rect_x < width - rect_width:
            rect_x += rect_speed
            current_character = next(move_right_cycle)
            facing_right = True
            is_moving = True
            idle_clock = pygame.time.get_ticks()
        else:
            is_moving = False
            current_time = pygame.time.get_ticks()
            if current_time - idle_clock >= idle_time:
                is_idle = True
                if current_time - image_change_clock >= image_change_time:
                    current_character = next(right_idle_cycle) if facing_right else next(left_idle_cycle)
                    image_change_clock = current_time
            else:
                current_character = character_right if facing_right else character_left

    if not is_jumping and not is_falling:
        if keys[pygame.K_SPACE]:
            is_jumping = True
            jump_y = rect_y
            rect_y -= jump_speed
            current_character = character_jump_right if facing_right else character_jump_left
    elif is_jumping:
        if rect_y > max_jump_height:
            rect_y -= jump_speed
            current_character = character_jump_right if facing_right else character_jump_left
        else:
            is_jumping = False
            is_falling = True
    elif is_falling:
        if rect_y < initial_y:
            rect_y += fall_speed
            current_character = character_jump_right if facing_right else character_jump_left
        else:
            is_falling = False

    current_time = time.time()
    if not is_avoiding and keys[pygame.K_LSHIFT] and (current_time - last_avoid_time) > avoid_cooldown:
        is_avoiding = True
        avoid_start_time = time.time()
        last_avoid_time = avoid_start_time
        if facing_right:
            current_character = next(avoid_right_cycle)
        else:
            current_character = next(avoid_left_cycle)

    if is_avoiding:
        elapsed_time = time.time() - avoid_start_time
        if elapsed_time < avoid_duration:
            if facing_right:
                current_character = next(avoid_right_cycle)
            else:
                current_character = next(avoid_left_cycle)
        else:
            is_avoiding = False

    if not is_attacking and keys[pygame.K_LCTRL] and (current_time - last_kick_time) > kick_cooldown:
        is_attacking = True
        attack_start_time = time.time()
        last_kick_time = attack_start_time
        if facing_right:
            current_character = next(kick_right_cycle)
        else:
            current_character = next(kick_left_cycle)

    if is_attacking:
        elapsed_time = time.time() - attack_start_time
        if elapsed_time < attack_duration:
            if facing_right:
                current_character = next(kick_right_cycle)
            else:
                current_character = next(kick_left_cycle)
        else:
            is_attacking = False

    current_time = time.time()
    if next_track_time and current_time >= next_track_time:
        play_next_track()

    # Háttér görgetés
    rel_x = bg_x % BG.get_rect().width
    screen.blit(BG, (rel_x - BG.get_rect().width, 0))
    if rel_x < width:
        screen.blit(BG, (rel_x, 0))
    bg_x -= rect_speed // bg_speed_factor

    # Játékos karakter megjelenítése
    screen.blit(current_character, (rect_x, rect_y))

    # Idő megjelenítése
    elapsed_time = int(time.time() - start_time)
    elapsed_text = font.render(f"Idő: {elapsed_time} s", True, (255, 255, 255))
    screen.blit(elapsed_text, (10, 10))

    # FPS megjelenítése
    fps.render(screen)

    # Képfrissítés
    pygame.display.flip()

    # Frame rate beállítása
    fps.clock.tick(75)

pygame.quit()
