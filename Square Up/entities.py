# entities.py
import math
import random
import pygame
from config import *
from utils import clamp, check_grid_collision, has_line_of_sight, get_path_bfs, distance


# --- BULLET CLASS ---
class Bullet:
    def __init__(self, wx, wy, vx, vy, speed, damage, pierce_count, color, owner_id):
        self.wx = wx
        self.wy = wy
        l = math.hypot(vx, vy)
        if l == 0: l = 1
        self.vx = (vx / l) * speed
        self.vy = (vy / l) * speed
        self.damage = damage
        self.pierce = pierce_count
        self.lifetime = 3.0
        self.radius = 5
        self.hit_list = []
        self.color = color
        self.owner_id = owner_id

    def update(self, dt):
        self.wx += self.vx * dt
        self.wy += self.vy * dt
        self.lifetime -= dt

    def draw(self, surf, cam):
        sx, sy = cam.world_to_screen(self.wx, self.wy)
        r = self.radius * cam.zoom
        pygame.draw.circle(surf, (255, 200, 50), (sx, sy), r + 2, 1)
        pygame.draw.circle(surf, self.color, (sx, sy), r)


# --- GRENADE CLASS ---
class Grenade:
    def __init__(self, start_x, start_y, target_x, target_y):
        self.x = start_x
        self.y = start_y
        self.z = 15
        max_throw = 6.0
        dist = distance(start_x, start_y, target_x, target_y)
        if dist > max_throw:
            angle = math.atan2(target_y - start_y, target_x - start_x)
            target_x = start_x + math.cos(angle) * max_throw
            target_y = start_y + math.sin(angle) * max_throw
            dist = max_throw
        speed_xy = 8.0
        angle = math.atan2(target_y - start_y, target_x - start_x)
        self.vx = math.cos(angle) * speed_xy
        self.vy = math.sin(angle) * speed_xy
        self.vz = 20 + (dist * 2.0)
        self.timer = 2.0
        self.exploded = False
        self.radius = 4.0

    def update(self, dt, grid):
        if self.exploded: return
        next_x = self.x + self.vx * dt
        next_y = self.y + self.vy * dt
        if check_grid_collision(next_x, self.y, grid):
            self.vx = -self.vx * 0.6
        else:
            self.x = next_x
        if check_grid_collision(self.x, next_y, grid):
            self.vy = -self.vy * 0.6
        else:
            self.y = next_y
        self.z += self.vz * dt
        self.vz -= GRAVITY * 2 * dt
        if self.z < 0:
            self.z = 0
            self.vz = -self.vz * 0.5
            self.vx *= 0.4
            self.vy *= 0.4
            if abs(self.vx) < 0.1: self.vx = 0
            if abs(self.vy) < 0.1: self.vy = 0
        self.timer -= dt
        if self.timer <= 0: self.exploded = True

    def draw(self, surf, cam):
        sx, sy = cam.world_to_screen(self.x, self.y)
        pygame.draw.circle(surf, (0, 0, 0), (sx, sy), 5 * cam.zoom)
        z_offset = self.z * TILE_H_BASE / 2 * cam.zoom
        pygame.draw.circle(surf, COL_GRENADE, (sx, sy - z_offset), 6 * cam.zoom)
        if self.timer < 0.5 and (int(self.timer * 20) % 2 == 0):
            pygame.draw.circle(surf, (255, 255, 255), (sx, sy - z_offset), 6 * cam.zoom)


