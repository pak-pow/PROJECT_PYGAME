Tags: [[Programming]], [[Python]], [[PyGame]], [[Game]], [[OpenGL]]

----
### 1) Learning Goal

You will architect a complete **3D First-Person Shooter** loop. This involves managing a **First Person Controller** (Mouse Look + WASD Physics), an **Entity Manager** for enemies and projectiles, and a **Hybrid Rendering System** (3D World + 2D Crosshair).

### 2) Clear Overview

* **The Player:** A physics-based camera. You accelerate with WASD and look with the Mouse.
* **The Enemies:** Red cubes that spawn **in front of you** (in your vision cone) and chase you.
* **The Mechanics:**
* **Shooting:** Left Click spawns a bullet traveling along your view vector.
* **UI:** A green crosshair drawn using "Orthographic" (2D) projection on top of the 3D world.
* **Game Loop:** Spawn -> Update Physics -> Check Collisions -> Render.



### 3) Deep Explanation

**A. The First Person Controller**
We don't just teleport the camera. We apply **Force** to **Velocity**.

* `Velocity += Input * Acceleration`
* `Velocity *= Friction` (This creates the smooth "slide" stop).
* **Mouse Look:** We map X-movement to `Yaw` (Horizontal) and Y-movement to `Pitch` (Vertical).

**B. 3D Projectiles (Vectors)**
To shoot where you look, we convert Spherical Coordinates (Pitch/Yaw) into a Cartesian Vector (X, Y, Z).


**C. Hybrid Rendering (The Crosshair)**
OpenGL usually renders in 3D perspective (things get smaller when far away). To draw a UI (Crosshair), we must:

1. Save the 3D Lens (`glPushMatrix`).
2. Switch to **2D Orthographic Mode** (`gluOrtho2D`).
3. Draw the lines.
4. Restore the 3D Lens (`glPopMatrix`).

### 4) Runnable Pygame Code Example

**Controls:**

* **Mouse:** Look Aim.
* **WASD:** Move / Strafe.
* **Left Click:** Shoot.
* **ESC:** Unlock Mouse.

