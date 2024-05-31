import pygame
import sys
import time

# Inicializáljuk a Pygame-et
pygame.init()

# Képernyő méretek
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Animált kocka')

# Színek definiálása
white = (255, 255, 255)
red = (255, 0, 0)

# Képek betöltése és méretezése
image1 = pygame.image.load('sprite/mosquito/mosquito_left1.png')
image2 = pygame.image.load('sprite/mosquito/mosquito_left2.png')
new_size = (100, 100)  # Új méret (szélesség, magasság)
image1 = pygame.transform.scale(image1, new_size)
image2 = pygame.transform.scale(image2, new_size)

# Animált kocka kezdő pozíciója és mérete
animated_square_x = screen_width
animated_square_y = 500 # Kocka magassága pixelben

# Animált kocka sebessége
animated_square_speed = 5

# Animáció beállítások
frame_duration = 0.2  # Egy képkocka időtartama másodpercben
last_frame_change_time = time.time()
current_frame = 0

# Piros kocka kezdő pozíciója és mérete
red_square_size = 50
red_square_x = screen_width // 2
red_square_y = screen_height - red_square_size
red_square_speed = 5

# Futási ciklus
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Nyíl billentyűk kezelése a piros kockához
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        red_square_x -= red_square_speed
    if keys[pygame.K_RIGHT]:
        red_square_x += red_square_speed

    # Korlátozzuk a piros kockát, hogy ne hagyja el a képernyőt
    if red_square_x < 0:
        red_square_x = 0
    if red_square_x > screen_width - red_square_size:
        red_square_x = screen_width - red_square_size

    # Animált kocka mozgatása balra
    animated_square_x -= animated_square_speed

    # Ha az animált kocka elhagyja a képernyőt balról, kezdjük újra jobbról
    if animated_square_x < -new_size[0]:
        animated_square_x = screen_width

    # Animáció váltása
    current_time = time.time()
    if current_time - last_frame_change_time >= frame_duration:
        current_frame = (current_frame + 1) % 2  # Váltás a két képkocka között
        last_frame_change_time = current_time

    # Képernyő frissítése
    screen.fill(white)  # Képernyő törlése fehérre
    if current_frame == 0:
        screen.blit(image1, (animated_square_x, animated_square_y))  # Első képkocka rajzolása
    else:
        screen.blit(image2, (animated_square_x, animated_square_y))  # Második képkocka rajzolása

    # Piros kocka rajzolása
    pygame.draw.rect(screen, red, (red_square_x, red_square_y, red_square_size, red_square_size))

    # Ütközés ellenőrzése
    animated_square_rect = pygame.Rect(animated_square_x, animated_square_y, new_size[0], new_size[1])
    red_square_rect = pygame.Rect(red_square_x, red_square_y, red_square_size, red_square_size)
    if animated_square_rect.colliderect(red_square_rect):
        running = False

    pygame.display.flip()  # Képernyő frissítése

    # Keret sebességének szabályozása
    pygame.time.Clock().tick(60)

# Kilépés Pygame-ből
pygame.quit()
sys.exit()