# --- BASE ENTITY ---
class Entity:
    def __init__(self, wx, wy):
        self.wx = wx
        self.wy = wy
        self.z = 0
        self.radius = 0.4
        self.dead = False
        self.uid = id(self)
        self.knockback_x = 0
        self.knockback_y = 0

    def get_sort_y(self):
        return self.wx + self.wy

    def apply_knockback(self, kx, ky):
        self.knockback_x += kx
        self.knockback_y += ky

    def physics_update(self, dt, grid=None):
        if grid:
            kx_step = self.knockback_x * dt
            ky_step = self.knockback_y * dt
            self.check_wall_collision(kx_step, ky_step, grid)
        else:
            self.wx += self.knockback_x * dt
            self.wy += self.knockback_y * dt

        fric = 5.0
        self.knockback_x -= self.knockback_x * fric * dt
        self.knockback_y -= self.knockback_y * fric * dt
        if abs(self.knockback_x) < 0.1: self.knockback_x = 0
        if abs(self.knockback_y) < 0.1: self.knockback_y = 0

    def check_area_collision(self, min_x, max_x, min_y, max_y, grid):
        start_x = int(math.floor(min_x))
        end_x = int(math.ceil(max_x))
        start_y = int(math.floor(min_y))
        end_y = int(math.ceil(max_y))

        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                if x < 0 or x >= len(grid[0]) or y < 0 or y >= len(grid):
                    return True
                if grid[y][x] == 1:
                    return True
        return False

    def check_wall_collision(self, dx, dy, grid):
        margin = self.radius - 0.05
        if dx != 0:
            original_x = self.wx
            self.wx += dx
            if self.check_area_collision(self.wx - margin, self.wx + margin, self.wy - margin, self.wy + margin, grid):
                self.wx = original_x
                self.knockback_x = 0
        if dy != 0:
            original_y = self.wy
            self.wy += dy
            if self.check_area_collision(self.wx - margin, self.wx + margin, self.wy - margin, self.wy + margin, grid):
                self.wy = original_y
                self.knockback_y = 0
        self.wx = clamp(self.wx, 1.1, MAP_W - 1.1)
        self.wy = clamp(self.wy, 1.1, MAP_H - 1.1)

    def draw_shadow(self, surf, cam):
        sx, sy = cam.world_to_screen(self.wx, self.wy)
        shadow_w = 30 * cam.zoom
        shadow_h = 10 * cam.zoom
        pygame.draw.ellipse(surf, (0, 0, 0, 100), (sx - shadow_w // 2, sy + shadow_h // 2, shadow_w, shadow_h))

    def draw(self, surf, cam):
        pass


# --- ENERGY ORB ---
class EnergyOrb(Entity):
    def __init__(self, wx, wy):
        super().__init__(wx, wy)
        self.radius = 0.3
        self.lifetime = 15.0
        self.bob_offset = random.uniform(0, 6.28)
        self.color = COL_ENERGY

    def update(self, dt):
        self.lifetime -= dt
        self.bob_offset += dt * 5

    def draw(self, surf, cam):
        sx, sy = cam.world_to_screen(self.wx, self.wy)
        bob = math.sin(self.bob_offset) * 5
        for i in range(3):
            alpha = 100 - (i * 30)
            r = (8 + i * 4) * cam.zoom
            s = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*self.color, alpha), (r, r), r)
            surf.blit(s, (sx - r, sy - r - 10 - bob))
        pygame.draw.circle(surf, (255, 255, 255), (sx, sy - 10 - bob), 4 * cam.zoom)


# --- WALL BLOCK ---
class WallBlock(Entity):
    def __init__(self, wx, wy, color_top, color_side):
        super().__init__(wx, wy)
        self.color_top = color_top
        self.color_side = color_side
        self.wx = wx + 0.5
        self.wy = wy + 0.5

    def draw_shadow(self, surf, cam):
        pass

    def draw(self, surf, cam):
        x1, y1 = self.wx - 0.5, self.wy - 0.5
        x2, y2 = self.wx + 0.5, self.wy - 0.5
        x3, y3 = self.wx + 0.5, self.wy + 0.5
        x4, y4 = self.wx - 0.5, self.wy + 0.5

        s1 = cam.world_to_screen(x1, y1)
        s2 = cam.world_to_screen(x2, y2)
        s3 = cam.world_to_screen(x3, y3)
        s4 = cam.world_to_screen(x4, y4)

        wall_h = 30 * cam.zoom

        t1 = (s1[0], s1[1] - wall_h)
        t2 = (s2[0], s2[1] - wall_h)
        t3 = (s3[0], s3[1] - wall_h)
        t4 = (s4[0], s4[1] - wall_h)

        corners = [s1, s2, s3, s4]
        top_corners = [t1, t2, t3, t4]

        lowest_i = 0
        max_y = corners[0][1]
        for i in range(1, 4):
            if corners[i][1] > max_y:
                max_y = corners[i][1]
                lowest_i = i

        prev_i = (lowest_i - 1) % 4
        next_i = (lowest_i + 1) % 4

        poly_side1 = [corners[lowest_i], corners[prev_i], top_corners[prev_i], top_corners[lowest_i]]
        poly_side2 = [corners[lowest_i], corners[next_i], top_corners[next_i], top_corners[lowest_i]]

        pygame.draw.polygon(surf, self.color_side, poly_side1)
        pygame.draw.polygon(surf, self.color_side, poly_side2)
        pygame.draw.polygon(surf, self.color_top, top_corners)
        pygame.draw.polygon(surf, (0, 0, 0), top_corners, 1)


