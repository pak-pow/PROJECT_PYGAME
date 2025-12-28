import pygame
import math
import random

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# ========== CONFIG =============
DISPLAY_WIDTH = 1200
DISPLAY_HEIGHT = 800
DISPLAY = (DISPLAY_WIDTH, DISPLAY_HEIGHT)

MOUSE_LOOK_SENSITIVITY = 0.05

PLAYER_ACCELERATION = 20.0
GROUND_FRICTION = 8.0
GRAVITY_FORCE = 25.0
JUMP_STRENGTH = 10.0
AIR_RESISTANCE = 2.0

PROJECTILE_SPEED = 40.0

# ========= PLAYER ==============
class FPController:
    def __init__(self):

        self.position = [0.0, 5.0, 0.0]        # [x, y, z] position relative to the 3D Space
        self.velocity = [0.0, 0.0, 0.0]        # Same Ideo but for motion Vector

        self.look_angle_horizontal = 0.0       # YAW (Left / Right)
        self.look_angle_vertical = 0.0         # PITCH (Up / Down)

        self.player_height = 2.0
        self.on_ground = False

    def get_shoot_direction(self):

        yaw = math.radians(self.look_angle_horizontal)
        pitch = math.radians(self.look_angle_vertical)

        return (
            math.sin(yaw) * math.cos(pitch),
            -math.sin(pitch),
            -math.cos(yaw) * math.cos(pitch)
        )

    def update(self, keys, mouse_delta, dt):

        mx, my = mouse_delta
        self.look_angle_horizontal += mx * MOUSE_LOOK_SENSITIVITY
        self.look_angle_vertical += my * MOUSE_LOOK_SENSITIVITY
        self.look_angle_vertical = max(-89, min(89, self.look_angle_vertical))

        yaw = math.radians(self.look_angle_horizontal)
        sin_yaw, cos_yaw = math.sin(yaw), math.cos(yaw)

        accel_x = 0.0
        accel_z = 0.0

        if keys[K_w]:
            accel_x += sin_yaw * PLAYER_ACCELERATION
            accel_z -= cos_yaw * PLAYER_ACCELERATION

        if keys[K_s]:
            accel_x -= sin_yaw * PLAYER_ACCELERATION
            accel_z += cos_yaw * PLAYER_ACCELERATION

        if keys[K_a]:
            accel_x -= cos_yaw * PLAYER_ACCELERATION
            accel_z -= sin_yaw * PLAYER_ACCELERATION

        if keys[K_d]:
            accel_x += cos_yaw * PLAYER_ACCELERATION
            accel_z += sin_yaw * PLAYER_ACCELERATION

        self.velocity[0] += accel_x * dt
        self.velocity[2] += accel_z * dt

        if keys[K_SPACE] and self.on_ground:
            self.velocity[1] = JUMP_STRENGTH
            self.on_ground = False

        self.velocity[1] -= GRAVITY_FORCE * dt

        friction = GROUND_FRICTION if self.on_ground else AIR_RESISTANCE
        self.velocity[0] -= self.velocity[0] * friction * dt
        self.velocity[2] -= self.velocity[2] * friction * dt

        for i in range(3):
            self.position[i] += self.velocity[i] * dt

        floor_y = -5
        if self.position[1] < floor_y + self.player_height:
            self.position[1] = floor_y + self.player_height
            self.velocity[1] = 0
            self.on_ground = True

class Renderer:
    def __init__(self):
        pass

    def begin_frame(self):
        pass

    def apply_camera(self):
        pass

    def draw_cube(self):
        pass

    def draw_grid(self):
        pass

    def draw_crosshair(self):
        pass

class Main:
    def __init__(self):
        pass

    def run(self):
        pass


if __name__ == '__main__':
    app = Main()
    app.run()