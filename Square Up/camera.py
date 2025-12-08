# camera.py
import random
from config import *

class Camera:
    def __init__(self, width, height):
        self.w = width
        self.h = height

        # Focus Point (World Coordinates)
        self.focus_wx = 0.0
        self.focus_wy = 0.0
        self.target_wx = 0.0
        self.target_wy = 0.0

        self.zoom = 1.0
        self.target_zoom = 1.0

        self.shake_timer = 0.0
        self.shake_mag = 0.0
        self.shake_offset_x = 0
        self.shake_offset_y = 0

    def add_shake(self, amount):
        self.shake_mag = min(self.shake_mag + amount, 30.0)
        self.shake_timer = 0.3

    def zoom_in(self):
        self.target_zoom = min(self.target_zoom + 0.1, ZOOM_MAX)

    def zoom_out(self):
        self.target_zoom = max(self.target_zoom - 0.1, ZOOM_MIN)

    def set_target(self, wx, wy):
        self.target_wx = wx
        self.target_wy = wy

    def update(self, dt):
        # Smoothly interpolate Focus Point and Zoom
        speed = 5.0
        self.focus_wx += (self.target_wx - self.focus_wx) * speed * dt
        self.focus_wy += (self.target_wy - self.focus_wy) * speed * dt
        self.zoom += (self.target_zoom - self.zoom) * speed * dt

        # Handle Shake
        if self.shake_timer > 0:
            self.shake_timer -= dt
            self.shake_offset_x = random.uniform(-self.shake_mag, self.shake_mag)
            self.shake_offset_y = random.uniform(-self.shake_mag, self.shake_mag)
            self.shake_mag = max(0, self.shake_mag - 60 * dt)
        else:
            self.shake_offset_x = 0
            self.shake_offset_y = 0

    def world_to_screen(self, wx, wy):
        tile_w = TILE_W_BASE * self.zoom
        tile_h = TILE_H_BASE * self.zoom

        # Project World Point
        iso_x = (wx - wy) * (tile_w / 2.0)
        iso_y = (wx + wy) * (tile_h / 2.0)

        # Project Camera Focus
        cam_iso_x = (self.focus_wx - self.focus_wy) * (tile_w / 2.0)
        cam_iso_y = (self.focus_wx + self.focus_wy) * (tile_h / 2.0)

        # Center Offset
        offset_x = (self.w / 2.0) - cam_iso_x
        offset_y = (self.h / 2.0) - cam_iso_y

        final_sx = iso_x + offset_x + self.shake_offset_x
        final_sy = iso_y + offset_y + self.shake_offset_y

        return final_sx, final_sy

    def screen_to_world(self, sx, sy):
        tile_w = TILE_W_BASE * self.zoom
        tile_h = TILE_H_BASE * self.zoom

        cam_iso_x = (self.focus_wx - self.focus_wy) * (tile_w / 2.0)
        cam_iso_y = (self.focus_wx + self.focus_wy) * (tile_h / 2.0)

        offset_x = (self.w / 2.0) - cam_iso_x + self.shake_offset_x
        offset_y = (self.h / 2.0) - cam_iso_y + self.shake_offset_y

        adj_x = sx - offset_x
        adj_y = sy - offset_y

        wx = (adj_x / (tile_w / 2.0) + adj_y / (tile_h / 2.0)) / 2.0
        wy = (adj_y / (tile_h / 2.0) - (adj_x / (tile_w / 2.0))) / 2.0
        return wx, wy