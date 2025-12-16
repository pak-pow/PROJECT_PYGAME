import pygame
import sys

from pygame.locals import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

    def update(self):
        pass

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

    def update(self):
        pass


class Main:

    DISPLAY_WIDTH = 800
    DISPLAY_HEIGHT = 600
    DISPLAY_COLOR = (0,0,0)

    def __init__(self):

        pygame.init()
        self.DISPLAY = pygame.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))
        self.DISPLAY.fill(self.DISPLAY_COLOR)

        pygame.display.set_caption("DAY19")
        self.CLOCK = pygame.time.Clock()
        self.FPS = 60

    def run(self):

        while True:

            dt = self.CLOCK.tick(self.FPS) / 1000

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

if __name__ == "__main__":
    app = Main()
    app.run()