# --- BASE ENEMY ---
class Enemy(Entity):
    def __init__(self, wx, wy, level, vm):
        super().__init__(wx, wy)
        self.vm = vm
        self.level_scaling = level
        self.max_health = 10
        self.health = 10
        self.speed = 2.5 + (level * 0.15)
        self.money_value = 5
        self.color = (200, 50, 50)
        self.damage_to_player = 10
        self.flash_timer = 0.0
        self.debris_type = "blood"
        self.path = []
        self.path_timer = 0.0

    def take_damage(self, amt):
        self.health -= amt
        self.flash_timer = 0.1
        if self.health <= 0:
            self.dead = True
            self.vm.add_debris(self.wx, self.wy, self.debris_type, self.color)

    def update(self, dt, player, grid, bullets, cam):
        self.physics_update(dt, grid)

        if self.flash_timer > 0:
            self.flash_timer -= dt

        if abs(self.knockback_x) + abs(self.knockback_y) < 2.0:
            dist_to_player = distance(self.wx, self.wy, player.wx, player.wy)

            # Simple Line of Sight Check
            can_see = has_line_of_sight(self.wx, self.wy, player.wx, player.wy, grid)

            if can_see:
                self.path = []
                dx = player.wx - self.wx
                dy = player.wy - self.wy
                if dist_to_player > 0.1:
                    self.move_towards(dx, dy, dist_to_player, dt, grid)
            else:
                self.path_timer -= dt
                if self.path_timer <= 0:
                    self.path_timer = 0.2
                    if dist_to_player > 1.0:
                        self.path = get_path_bfs((int(self.wx), int(self.wy)), (int(player.wx), int(player.wy)), grid)
                    else:
                        self.path = []

                target_wx, target_wy = player.wx, player.wy
                if self.path:
                    next_node = self.path[0]
                    tx, ty = next_node[0] + 0.5, next_node[1] + 0.5

                    if distance(self.wx, self.wy, tx, ty) < 0.2:
                        self.path.pop(0)
                    else:
                        target_wx, target_wy = tx, ty

                dx = target_wx - self.wx
                dy = target_wy - self.wy
                dist = math.hypot(dx, dy)
                if dist > 0.1:
                    self.move_towards(dx, dy, dist, dt, grid)

    def move_towards(self, dx, dy, dist, dt, grid):
        move_step = self.speed * dt
        vx = (dx / dist) * move_step
        vy = (dy / dist) * move_step
        self.check_wall_collision(vx, vy, grid)

    def draw(self, surf, cam):
        sx, sy = cam.world_to_screen(self.wx, self.wy)
        col = (255, 255, 255) if self.flash_timer > 0 else self.color
        r = 16 * cam.zoom
        pygame.draw.circle(surf, col, (sx, sy - r), r)
        self.draw_hp(surf, sx, sy - r * 2.5, cam.zoom)

    def draw_hp(self, surf, sx, sy, zoom):
        pct = clamp(self.health / self.max_health, 0, 1)
        w = 30 * zoom
        h = 6 * zoom
        pygame.draw.rect(surf, (0, 0, 0), (sx - w // 2, sy, w, h))
        pygame.draw.rect(surf, (50, 200, 50), (sx - w // 2 + 1, sy + 1, int((w - 2) * pct), h - 2))


# --- ORB ENEMY ---
class OrbEnemy(Enemy):
    def __init__(self, wx, wy, level, vm):
        super().__init__(wx, wy, level, vm)
        self.max_health = 15 + level * 5
        self.health = self.max_health
        self.speed = 2.8 + (level * 0.15)
        self.color = (200, 60, 60)
        self.money_value = 10 + level

    def draw(self, surf, cam):
        sx, sy = cam.world_to_screen(self.wx, self.wy)
        col = (255, 255, 255) if self.flash_timer > 0 else self.color
        r = 18 * cam.zoom
        pygame.draw.circle(surf, col, (sx, sy - r), r)
        pygame.draw.circle(surf, (255, 100, 100), (sx - 5 * cam.zoom, sy - 20 * cam.zoom), 5 * cam.zoom)
        self.draw_hp(surf, sx, sy - r * 2.5, cam.zoom)


# --- BLOCK ENEMY ---
class BlockEnemy(Enemy):
    def __init__(self, wx, wy, level, vm):
        super().__init__(wx, wy, level, vm)
        self.max_health = 40 + level * 10
        self.health = self.max_health
        self.speed = 1.5 + (level * 0.1)
        self.radius = 0.5
        self.color = (60, 100, 200)
        self.money_value = 25 + level * 2
        self.debris_type = "robot_parts"

        # Jump Ability
        self.jump_cooldown = random.uniform(2.0, 4.0)
        self.is_jumping = False
        self.jump_timer = 0.0
        self.jump_duration = 0.6
        self.jump_target = (0, 0)
        self.jump_start = (0, 0)
        self.z = 0

    def update(self, dt, player, grid, bullets, cam):
        self.physics_update(dt, grid)
        if self.flash_timer > 0: self.flash_timer -= dt

        dist_to_player = distance(self.wx, self.wy, player.wx, player.wy)

        if self.is_jumping:
            self.jump_timer += dt
            t = self.jump_timer / self.jump_duration

            self.wx = self.jump_start[0] + (self.jump_target[0] - self.jump_start[0]) * t
            self.wy = self.jump_start[1] + (self.jump_target[1] - self.jump_start[1]) * t
            self.z = 5.0 * math.sin(t * math.pi)

            if t >= 1.0:
                self.is_jumping = False
                self.z = 0
                sx, sy = cam.world_to_screen(self.wx, self.wy)
                self.vm.add_explosion(sx, sy, (100, 150, 255))
                cam.add_shake(15)

                impact_range = 2.5
                if distance(self.wx, self.wy, player.wx, player.wy) < impact_range:
                    player.health -= 15
                    angle = math.atan2(player.wy - self.wy, player.wx - self.wx)
                    player.apply_knockback(math.cos(angle) * 10, math.sin(angle) * 10)
                    self.vm.add_text(sx, sy - 50, "SMASH!", (255, 50, 50), 1.0, 30)

                self.jump_cooldown = random.uniform(3.0, 5.0)

        else:
            self.jump_cooldown -= dt
            if self.jump_cooldown <= 0 and dist_to_player < 7.0 and dist_to_player > 1.5:
                self.is_jumping = True
                self.jump_timer = 0
                self.jump_start = (self.wx, self.wy)
                pred_x = player.wx + player.vx * 0.4
                pred_y = player.wy + player.vy * 0.4
                self.jump_target = (pred_x, pred_y)
            else:
                super().update(dt, player, grid, bullets, cam)

    def draw(self, surf, cam):
        sx, sy = cam.world_to_screen(self.wx, self.wy)
        col = (255, 255, 255) if self.flash_timer > 0 else self.color
        if not self.is_jumping and self.jump_cooldown < 0.5 and int(self.jump_cooldown * 10) % 2 == 0:
            col = (255, 50, 50)
        s = 40 * cam.zoom
        draw_y = sy - (self.z * 15 * cam.zoom)
        rect = pygame.Rect(0, 0, s, s)
        rect.center = (sx, draw_y - s // 2)
        pygame.draw.rect(surf, col, rect)
        pygame.draw.rect(surf, (20, 20, 50), rect, int(2 * cam.zoom))
        self.draw_hp(surf, sx, draw_y - s - 10, cam.zoom)


# --- SPIKE ENEMY (TRIANGLE) - FIX APPLIED HERE ---
class SpikeEnemy(Enemy):
    def __init__(self, wx, wy, level, vm):
        super().__init__(wx, wy, level, vm)
        self.max_health = 8 + level * 3
        self.health = self.max_health
        self.base_speed = 4.0 + (level * 0.2)
        self.speed = self.base_speed
        self.color = (200, 200, 50)
        self.money_value = 15 + level
        self.move_timer = 0
        self.move_dir = (0, 0)

        # Dash Ability
        self.dash_active = False
        self.dash_timer = 0
        self.ghost_timer = 0
        self.dash_cooldown = 2.0

    def update(self, dt, player, grid, bullets, cam):
        # 30% Chance to Dash Logic
        if not self.dash_active:
            self.dash_cooldown -= dt
            if self.dash_cooldown <= 0:
                self.dash_cooldown = random.uniform(2.0, 4.0)
                if random.random() < 0.30:  # 30% Chance
                    self.dash_active = True
                    self.dash_timer = 0.5  # Dash duration
                    self.speed = self.base_speed * 3.5  # Super fast
                    self.damage_to_player = 25  # Deadlier

                    # Aim dash at player
                    dx = player.wx - self.wx
                    dy = player.wy - self.wy
                    ang = math.atan2(dy, dx)
                    self.move_dir = (math.cos(ang), math.sin(ang))
                    self.move_timer = 99  # Lock direction

        if self.dash_active:
            self.dash_timer -= dt
            self.ghost_timer -= dt

            if self.ghost_timer <= 0:
                self.vm.add_ghost(self.wx, self.wy, (255, 255, 100), 0.8)
                self.ghost_timer = 0.05

            # Wind Particles
            sx, sy = cam.world_to_screen(self.wx, self.wy)
            self.vm.add_particle(sx + random.randint(-10, 10), sy + random.randint(-10, 10), (200, 255, 255))

            if self.dash_timer <= 0:
                self.dash_active = False
                self.speed = self.base_speed
                self.damage_to_player = 10
                # FIX: RESET MOVE TIMER SO IT DOESN'T GET STUCK MOVING IN ONE DIRECTION
                self.move_timer = 0

                # Movement
        if self.dash_active:
            # Force movement in dash direction
            vx = self.move_dir[0] * self.speed * dt
            vy = self.move_dir[1] * self.speed * dt
            self.check_wall_collision(vx, vy, grid)
            self.physics_update(dt, grid)
        else:
            # Normal movement
            self.move_towards(0, 0, 0, dt, grid)
            self.physics_update(dt, grid)

    def move_towards(self, dx, dy, dist, dt, grid):
        self.move_timer -= dt
        if self.move_timer <= 0:
            self.move_timer = random.uniform(0.3, 0.8)
            angle = random.uniform(0, 6.28)
            self.move_dir = (math.cos(angle), math.sin(angle))

        vx = self.move_dir[0] * self.speed * dt
        vy = self.move_dir[1] * self.speed * dt
        self.check_wall_collision(vx, vy, grid)

    def draw(self, surf, cam):
        sx, sy = cam.world_to_screen(self.wx, self.wy)
        col = (255, 255, 255) if self.flash_timer > 0 else self.color
        if self.dash_active: col = (255, 255, 200)

        h = 40 * cam.zoom
        w = 15 * cam.zoom
        p1 = (sx, sy - h)
        p2 = (sx - w, sy)
        p3 = (sx + w, sy)
        pygame.draw.polygon(surf, col, [p1, p2, p3])
        self.draw_hp(surf, sx, sy - h - 10, cam.zoom)


# --- BOSS - FIX APPLIED HERE ---
class HexBoss(Enemy):
    def __init__(self, wx, wy, level, vm):
        super().__init__(wx, wy, level, vm)
        self.max_health = 2000 + (level * 500)
        self.health = self.max_health
        self.speed = 1.0 + (level * 0.05)
        self.radius = 0.4
        self.color = (150, 50, 200)
        self.money_value = 1000
        self.damage_to_player = 30
        self.debris_type = "scorch"

        self.shoot_timer = 2.0
        self.burst_count = 0
        self.pattern_timer = 0
        self.current_stage = 1
        self.phase = "IDLE"

    def update(self, dt, player, grid, bullets, cam):
        super().update(dt, player, grid, bullets, cam)

        hp_pct = self.health / self.max_health
        if hp_pct > 0.66:
            self.current_stage = 1
            self.color = (150, 50, 200)
        elif hp_pct > 0.33:
            self.current_stage = 2
            self.color = (200, 50, 50)
        else:
            self.current_stage = 3
            self.color = (50, 0, 0)

        self.shoot_timer -= dt

        # FIX: ONLY PICK NEW PATTERN IF IDLE
        if self.phase == "IDLE" and self.shoot_timer <= 0:
            # Pick a pattern
            if random.random() < 0.6:
                self.phase = "RAPID"
                self.shoot_timer = 0.1
                self.burst_count = 10
            else:
                self.phase = "NOVA"
                self.shoot_timer = 2.0

        if self.phase == "RAPID":
            if self.shoot_timer <= 0:
                self.shoot_timer = 0.15
                self.burst_count -= 1

                dx = player.wx - self.wx
                dy = player.wy - self.wy
                angle = math.atan2(dy, dx) + random.uniform(-0.2, 0.2)
                bx = math.cos(angle)
                by = math.sin(angle)

                b = Bullet(self.wx, self.wy, bx, by, 7.0, 15, 0, (255, 0, 255), self.uid)
                b.radius = 8
                bullets.append(b)

                if self.burst_count <= 0:
                    self.phase = "IDLE"
                    self.shoot_timer = 3.0

        elif self.phase == "NOVA":
            if self.shoot_timer <= 0:
                self.phase = "IDLE"
                self.shoot_timer = 2.5
                for i in range(12):
                    angle = (6.28 / 12) * i
                    bx = math.cos(angle)
                    by = math.sin(angle)
                    b = Bullet(self.wx, self.wy, bx, by, 5.0, 20, 0, (200, 100, 255), self.uid)
                    b.radius = 6
                    bullets.append(b)

    def fire_spread(self, bullets, player, count, spread):
        dx = player.wx - self.wx
        dy = player.wy - self.wy
        base_ang = math.atan2(dy, dx)

        for _ in range(count):
            ang = base_ang + random.uniform(-spread, spread)
            bx = math.cos(ang)
            by = math.sin(ang)
            b = Bullet(self.wx, self.wy, bx, by, 8.0, 15, 0, (255, 50, 255), self.uid)
            bullets.append(b)

    def draw(self, surf, cam):
        sx, sy = cam.world_to_screen(self.wx, self.wy)
        col = (255, 255, 255) if self.flash_timer > 0 else self.color

        if self.phase == "NOVA" and int(pygame.time.get_ticks() / 100) % 2 == 0:
            col = (255, 200, 255)

        pts = []
        radius = 40 * cam.zoom
        spin_speed = 0.1 * self.current_stage

        for i in range(6):
            ang = math.radians(i * 60 + pygame.time.get_ticks() * spin_speed)
            px = sx + math.cos(ang) * radius
            py = (sy - 20 * cam.zoom) + math.sin(ang) * radius * 0.7
            pts.append((px, py))

        pygame.draw.polygon(surf, col, pts)
        pygame.draw.polygon(surf, (255, 255, 255), pts, int(3 * cam.zoom))
        self.draw_hp(surf, sx, sy - 80 * cam.zoom, cam.zoom)


# --- DRONE CLASS ---
class Drone:
    def __init__(self, player, index, total_drones):
        self.player = player
        self.index = index
        self.total = total_drones
        self.angle_offset = (6.28 / total_drones) * index
        self.dist = 1.5
        self.rotation_speed = 2.0
        self.wx = 0
        self.wy = 0
        self.last_shot = 0
        self.fire_rate = 2.0
        self.damage = 5

    def update(self, dt, enemies, bullet_list):
        self.angle_offset += self.rotation_speed * dt
        self.wx = self.player.wx + math.cos(self.angle_offset) * self.dist
        self.wy = self.player.wy + math.sin(self.angle_offset) * self.dist
        self.last_shot += dt
        if self.last_shot >= 1.0 / self.fire_rate:
            closest = None
            min_d = 10.0
            for e in enemies:
                d = distance(self.wx, self.wy, e.wx, e.wy)
                if d < min_d:
                    min_d = d
                    closest = e
            if closest:
                self.last_shot = 0
                dx = closest.wx - self.wx
                dy = closest.wy - self.wy
                b = Bullet(self.wx, self.wy, dx, dy, 10.0, self.damage, 0, (100, 255, 100), self.player.uid)
                bullet_list.append(b)

    def draw(self, surf, cam):
        sx, sy = cam.world_to_screen(self.wx, self.wy)
        bob = math.sin(pygame.time.get_ticks() * 0.005) * 5
        pygame.draw.circle(surf, (100, 255, 100), (sx, sy - 20 - bob), 5 * cam.zoom)
        pygame.draw.line(surf, (50, 150, 50), (sx, sy - 20 - bob), (sx, sy), 1)


# --- PLAYER CLASS ---
class Player(Entity):
    def __init__(self):
        super().__init__(MAP_W / 2, MAP_H / 2)
        self.vx = 0
        self.vy = 0
        self.weapon_type = "pistol"
        self.grenade_count = PLAYER_START_GRENADES
        self.dash_cooldown = 0
        self.is_dashing = False
        self.dash_timer = 0
        self.ghost_spawn_timer = 0
        self.money = 0
        self.energy = 0
        self.max_energy = 100
        self.ultimate_active = False
        self.ultimate_timer = 0.0
        self.ultimate_duration = 5.0
        self.stats = {
            "hp_max": PLAYER_START_HP,
            "hp_regen": 0.0,
            "speed": PLAYER_BASE_SPEED,
            "damage": 10.0,
            "fire_rate": 4.0,
            "bullet_speed": 12.0,
            "spread": 0.05,
            "pierce": 0,
            "dash_duration": 0.25,
            "dash_speed_mult": 3.0
        }
        self.health = self.stats["hp_max"]
        self.last_shot = 0
        self.anim_timer = 0
        self.color_body = (60, 150, 255)
        self.drones = []

    def add_drone(self):
        self.drones.append(Drone(self, len(self.drones), len(self.drones) + 1))
        count = len(self.drones)
        for i, d in enumerate(self.drones):
            d.total = count
            d.index = i
            d.angle_offset = (6.28 / count) * i

    def activate_ultimate(self):
        if self.energy >= self.max_energy:
            self.energy = 0
            self.ultimate_active = True
            self.ultimate_timer = self.ultimate_duration
            return True
        return False

    def update(self, dt, enemies, bullets, grid, vm):
        self.physics_update(dt, grid)
        if self.dash_cooldown > 0: self.dash_cooldown -= dt
        if self.ultimate_active:
            self.ultimate_timer -= dt
            if self.ultimate_timer <= 0: self.ultimate_active = False

        if self.is_dashing:
            self.dash_timer -= dt
            self.ghost_spawn_timer -= dt
            if self.ghost_spawn_timer <= 0:
                vm.add_ghost(self.wx, self.wy, (100, 100, 255), 14)
                self.ghost_spawn_timer = 0.03
            if self.dash_timer <= 0:
                self.is_dashing = False
                self.vx /= self.stats["dash_speed_mult"]
                self.vy /= self.stats["dash_speed_mult"]

        step_x = self.vx * dt
        step_y = self.vy * dt
        self.check_wall_collision(step_x, step_y, grid)
        if self.health < self.stats["hp_max"] and self.stats["hp_regen"] > 0:
            self.health += self.stats["hp_regen"] * dt
            if self.health > self.stats["hp_max"]: self.health = self.stats["hp_max"]

        self.last_shot += dt
        self.anim_timer += dt * 5
        for d in self.drones: d.update(dt, enemies, bullets)

    def attempt_dash(self):
        if self.dash_cooldown <= 0 and not self.is_dashing:
            self.is_dashing = True
            self.dash_timer = self.stats["dash_duration"]
            self.dash_cooldown = 1.2
            self.vx *= self.stats["dash_speed_mult"]
            self.vy *= self.stats["dash_speed_mult"]
            return True
        return False

    def shoot(self, target_wx, target_wy, vm):
        fire_rate = self.stats["fire_rate"]
        cooldown_mod = 1.0
        recoil_force = 0.0
        if self.ultimate_active:
            if self.weapon_type == "pistol":
                fire_rate *= 4.0
                cooldown_mod = 0.2
                recoil_force = 0
            elif self.weapon_type == "shotgun":
                fire_rate *= 2.5
                cooldown_mod = 0.4
                recoil_force = 0
            elif self.weapon_type == "sniper":
                fire_rate *= 2.0
                cooldown_mod = 0.5
                recoil_force = 0
        else:
            if self.weapon_type == "shotgun":
                cooldown_mod = 1.5
                recoil_force = 3.0
            if self.weapon_type == "sniper":
                cooldown_mod = 2.5
                recoil_force = 6.0

        if self.last_shot < (1.0 / fire_rate): return []
        self.last_shot = 0 - (1.0 / fire_rate) * (cooldown_mod - 1.0)
        bullets = []
        dx = target_wx - self.wx
        dy = target_wy - self.wy
        base_angle = math.atan2(dy, dx)
        if recoil_force > 0:
            self.apply_knockback(-math.cos(base_angle) * recoil_force, -math.sin(base_angle) * recoil_force)

        if self.weapon_type == "shotgun":
            pellets = 5
            spread = 0.3
            color = (255, 100, 100)
            if self.ultimate_active:
                pellets = 7
                spread = 0.6
                color = (255, 50, 0)
            for _ in range(pellets):
                angle = base_angle + random.uniform(-spread, spread)
                bx = math.cos(angle)
                by = math.sin(angle)
                spd = self.stats["bullet_speed"] * random.uniform(0.8, 1.1)
                dmg = self.stats["damage"] * 0.6
                b = Bullet(self.wx, self.wy, bx, by, spd, dmg, 0, color, self.uid)
                b.lifetime = 0.6
                bullets.append(b)
        elif self.weapon_type == "sniper":
            bx = math.cos(base_angle)
            by = math.sin(base_angle)
            dmg = self.stats["damage"] * 4.0
            pierce = self.stats["pierce"] + 10
            spd = self.stats["bullet_speed"] * 2.0
            col = (100, 255, 255)
            if self.ultimate_active:
                pierce = 999
                dmg *= 2.0
                spd *= 1.5
                col = (0, 255, 255)
            b = Bullet(self.wx, self.wy, bx, by, spd, dmg, pierce, col, self.uid)
            bullets.append(b)
        else:
            angle = base_angle + random.uniform(-self.stats["spread"], self.stats["spread"])
            if self.ultimate_active: angle = random.uniform(0, 6.28)
            bx = math.cos(angle)
            by = math.sin(angle)
            b = Bullet(self.wx, self.wy, bx, by, self.stats["bullet_speed"], self.stats["damage"],
                       int(self.stats["pierce"]), (255, 255, 150), self.uid)
            bullets.append(b)
        return bullets

    def draw(self, surf, cam):
        sx, sy = cam.world_to_screen(self.wx, self.wy)
        bob = math.sin(self.anim_timer) * 3
        center_y = sy - (15 * cam.zoom) + bob
        col = self.color_body
        if self.ultimate_active:
            col = (0, 255, 255)
            pygame.draw.circle(surf, (0, 255, 255), (sx, center_y), 18 * cam.zoom, 2)
        if self.is_dashing: col = (200, 200, 255)
        pygame.draw.circle(surf, col, (sx, center_y), 14 * cam.zoom)
        if self.weapon_type == "shotgun":
            pygame.draw.circle(surf, (255, 50, 50), (sx + 10 * cam.zoom, center_y), 5 * cam.zoom)
        elif self.weapon_type == "sniper":
            pygame.draw.line(surf, (50, 255, 50), (sx, center_y), (sx + 15 * cam.zoom, center_y), int(3 * cam.zoom))
        pygame.draw.circle(surf, (150, 200, 255), (sx - 4 * cam.zoom, center_y - 4 * cam.zoom), 5 * cam.zoom)
        for d in self.drones: d.draw(surf, cam)
        w = 40 * cam.zoom
        h = 6 * cam.zoom
        bar_x = sx - w // 2
        bar_y = sy - 40 * cam.zoom
        pygame.draw.rect(surf, (20, 20, 20), (bar_x, bar_y, w, h))
        pct = clamp(self.health / self.stats["hp_max"], 0, 1)
        pygame.draw.rect(surf, (50, 255, 50), (bar_x + 1, bar_y + 1, int((w - 2) * pct), h - 2))