import random

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

        self.image = pygame.Surface((30,30))
        self.image.fill((255,50,50))

        self.rect = self.image.get_rect(center = (100,100))

        self.pos = pygame.math.Vector2(100,100)
        self.speed = 150

        self.player = player
        self.state = "WANDER"

        self.aggro_radius = 200

        self.wander = pygame.math.Vector2(100,100)
        self.wander_time = 0

    def update(self, dt):

        to_player = self.player.pos - self.pos
        distance = to_player.length()

        if distance < self.aggro_radius:
            self.state = "CHASE"

        else:
            self.state = "WANDER"

        if self.state == "CHASE":
            self.image.fill((255,0,0))

            if distance > 0:
                direction = to_player.normalize()
                self.pos += direction * self.speed * dt

        elif self.state == "WANDER":
            self.image.fill((100,50,50))
            self.wander_time += dt

            if self.wander_time > 2.0:
                self.wander = pygame.math.Vector2(
                    random.randint(15, Main.DISPLAY_WIDTH - 15),
                    random.randint(15, Main.DISPLAY_HEIGHT - 15)
                )
                self.wander_time = 0

            to_target = self.wander - self.pos

            if to_target.length() > 5:
                self.pos += to_target.normalize() * (self.speed * 0.5) * dt

        self.rect.center = (round(self.pos.x), round(self.pos.y))

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
        all_sprites = pygame.sprite.Group(player, enemy)

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