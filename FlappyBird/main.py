import pygame
import sys
import random

from pygame.locals import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        original_image = pygame.image.load("bird.png").convert_alpha()
        self.image = pygame.transform.scale(original_image, (40, 40))

        self.rect = self.image.get_rect(center=(Main.DISPLAY_WIDTH // 2, Main.DISPLAY_HEIGHT // 2))
        self.pos = pygame.Vector2(self.rect.center)
        self.velocity = pygame.Vector2()

    def jump(self):
        self.velocity.y = Main.JUMP_STRENGTH

    def update(self, dt):
        self.velocity.y += Main.GRAVITY * dt
        self.pos += self.velocity * dt

        if self.pos.y >= Main.FLOOR_Y:
            self.pos.y = Main.FLOOR_Y
            self.velocity.y = 0

        if self.pos.y < 0:
            self.pos.y = 0
            self.velocity.y = 0

        self.rect.center = round(self.pos)

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, is_top):
        super().__init__()

        width = 100
        height = 350

        original = pygame.image.load("pipe.png").convert_alpha()

        visible_rect = original.get_bounding_rect()
        cropped_image = original.subsurface(visible_rect)

        self.image = pygame.transform.scale(cropped_image, (width, height))

        if is_top:
            self.rect = self.image.get_rect(bottomleft=(x, y))

        else:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, dt):
        self.rect.x -= 300 * dt
        if self.rect.right < 0:
            self.kill()

class Main:

    UI_WHITE = (245, 245, 245)
    UI_LIGHT_GRAY = (230, 230, 230)
    UI_GRAY = (180, 180, 180)
    UI_DARK_GRAY = (100, 100, 100)
    UI_BLACK = (20, 20, 20)

    UI_SKY_BLUE = (93, 173, 226)
    UI_NAVY_BLUE = (52, 73, 94)
    UI_PURPLE = (155, 89, 182)
    UI_GREEN = (46, 204, 113)
    UI_ORANGE = (243, 156, 18)
    UI_RED = (231, 76, 60)

    DISPLAY_WIDTH = 800
    DISPLAY_HEIGHT = 500
    FLOOR_Y = 490

    GRAVITY = 2000
    MOVE_SPEED = 800
    JUMP_STRENGTH = -600

    CLOCK = pygame.time.Clock()
    FPS = 60

    def __init__(self):

        pygame.init()
        pygame.display.set_caption("Flappy Bird")
        self.DISPLAY = pygame.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))

        bg_raw = pygame.image.load("background.png").convert()
        self.bg_image = pygame.transform.scale(bg_raw, (self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))

        self.SPAWN_PIPE_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.SPAWN_PIPE_EVENT, 1500)

    def run(self):

        all_sprite = pygame.sprite.Group()
        player = Player()

        all_sprite.add(player)

        while True:

            dt = self.CLOCK.tick(self.FPS) / 1000
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        player.jump()

                if event.type == self.SPAWN_PIPE_EVENT:

                    gap_size = 150  # Space between pipes
                    gap_y = random.randint(gap_size + 50, self.DISPLAY_HEIGHT - gap_size - 50)

                    top_pipe_y = gap_y - (gap_size // 2)
                    bottom_pipe_y = gap_y + (gap_size // 2)

                    spawn_x = self.DISPLAY_WIDTH + 10

                    new_top = Pipe(spawn_x, top_pipe_y, is_top=True)
                    new_bottom = Pipe(spawn_x, bottom_pipe_y, is_top=False)

                    all_sprite.add(new_top)
                    all_sprite.add(new_bottom)

            all_sprite.update(dt)
            self.DISPLAY.blit(self.bg_image, (0, 0))

            all_sprite.draw(self.DISPLAY)
            pygame.display.update()

if __name__ == "__main__":
    app = Main()
    app.run()