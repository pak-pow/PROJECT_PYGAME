import pygame
import sys

from pygame.locals import *

class Player(pygame.sprite.Sprite):

    def __init__(self, sheet):
        super().__init__()

class Main:

    WHITE = (255,255,255)

    def __init__(self):

        pygame.init()

        self.sheet = None
        self.DISPLAY_WIDTH = 600
        self.DISPLAY_HEIGHT = 400
        self.DISPLAY_COLOR = self.WHITE
        self.DISPLAY = pygame.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))

    def generate_sprite_sheet(self):

        self.sheet = pygame.Surface((120,32))
        self.sheet.fill((0,0,0))

        pygame.draw.rect(self.sheet, (255, 0, 0), (0, 0, 32, 32))
        pygame.draw.circle(self.sheet, (0, 255, 0), (48, 16), 16)
        pygame.draw.rect(self.sheet, (0, 0, 255), (64, 0, 32, 32))
        pygame.draw.circle(self.sheet, (255, 255, 0), (112, 16), 16)

        return self.sheet

    def run(self):

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            self.DISPLAY.fill(self.DISPLAY_COLOR)
            pygame.display.update()

if __name__ == "__main__":
    app = Main()
    app.run()