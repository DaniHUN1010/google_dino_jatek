import pygame
import random
import time

# Pygame inicializálása 
pygame.init()
pygame.font.init()

# Ablak mérete
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

# Háttérszín beállítása
BG = pygame.transform.scale(pygame.image.load("hatter.jpg"), (width, height))

# FPS beállítása
class FPS:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Calibri", 30, bold=True)
        self.text = self.font.render(str(self.clock.get_fps()), 1, (255, 255, 255))

    def render(self, display):
        self.text = self.font.render(str(round(self.clock.get_fps(), 0)), 1, (255, 255, 255))
        display.blit(self.text, (735, 10))

fps = FPS()

# Négyzet adatai
rect_width, rect_height = 50, 50
rect_x, rect_y = width // 2, height - rect_height
rect_color = (150, 0, 150)  # Piros szín
rect_speed = 5  # Sebesség

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

    # Ideiglenes felület létrehozása
    temp_surface = pygame.Surface((width, height))
    temp_surface.blit(BG, (0, 0))  # Háttérkép kirajzolása

    # FPS kiírása
    fps.render(temp_surface)

    # Négyzet rajzolása
    pygame.draw.rect(temp_surface, rect_color, pygame.Rect(rect_x, rect_y, rect_width, rect_height))

    # Időszámláló rajzolása
    elapsed_time = int(time.time() - start_time)
    time_text = font.render(f"Idő: {elapsed_time}", True, (255, 255, 255))
    temp_surface.blit(time_text, (10, 10))

    # Ideiglenes felület kirajzolása a képernyőre
    screen.blit(temp_surface, (0, 0))

    # Képernyő frissítése
    pygame.display.update()

    # FPS szabályozása
    fps.clock.tick(60)

# Pygame leállítása
pygame.quit()
