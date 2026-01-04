import pygame
import sys

from pygame.locals import *

class Main:

    DISPLAY_WIDTH = 600
    DISPLAY_HEIGHT = 800
    DISPLAY_COLOR = (10,10,10)

    CLOCK = pygame.time.Clock()
    FPS = 60

    def __init__(self):

        pygame.init()
        pygame.display.set_caption("Tetris: Copy")
        self.DISPLAY = pygame.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))

    def run(self):
        
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            self.DISPLAY.fill(self.DISPLAY_COLOR)
            pygame.display.update()

if __name__ == '__main__':
    app = Main()
    app.run()
