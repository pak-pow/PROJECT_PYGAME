import pygame
import sys

from pygame.locals import *

class Player(pygame.sprite.Sprite):

    def __init__(self, sheet):
        super().__init__()

        self.frames = []
        frame_width = 32
        frame_height = 32

        for i in range(4):

            self.frame_location = (i * frame_width, 0, frame_width, frame_height)
            self.frame_image = sheet.subsurface(self.frame_location)
            self.frames.append(self.frame_image)

        self.frame_index = 0.0
        self.animation_speed = 8

        self.image = self.frames[0]
        self.rect = self.image.get_rect(center = (300, 200))
        self.pos = pygame.math.Vector2(300,200)
        self.velocity = pygame.math.Vector2(0,0)
        self.speed = 300
        self.facing_right = True

    def get_input(self):

        keys = pygame.key.get_pressed()
        self.velocity.x = 0

        if keys[K_LEFT] or keys[K_a]:
            self.velocity.x = -self.speed
            self.facing_right = False

        if keys[K_RIGHT] or keys[K_d]:
            self.velocity.x = self.speed
            self.facing_right = True

    def animate(self, dt):

        if self.velocity.x != 0:
            self.frame_index += self.animation_speed * dt

            if self.frame_index >= len(self.frames):
                self.frame_index = 0
        else:
            self.frame_index = 0

        current_image = self.frames[int(self.frame_index)]

        if not self.facing_right:
            self.image = pygame.transform.flip(current_image, True, False)
        else:
            self.image = current_image

    def update(self, dt):
        self.get_input()
        self.pos += self.velocity * dt
        self.rect.center = round(self.pos)

        self.animate(dt)


class Main:

    WHITE = (255,255,255)

    def __init__(self):

        self.dt = None
        pygame.init()

        self.clock = pygame.time.Clock()
        self.sheet = None
        self.DISPLAY_WIDTH = 600
        self.DISPLAY_HEIGHT = 400
        self.DISPLAY_COLOR = self.WHITE
        self.DISPLAY = pygame.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))

        self.sprite_sheet = self.generate_sprite_sheet()
        self.player = Player(self.sprite_sheet)
        self.all_sprites = pygame.sprite.Group(self.player)

    def generate_sprite_sheet(self):

        self.sheet = pygame.Surface((128,32))
        self.sheet.fill((0,0,0))

        pygame.draw.rect(self.sheet, (255, 0, 0), (0, 0, 32, 32))
        pygame.draw.circle(self.sheet, (0, 255, 0), (48, 16), 16)
        pygame.draw.rect(self.sheet, (0, 0, 255), (64, 0, 32, 32))
        pygame.draw.circle(self.sheet, (255, 255, 0), (112, 16), 16)

        return self.sheet

    def run(self):

        while True:

            self.dt = self.clock.tick(60) / 1000

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            self.DISPLAY.fill(self.DISPLAY_COLOR)
            self.all_sprites.update(self.dt)
            self.all_sprites.draw(self.DISPLAY)

            self.DISPLAY.blit(self.sprite_sheet, (10,10))
            pygame.display.update()

if __name__ == "__main__":
    app = Main()
    app.run()