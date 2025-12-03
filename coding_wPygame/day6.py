"""
DAY 6 about collisions and shit
"""

# imports
import pygame
import sys
import random
import pygame.font

from pygame.sprite import Sprite
from pygame.time import Clock
from pygame.locals import *

class Player(Sprite):

    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((50,50))
        self.image.fill((0,0,255))
        self.rect = self.image.get_rect(center = (300,200))

    def update(self, dt):
        pos = pygame.mouse.get_pos()
        self.rect.center = pos

class Coin(Sprite):

    def __init__(self, width, height, player_rect):
        super().__init__()

        self.image = pygame.Surface((20,20))
        self.image.fill((0,255,0))
        self.rect = self.image.get_rect()

        while True:
            self.rect.x = random.randrange(0, width - self.rect.width)
            self.rect.y = random.randrange(0, height - self.rect.height)

            if not self.rect.colliderect(player_rect):
                break


def main():

    # initialize the pygame
    pygame.init()

    # Display setting
    DISPLAY_WIDTH = 600
    DISPLAY_HEIGHT = 500
    DISPLAY_COLOR = (255,255,255)

    # Render the display
    DISPLAY = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

    # For delta clock
    CLOCK = Clock()
    FPS = 60

    all_sprites = pygame.sprite.Group()
    coin_group = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)

    for i in range(0,30):
        coin = Coin(DISPLAY_WIDTH, DISPLAY_HEIGHT, player.rect)
        all_sprites.add(coin)
        coin_group.add(coin)

    coin = 0
    font = pygame.font.SysFont(None, 30)

    while True:

        dt = CLOCK.tick(FPS) / 1000

        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        all_sprites.update(dt)

        hit_list = pygame.sprite.spritecollide(player, coin_group, True)

        if hit_list:
            coin += 1

        DISPLAY.fill(DISPLAY_COLOR)
        all_sprites.draw(DISPLAY)

        score_text = font.render(f"Score: {coin}", True, (0, 0, 0))
        DISPLAY.blit(score_text, (10, 10))

        pygame.display.update()

        print(len(coin_group))
if __name__ == "__main__":
    main()