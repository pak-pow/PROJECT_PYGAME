import pygame
import sys

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

class Main:

    DISPLAY_WIDTH = 800
    DISPLAY_HEIGHT = 600
    CLOCK = pygame.time.Clock()
    FPS = 60

    def __init__(self):

        pygame.init()
        self.DISPLAY = pygame.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))
        pygame.display.set_caption("DAY 26")

    def run(self):

        dt = self.CLOCK.tick(self.FPS) / 1000

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    quit()

            self.DISPLAY.fill((0,0,0))
            pygame.display.update()

if __name__ == "__main__":
    app = Main()
    app.run()