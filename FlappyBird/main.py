import pygame
import sys

from pygame.locals import *

class Main:

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

    DISPLAY_WIDTH = 800
    DISPLAY_HEIGHT = 600
    FLOOR_Y = 600

    GRAVITY = 2000
    MOVE_SPEED = 800
    JUMP_STRENGTH = -800

    CLOCK = pygame.time.Clock()
    FPS = 60

    def __init__(self):

        pygame.init()
        pygame.display.set_caption("Flappy Bird")
        self.DISPLAY = pygame.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))

    def run(self):

        while True:

            dt = self.CLOCK.tick(self.FPS) / 1000
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            self.DISPLAY.fill(self.UI_BLACK)
            pygame.display.update()

if __name__ == "__main__":
    app = Main()
    app.run()