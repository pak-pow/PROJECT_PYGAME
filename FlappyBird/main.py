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
    UI_BLACK = (20, 20, 20)

    DISPLAY_WIDTH = 800
    DISPLAY_HEIGHT = 500
    FLOOR_Y = 490

    GRAVITY = 2000
    JUMP_STRENGTH = -600

    CLOCK = pygame.time.Clock()
    FPS = 60

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Flappy Bird")
        self.DISPLAY = pygame.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))

        self.font = pygame.font.SysFont('Arial', 40, bold=True)

        bg_raw = pygame.image.load("background.png").convert()
        self.bg_image = pygame.transform.scale(bg_raw, (self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))

        self.SPAWN_PIPE_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.SPAWN_PIPE_EVENT, 1500)

        self.game_active = True

    def reset_game(self):
        self.game_active = True
        return pygame.sprite.Group(), pygame.sprite.Group(), Player()

    def run(self):
        all_sprite = pygame.sprite.Group()
        pipes_group = pygame.sprite.Group()
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
                        if self.game_active:
                            player.jump()

                        else:
                            all_sprite, pipes_group, player = self.reset_game()
                            all_sprite.add(player)

                if event.type == self.SPAWN_PIPE_EVENT and self.game_active:
                    gap_size = 200
                    padding = 50

                    min_y = padding + (gap_size // 2)
                    max_y = self.DISPLAY_HEIGHT - padding - (gap_size // 2)

                    if min_y >= max_y:
                        gap_y = self.DISPLAY_HEIGHT // 2

                    else:
                        gap_y = random.randint(min_y, max_y)

                    top_pipe_y = gap_y - (gap_size // 2)
                    bottom_pipe_y = gap_y + (gap_size // 2)

                    spawn_x = self.DISPLAY_WIDTH + 10

                    new_top = Pipe(spawn_x, top_pipe_y, is_top=True)
                    new_bottom = Pipe(spawn_x, bottom_pipe_y, is_top=False)

                    pipes_group.add(new_top, new_bottom)
                    all_sprite.add(new_top, new_bottom)

            if self.game_active:
                all_sprite.update(dt)

                if pygame.sprite.spritecollide(player, pipes_group, False):
                    self.game_active = False

            else:
                if player.rect.bottom < self.FLOOR_Y:
                    player.velocity.y += self.GRAVITY * dt
                    player.pos.y += player.velocity.y * dt
                    player.rect.center = round(player.pos)

                    if player.pos.y >= self.FLOOR_Y:
                        player.pos.y = self.FLOOR_Y

            self.DISPLAY.blit(self.bg_image, (0, 0))
            all_sprite.draw(self.DISPLAY)

            if not self.game_active:
                text_surf = self.font.render("GAME OVER - Press SPACE", True, self.UI_BLACK)
                text_rect = text_surf.get_rect(center=(self.DISPLAY_WIDTH / 2, self.DISPLAY_HEIGHT / 2))
                self.DISPLAY.blit(text_surf, text_rect)

            pygame.display.update()

if __name__ == "__main__":
    app = Main()
    app.run()