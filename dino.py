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
pygame.display.set_caption("Dino Game")


# Mosquito kezdő pozíciója és mérete
mosquito_size = 50
mosquito_x = width
mosquito_y = 295
mosquito_speed = 3.5

mosquito1 = pygame.image.load("sprite/mosquito/mosquito1.png")
mosquito2 = pygame.image.load("sprite/mosquito/mosquito2.png")

mosquito_size = (80, 80)  # Új méret (szélesség, magasság)
mosquito1 = pygame.transform.scale(mosquito1, mosquito_size)
mosquito2 = pygame.transform.scale(mosquito2, mosquito_size)
# Turtle kezdő pozíciója és mérete
turtle_size = 50
turtle_x = width
turtle_y = 530
turtle_speed = 2.4  # Csökkentett sebesség a könnyebb játék érdekében

turtle = pygame.image.load("sprite/turtle/turtle_left.png")
turtle1 = pygame.image.load("sprite/turtle/turtle_left1.png")
turtle2 = pygame.image.load("sprite/turtle/turtle_left2.png")

turtle_size = (80, 80)  # Új méret (szélesség, magasság)
turtle = pygame.transform.scale(turtle, turtle_size)
turtle1 = pygame.transform.scale(turtle1, turtle_size)
turtle2 = pygame.transform.scale(turtle2, turtle_size)
# TURTLE BALRA NÉZŐ SPRITEJA

turtle_size = 50
turtle_x_right = width
turtle_y_right = 530
turtle_speed_right = 2.1  # Csökkentett sebesség a könnyebb játék érdekében

turtle_right = pygame.image.load("sprite/turtle/turtle_right.png")
turtle_right1 = pygame.image.load("sprite/turtle/turtle_right1.png")
turtle_right2 = pygame.image.load("sprite/turtle/turtle_right2.png")

turtle_right = pygame.transform.scale(turtle_right, (80, 80))
turtle_right1 = pygame.transform.scale(turtle_right1, (80, 80))
turtle_right2 = pygame.transform.scale(turtle_right2, (80, 80))

# TURTLE JOBBRA NÉZŐ SPRITEJA      

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
rect_speed = 4  # Vízszintes sebesség

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

# Karakter képek méretezése
character_right = pygame.transform.scale(character_right, (rect_width, rect_height))
character_left = pygame.transform.scale(character_left, (rect_width, rect_height))
character_jump_right = pygame.transform.scale(character_jump_right, (rect_width, rect_height))
character_jump_left = pygame.transform.scale(character_jump_left, (rect_width, rect_height))
idle_right_images = [pygame.transform.scale(img, (rect_width, rect_height)) for img in idle_right_images]
idle_left_images = [pygame.transform.scale(img, (rect_width, rect_height)) for img in idle_left_images]
move_right_images = [pygame.transform.scale(img, (rect_width, rect_height)) for img in move_right_images]
move_left_images = [pygame.transform.scale(img, (rect_width, rect_height)) for img in move_left_images]

current_character = character_right  # Kezdő nézet

# Ugrás változók
is_jumping = False
is_falling = False
initial_y = rect_y
jump_height = rect_height * 2  # Ugrási magasság
jump_speed = rect_speed * 2  # Ugrási sebesség növelése a gyorsabb és magasabb ugráshoz
fall_speed = jump_speed * 0.8  # Esési sebesség egy kicsit kisebb, hogy simább legyen az esés
max_jump_height = initial_y - jump_height

# Időszámláló
start_time = time.time()
pause_start_time = None
total_pause_time = 0

# Betűtípus
font = pygame.font.Font(None, 36)

# Játék kezdőképernyője
show_start_message = True

# Pontszám változó
score = -1

# Ready és Go képek betöltése
ready_image = pygame.image.load("kepek/ready.png").convert_alpha()
go_image = pygame.image.load("kepek/go.png").convert_alpha()

# Zene késleltetési változók
play_track_delay = 1  # Másodpercnext_track_time = None
current_track_index = 0

# Zenék betöltése
start_sound = "zenek/start.mp3"
elso_track = pygame.mixer.Sound("zenek/elso_track.mp3")
masodik_track = pygame.mixer.Sound("zenek/masodik_track.mp3")
harmadik_track = pygame.mixer.Sound("zenek/harmadik_track.mp3")
negyedik_track = pygame.mixer.Sound("zenek/negyedik_track.mp3")
otodik_track = pygame.mixer.Sound("zenek/otodik_track.mp3")
hatodik_track = pygame.mixer.Sound("zenek/hatodik_track.mp3")
hetedik_track = pygame.mixer.Sound("zenek/hetedik_track.mp3")
nyolcadik_track = pygame.mixer.Sound("zenek/nyolcadik_track.mp3")
kilencedik_track = pygame.mixer.Sound("zenek/kilencedik_track.wav")
tizedik_track = pygame.mixer.Sound("zenek/tizedik_track.wav")
ten_points_sound = pygame.mixer.Sound("zenek/10points.mp3")
halal = pygame.mixer.Sound("zenek/halal.ogg")

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

