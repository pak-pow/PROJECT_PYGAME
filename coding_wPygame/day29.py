import pygame
import math
import random

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# ============ CONFIGURATION ============
class Config:
    # Window
    WIDTH = 1200
    HEIGHT = 800
    TITLE = "Day 29: Class-Based FPS | 60 FPS"

    # Physics
    MOUSE_SENSITIVITY = 0.06
    ACCELERATION = 0.10
    FRICTION = 0.90
    GRAVITY = 0.02
    JUMP_FORCE = 0.5
    AIR_RESISTANCE = 0.98
    PLAYER_HEIGHT = 2.0

    # Gameplay
    BULLET_SPEED = 4.0
    ENEMY_SPAWN_RATE = 60
    ENEMY_SPEED = 0.7
    BULLET_RANGE = 400
    FLOOR_LEVEL = -5.0


# ============ RENDERER ENGINE ============
class Renderer:
    def __init__(self):

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(100, (Config.WIDTH / Config.HEIGHT), 0.1, 500.0)
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_DEPTH_TEST)

        # Display Lists IDs
        self.cube_list = None
        self.grid_list = None
        self.compile_lists()

    def compile_lists(self):

        self.cube_list = glGenLists(1)
        glNewList(self.cube_list, GL_COMPILE)

        vertices = (
            (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1),
            (1, -1, 1), (1, 1, 1), (-1, -1, 1), (-1, 1, 1)
        )
        edges = (
            (0, 1), (0, 3), (0, 4), (2, 1), (2, 3), (2, 7),
            (6, 3), (6, 4), (6, 7), (5, 1), (5, 4), (5, 7)
        )

        glBegin(GL_LINES)
        for edge in edges:
            for v in edge:
                glVertex3fv(vertices[v])
        glEnd()
        glEndList()

        # 2. GRID
        self.grid_list = glGenLists(1)
        glNewList(self.grid_list, GL_COMPILE)

        glBegin(GL_LINES)
        glColor3f(0.2, 0.2, 0.2)
        grid_size = 1000
        spacing = 20
        y = Config.FLOOR_LEVEL

        for i in range(-grid_size, grid_size + 1, spacing):
            glVertex3f(i, y, -grid_size);
            glVertex3f(i, y, grid_size)
            glVertex3f(-grid_size, y, i);
            glVertex3f(grid_size, y, i)
        glEnd()
        glEndList()

    def draw_scene(self, player, bullets, enemies):

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()


        glRotatef(player.pitch, 1, 0, 0)
        glRotatef(player.yaw, 0, 1, 0)
        glTranslatef(-player.pos[0], -player.pos[1], -player.pos[2])

        glCallList(self.grid_list)

        glColor3f(1, 1, 0)
        for b in bullets:
            glPushMatrix()
            glTranslatef(b[0], b[1], b[2])
            glScalef(0.1, 0.1, 0.1)
            glCallList(self.cube_list)
            glPopMatrix()

        glColor3f(1, 0, 0)
        for e in enemies:
            glPushMatrix()
            glTranslatef(e[0], e[1], e[2])

            dx = player.pos[0] - e[0]
            dz = player.pos[2] - e[2]
            angle = math.degrees(math.atan2(dx, dz))
            glRotatef(angle, 0, 1, 0)

            glCallList(self.cube_list)
            glPopMatrix()

    def draw_ui(self):

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, Config.WIDTH, Config.HEIGHT, 0)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glDisable(GL_DEPTH_TEST)
        glLineWidth(2.0)

        cx, cy = Config.WIDTH // 2, Config.HEIGHT // 2
        size = 2

        glBegin(GL_LINES)
        glColor3f(0, 1, 0)
        glVertex2f(cx - size, cy);
        glVertex2f(cx + size, cy)
        glVertex2f(cx, cy - size);
        glVertex2f(cx, cy + size)
        glEnd()

        glLineWidth(1.0)
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()


