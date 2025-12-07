import pygame
import sys
import random

from pygame.locals import *
from pygame.sprite import Sprite

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

GRID_SIZE = 20


class Snake(Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.grid_x = x
        self.grid_y = y
        self.direction = random.choice(["UP", "DOWN", "RIGHT"])
        self.body = [(x, y), (x - 1, y), (x - 2, y)]
        self.growing = False

    def get_head_pos(self):
        return self.body[0]

    def update(self, grid_width, grid_height):
        head_x, head_y = self.body[0]

        if self.direction == 'UP':
            head_y -= 1
        elif self.direction == 'DOWN':
            head_y += 1
        elif self.direction == 'LEFT':
            head_x -= 1
        elif self.direction == 'RIGHT':
            head_x += 1

        head_x = head_x % grid_width
        head_y = head_y % grid_height

        new_head = (head_x, head_y)
        self.body.insert(0, new_head)

        if not self.growing:
            self.body.pop()
        else:
            self.growing = False

    def change_direction(self, new_direction):
        opposite = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}
        if new_direction != opposite.get(self.direction):
            self.direction = new_direction

    def grow(self):
        self.growing = True

    def check_collision(self):
        head = self.body[0]
        return head in self.body[1:]

    def draw(self, surface):
        for i, segment in enumerate(self.body):
            x = segment[0] * GRID_SIZE
            y = segment[1] * GRID_SIZE

            color = UI_SKY_BLUE if i == 0 else UI_NAVY_BLUE
            pygame.draw.rect(surface, color, (x, y, GRID_SIZE - 2, GRID_SIZE - 2), border_radius=3)


class Apple(Sprite):
    def __init__(self, grid_width, grid_height, snake_body):
        super().__init__()
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.randomize_position(snake_body)

    def randomize_position(self, snake_body):
        while True:
            self.grid_x = random.randint(0, self.grid_width - 1)
            self.grid_y = random.randint(0, self.grid_height - 1)
            if (self.grid_x, self.grid_y) not in snake_body:
                break

    def draw(self, surface):
        x = self.grid_x * GRID_SIZE
        y = self.grid_y * GRID_SIZE
        pygame.draw.circle(surface, UI_RED,(x + GRID_SIZE // 2, y + GRID_SIZE // 2), GRID_SIZE // 2 - 2)

class Main:
    def __init__(self):
        pygame.init()

        self.DISPLAY_WIDTH = 800
        self.DISPLAY_HEIGHT = 600
        self.DISPLAY = pygame.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))

        self.CLOCK = pygame.time.Clock()
        self.FPS = 60

        self.grid_width = self.DISPLAY_WIDTH // GRID_SIZE
        self.grid_height = self.DISPLAY_HEIGHT // GRID_SIZE

        self.snake = Snake(self.grid_width // 2, self.grid_height // 2)
        self.apple = Apple(self.grid_width, self.grid_height, self.snake.body)

        self.score = 0
        self.game_over = False
        self.move_timer = 0
        self.move_delay = 0.1

        self.font = pygame.font.Font(None, 36)

    def reset_game(self):
        self.snake = Snake(self.grid_width // 2, self.grid_height // 2)
        self.apple = Apple(self.grid_width, self.grid_height, self.snake.body)
        self.score = 0
        self.game_over = False

    def run(self):
        while True:
            dt = self.CLOCK.tick(self.FPS) / 1000

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:

                    if not self.game_over:

                        if event.key == K_UP or event.key == K_w:
                            self.snake.change_direction('UP')

                        elif event.key == K_DOWN or event.key == K_s:
                            self.snake.change_direction('DOWN')

                        elif event.key == K_LEFT or event.key == K_a:
                            self.snake.change_direction('LEFT')

                        elif event.key == K_RIGHT or event.key == K_d:
                            self.snake.change_direction('RIGHT')

                    else:
                        if event.key == K_SPACE:
                            self.reset_game()

            if not self.game_over:
                self.move_timer += dt

                if self.move_timer >= self.move_delay:
                    self.move_timer = 0
                    self.snake.update(self.grid_width, self.grid_height)

                    # Check collision with self
                    if self.snake.check_collision():
                        self.game_over = True

                    # Check collision with apple
                    head = self.snake.get_head_pos()
                    if head == (self.apple.grid_x, self.apple.grid_y):
                        self.snake.grow()
                        self.score += 10
                        self.apple.randomize_position(self.snake.body)
                        # Increase speed slightly
                        self.move_delay = max(0.05, self.move_delay * 0.95)

            # Draw everything
            self.DISPLAY.fill(UI_WHITE)

            # Draw grid
            for x in range(0, self.DISPLAY_WIDTH, GRID_SIZE):
                pygame.draw.line(self.DISPLAY, UI_LIGHT_GRAY, (x, 0), (x, self.DISPLAY_HEIGHT))

            for y in range(0, self.DISPLAY_HEIGHT, GRID_SIZE):
                pygame.draw.line(self.DISPLAY, UI_LIGHT_GRAY, (0, y), (self.DISPLAY_WIDTH, y))

            self.apple.draw(self.DISPLAY)
            self.snake.draw(self.DISPLAY)

            # Draw score
            score_text = self.font.render(f'Score: {self.score}', True, UI_DARK_GRAY)
            self.DISPLAY.blit(score_text, (10, 10))

            # Draw game over
            if self.game_over:
                game_over_text = self.font.render('GAME OVER!', True, UI_RED)
                restart_text = self.font.render('Press SPACE to restart', True, UI_DARK_GRAY)

                text_rect = game_over_text.get_rect(center=(self.DISPLAY_WIDTH // 2, self.DISPLAY_HEIGHT // 2 - 20))
                restart_rect = restart_text.get_rect(center=(self.DISPLAY_WIDTH // 2, self.DISPLAY_HEIGHT // 2 + 20))

                self.DISPLAY.blit(game_over_text, text_rect)
                self.DISPLAY.blit(restart_text, restart_rect)

            pygame.display.set_caption(f"SNAKE - Score: {self.score}")
            pygame.display.update()


if __name__ == "__main__":
    game = Main()
    game.run()