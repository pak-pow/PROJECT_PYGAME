import pygame
import sys

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
        pass

    def update(self):
        pass

class Main:
    def __init__(self):

        pygame.init()
        self.DISPLAY_WIDTH = 800
        self.DISPLAY_HEIGHT = 600
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