# ============ PLAYER CONTROLLER ============
class Player:
    def __init__(self):
        self.pos = [0.0, 5.0, 0.0]
        self.vel = [0.0, 0.0, 0.0]
        self.yaw = 0.0
        self.pitch = 0.0
        self.on_ground = False

    def update(self, keys, mouse_delta):

        self.yaw += mouse_delta[0] * Config.MOUSE_SENSITIVITY
        self.pitch += mouse_delta[1] * Config.MOUSE_SENSITIVITY
        self.pitch = max(-89, min(89, self.pitch))

        rad = math.radians(self.yaw)
        s = math.sin(rad)
        c = math.cos(rad)

        fx, fz = 0, 0
        if keys[K_w]: fx += s; fz -= c
        if keys[K_s]: fx -= s; fz += c
        if keys[K_a]: fx -= c; fz -= s
        if keys[K_d]: fx += c; fz += s

        self.vel[0] += fx * Config.ACCELERATION
        self.vel[2] += fz * Config.ACCELERATION

        if keys[K_SPACE] and self.on_ground:
            self.vel[1] = Config.JUMP_FORCE
            self.on_ground = False

        self.vel[1] -= Config.GRAVITY
        friction = Config.FRICTION if self.on_ground else Config.AIR_RESISTANCE
        self.vel[0] *= friction
        self.vel[2] *= friction

        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.pos[2] += self.vel[2]

        if self.pos[1] < Config.FLOOR_LEVEL + Config.PLAYER_HEIGHT:
            self.pos[1] = Config.FLOOR_LEVEL + Config.PLAYER_HEIGHT
            self.vel[1] = 0
            self.on_ground = True
        else:
            self.on_ground = False

    def get_shoot_vector(self):
        yaw_rad = math.radians(self.yaw)
        pitch_rad = math.radians(self.pitch)

        x = math.sin(yaw_rad) * math.cos(pitch_rad)
        y = -math.sin(pitch_rad)
        z = -math.cos(yaw_rad) * math.cos(pitch_rad)

        return x, y, z


# ============ GAME MANAGER ============
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (Config.WIDTH, Config.HEIGHT), DOUBLEBUF | OPENGL
        )
        pygame.display.set_caption(Config.TITLE)

        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        self.score = 0

        # Setup Systems
        self.renderer = Renderer()
        self.player = Player()

        # Mouse Setup
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)

        # Entities
        self.bullets = []
        self.enemies = []
        self.spawn_timer = 0

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    grab = not pygame.event.get_grab()
                    pygame.event.set_grab(grab)
                    pygame.mouse.set_visible(not grab)

                if event.key == K_r and self.game_over:
                    self.reset_game()

            if event.type == MOUSEBUTTONDOWN and not self.game_over:
                if event.button == 1:
                    self.shoot()

    def shoot(self):
        dx, dy, dz = self.player.get_shoot_vector()
        self.bullets.append([
            self.player.pos[0], self.player.pos[1], self.player.pos[2],
            dx * Config.BULLET_SPEED, dy * Config.BULLET_SPEED, dz * Config.BULLET_SPEED
        ])

    def spawn_enemy(self):

        angle_offset = random.uniform(-60, 60)
        final_angle = self.player.yaw + angle_offset
        rad = math.radians(final_angle)
        dist = 40

        ex = self.player.pos[0] + math.sin(rad) * dist
        ez = self.player.pos[2] - math.cos(rad) * dist
        self.enemies.append([ex, -4, ez])

    def update(self):
        if self.game_over: return

        if pygame.event.get_grab():
            self.player.update(pygame.key.get_pressed(), pygame.mouse.get_rel())
        else:
            self.player.update(pygame.key.get_pressed(), (0, 0))

        self.spawn_timer += 1
        if self.spawn_timer > Config.ENEMY_SPAWN_RATE:
            self.spawn_timer = 0
            self.spawn_enemy()

        # Bullets
        for b in self.bullets[:]:
            b[0] += b[3]
            b[1] += b[4]
            b[2] += b[5]
            dist = math.sqrt((b[0] - self.player.pos[0]) ** 2 + (b[2] - self.player.pos[2]) ** 2)

            if b[1] < -10 or dist > Config.BULLET_RANGE:
                self.bullets.remove(b)

        for e in self.enemies[:]:
            # AI
            dx = self.player.pos[0] - e[0]
            dy = self.player.pos[1] - e[1]
            dz = self.player.pos[2] - e[2]
            dist = math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)

            if dist > 0:
                e[0] += (dx / dist) * Config.ENEMY_SPEED
                e[1] += (dy / dist) * Config.ENEMY_SPEED
                e[2] += (dz / dist) * Config.ENEMY_SPEED

            if dist < 1.5:
                self.game_over = True
                print(f"GAME OVER! Final Score: {self.score}")

            for b in self.bullets[:]:
                b_dist = math.sqrt((b[0] - e[0]) ** 2 + (b[1] - e[1]) ** 2 + (b[2] - e[2]) ** 2)
                if b_dist < 3.5:
                    if e in self.enemies: self.enemies.remove(e)
                    if b in self.bullets: self.bullets.remove(b)
                    self.score += 100
                    print(f"Score: {self.score}")
                    break

    def render(self):

        if self.game_over:
            glClearColor(0.3, 0, 0, 1)
        else:
            glClearColor(0, 0, 0, 1)

        self.renderer.draw_scene(self.player, self.bullets, self.enemies)
        self.renderer.draw_ui()
        pygame.display.flip()

    def reset_game(self):
        self.game_over = False
        self.player = Player()
        self.enemies.clear()
        self.bullets.clear()
        self.score = 0

    def run(self):

        while self.running:
            self.clock.tick(60)
            self.handle_input()
            self.update()
            self.render()

        pygame.quit()


# ============ ENTRY POINT ============
if __name__ == "__main__":
    game = Game()
    game.run()