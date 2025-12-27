Tags: [[Programming]], [[Python]], [[PyGame]], [[Game]], [[OpenGL]]

---
### 1) Learning Goal

You will learn to **Externalize Variables** (move "Magic Numbers" out of your code) so you can tweak game feel in real-time, and learn how to prevent **Clipping** (seeing inside objects) and **Tunneling** (moving through walls).

### 2) Clear Overview

* **Magic Numbers:** Hard-coding `speed = 0.5` is bad. If you want to change it later, you have to find it in 50 different places.
* **The Solution:** A `Config` class or dictionary at the top of your script.
* **The Bug (Clipping):** In 3D, if you get too close to an object (closer than the "Near Plane" of your camera lens), it slices open. We fix this with collision buffers.
* **The Bug (Tunneling):** If you move 10 units per frame, but a wall is only 1 unit thick, you will teleport to the other side without touching it.

### 3) Deep Explanation

**A. The "Tweakables" Pattern**
Instead of scattering numbers, we group them.

```python
class Settings:
    MOVE_SPEED = 5.0
    TURN_SPEED = 90.0
    FOV = 45

```

Now you can change `Settings.FOV` in one place, and the whole game updates.

**B. Real-Time Balancing**
Great developers don't restart the game to change speed. They add **Hotkeys**.

* `[+]` / `[-]`: Increase/Decrease Speed.
* `[F1]`: Toggle Debug View.
This allows you to "find the fun" by playing and tweaking simultaneously.

**C. Near-Plane Clipping**
Your `gluPerspective` has a `near` value (usually 0.1). If your camera position is inside a cube, the math breaks.

* **Fix:** Stop the player *before* `distance < 0.1`. Keep a "Personal Bubble" radius (e.g., 0.5 units).

### 4) Runnable Pygame Code Example

**Controls:**

* **WASD:** Move.
* **UP/DOWN (Arrow Keys):** Change **FOV** (Field of View) dynamically.
* **LEFT/RIGHT (Arrow Keys):** Change **Movement Speed**.
* **Check the Window Title:** See your current values in real-time.

```python
import pygame, math
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# 1. THE CONFIG CLASS (Tweakables)
class Config:
    fov = 45.0
    move_speed = 5.0
    mouse_sens = 2.0
    
    # Constraints
    min_fov = 10.0
    max_fov = 120.0
    min_speed = 1.0
    max_speed = 20.0

# Setup
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
clock = pygame.time.Clock()

# --- HELPER: Update Lens ---
def update_projection():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Use Config.fov here!
    gluPerspective(Config.fov, (display[0]/display[1]), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

# Initial Setup
update_projection()

# State
cam_x, cam_y, cam_z = 0, 0, -5
cam_yaw = 0

# Cube Data
vertices = (
    (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1),
    (1, -1, 1), (1, 1, 1), (-1, -1, 1), (-1, 1, 1)
)
edges = ((0,1),(0,3),(0,4),(2,1),(2,3),(2,7),(6,3),(6,4),(6,7),(5,1),(5,4),(5,7))

def draw_grid():
    # Draw a reference floor
    glBegin(GL_LINES)
    glColor3f(0.3, 0.3, 0.3)
    for i in range(-10, 11):
        glVertex3f(i, -1, -10)
        glVertex3f(i, -1, 10)
        glVertex3f(-10, -1, i)
        glVertex3f(10, -1, i)
    glEnd()

def draw_cube():
    glBegin(GL_LINES)
    glColor3f(1, 1, 0) # Yellow
    for edge in edges:
        for v in edge:
            glVertex3fv(vertices[v])
    glEnd()

while True:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
            
    # --- REAL-TIME BALANCING INPUTS ---
    keys = pygame.key.get_pressed()
    
    # Adjust FOV (The "Zoom" Effect)
    if keys[K_UP]:
        Config.fov += 20 * dt
        if Config.fov > Config.max_fov: Config.fov = Config.max_fov
        update_projection() # Apply change immediately
        
    if keys[K_DOWN]:
        Config.fov -= 20 * dt
        if Config.fov < Config.min_fov: Config.fov = Config.min_fov
        update_projection()

    # Adjust Speed
    if keys[K_RIGHT]:
        Config.move_speed += 5 * dt
    if keys[K_LEFT]:
        Config.move_speed -= 5 * dt
        if Config.move_speed < Config.min_speed: Config.move_speed = Config.min_speed

    # --- STANDARD MOVEMENT ---
    if keys[K_q]: cam_yaw -= 90 * dt
    if keys[K_e]: cam_yaw += 90 * dt
    
    rad = math.radians(cam_yaw)
    if keys[K_w]:
        cam_x += math.sin(rad) * Config.move_speed * dt
        cam_z -= math.cos(rad) * Config.move_speed * dt
    if keys[K_s]:
        cam_x -= math.sin(rad) * Config.move_speed * dt
        cam_z += math.cos(rad) * Config.move_speed * dt

    # --- DEBUG UI (Window Title) ---
    caption = f"FOV: {int(Config.fov)} | Speed: {Config.move_speed:.1f} | FPS: {int(clock.get_fps())}"
    pygame.display.set_caption(caption)

    # --- RENDER ---
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    # Camera
    glRotatef(-cam_yaw, 0, 1, 0)
    glTranslatef(-cam_x, -cam_y, -cam_z)
    
    draw_grid()
    draw_cube() # Drawn at 0,0,0

    pygame.display.flip()

```

