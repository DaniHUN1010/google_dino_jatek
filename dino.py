import pygame
import random
import time

# Pygame inicializálása
pygame.init()

# Ablak mérete
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

# Négyzet adatai
rect_width, rect_height = 50, 50
rect_x, rect_y = width // 2, height - rect_height
rect_color = (150, 0, 150)  # Piros szín
rect_speed = 0.5  # Sebesség

# Időszámláló
start_time = time.time()

# Betűtípus
font = pygame.font.Font(None, 36)

# Fő játékciklus
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Billentyűzet bemenetek kezelése
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        rect_x -= rect_speed
    if keys[pygame.K_RIGHT]:
        rect_x += rect_speed

    # Négyzet pozíciójának korlátozása
    rect_x = max(0, min(rect_x, width - rect_width))

    # Képernyő színe
    screen.fill((150, 200, 255))

    # Négyzet rajzolása
    pygame.draw.rect(screen, rect_color, pygame.Rect(rect_x, rect_y, rect_width, rect_height))


    # Időszámláló rajzolása
    elapsed_time = int(time.time() - start_time)
    time_text = font.render(f"Idő: {elapsed_time}", True, (255, 255, 255))
    screen.blit(time_text, (10, 10))

    # Képernyő frissítése
    pygame.display.flip()

# Pygame leállítása
pygame.quit()