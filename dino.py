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





# Mosquito kezdő pozíciója és mérete
mosquito_size = 50
mosquito_x = width
mosquito_y = 300
mosquito_speed = 6

mosquito1 = pygame.image.load("sprite/mosquito/mosquito_left1.png")
mosquito2 = pygame.image.load("sprite/mosquito/mosquito_left2.png")

mosquito_size = (80, 80)  # Új méret (szélesség, magasság)
mosquito1 = pygame.transform.scale(mosquito1, mosquito_size)
mosquito2 = pygame.transform.scale(mosquito2, mosquito_size)

# Animáció beállítások
frame_duration = 0.2  # Egy képkocka időtartama másodpercben
last_frame_change_time = time.time()
current_frame = 0





# Háttérkép betöltése
BG = pygame.transform.scale(pygame.image.load("kepek/hatter.jpg"), (width, height))
fox_hatter = pygame.transform.scale(pygame.image.load("kepek/fox_hatter.webp"), (width, height))
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
initial_y = rect_y
jump_height = rect_height * 2  # Ugrási magasság
jump_speed = rect_speed * 2.5  # Ugrási sebesség növelése a gyorsabb és magasabb ugráshoz
fall_speed = jump_speed * 0.8  # Esési sebesség egy kicsit kisebb, hogy simább legyen az esés
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

# Ready és Go képek betöltése
ready_image = pygame.image.load("kepek/ready.png").convert_alpha()
go_image = pygame.image.load("kepek/go.png").convert_alpha()

# Zene késleltetési változók
play_track_delay = 1  # Másodpercnext_track_time = None
current_track_index = 0

# Zenék betöltése
start_sound = "zenek/start.mp3"
elso_track = pygame.mixer.Sound("zenek/elso_track.wav")
masodik_track = pygame.mixer.Sound("zenek/masodik_track.wav")
harmadik_track = pygame.mixer.Sound("zenek/harmadik_track.mp3")
negyedik_track = pygame.mixer.Sound("zenek/negyedik_track.mp3")
otodik_track = pygame.mixer.Sound("zenek/otodik_track.mp3")
hatodik_track = pygame.mixer.Sound("zenek/hatodik_track.mp3")
hetedik_track = pygame.mixer.Sound("zenek/hetedik_track.mp3")
nyolcadik_track = pygame.mixer.Sound("zenek/nyolcadik_track.mp3")
kilencedik_track = pygame.mixer.Sound("zenek/kilencedik_track.mp3")
tizedik_track = pygame.mixer.Sound("zenek/tizedik_track.mp3")

