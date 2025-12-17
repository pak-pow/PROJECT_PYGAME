import pygame
import sys

from pygame.locals import *

class Main:

    DISPLAY_WIDTH = 800
    DISPLAY_HEIGHT = 600
    DISPLAY_COLOR = (0,0,0)

    def __init__(self):

        pygame.init()
        self.DISPLAY = pygame.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))

        self.CLOCK = pygame.time.Clock()
        self.FPS = 60

    def run(self):

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            self.DISPLAY.fill(self.DISPLAY_COLOR)
            pygame.display.set_caption("SPACE INVADERS")
            pygame.display.update()

if __name__ == "__main__":
    app = Main()
    app.run()