``` python

import pygame
import math
import random
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# ============ CONFIGURATION CONSTANTS ============
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
DISPLAY_DIMENSIONS = (WINDOW_WIDTH, WINDOW_HEIGHT)

# Input Settings
MOUSE_LOOK_SENSITIVITY = 0.2

# Physics Settings
PLAYER_ACCELERATION = 0.15      # How fast speed increases
GROUND_FRICTION = 0.90          # How fast you slow down (0.0-1.0)
GRAVITY_FORCE = 0.02            # Downward pull per frame
JUMP_STRENGTH = 0.5             # Initial upward velocity
AIR_RESISTANCE = 0.98           # Friction while jumping

# Gameplay Settings
PROJECTILE_SPEED = 3.0
FRAMES_BETWEEN_ENEMY_SPAWNS = 60

# ============ ENGINE SETUP ============
pygame.init()
pygame.display.set_mode(DISPLAY_DIMENSIONS, DOUBLEBUF | OPENGL)
pygame.display.set_caption("Day 29: Final FPS Build | WASD: Move | Click: Shoot")
game_clock = pygame.time.Clock()

# Configure 3D Camera Lens (Projection Matrix)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(45, (WINDOW_WIDTH / WINDOW_HEIGHT), 0.1, 500.0)

# Configure 3D World (Model View Matrix)
glMatrixMode(GL_MODELVIEW)
glEnable(GL_DEPTH_TEST) # Ensure objects block each other properly

# Input Capture
pygame.event.set_grab(True)
pygame.mouse.set_visible(False)


# ============ GAME CLASSES ============

class FirstPersonController:
    def __init__(self):
        # Position in 3D Space [x, y, z]
        self.position = [0.0, 5.0, 0.0] 
        # Motion Vector [x, y, z]
        self.velocity = [0.0, 0.0, 0.0]
        
        # View Angles (Degrees)
        self.look_angle_horizontal = 0.0   # Yaw (Left/Right)
        self.look_angle_vertical = 0.0     # Pitch (Up/Down)
        
        self.is_touching_ground = False
        self.player_height = 2.0 

    def process_input_and_physics(self, pressed_keys, mouse_movement_delta):
        """
        Updates camera angles based on mouse, and applies physics forces
        based on keyboard input (WASD).
        """
        # 1. UPDATE CAMERA ANGLES
        mouse_dx, mouse_dy = mouse_movement_delta
        self.look_angle_horizontal += mouse_dx * MOUSE_LOOK_SENSITIVITY
        self.look_angle_vertical += mouse_dy * MOUSE_LOOK_SENSITIVITY
        
        # Clamp vertical look to prevent neck breaking (90 degrees up/down)
        self.look_angle_vertical = max(-89, min(89, self.look_angle_vertical))

        # 2. CALCULATE MOVEMENT DIRECTION
        # We need to move relative to where the player is looking (Yaw)
        yaw_in_radians = math.radians(self.look_angle_horizontal)
        sin_yaw = math.sin(yaw_in_radians)
        cos_yaw = math.cos(yaw_in_radians)
        
        # Calculate Input Force (WASD)
        input_force_x = 0
        input_force_z = 0
        
        if pressed_keys[K_w]: # Forward
            input_force_x += sin_yaw * PLAYER_ACCELERATION
            input_force_z -= cos_yaw * PLAYER_ACCELERATION
        if pressed_keys[K_s]: # Backward
            input_force_x -= sin_yaw * PLAYER_ACCELERATION
            input_force_z += cos_yaw * PLAYER_ACCELERATION
        if pressed_keys[K_a]: # Strafe Left
            input_force_x -= cos_yaw * PLAYER_ACCELERATION
            input_force_z -= sin_yaw * PLAYER_ACCELERATION
        if pressed_keys[K_d]: # Strafe Right
            input_force_x += cos_yaw * PLAYER_ACCELERATION
            input_force_z += sin_yaw * PLAYER_ACCELERATION

        # Apply Input Force to Current Velocity
        self.velocity[0] += input_force_x
        self.velocity[2] += input_force_z

        # 3. HANDLE JUMPING
        if pressed_keys[K_SPACE] and self.is_touching_ground:
            self.velocity[1] = JUMP_STRENGTH
            self.is_touching_ground = False

        # 4. APPLY GRAVITY
        self.velocity[1] -= GRAVITY_FORCE
        
        # 5. APPLY FRICTION (Slow down over time)
        self.velocity[0] *= GROUND_FRICTION
        self.velocity[2] *= GROUND_FRICTION
        
        # Apply extra drag if in the air
        if not self.is_touching_ground:
            self.velocity[0] *= AIR_RESISTANCE
            self.velocity[2] *= AIR_RESISTANCE

        # 6. UPDATE POSITION (Pos += Vel)
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        self.position[2] += self.velocity[2]

        # 7. HANDLE FLOOR COLLISION
        floor_level_y = -5.0
        # If feet go below floor
        if self.position[1] < floor_level_y + self.player_height:
            self.position[1] = floor_level_y + self.player_height # Snap to floor
            self.velocity[1] = 0 # Stop falling
            self.is_touching_ground = True
        else:
            self.is_touching_ground = False

    def calculate_projectile_velocity(self):
        """
        Calculates a 3D vector representing the direction the player is currently facing.
        Used to determine where bullets should fly.
        """
        yaw_rad = math.radians(self.look_angle_horizontal)
        pitch_rad = math.radians(self.look_angle_vertical)
        
        # Convert spherical coordinates (Angles) to Cartesian coordinates (XYZ Vector)
        direction_x = math.sin(yaw_rad) * math.cos(pitch_rad)
        direction_y = -math.sin(pitch_rad)
        direction_z = -math.cos(yaw_rad) * math.cos(pitch_rad)
        
        return direction_x, direction_y, direction_z


# ============ RENDERING FUNCTIONS ============
CUBE_VERTICES = (
    (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1),
    (1, -1, 1), (1, 1, 1), (-1, -1, 1), (-1, 1, 1)
)
CUBE_EDGES = (
    (0,1), (0,3), (0,4), (2,1), (2,3), (2,7), 
    (6,3), (6,4), (6,7), (5,1), (5,4), (5,7)
)

def render_3d_cube_wireframe(color_rgb):
    """Draws a simple wireframe cube at the current GL position."""
    glBegin(GL_LINES)
    glColor3fv(color_rgb)
    for edge in CUBE_EDGES:
        for vertex_index in edge:
            glVertex3fv(CUBE_VERTICES[vertex_index])
    glEnd()

def render_infinite_grid_floor():
    """Draws a large grid to represent the ground."""
    glBegin(GL_LINES)
    glColor3f(0.2, 0.2, 0.2) # Dark Grey
    floor_y = -5
    grid_size = 100
    grid_spacing = 10
    
    for i in range(-grid_size, grid_size + 1, grid_spacing):
        glVertex3f(i, floor_y, -grid_size)
        glVertex3f(i, floor_y, grid_size)
        glVertex3f(-grid_size, floor_y, i)
        glVertex3f(grid_size, floor_y, i)
    glEnd()

def render_hud_crosshair():
    """
    Switches to 2D Orthographic mode to draw a crosshair 
    on top of the 3D scene.
    """
    glMatrixMode(GL_PROJECTION)
    glPushMatrix() # Save 3D Lens
    glLoadIdentity()
    gluOrtho2D(0, WINDOW_WIDTH, WINDOW_HEIGHT, 0)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix() # Save 3D World Position
    glLoadIdentity()
    
    center_x = WINDOW_WIDTH // 2
    center_y = WINDOW_HEIGHT // 2
    crosshair_size = 15
    
    glDisable(GL_DEPTH_TEST) # Ignore depth so it draws ON TOP
    glLineWidth(2.0)
    
    glBegin(GL_LINES)
    glColor3f(0, 1, 0) # Green
    glVertex2f(center_x - crosshair_size, center_y)
    glVertex2f(center_x + crosshair_size, center_y)
    glVertex2f(center_x, center_y - crosshair_size)
    glVertex2f(center_x, center_y + crosshair_size)
    glEnd()
    
    glLineWidth(1.0)
    glEnable(GL_DEPTH_TEST)
    
    glMatrixMode(GL_PROJECTION)
    glPopMatrix() # Restore 3D Lens
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix() # Restore 3D World


# ============ MAIN GAME LOOP ============

player = FirstPersonController()
active_bullets = [] 
active_enemies = [] 

enemy_spawn_timer = 0
player_score = 0
is_game_over = False
is_running = True

while is_running:
    delta_time = game_clock.tick(60)

    # 1. EVENT LISTENER
    for event in pygame.event.get():
        if event.type == QUIT:
            is_running = False
        
        if event.type == KEYDOWN:
            # Toggle Mouse Lock with ESC
            if event.key == K_ESCAPE:
                current_grab = pygame.event.get_grab()
                pygame.event.set_grab(not current_grab)
                pygame.mouse.set_visible(current_grab)
            
            # Restart Game
            if event.key == K_r and is_game_over:
                is_game_over = False
                active_enemies = []
                active_bullets = []
                player.position = [0, 5, 0]
                player.velocity = [0, 0, 0]
                player_score = 0

        # Shooting Input
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1 and not is_game_over: # Left Click
                # Get shooting direction
                dir_x, dir_y, dir_z = player.calculate_projectile_velocity()
                
                # Add bullet to list
                active_bullets.append([
                    player.position[0], player.position[1], player.position[2], # Position
                    dir_x * PROJECTILE_SPEED, dir_y * PROJECTILE_SPEED, dir_z * PROJECTILE_SPEED # Velocity
                ])

    if not is_game_over:
        # 2. GAME LOGIC UPDATE
        keys = pygame.key.get_pressed()
        
        # Only move camera if mouse is locked/grabbed
        if pygame.event.get_grab():
            mouse_delta = pygame.mouse.get_rel()
            player.process_input_and_physics(keys, mouse_delta)
        else:
            player.process_input_and_physics(keys, (0,0))

        # --- SPAWN ENEMIES (FRONT CONE) ---
        enemy_spawn_timer += 1
        if enemy_spawn_timer > FRAMES_BETWEEN_ENEMY_SPAWNS:
            enemy_spawn_timer = 0
            
            # 1. Pick angle relative to player look (-60 to +60 degrees)
            spawn_angle_offset = random.uniform(-60, 60)
            final_spawn_angle = player.look_angle_horizontal + spawn_angle_offset
            
            spawn_rad = math.radians(final_spawn_angle)
            spawn_distance = 40
            
            # 2. Calculate pos using sin / -cos (Matches Player Forward)
            enemy_x = player.position[0] + math.sin(spawn_rad) * spawn_distance
            enemy_z = player.position[2] - math.cos(spawn_rad) * spawn_distance
            enemy_y = -4 # Spawn just above floor
            
            active_enemies.append([enemy_x, enemy_y, enemy_z])

        # --- UPDATE BULLETS ---
        for bullet in active_bullets[:]:
            bullet[0] += bullet[3]
            bullet[1] += bullet[4]
            bullet[2] += bullet[5]
            
            distance_from_player = math.sqrt((bullet[0]-player.position[0])**2 + (bullet[2]-player.position[2])**2)
            
            # Remove if hitting floor OR flying too far (Increased range to 400)
            if bullet[1] < -5 or distance_from_player > 400:
                active_bullets.remove(bullet)

        # --- UPDATE ENEMIES & COLLISIONS ---
        for enemy in active_enemies[:]:
            # Simple AI: Move toward player
            diff_x = player.position[0] - enemy[0]
            diff_y = player.position[1] - enemy[1]
            diff_z = player.position[2] - enemy[2]
            
            distance_to_player = math.sqrt(diff_x**2 + diff_y**2 + diff_z**2)
            
            if distance_to_player > 0:
                enemy_speed = 0.1
                enemy[0] += (diff_x / distance_to_player) * enemy_speed
                enemy[1] += (diff_y / distance_to_player) * enemy_speed
                enemy[2] += (diff_z / distance_to_player) * enemy_speed
            
            # CHECK LOSS: Enemy touched player
            if distance_to_player < 1.0:
                is_game_over = True
                print("GAME OVER")

            # CHECK KILL: Bullet touched Enemy
            for bullet in active_bullets[:]:
                b_diff_x = bullet[0] - enemy[0]
                b_diff_y = bullet[1] - enemy[1]
                b_diff_z = bullet[2] - enemy[2]
                
                bullet_to_enemy_dist = math.sqrt(b_diff_x**2 + b_diff_y**2 + b_diff_z**2)
                
                # Hit radius (Increased to 3.5 for easier aiming)
                if bullet_to_enemy_dist < 3.5: 
                    if enemy in active_enemies: active_enemies.remove(enemy)
                    if bullet in active_bullets: active_bullets.remove(bullet)
                    player_score += 100
                    print(f"Score: {player_score}")
                    break

    # 3. RENDER SCENE
    if is_game_over: 
        glClearColor(0.2, 0, 0, 1) # Red background
    else: 
        glClearColor(0, 0, 0, 1) # Black background
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Move World relative to Camera (Inverse Transformation)
    glRotatef(player.look_angle_vertical, 1, 0, 0)   # Tilt Up/Down (Pitch)
    glRotatef(player.look_angle_horizontal, 0, 1, 0) # Turn Left/Right (Yaw)
    glTranslatef(-player.position[0], -player.position[1], -player.position[2]) # Move World Back

    render_infinite_grid_floor()

    # Draw Bullets (Yellow)
    for b in active_bullets:
        glPushMatrix()
        glTranslatef(b[0], b[1], b[2])
        glScalef(0.1, 0.1, 0.1) 
        render_3d_cube_wireframe((1, 1, 0))
        glPopMatrix()

    # Draw Enemies (Red)
    for e in active_enemies:
        glPushMatrix()
        glTranslatef(e[0], e[1], e[2])
        
        # Look-At Logic: Rotate enemy to face player
        diff_x = player.position[0] - e[0]
        diff_z = player.position[2] - e[2]
        angle_to_player = math.degrees(math.atan2(diff_x, diff_z))
        
        glRotatef(angle_to_player, 0, 1, 0)
        render_3d_cube_wireframe((1, 0, 0))
        glPopMatrix()
    
    # Draw UI (Last)
    render_hud_crosshair()

    pygame.display.flip()

pygame.quit()

```

