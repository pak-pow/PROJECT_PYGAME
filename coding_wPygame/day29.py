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
        pass

    def get_shoot_direction(self):
        pass

    def update(self):
        pass

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