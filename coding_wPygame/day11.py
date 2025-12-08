import pygame
import sys

from PIL.ImageChops import offset
from pygame.locals import *

# ============= UI COLORS ============
UI_WHITE         = (245, 245, 245)
UI_LIGHT_GRAY    = (230, 230, 230)
UI_GRAY          = (180, 180, 180)
UI_DARK_GRAY     = (100, 100, 100)
UI_BLACK         = ( 20,  20,  20)

UI_SKY_BLUE      = ( 93, 173, 226)
UI_NAVY_BLUE     = ( 52,  73,  94)
UI_PURPLE        = (155,  89, 182)
UI_GREEN         = ( 46, 204, 113)
UI_ORANGE        = (243, 156,  18)
UI_RED           = (231,  76,  60)
# ====================================


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        pass

    def update(self):
        pass

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        self.CAMERA_DISPLAY_SURFACE = pygame.display.get_surface()

        self.OFFSET = pygame.math.Vector2()
        self.ZOOM_SCALE = 1.0
        self.INTERNAL_SURFACE_SIZE = (2500,2500)
        self.INTERNAL_SURFACE = pygame.Surface(self.INTERNAL_SURFACE_SIZE, pygame.SRCALPHA)
        self.INTERNAL_RECT = self.INTERNAL_SURFACE.get_rect(center = (Main.DISPLAY_WIDTH // 2, Main.DISPLAY_HEIGHT // 2))


    def custom_draw(self, player):

        keys = pygame.key.get_pressed()

        if keys[K_q]:
            self.ZOOM_SCALE += 0.05
        if keys[K_e]:
            self.ZOOM_SCALE -= 0.05

        if self.ZOOM_SCALE < 0.3:
            self.ZOOM_SCALE = 0.3
        if self.ZOOM_SCALE > 2.0:
            self.ZOOM_SCALE = 2.0

        self.OFFSET.x = player.rect.centerx - Main.DISPLAY_WIDTH // 2
        self.OFFSET.y = player.rect.centery - Main.DISPLAY_HEIGHT // 2

        for sprite in sorted(self.sprites(), key = lambda  s: s.rect.centery):

            OFFSET_POS = sprite.rect.topleft - self.OFFSET
            CENTER_OFFSET = OFFSET_POS - pygame.math.Vector2(Main.DISPLAY_WIDTH // 2, Main.DISPLAY_HEIGHT // 2)
            ZOOMED_OFFSET = CENTER_OFFSET * self.ZOOM_SCALE
            FINAL_POS = ZOOMED_OFFSET + pygame.math.Vector2(Main.DISPLAY_WIDTH // 2, Main.DISPLAY_HEIGHT // 2)

            new_W = int(sprite.rect.width * self.ZOOM_SCALE)
            new_H = int(sprite.rect.height * self.ZOOM_SCALE)

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

    def run(self):


        while True:

            dt = self.CLOCK.tick(self.FPS) / 1000

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            self.DISPLAY.fill(UI_WHITE)
            pygame.display.set_caption("DAY11: Camera Work")
            pygame.display.update()

if __name__ == '__main__':
    app = Main()
    app.run()