### 5) 20-Minute Drill

**Task: Sprint Mechanic**

1. Inside `FirstPersonController`, add `self.is_sprinting = False`.
2. In `process_input`, check if `K_LSHIFT` is pressed.
* If `True`: Multiply `PLAYER_ACCELERATION` by 2.0.
* If `False`: Use normal acceleration.


3. **Visual Polish:** When sprinting, slightly increase FOV (`gluPerspective(50, ...)`) for a "speed effect."

### 6) Quick Quiz

1. **Why do we disable `GL_DEPTH_TEST` before drawing the crosshair?**
2. **What does `math.radians()` do, and why do we need it for `math.sin`?**
3. **Why do we use `glPushMatrix()` before drawing an enemy?**

**Answers:**

1. To ensure the crosshair is drawn **on top** of everything else, ignoring distance.
2. Converts Degrees (0-360) to Radians (0-2π). Python's math functions expect Radians.
3. To save the world's position before we translate/rotate for that specific enemy.

### 7) Homework for Tomorrow

**Day 30: The Conclusion.**

* Playtest your game for 10 minutes.
* Write down 3 things you would add if you had another month (e.g., Sound, textures, menus).
* Prepare to archive your project!

### 8) Progress to Mastery

🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩⬜ **97%**

### 9) Obsidian Note

