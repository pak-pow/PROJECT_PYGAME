import pygame
import sys

from pygame.locals import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((30, 30))
        self.image.fill((0, 255, 0))

        self.rect = self.image.get_rect(center=(400, 300))
        self.pos = pygame.math.Vector2(400, 300)
        self.speed = 250

    def update(self, dt):
        keys = pygame.key.get_pressed()
        input_vec = pygame.math.Vector2(0, 0)

        if keys[K_w]:
            input_vec.y -= 1

        if keys[K_s]:
            input_vec.y += 1

        if keys[K_a]:
            input_vec.x -= 1

        if keys[K_d]:
            input_vec.x += 1

        if input_vec.length() > 0:
            self.pos += input_vec.normalize() * self.speed * dt
            self.rect.center = round(self.pos)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()

    def update(self, dt):
        pass

class Main:

    DISPLAY_WIDTH = 800
    DISPLAY_HEIGHT = 600
    DISPLAY_COLOR = (0,0,0)

    def __init__(self):

        pygame.init()
        self.DISPLAY = pygame.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))

        pygame.display.set_caption("DAY19")
        self.CLOCK = pygame.time.Clock()
        self.FPS = 60

    def run(self):

        player = Player()
        enemy = Enemy(player)
        all_sprites = pygame.sprite.Group(player)

        while True:

            dt = self.CLOCK.tick(self.FPS) / 1000

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            all_sprites.update(dt)
            self.DISPLAY.fill(self.DISPLAY_COLOR)

            all_sprites.draw(self.DISPLAY)
            pygame.display.update()

if __name__ == "__main__":
    app = Main()
    app.run()