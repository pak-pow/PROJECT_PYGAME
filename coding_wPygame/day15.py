import pygame, sys

# ----------------------------------------
# 1. Setup
# ----------------------------------------
pygame.init()
SCREEN_W, SCREEN_H = 600, 400
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
clock = pygame.time.Clock()
TILE_SIZE = 40
pygame.display.set_caption("Platformer Demo")

# ----------------------------------------
# LEVEL (ASCII ART)
# ----------------------------------------
LEVEL_MAP = [
    'XXXXXXXXXXXXXXX',
    'X             X',
    'X             X',
    'X      XXX    X',
    'X             X',
    'XXXX       XXXX',
    'X             X',
    'XP   WWWWW    X',
    'XXXXXXXXXXXXXXX'
]


# ----------------------------------------
# CLASSES
# ----------------------------------------
class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, type):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))

        # Colors for different tile types
        if type == 'X':
            self.image.fill((180, 180, 180))  # Wall
            pygame.draw.rect(self.image, (80, 80, 80), (0, 0, TILE_SIZE, TILE_SIZE), 3)
        elif type == 'W':
            self.image.fill((30, 30, 200))  # Water
            pygame.draw.rect(self.image, (10, 10, 100), (0, 0, TILE_SIZE, TILE_SIZE), 3)

        self.rect = self.image.get_rect(topleft=pos)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, walls):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 100, 100))
        pygame.draw.rect(self.image, (200, 50, 50), (0, 0, 30, 30), 3)

        self.rect = self.image.get_rect(topleft=pos)
        self.walls = walls

        # Movement physics
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(0, 0)
        self.speed = 250
        self.gravity = 900
        self.jump_force = -500

        # Double jump
        self.can_double = True
        self.grounded = False

    def horizontal_movement(self, dt):
        keys = pygame.key.get_pressed()
        self.vel.x = 0

        if keys[pygame.K_LEFT]:
            self.vel.x = -self.speed
        if keys[pygame.K_RIGHT]:
            self.vel.x = self.speed

        # Move horizontally
        self.pos.x += self.vel.x * dt
        self.rect.x = round(self.pos.x)

        # Horizontal collisions
        hits = pygame.sprite.spritecollide(self, self.walls, False)
        for tile in hits:
            if self.vel.x > 0:
                self.rect.right = tile.rect.left
            elif self.vel.x < 0:
                self.rect.left = tile.rect.right
            self.pos.x = self.rect.x

    def vertical_movement(self, dt):
        keys = pygame.key.get_pressed()

        # Apply gravity
        self.vel.y += self.gravity * dt
        self.vel.y = min(self.vel.y, 900)  # Clamp fall speed

        # Move vertically
        self.pos.y += self.vel.y * dt
        self.rect.y = round(self.pos.y)

        # Vertical collision
        hits = pygame.sprite.spritecollide(self, self.walls, False)
        self.grounded = False

        for tile in hits:
            if self.vel.y > 0:  # Falling
                self.rect.bottom = tile.rect.top
                self.pos.y = self.rect.y
                self.vel.y = 0
                self.grounded = True
                self.can_double = True  # Reset double jump

            elif self.vel.y < 0:  # Hitting ceiling
                self.rect.top = tile.rect.bottom
                self.pos.y = self.rect.y
                self.vel.y = 0

        # Jumping logic
        if keys[pygame.K_SPACE]:
            if self.grounded:
                self.vel.y = self.jump_force
            elif self.can_double:
                self.vel.y = self.jump_force
                self.can_double = False

    def update(self, dt):
        self.horizontal_movement(dt)
        self.vertical_movement(dt)


# ----------------------------------------
# LEVEL PARSING
# ----------------------------------------
tile_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

for row_index, row in enumerate(LEVEL_MAP):
    for col_index, char in enumerate(row):

        x = col_index * TILE_SIZE
        y = row_index * TILE_SIZE

        if char in ('X', 'W'):
            tile = Tile((x, y), char)
            tile_group.add(tile)

        elif char == 'P':
            player = Player((x, y), tile_group)
            player_group.add(player)

# ----------------------------------------
# GAME LOOP
# ----------------------------------------
while True:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((20, 20, 20))

    tile_group.draw(screen)
    player_group.update(dt)
    player_group.draw(screen)

    pygame.display.update()
