import pygame
import time

# Pygame inicializálása
pygame.init()
pygame.font.init()

# Ablak mérete
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

# Háttérkép betöltése
BG = pygame.transform.scale(pygame.image.load("hatter.jpg"), (width, height))

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
rect_width, rect_height = 80, 80  # Sprite méret
rect_x, rect_y = width // 2, height - rect_height
rect_speed = 5  # Vízszintes sebesség

# Karakter képek betöltése és méretezése
character_right = pygame.image.load("sprite_right_fixed.png").convert_alpha()
character_left = pygame.image.load("sprite_left_fixed.png").convert_alpha()
character_right = pygame.transform.scale(character_right, (rect_width, rect_height))
character_left = pygame.transform.scale(character_left, (rect_width, rect_height))
current_character = character_right  # Kezdő nézet

# Ugrás változók
is_jumping = False
is_falling = False
jump_height = rect_height * 2 # Ugrási magasság
jump_speed = rect_speed * 2  # Ugrási sebesség növelése a gyors felugráshoz
fall_speed = jump_speed * 1  # Esési sebesség
initial_y = rect_y
max_jump_height = initial_y - jump_height

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
        current_character = character_left
    if keys[pygame.K_RIGHT]:
        rect_x += rect_speed
        current_character = character_right
    if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and not is_jumping and not is_falling:
        is_jumping = True
    if not (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and is_jumping:
        is_jumping = False
        is_falling = True

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

    # Négyzet pozíciójának korlátozása
    rect_x = max(0, min(rect_x, width - rect_width))

    # Ideiglenes felület létrehozása
    temp_surface = pygame.Surface((width, height))
    temp_surface.blit(BG, (0, 0))  # Háttérkép kirajzolása

    # FPS kirajzolása
    fps.render(temp_surface)

    # Karakter kirajzolása
    temp_surface.blit(current_character, (rect_x, rect_y))

    # Időszámláló kirajzolása
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
