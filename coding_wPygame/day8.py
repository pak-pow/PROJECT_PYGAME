import pygame
import sys

from pygame.locals import *
from pygame.math import Vector2
from pygame.time import Clock


class Main:

    def __init__(self):
        pass

    def to_iso(self, x, y):
        iso_x = (x - y)
        iso_y = (x + y) / 2
        return iso_x, iso_y

    def draw_iso_grid(self, surface, tile_size=40):
        color = (255, 255, 255)
        rows = 20
        cols = 20
        for r in range(rows):
            for c in range(cols):
                x = c * tile_size
                y = r * tile_size
                iso_x, iso_y = self.to_iso(x, y)
                iso_x += self.DISPLAY_WIDTH // 2
                iso_y += 50
                points = [
                    (iso_x, iso_y - tile_size/4),
                    (iso_x + tile_size/2, iso_y),
                    (iso_x, iso_y + tile_size/4),
                    (iso_x - tile_size/2, iso_y)
                ]
                pygame.draw.polygon(surface, color, points, 1)

    def run(self):

        pygame.init()

        self.DISPLAY_WIDTH = 800
        self.DISPLAY_HEIGHT = 600
        self.DISPLAY = pygame.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))

        self.CLOCK = Clock()
        self.FPS = 60

        # Player positions
        self.PLAYER_POS = Vector2(400, 300)
        self.BAD_POS = [400, 300]

        self.PLAYER_SPEED = 200

        while True:

            dt = self.CLOCK.tick(self.FPS) / 1000

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            # Movement input
            keys = pygame.key.get_pressed()
            input_vector = Vector2(0, 0)

            if keys[K_LEFT]:
                input_vector.x -= 1
                self.BAD_POS[0] -= self.PLAYER_SPEED * dt
            if keys[K_RIGHT]:
                input_vector.x += 1
                self.BAD_POS[0] += self.PLAYER_SPEED * dt
            if keys[K_UP]:
                input_vector.y -= 1
                self.BAD_POS[1] -= self.PLAYER_SPEED * dt
            if keys[K_DOWN]:
                input_vector.y += 1
                self.BAD_POS[1] += self.PLAYER_SPEED * dt

            if input_vector.length() > 0:
                input_vector = input_vector.normalize()
                self.PLAYER_POS += input_vector * self.PLAYER_SPEED * dt

            # Convert to iso
            iso_px, iso_py = self.to_iso(self.PLAYER_POS.x, self.PLAYER_POS.y)
            iso_px += self.DISPLAY_WIDTH // 2
            iso_py += 50

            iso_bx, iso_by = self.to_iso(self.BAD_POS[0], self.BAD_POS[1])
            iso_bx += self.DISPLAY_WIDTH // 2
            iso_by += 50

            # DRAW
            self.DISPLAY.fill((0, 0, 0))  # black BG
            self.draw_iso_grid(self.DISPLAY)

            # Red "bad player"
            pygame.draw.rect(
                self.DISPLAY,
                (255, 0, 0),
                (iso_bx - 10, iso_by - 20, 20, 40)
            )

            # Green "vector player"
            pygame.draw.rect(
                self.DISPLAY,
                (0, 255, 0),
                (iso_px - 10, iso_py - 20, 20, 40)
            )

            pygame.display.set_caption("Isometric Grid Movement Demo")
            pygame.display.update()


if __name__ == "__main__":
    app = Main()
    app.run()
