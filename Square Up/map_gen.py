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

    for y in range(h):
        for x in range(w):
            sx, sy = cam.world_to_screen(x, y)
            if sx < -tile_w or sx > SCREEN_W + tile_w or sy < -tile_h or sy > SCREEN_H + tile_h: continue

            p_top = [
                (sx, sy),
                (sx + tile_w//2, sy + tile_h//2),
                (sx, sy + tile_h),
                (sx - tile_w//2, sy + tile_h//2)
            ]
            pygame.draw.polygon(surf, col_floor, p_top)
            pygame.draw.polygon(surf, col_line, p_top, 1)