import pygame
import sys
import random

from pygame.locals import *

# -------------------- PLAYER --------------------
class Player(pygame.sprite.Sprite):
    def __init__(self, all_sprites, bullet_group):
        super().__init__()

        self.all_sprites = all_sprites
        self.bullet_group = bullet_group

        self.image = pygame.Surface((40, 40))
        self.image.fill((0, 255, 0))

        self.rect = self.image.get_rect(center=(400, 300))
        self.pos = pygame.math.Vector2(self.rect.center)

        self.speed = 300
        self.last_shot_time = 0
        self.shoot_delay = 250  # ms

    def get_input(self, dt):
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
            input_vec = input_vec.normalize()
            self.pos += input_vec * self.speed * dt
            self.rect.center = (int(self.pos.x), int(self.pos.y))

        if pygame.mouse.get_pressed()[0]:
            self.shoot()

    def shoot(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_shot_time >= self.shoot_delay:
            self.last_shot_time = current_time

            mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos())
            direction = mouse_pos - self.pos

            if direction.length() > 0:
                direction = direction.normalize()

                bullet = Bullet(self.rect.center, direction)
                self.bullet_group.add(bullet)
                self.all_sprites.add(bullet)

    def update(self, dt):
        self.get_input(dt)


# -------------------- BULLET --------------------
class Bullet(pygame.sprite.Sprite):
    def __init__(self, start_pos, direction):
        super().__init__()

        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=start_pos)

        self.pos = pygame.math.Vector2(start_pos)
        self.velocity = direction * 600
        self.lifetime = 1000  # ms
        self.spawn_time = pygame.time.get_ticks()

    def update(self, dt):
        self.pos += self.velocity * dt
        self.rect.center = (int(self.pos.x), int(self.pos.y))

        if (
            pygame.time.get_ticks() - self.spawn_time > self.lifetime
            or not Main.DISPLAY.get_rect().colliderect(self.rect)
        ):
            self.kill()


# -------------------- ENEMY --------------------
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(
            center=(
                random.randint(0, Main.DISPLAY_WIDTH),
                random.randint(0, Main.DISPLAY_HEIGHT),
            )
        )


# -------------------- MAIN --------------------
class Main:
    DISPLAY_WIDTH = 800
    DISPLAY_HEIGHT = 600
    DISPLAY_COLOR = (0,0,0)

    def __init__(self):
        pygame.init()

        self.DISPLAY = pygame.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))
        Main.DISPLAY = self.DISPLAY

        pygame.display.set_caption("DAY16")

        self.CLOCK = pygame.time.Clock()
        self.FPS = 60

    def run(self):
        all_sprites = pygame.sprite.Group()
        bullet_group = pygame.sprite.Group()
        enemy_group = pygame.sprite.Group()

        player = Player(all_sprites, bullet_group)
        all_sprites.add(player)

        spawn_timer = 0
        # ---------------- GAME LOOP ----------------
        while True:
            dt = self.CLOCK.tick(self.FPS) / 1000

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            # SPAWN ENEMIES
            spawn_timer += dt
            if spawn_timer > 0.5:  # Every 1 second
                enemy = Enemy()
                enemy_group.add(enemy)
                all_sprites.add(enemy)
                spawn_timer = 0

            # UPDATE
            all_sprites.update(dt)

            # COMBAT LOGIC (The Magic Line)
            # Check if ANY bullet hit ANY enemy. Kill both (True, True)
            hits = pygame.sprite.groupcollide(bullet_group, enemy_group, True, True)

            all_sprites.update(dt)

            self.DISPLAY.fill(self.DISPLAY_COLOR)
            all_sprites.draw(self.DISPLAY)
            pygame.display.update()


# -------------------- RUN --------------------
if __name__ == "__main__":
    app = Main()
    app.run()