def reset_game():
    global mosquito_x, turtle_x, turtle_x_right, rect_x, rect_y, is_jumping, is_falling, game_over, game_started, animation_played, start_time, score, current_track_index, halal
    mosquito_x = width
    turtle_x = width
    turtle_x_right = width
    rect_x = width // 2 - rect_width // 2
    rect_y = height - rect_height
    is_jumping = False
    is_falling = False
    game_over = False
    game_started = True
    animation_played = False
    start_time = time.time()
    score = -1
    current_track_index = 0
    # Állítsuk meg az összes zenét
    pygame.mixer.music.stop()
    for track in tracks:
        track.stop()
    # Halál zene megállítása
    halal.stop()
    play_next_track()

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

# Fő játékciklus
running = True
facing_right = True  # Jelenlegi nézési irány
is_moving = False
game_started = False  # Új változó a játék kezdésének követéséhez
# Játék megállítás változó
game_paused = False
game_over = False  # Új változó a játék megállításához halál után
animation_played = False


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if not game_started:  # Ha a játék még nem kezdődött el
                game_started = True
                show_ready_go()
                start_game()
            elif game_over:  # Ha a játék vége van, újraindítás
                reset_game()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game_over:  # Ha a játék vége, kilépés
                    running = False
                else:
                    game_paused = not game_paused
                    if game_paused:  # Ha a játék megállítva
                        pause_start_time = time.time()
                        # Zene szüneteltetése
                        pygame.mixer.music.pause()
                        for track in tracks:
                            track.stop()
                        # Fekete háttér
                        screen.fill((0, 0, 0))
                        # "A játék megállítva" szöveg kirajzolása
                        pause_text = font.render("A játék megállítva", True, (255, 255, 255))
                        text_rect = pause_text.get_rect(center=(width // 2, height // 2))
                        screen.blit(pause_text, text_rect)
                        pygame.display.update()
                    else:
                        total_pause_time = time.time() - pause_start_time
                        start_time += total_pause_time
                        # Zene újraindítása
                        pygame.mixer.music.unpause()
                        if current_track_index < len(tracks):
                            tracks[current_track_index - 1].play()

            elif event.key == pygame.K_SPACE and not is_jumping and not is_falling:  # Csak a space gombra ugrik
                is_jumping = True
                jump_start_y = rect_y  # Az ugrás kezdő y pozíciójának mentése
            elif event.key == pygame.K_UP and not is_jumping and not is_falling:  # Csak a felfelé nyílra ugrik
                is_jumping = True
                jump_start_y = rect_y  # Az ugrás kezdő y pozíciójának mentése

        elif event.type == pygame.USEREVENT and game_over:
            # 1 másodperc után esemény kezelése
            screen.fill((0, 0, 0))
            score_text = font.render(f"Pontszámod: {score}", True, (255, 255, 255))
            screen.blit(score_text, (width // 2 - score_text.get_width() // 2, height // 2 - 40))
            dead_text = font.render("Játék vége!", True, (255, 255, 255))
            text_rect = dead_text.get_rect(center=(width // 2, height // 2))
            screen.blit(dead_text, text_rect)
            exit_text = font.render("Kilépés: Esc", True, (255, 255, 255))
            screen.blit(exit_text, (10, height - 30))
            restart_text = font.render("Újraindítás: Enter", True, (255, 255, 255))
            screen.blit(restart_text, (width - restart_text.get_width() - 10, height - 30))
            pygame.display.update()
            pygame.time.set_timer(pygame.USEREVENT, 0)  # Timer kikapcsolása


    if game_over:
        screen.fill((0, 0, 0))
        score_text = font.render(f"Pontszámod: {score}", True, (255, 255, 255))
        screen.blit(score_text, (width // 2 - score_text.get_width() // 2, height // 2 - 40))
        dead_text = font.render("Játék vége!", True, (255, 255, 255))
        text_rect = dead_text.get_rect(center=(width // 2, height // 2))
        screen.blit(dead_text, text_rect)
        exit_text = font.render("Kilépés: Esc", True, (255, 255, 255))
        screen.blit(exit_text, (10, height - 30))
        restart_text = font.render("Újraindítás: Enter", True, (255, 255, 255))
        screen.blit(restart_text, (width - restart_text.get_width() - 10, height - 30))
        pygame.display.update()
        continue  # Ne folytassuk a játék logikát, ha a játék vége

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
        if game_paused:  # Ha a játék megállítva
            # Időszámláló megállítása
            continue  # A ciklus újrakezdése

        if pause_start_time:
            total_pause_time += time.time() - pause_start_time
            pause_start_time = None

        if next_track_time and time.time() >= next_track_time:
            play_next_track()


        # Billentyűzet bemenetek kezelése
        keys = pygame.key.get_pressed()
        if any(keys):
            idle_clock = pygame.time.get_ticks()
            is_idle = False
            is_moving = True
            if keys[pygame.K_LEFT] and rect_x > width // 2 - 300:
                rect_x -= rect_speed
                bg_x += rect_speed  # Háttér mozgása jobbra
                mosquito_x += rect_speed  # Mosquito pozíciójának korrigálása
                turtle_x += rect_speed  # Turtle pozíciójának korrigálása
                if pygame.time.get_ticks() - image_change_clock >= move_image_change_time:
                    image_change_clock = pygame.time.get_ticks()
                    current_character = next(move_left_cycle)
                facing_right = False
            elif keys[pygame.K_RIGHT] and rect_x < width // 2 + 300 - rect_width:
                rect_x += rect_speed
                bg_x -= rect_speed  # Háttér mozgása balra
                mosquito_x -= rect_speed  # Mosquito pozíciójának korrigálása
                turtle_x -= rect_speed  # Turtle pozíciójának korrigálása
                if pygame.time.get_ticks() - image_change_clock >= move_image_change_time:
                    image_change_clock = pygame.time.get_ticks()
                    current_character = next(move_right_cycle)
                facing_right = True
            else:
                is_moving = False
                current_character = character_right if facing_right else character_left
        else:
            is_moving = False
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

        # Pontszám kirajzolása
        score_text = font.render(f"Pontszámod: {score}", True, (255, 255, 255))
        screen.blit(score_text, (width // 2 - score_text.get_width() // 2, 10))

        # Mosquito mozgatása balra
        mosquito_x -= mosquito_speed

        # Turtle mozgatása balra
        turtle_x -= turtle_speed  # Turtle mozgása balra a saját sebességével

        # Turtle mozgatása jobbra
        turtle_x_right += turtle_speed_right  # Turtle right mozgása jobbra a saját sebességével

        # Ha a mosquito elhagyja a képernyőt balról, kezdjük újra jobbról
        if mosquito_x < -mosquito1.get_width():
            mosquito_x = width

        # Ha a turtle elhagyja a képernyőt balról, kezdjük újra jobbról
        if turtle_x < -turtle.get_width():
            turtle_x = width
            score += 1  # Pontszám növelése
            if score % 10 == 0 and score != 0:  # Minden 10. kikerült turtle után játssza be a zenét
                ten_points_sound.play()

        # Ha a turtle elhagyja a képernyőt jobbról, kezdjük újra balról
        if turtle_x_right > width:
            turtle_x_right = -turtle_right.get_width()
            score += 1  # Pontszám növelése
            if score % 10 == 0 and score != 0:  # Minden 10. kikerült turtle után játssza be a zenét
                ten_points_sound.play()
        
        # Akadályok gyorsítása
        next_threshold = 10
        if score == next_threshold:
            mosquito_speed += 0.003
            turtle_speed += 0.005
            turtle_speed_right += 0.003
            next_threshold += 10       
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

        # Képernyő frissítése (Turtle)
        if current_frame == 0:
            screen.blit(turtle, (turtle_x, turtle_y))  # Első képkocka rajzolása
        if current_frame == 0:
            screen.blit(turtle1, (turtle_x, turtle_y))  # Második képkocka rajzolása
        else:
            screen.blit(turtle2, (turtle_x, turtle_y))  # Harmadik képkocka rajzolása

        # Képernyő frissítése (Turtle-jobbra néző sprite)
        if current_frame == 0:
            screen.blit(turtle_right, (turtle_x_right, turtle_y_right))  # Első képkocka rajzolása
        if current_frame == 0:
            screen.blit(turtle_right1, (turtle_x_right, turtle_y_right))  # Második képkocka rajzolása
        else:
            screen.blit(turtle_right2, (turtle_x_right, turtle_y_right))  # Harmadik képkocka rajzolása
        pygame.display.update()
        
        # Ütközés ellenőrzése
        mosquito_rect = mosquito1.get_rect(topleft=(mosquito_x, mosquito_y)).inflate(-30, -30)
        character_rect = current_character.get_rect(topleft=(rect_x, rect_y)).inflate(-20, -20)

        if mosquito_rect.colliderect(character_rect) and not animation_played:
            # Animáció lejátszása ütközéskor
            death_animation_images = [
                pygame.image.load("sprite/character/dead/dead1.png").convert_alpha(),
                pygame.image.load("sprite/character/dead/dead2.png").convert_alpha(),
                pygame.image.load("sprite/character/dead/dead3.png").convert_alpha(),
                pygame.image.load("sprite/character/dead/dead4.png").convert_alpha()
            ]
            character_size = (rect_width, rect_height)  # Karakter mérete
            death_animation_images = [pygame.transform.scale(img, character_size) for img in death_animation_images]

            death_frame_duration = 0.2  # Minden képkocka időtartama másodpercben
            for img in death_animation_images:
                screen.fill((0, 0, 0))  # Fekete háttér rajzolása
                current_character = img
                screen.blit(current_character, (rect_x, rect_y))
                pygame.display.update()
                pygame.time.delay(int(death_frame_duration * 1000))  # Várakozás képkockánként

            game_over = True
            animation_played = True
            for track in tracks:
                track.stop()  # Állítsuk meg az összes zenét
            halal = pygame.mixer.Sound("zenek/halal.ogg")
            halal.play(10)
            pygame.time.set_timer(pygame.USEREVENT, 1000)  # 1 másodperc után eseményt generál

        # Ütközés ellenőrzése (Turtle)
        turtle_rect = turtle.get_rect(topleft=(turtle_x, turtle_y)).inflate(-30, -30)  # Csökkentett hitbox
        if turtle_rect.colliderect(character_rect) and not animation_played:
            # Animáció lejátszása ütközéskor
            death_animation_images = [
                pygame.image.load("sprite/character/dead/dead1.png").convert_alpha(),
                pygame.image.load("sprite/character/dead/dead2.png").convert_alpha(),
                pygame.image.load("sprite/character/dead/dead3.png").convert_alpha(),
                pygame.image.load("sprite/character/dead/dead4.png").convert_alpha()
            ]
            character_size = (rect_width, rect_height)  # Karakter mérete
            death_animation_images = [pygame.transform.scale(img, character_size) for img in death_animation_images]

            death_frame_duration = 0.2  # Minden képkocka időtartama másodpercben
            for img in death_animation_images:
                screen.fill((0, 0, 0))  # Fekete háttér rajzolása
                current_character = img
                screen.blit(current_character, (rect_x, rect_y))
                pygame.display.update()
                pygame.time.delay(int(death_frame_duration * 1000))  # Várakozás képkockánként

            game_over = True
            animation_played = True
            for track in tracks:
                track.stop()  # Állítsuk meg az összes zenét
            halal = pygame.mixer.Sound("zenek/halal.ogg")
            halal.play(10)
            pygame.time.set_timer(pygame.USEREVENT, 1000)  # 1 másodperc után eseményt generál

        # Ütközés ellenőrzése (Turtle-jobbra néző spriteja)
        turtle_rect_right = turtle_right.get_rect(topleft=(turtle_x_right, turtle_y_right)).inflate(-30, -30)  # Csökkentett hitbox
        if turtle_rect_right.colliderect(character_rect) and not animation_played:
            # Animáció lejátszása ütközéskor
            death_animation_images = [
                pygame.image.load("sprite/character/dead/dead1.png").convert_alpha(),
                pygame.image.load("sprite/character/dead/dead2.png").convert_alpha(),
                pygame.image.load("sprite/character/dead/dead3.png").convert_alpha(),
                pygame.image.load("sprite/character/dead/dead4.png").convert_alpha()
            ]
            character_size = (rect_width, rect_height)  # Karakter mérete
            death_animation_images = [pygame.transform.scale(img, character_size) for img in death_animation_images]

            death_frame_duration = 0.2  # Minden képkocka időtartama másodpercben
            for img in death_animation_images:
                screen.fill((0, 0, 0))  # Fekete háttér rajzolása
                current_character = img
                screen.blit(current_character, (rect_x, rect_y))
                pygame.display.update()
                pygame.time.delay(int(death_frame_duration * 1000))  # Várakozás képkockánként

            game_over = True
            animation_played = True
            for track in tracks:
                track.stop()  # Állítsuk meg az összes zenét
            halal = pygame.mixer.Sound("zenek/halal.ogg")
            halal.play(10)
            pygame.time.set_timer(pygame.USEREVENT, 1000)  # 1 másodperc után eseményt generál

        # FPS korlátozása
        fps.clock.tick(75)


# Pygame kilépése
pygame.quit()