## 🧠 CONCEPT SUMMARY

#### First Person Controller
A specialized camera class that tracks `position`, `velocity`, and `look_angles`.
* **Look:** Uses `pygame.mouse.get_rel()` to change Pitch/Yaw.
* **Move:** Uses `sin(yaw)` and `cos(yaw)` to move relative to the view.

#### Orthographic UI (HUD)
To draw 2D elements (Crosshair, Health) over a 3D world:
1.  Switch Matrix Mode to `GL_PROJECTION`.
2.  Use `gluOrtho2D(0, width, height, 0)`.
3.  Disable `GL_DEPTH_TEST`.
4.  Draw lines/rects.
5.  Restore Perspective Mode.

#### Clean Code Practices
* **Variables:** Use `velocity_x` instead of `vx`.
* **Classes:** encapsulate logic (`controller.update()`) so the Main Loop stays clean.
* **Constants:** Put numbers like `0.2` (Sensitivity) at the top of the file as `MOUSE_SENSITIVITY`.

---

## 🛠️ WHAT I DID TODAY
* **Refactored Code:** Renamed variables to be self-explanatory.
* **Integrated Systems:** Combined Physics (Gravity/Friction) with Space Shooter logic.
* **Polished Mechanics:** Added Crosshair, Front-Cone Spawning, and Long-Range bullets.

---

## 💻 SOURCE CODE
> [!example]- CROSSHAIR LOGIC
> ```python
> glDisable(GL_DEPTH_TEST)
> glMatrixMode(GL_PROJECTION)
> gluOrtho2D(0, W, H, 0)
> # Draw Lines...
> glEnable(GL_DEPTH_TEST)
> ```

---

## 🎯 GOALS FOR TOMORROW
> [!todo] 🎓 **Day 30: The Conclusion**
> * **Post-Mortem:** Analyzing what went well and what failed.
> * **Portfolio Prep:** How to package this code to show employers or friends.
> * **The Path Forward:** Where to go next? (Unity, Godot, Unreal, or Advanced Python).

