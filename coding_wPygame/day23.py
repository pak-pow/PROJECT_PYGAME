import pygame
import sys

from pygame.locals import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((40,40))
        self.image.fill((0,0,255))

        self.rect = self.image.get_rect(center = (400,300))
        self.pos = pygame.Vector2(self.rect.center)
        self.velocity = pygame.Vector2()

        self.max_speed = 300
        self.acceleration = 3000
        self.friction = 0.90
        self.threshold = 20

    def update(self, dt):

        keys = pygame.key.get_pressed()
        direction = pygame.Vector2(0,0)

        if keys[K_w]:
            direction.y -= 1

        if keys[K_s]:
            direction.y += 1

        if keys[K_a]:
            direction.x -= 1

        if keys[K_d]:
            direction.x += 1

        if direction.length_squared() > 0:
            direction.normalize()
            self.velocity += direction * self.acceleration * dt

        else:
            self.velocity *= self.friction

            if self.velocity.length() < self.threshold:
                self.velocity.update(0,0)

        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        self.pos += self.velocity * dt

        self.pos.x = max(20, min(Main.DISPLAY_WIDTH - 20, self.pos.x))
        self.pos.y = max(20, min(Main.DISPLAY_HEIGHT - 20, self.pos.y))

        self.rect.center = round(self.pos)

class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y, text):
        super().__init__()

        self.image = pygame.Surface((40,40))
        self.image.fill((255,255,0))

        self.rect = self.image.get_rect(center = (x,y))
        self.pos = pygame.Vector2(self.rect.center)

        self.text = text


class Main:

    DISPLAY_WIDTH = 800
    DISPLAY_HEIGHT = 600
    DISPLAY_COLOR = (0,0,0)

    CLOCK = pygame.time.Clock()
    FPS = 60

    def __init__(self):

        pygame.init()
        self.DISPLAY = pygame.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))
        pygame.display.set_caption("DAY23")

        self.FONT = pygame.font.SysFont("Arial", 24)
        self.TIP_FONT = pygame.font.SysFont("Arial", 16, bold = True)

    def dialog_box(self, surface, text):

        self.box_rect = pygame.Rect(50,450,700,100)
        pygame.draw.rect(self.DISPLAY, (0,0,0), self.box_rect)
        pygame.draw.rect(self.DISPLAY, (255,255,255), self.box_rect, 3)

        self.text_surface = self.FONT.render(text, True, (255,255,255))
        surface.blit(self.text_surface, (70,470))

        self.hint = self.TIP_FONT.render("[Press E to Close]", True, (150, 150, 150))
        surface.blit(self.hint, (600, 520))

    def run(self):

        all_sprite = pygame.sprite.Group()
        player = Player()
        npc = NPC(600,300, "Greetings, traveler! Welcome to Pygame!")

        all_sprite.add(player)
        all_sprite.add(npc)

        active_dialog = False
        active_text = ""

        while True:
            dt = self.CLOCK.tick(self.FPS) / 1000

            dist = (player.pos - npc.pos).length()
            can_interact = dist < 70

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:

                        if active_dialog:
                            active_dialog = False

                        elif can_interact:
                            active_dialog = True
                            active_text = npc.text

            if not active_dialog:
                all_sprite.update(dt)

            self.DISPLAY.fill(self.DISPLAY_COLOR)
            all_sprite.draw(self.DISPLAY)

            if can_interact and not active_dialog:
                prompt = self.TIP_FONT.render("[E] TALK", True, (255, 255, 255))
                self.DISPLAY.blit(prompt, (npc.rect.centerx - 20, npc.rect.top - 20))

            if active_dialog:
                self.dialog_box(self.DISPLAY, active_text)

            pygame.display.update()

if __name__ == "__main__":
    app = Main()
    app.run()