# Trackek betöltése
tracks = [elso_track, masodik_track, harmadik_track, negyedik_track, otodik_track, hatodik_track, hetedik_track, nyolcadik_track, kilencedik_track, tizedik_track]

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
    global start_sound  # Használjuk a globális start_sound változót
    screen.fill((0, 0, 0))
    screen.blit(ready_image, (width // 2 - ready_image.get_width() // 2, height // 2 - ready_image.get_height() // 2))
    pygame.display.update()

    
    # Only play the ready and go sound effects
    pygame.mixer.music.load(start_sound)  # Sound effect
    pygame.mixer.music.play()  # Play sound effect
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
move_image_change_time = 100  # 0.1 másodperc képenként a mozgáshoz
idle_image_change_time = 500  # 0.5 másodperc képenként a várakozáshoz
attack_image_change_time = 300  # 0.3 másodperc képenként a támadáshoz
avoid_image_change_time = 200  # 0.2 másodperc képenként az elkerüléshez
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
game_started = False  # Új változó a játék kezdésének követéséhez

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if not game_started:  # Ha a játék még nem kezdődött el
                game_started = True
                show_ready_go()
                start_game()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE and not is_jumping and not is_falling:  # Csak a space gombra ugrik
                is_jumping = True
                jump_start_y = rect_y  # Az ugrás kezdő y pozíciójának mentése
            elif event.key == pygame.K_UP and not is_jumping and not is_falling:  # Csak a felfelé nyílra ugrik
                is_jumping = True
                jump_start_y = rect_y  # Az ugrás kezdő y pozíciójának mentése
            # Támadás indítása
            elif event.key == pygame.K_x and time.time() - last_kick_time >= kick_cooldown and not is_jumping and not is_falling:
                is_attacking = True
                attack_start_time = time.time()
                last_kick_time = time.time()
                attack_cycle = cycle(kick_right_images if facing_right else kick_left_images)
            elif event.key == pygame.K_LSHIFT and time.time() - last_avoid_time >= avoid_cooldown:  # Avoid cooldown ellenőrzése
                is_avoiding = True
                avoid_start_time = time.time()
                last_avoid_time = time.time()  # Utolsó elkerülés időpontjának frissítése
                if facing_right:
                    avoid_cycle = cycle(avoid_right_images)
                else:
                    avoid_cycle = cycle(avoid_left_images)

    if not game_started:  # Ha a játék még nem kezdődött el
        # Háttérkép kirajzolása a képernyő közepére
        screen.blit(fox_hatter, ((width - BG.get_width()) // 2, (height - BG.get_height()) // 2))
        # Üzenet kirajzolása a kezdéshez
        start_text = font.render("Nyomj egy entert a kezdéshez", True, (255, 255, 255))
        text_rect = start_text.get_rect(center=(width // 2, height // 2))
        screen.blit(start_text, text_rect)
        pygame.display.update()
        continue  # A ciklus újrakezdése
    else:
        if next_track_time and time.time() >= next_track_time:
            play_next_track()

        # Billentyűzet bemenetek kezelése
        keys = pygame.key.get_pressed()
        if any(keys) and not is_attacking and not is_avoiding:
            idle_clock = pygame.time.get_ticks()
            is_idle = False
            is_moving = True
            if keys[pygame.K_LEFT]:
                bg_x += rect_speed  # Háttér mozgása jobbra
                if pygame.time.get_ticks() - image_change_clock >= move_image_change_time:
                    image_change_clock = pygame.time.get_ticks()
                    current_character = next(move_left_cycle)
                facing_right = False
            elif keys[pygame.K_RIGHT]:
                bg_x -= rect_speed  # Háttér mozgása balra
                if pygame.time.get_ticks() - image_change_clock >= move_image_change_time:
                    image_change_clock = pygame.time.get_ticks()
                    current_character = next(move_right_cycle)
                facing_right = True
            else:
                is_moving = False
                if facing_right:
                    current_character = character_right
                else:
                    current_character = character_left
                current_character = character_right if facing_right else character_left
        else:
            is_moving = False
            if facing_right:
                current_character = character_right
            else:
                current_character = character_left
            current_character = character_right if facing_right else character_left

        # Ugrás és esés kezelése
        if is_jumping:
            rect_y -= jump_speed
            if rect_y <= max_jump_height:
                is_jumping = False
                is_falling = True
        if is_falling:
            rect_y += fall_speed
            if rect_y >= initial_y:
                is_falling = False
                rect_y = initial_y

        # Támadás logika
        if is_attacking:
            if time.time() - attack_start_time >= attack_duration:
                is_attacking = False
                current_character = character_right if facing_right else character_left
                if is_moving:
                    if facing_right:
                        current_character = next(move_right_cycle)
                    else:
                        current_character = next(move_left_cycle)
            else:
                if pygame.time.get_ticks() - image_change_clock >= attack_image_change_time:
                    image_change_clock = pygame.time.get_ticks()
                    current_character = next(attack_cycle)
        
        # Elkerülés logika
        if is_avoiding:
            if time.time() - avoid_start_time >= avoid_duration:
                is_avoiding = False
                current_character = character_right if facing_right else character_left
                if is_moving:
                    if facing_right:
                        current_character = next(move_right_cycle)
                    else:
                        current_character = next(move_left_cycle)
            else:
                if pygame.time.get_ticks() - image_change_clock >= avoid_image_change_time:
                    image_change_clock = pygame.time.get_ticks()
                    current_character = next(avoid_cycle)


        # Háttér mozgatása és ismétlése
        bg_x = bg_x % width  # A háttérkép folyamatos ismétlődésének biztosítása
        screen.blit(BG, (bg_x - width, 0))  # Háttérkép bal oldalon
        screen.blit(BG, (bg_x, 0))  # Háttérkép középen
        screen.blit(BG, (bg_x + width, 0))  # Háttérkép jobb oldalon
        

        # Karakter megjelenítése
        screen.blit(current_character, (rect_x, rect_y))
            
        # FPS megjelenítése
        fps.render(screen)

        # Időszámláló kirajzolása
        elapsed_time = int(time.time() - start_time)
        time_text = font.render(f"Idő: {elapsed_time}", True, (255, 255, 255))
        screen.blit(time_text, (10, 10))




        # Moswuito mozgatása balra
        mosquito_x -= mosquito_speed

        # Ha a kocka elhagyja a képernyőt balról, kezdjük újra jobbról
        if mosquito_x < -mosquito1.get_width():
            mosquito_x = width

        # Animáció váltása
        current_time = time.time()
        if current_time - last_frame_change_time >= frame_duration:
            current_frame = (current_frame + 1) % 2  # Váltás a két képkocka között
            last_frame_change_time = current_time




        # Képernyő frissítése
        if current_frame == 0:
            screen.blit(mosquito1, (mosquito_x, mosquito_y))  # Első képkocka rajzolása
        else:
            screen.blit(mosquito2, (mosquito_x, mosquito_y))  # Második képkocka rajzolása
        pygame.display.update()
        
        # Ütközés ellenőrzése (mosquito)
        mosquito_rect = mosquito1.get_rect(topleft=(mosquito_x, mosquito_y))
        character_rect = current_character.get_rect(topleft=(rect_x, rect_y))
        
        if mosquito_rect.colliderect(character_rect):
            running = False


        # FPS korlátozása
        fps.clock.tick(75)

# Pygame kilépése
pygame.quit()