### 5) 20-Minute Drill

**Task: Fix the Clipping Bug.**

Currently, if you walk INTO the yellow cube, the lines disappear weirdly (Clipping).

1. **Add Logic:** In the movement section (`if keys[K_w]`), calculate the *future* position before moving.
2. **Distance Check:** Calculate `dist_to_center = math.sqrt(future_x**2 + future_z**2)`.
3. **The Clamp:** If `dist_to_center < 1.5` (Cube radius + Personal Bubble), **don't apply the movement**.
4. **Result:** You will act like a solid object that collides with the cube instead of walking through it.

### 6) Quick Quiz

1. **Why is `FOV: 120` generally bad for a standard monitor?**
2. **What is the "Magic Number" anti-pattern?**
3. **If my player moves 100 units per frame, and a wall is at unit 50, what happens?**

**Answers:**

1. It creates a "Fisheye" distortion effect that makes objects in the center look tiny and objects on the edges look stretched.
2. Using raw numbers (e.g., `x += 5`) directly in logic code instead of named constants (`x += SPEED`).
3. **Tunneling.** The player teleports from 0 to 100, completely skipping the check at 50.

### 7) Homework for Tomorrow

**Prepare for the Final Project.**

* Day 29 and 30 are dedicated to your **Capstone**.
* **The Prompt:** "Space Station Dogfight."
* **Your Task:** Write down the Asset List.
* What 3D shapes do you need? (Cube for station, small cubes for ships).
* What Controls? (Flight controls).
* What Logic? (Enemies that look-at you and move).



### 8) Progress to Mastery

🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩⬜ **93%**

### 9) Obsidian Note
## 🧠 CONCEPT SUMMARY

#### Tweakables (Externalizing Constants)
Never bury numbers deep in your code.
* **Bad:** `player.x += 5`
* **Good:** `player.x += Settings.PLAYER_SPEED`
This allows you to change `PLAYER_SPEED` in one place, or even link it to a UI slider for real-time balancing.

#### Common 3D Bugs
1.  **Clipping (Near Plane):** If an object gets closer than `gluPerspective`'s `near` value (e.g., 0.1), it is sliced open.
    * *Fix:* Implement collision bubbles to stop movement before distance < 0.1.
2.  **Tunneling:** Fast objects skipping collision checks.
    * *Fix:* Raycasting (checking the line ahead) or Sub-stepping (moving 10x at 0.1 speed).
3.  **Z-Fighting:** Two surfaces at the exact same position flickering.
    * *Fix:* Move one surface slightly (`0.001`) forward.

---

## 🛠️ WHAT I DID TODAY
* **Built a Config Class:** Created a central place for game constants.
* **Implemented Real-Time Balancing:** Mapped keyboard inputs to modify global game variables (FOV, Speed) live.
* **Used Window Title for Debugging:** Used `set_caption` to display data without needing a complex 3D Text Renderer.

---

## 💻 SOURCE CODE
> [!example]- DYNAMIC PROJECTION
> ```python
> def update_fov(new_fov):
>     glMatrixMode(GL_PROJECTION)
>     glLoadIdentity()
>     gluPerspective(new_fov, aspect, 0.1, 50.0)
>     glMatrixMode(GL_MODELVIEW)
> ```

---
## 🎯 GOALS FOR TOMORROW

> [!todo] 🏆 **Day 29: Final Project Build**
> * Combine everything!
> * 3D Movement + AI + Shooting + Tweakables.
> * Build "Space Station Dogfight."
