# map_gen.py
import random
import pygame
from config import *
from entities import WallBlock

def generate_map(w, h, seed):
    random.seed(seed)
    grid = [[0 for _ in range(w)] for __ in range(h)]
    for y in range(h):
        for x in range(w):
            if random.random() < 0.1:
                grid[y][x] = 1
            else:
                grid[y][x] = 0
    cx, cy = w//2, h//2
    for y in range(cy-2, cy+3):
        for x in range(cx-2, cx+3):
            grid[y][x] = 0
    random.seed()
    return grid

def create_wall_entities(grid, level):
    walls = []
    hue_shift = (level * 35) % 360
    base_col = pygame.Color(0)
    base_col.hsla = (hue_shift, 40, 40, 100)
    col_top = (min(255, base_col.r + 50), min(255, base_col.g + 50), min(255, base_col.b + 50))
    col_side = (base_col.r, base_col.g, base_col.b)

    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == 1:
                walls.append(WallBlock(x, y, col_top, col_side))
    return walls

def draw_floor_grid(surf, cam, w, h, level):
    hue_shift = (level * 35) % 360
    base_col = pygame.Color(0)
    base_col.hsla = (hue_shift, 40, 20, 100) # Dark floor
    col_floor = (base_col.r, base_col.g, base_col.b)
    col_line = (max(0, base_col.r-20), max(0, base_col.g-20), max(0, base_col.b-20))

    tile_w = TILE_W_BASE * cam.zoom
    tile_h = TILE_H_BASE * cam.zoom

    # Helper to project a point
    def proj(wx, wy):
        return cam.world_to_screen(wx, wy)

    for y in range(h):
        for x in range(w):
            # Optimization: Rough check if tile is on screen
            sx, sy = proj(x + 0.5, y + 0.5)
            if sx < -100 or sx > SCREEN_W + 100 or sy < -100 or sy > SCREEN_H + 100:
                continue

            # Calculate the 4 true corners of the floor tile
            # This ensures the floor matches the walls even when rotated
            p1 = proj(x, y)
            p2 = proj(x + 1, y)
            p3 = proj(x + 1, y + 1)
            p4 = proj(x, y + 1)

            poly = [p1, p2, p3, p4]

            pygame.draw.polygon(surf, col_floor, poly)
            pygame.draw.polygon(surf, col_line, poly, 1)