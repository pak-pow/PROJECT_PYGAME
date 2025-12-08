import pygame
import sys
import random
from pygame.locals import *

# ============= UI COLORS ============
UI_WHITE = (245, 245, 245)
UI_LIGHT_GRAY = (230, 230, 230)
UI_GRAY = (180, 180, 180)
UI_DARK_GRAY = (100, 100, 100)
UI_BLACK = (20, 20, 20)

UI_SKY_BLUE = (93, 173, 226)
UI_NAVY_BLUE = (52, 73, 94)
UI_PURPLE = (155, 89, 182)
UI_GREEN = (46, 204, 113)
UI_ORANGE = (243, 156, 18)
UI_RED = (231, 76, 60)
# ====================================


class Player(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.Surface((40, 40))
        self.image.fill(UI_RED)
        # Spawn near center initially
        self.rect = self.image.get_rect(center=(1000, 1000))
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 400

    def update(self, dt):
        keys = pygame.key.get_pressed()
        input_vec = pygame.math.Vector2(0, 0)

        if keys[K_LEFT]: input_vec.x = -1
        if keys[K_RIGHT]: input_vec.x = 1
        if keys[K_UP]: input_vec.y = -1
        if keys[K_DOWN]: input_vec.y = 1

        if input_vec.length() > 0:
            input_vec = input_vec.normalize()
            self.pos += input_vec * self.speed * dt
            self.rect.center = round(self.pos)


class Star(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        size = random.randint(20, 50)
        self.image = pygame.Surface((size, size))
        self.image.fill(UI_WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 2000)
        self.rect.y = random.randint(0, 2000)


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        self.CAMERA_DISPLAY_SURFACE = pygame.display.get_surface()

        self.OFFSET = pygame.math.Vector2()
        self.ZOOM_SCALE = 1.0
        self.INTERNAL_SURFACE_SIZE = (2500, 2500)
        self.INTERNAL_SURFACE = pygame.Surface(self.INTERNAL_SURFACE_SIZE, pygame.SRCALPHA)
        self.INTERNAL_RECT = self.INTERNAL_SURFACE.get_rect(center=(Main.DISPLAY_WIDTH // 2, Main.DISPLAY_HEIGHT // 2))

    def custom_draw(self, player):
        # 1. Handle Zoom Input
        keys = pygame.key.get_pressed()

        if keys[K_q]:
            self.ZOOM_SCALE += 0.05
        if keys[K_e]:
            self.ZOOM_SCALE -= 0.05

        # Clamp Zoom
        if self.ZOOM_SCALE < 0.3:
            self.ZOOM_SCALE = 0.3
        if self.ZOOM_SCALE > 2.0:
            self.ZOOM_SCALE = 2.0

        # 2. Calculate Camera Center
        self.OFFSET.x = player.rect.centerx - Main.DISPLAY_WIDTH // 2
        self.OFFSET.y = player.rect.centery - Main.DISPLAY_HEIGHT // 2

        # 3. Draw Sprites with Vector Math
        for sprite in sorted(self.sprites(), key=lambda s: s.rect.centery):

            OFFSET_POS = sprite.rect.topleft - self.OFFSET
            CENTER_OFFSET = OFFSET_POS - pygame.math.Vector2(Main.DISPLAY_WIDTH // 2, Main.DISPLAY_HEIGHT // 2)
            ZOOMED_OFFSET = CENTER_OFFSET * self.ZOOM_SCALE
            FINAL_POS = ZOOMED_OFFSET + pygame.math.Vector2(Main.DISPLAY_WIDTH // 2, Main.DISPLAY_HEIGHT // 2)

            new_W = int(sprite.rect.width * self.ZOOM_SCALE)
            new_H = int(sprite.rect.height * self.ZOOM_SCALE)

            # Optimization: Only draw if visible on screen
            if -100 < FINAL_POS.x < Main.DISPLAY_WIDTH + 100 and -100 < FINAL_POS.y < Main.DISPLAY_HEIGHT + 100:
                ZOOMED_IMAGE = pygame.transform.scale(sprite.image, (new_W, new_H))
                self.CAMERA_DISPLAY_SURFACE.blit(ZOOMED_IMAGE, FINAL_POS)


class Main:
    DISPLAY_WIDTH = 800
    DISPLAY_HEIGHT = 600

    def __init__(self):

        pygame.init()
        self.DISPLAY = pygame.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))

        self.CLOCK = pygame.time.Clock()
        self.FPS = 60

        # Setup Camera and Objects
        self.camera_group = CameraGroup()
        self.player = Player(self.camera_group)

        # Create Stars
        for i in range(200):
            Star(self.camera_group)

        self.font = pygame.font.SysFont(None, 30)

    def run(self):

        while True:
            # Calculate Delta Time
            dt = self.CLOCK.tick(self.FPS) / 1000

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            # Using BLACK background so white stars are visible
            self.DISPLAY.fill(UI_BLACK)

            # Update and Draw
            self.camera_group.update(dt)
            self.camera_group.custom_draw(self.player)

            # UI Info (Zoom Level)
            info = self.font.render(f"Zoom: {self.camera_group.ZOOM_SCALE:.2f}", True, UI_GREEN)
            self.DISPLAY.blit(info, (10, 10))

            pygame.display.set_caption("DAY11: Camera Work")
            pygame.display.update()


if __name__ == '__main__':
    app = Main()
    app.run()