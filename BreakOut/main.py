import pygame
import sys
from pygame.locals import *

# --- CONFIGURATION ---
TILE_SIZE = 40
DISPLAY_WIDTH = 600
DISPLAY_HEIGHT = 800

LEVEL_MAP = [
    "XXXXXXXXXXXXXXX",
    "XBBBBBBBBBBBBBX",
    "XBBBBBBBBBBBBBX",
    "XBBBBBBBBBBBBBX",
    "XBBBBBBBBBBBBBX",
    "XBBBBBBBBBBBBBX",
    "X             X",
    "X             X",
    "X             X",
    "X             X",
    "X             X",
    "X             X",
    "X             X",
    "X             X",
    "X             X",
    "X             X",
    "X      O      X",
    "X             X",
    "X     PPP     X",
    "XXXXXXXXXXXXXXX",
]


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, type):
        super().__init__()

        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=pos)
        self.type = type  # Store type for logic if needed

        if type == "X":  # Wall
            self.image.fill((180, 180, 180))

            pygame.draw.rect(
                self.image,
                (80, 80, 80),
                (0, 0, TILE_SIZE, TILE_SIZE),
                3
            )

        elif type == "B":  # Brick
            self.image.fill((0, 150, 255))

            pygame.draw.rect(
                self.image,
                (0, 80, 250),
                self.image.get_rect(),
                2
            )


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        # The paddle is 3 tiles wide
        self.image = pygame.Surface((TILE_SIZE * 3, TILE_SIZE))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(center=pos)
        self.speed = 500

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[K_a] or keys[K_LEFT]:
            self.rect.x -= self.speed * dt
        if keys[K_d] or keys[K_RIGHT]:
            self.rect.x += self.speed * dt

        # Constrain to screen (accounting for wall thickness)
        if self.rect.left < TILE_SIZE:
            self.rect.left = TILE_SIZE

        if self.rect.right > DISPLAY_WIDTH - TILE_SIZE:
            self.rect.right = DISPLAY_WIDTH - TILE_SIZE

class Ball(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 255, 0), (10, 10), 10)

        self.rect = self.image.get_rect(center=pos)

        self.pos = pygame.math.Vector2(pos)
        self.velocity = pygame.math.Vector2(0, 500)

    def update(self, dt, paddle, bricks, walls):

        self.pos.x += self.velocity.x * dt
        self.rect.x = round(self.pos.x)

        hit_walls = pygame.sprite.spritecollide(self, walls, False)
        for wall in hit_walls:

            if self.velocity.x > 0:
                self.rect.right = wall.rect.left
                self.pos.x = self.rect.x
                self.velocity.x *= -1

            elif self.velocity.x < 0:
                self.rect.left = wall.rect.right
                self.pos.x = self.rect.x
                self.velocity.x *= -1

        if pygame.sprite.spritecollide(self, bricks, True):
            self.velocity.x *= -1

        self.pos.y += self.velocity.y * dt
        self.rect.y = round(self.pos.y)

        hit_walls = pygame.sprite.spritecollide(self, walls, False)
        for wall in hit_walls:

            if self.velocity.y > 0:
                self.rect.bottom = wall.rect.top
                self.pos.y = self.rect.y
                self.velocity.y *= -1

            elif self.velocity.y < 0:
                self.rect.top = wall.rect.bottom
                self.pos.y = self.rect.y
                self.velocity.y *= -1

        if self.rect.colliderect(paddle.rect):
            if self.velocity.y > 0:
                self.rect.bottom = paddle.rect.top
                self.pos.y = self.rect.y
                self.velocity.y *= -1

                offset = self.rect.centerx - paddle.rect.centerx
                self.velocity.x += offset * 3

        if pygame.sprite.spritecollide(self, bricks, True):
            self.velocity.y *= -1

        if self.rect.left < 0:
            self.rect.left = 0
            self.pos.x = 0
            self.velocity.x *= -1

        if self.rect.right > DISPLAY_WIDTH:
            self.rect.right = DISPLAY_WIDTH
            self.pos.x = self.rect.x
            self.velocity.x *= -1

        if self.rect.top < 0:
            self.rect.top = 0
            self.pos.y = 0
            self.velocity.y *= -1

class Main:
    def __init__(self):
        pygame.init()
        self.CLOCK = pygame.time.Clock()
        self.FPS = 60
        self.DISPLAY = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

        # Create Groups
        self.all_sprites = pygame.sprite.Group()
        self.wall_group = pygame.sprite.Group()
        self.brick_group = pygame.sprite.Group()

        self.player = None
        self.ball = None

        self.load_level()

    def load_level(self):
        player_created = False

        for row_index, row in enumerate(LEVEL_MAP):
            for col_index, tile_char in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE

                if tile_char == "X":
                    tile = Tile((x, y), "X")
                    self.wall_group.add(tile)
                    self.all_sprites.add(tile)

                elif tile_char == "B":
                    tile = Tile((x, y), "B")
                    self.brick_group.add(tile)
                    self.all_sprites.add(tile)

                elif tile_char == "P":
                    if not player_created:
                        self.player = Player((x + 100, y + 20))
                        self.all_sprites.add(self.player)
                        player_created = True

                elif tile_char == "O":
                    self.ball = Ball((x + 20, y + 20))
                    self.all_sprites.add(self.ball)

    def run(self):
        while True:
            dt = self.CLOCK.tick(self.FPS) / 1000

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            self.player.update(dt)
            self.ball.update(dt, self.player, self.brick_group, self.wall_group)

            self.DISPLAY.fill((0, 0, 0))
            self.all_sprites.draw(self.DISPLAY)

            pygame.display.set_caption(f"BreakOut | FPS: {int(self.CLOCK.get_fps())}")
            pygame.display.update()


if __name__ == "__main__":
    app = Main()
    app.run()