Tags: [[Programming]], [[Python]], [[PyGame]], [[Game]] 

---
Today is **Day 11: Camera Systems, Scrolling & Parallax**.

**Topic:** World Space vs. Screen Space.
#### 1) Learning Goal

We will learn to create a **Camera System** that allows our player to explore a world much larger than the window, and implement **Parallax Scrolling** to create a 3D depth effect.

#### 2) Clear Overview

- **The Problem:** Your screen is 800x600. Your game world is 5000x5000. How do you draw the player when they are at x=4000?
    
- **The Solution:** The **Camera**. The camera is just a Vector (x, y) that represents what the top-left corner of the screen is currently looking at.
    
- **The Trick:** We don't move the camera. We move **the entire world** in the opposite direction of the camera.

#### 3) Deep Explanation

**A. World Space vs. Screen Space**

- **World Space:** Where the object _actually_ is in the level (e.g., `player.x = 4000`).
    
- **Screen Space:** Where the object gets drawn on your monitor (e.g., `draw_x = 400`).
    
- **The Formula:** `Screen Position = World Position - Camera Position`
    

**B. The Custom Camera Group**

Standard Pygame Group.draw() is dumb; it just draws sprites at their rect coordinates.

We will write a custom CameraGroup class. Inside its .draw() method, we will apply the math formula above to every sprite before blitting it.

**C. Parallax Scrolling**

Parallax is the optical illusion where far-away objects move slower than close objects.

- **Foreground (Player):** Moves at 100% speed.
    
- **Background (Mountains):** Moves at 50% speed.
    
- **Deep Background (Stars):** Moves at 5% speed.
    

---

#### 4) Runnable Pygame Code Example

This code generates a massive field of stars and planets. You fly a spaceship through it.

Notice we use a custom CameraGroup class to handle the drawing logic.

``` Python

import pygame, sys, random

# 1. Setup
pygame.init()
SCREEN_W, SCREEN_H = 800, 600
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
clock = pygame.time.Clock()
pygame.display.set_caption("Day 11: Camera & Parallax")

# --- THE CAMERA SYSTEM ---
class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        
        # Camera Offset (The Vector that tracks the center)
        self.offset = pygame.math.Vector2()
        
        # Create a floor/background rect (Just for visualization)
        self.floor_rect = pygame.Rect(0, 0, 4000, 4000)

    def custom_draw(self, player):
        # 1. Calculate Offset
        # We want the player to be in the CENTER of the screen
        # Camera X = Player X - Half Screen Width
        self.offset.x = player.rect.centerx - SCREEN_W // 2
        self.offset.y = player.rect.centery - SCREEN_H // 2

        # 2. Draw Floor (Reference Frame)
        # Apply the offset formula: World_Pos - Camera_Offset
        floor_offset_pos = self.floor_rect.topleft - self.offset
        pygame.draw.rect(self.display_surface, (20, 20, 30), 
                         (*floor_offset_pos, self.floor_rect.width, self.floor_rect.height), 2)

        # 3. Draw Sprites
        # We sort sprites by Y coordinate so lower sprites overlap higher ones (Depth)
        for sprite in sorted(self.sprites(), key=lambda s: s.rect.centery):
            # Apply the Camera Offset to the sprite's position
            offset_pos = sprite.rect.topleft - self.offset
            
            # Blit at the NEW calculated position
            self.display_surface.blit(sprite.image, offset_pos)

# --- GAME OBJECTS ---
class Player(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 0, 0)) # Red
        self.rect = self.image.get_rect(center=(2000, 2000)) # Start in middle of big world
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 400

    def update(self, dt):
        keys = pygame.key.get_pressed()
        input_vec = pygame.math.Vector2(0, 0)
        
        if keys[pygame.K_LEFT]: input_vec.x = -1
        if keys[pygame.K_RIGHT]: input_vec.x = 1
        if keys[pygame.K_UP]: input_vec.y = -1
        if keys[pygame.K_DOWN]: input_vec.y = 1
        
        if input_vec.length() > 0:
            input_vec = input_vec.normalize()
            self.pos += input_vec * self.speed * dt
            self.rect.center = round(self.pos)

class Star(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        size = random.randint(5, 15)
        self.image = pygame.Surface((size, size))
        self.image.fill((255, 255, 255)) # White
        self.rect = self.image.get_rect()
        
        # Spawn randomly in the 4000x4000 world
        self.rect.x = random.randint(0, 4000)
        self.rect.y = random.randint(0, 4000)

# --- MAIN ---
camera_group = CameraGroup()
player = Player(camera_group)

# Create 500 random stars
for i in range(500):
    Star(camera_group)

while True:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0)) # Space Black

    # 1. Update (Logic uses World Coordinates)
    camera_group.update(dt)

    # 2. Draw (Uses Screen Coordinates calculated by Camera)
    camera_group.custom_draw(player)

    # UI (Does NOT move with camera - static on screen)
    debug_text = pygame.font.SysFont(None, 30).render(f"Pos: {int(player.pos.x)}, {int(player.pos.y)}", True, (0, 255, 0))
    screen.blit(debug_text, (10, 10))

    pygame.display.update()
```

#### Theory: How Zoom Works

Zooming is simply **multiplication**.

1. **Standard Camera:** `Screen_Pos = World_Pos - Camera_Offset`
2. **Zoomed Camera:** `Screen_Pos = (World_Pos - Camera_Offset) * Zoom_Scale`

	- If `Zoom_Scale` is **2.0**, everything is twice as big and twice as far apart (Zoom In).
    
	- If `Zoom_Scale` is **0.5**, everything is half size and squished together (Zoom Out).

> [!important] **IMPORTANT** 
> You must scale the _size_ of the sprites (`pygame.transform.scale`) AND their _positions_ relative to the center of the screen.

---

#### 🧪 Upgraded Code: Camera + Parallax + Zoom

I modified the `CameraGroup` class.

- **Controls:** Hold **Q** to Zoom In, **E** to Zoom Out.
    
- **Logic:** It calculates the distance of every object from the **Screen Center**, scales that distance by the zoom factor, and draws the scaled sprite.

``` Python
import pygame, sys, random

# 1. Setup
pygame.init()
SCREEN_W, SCREEN_H = 800, 600
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
clock = pygame.time.Clock()
pygame.display.set_caption("Day 11: Camera & Zoom")

# --- THE CAMERA SYSTEM ---
class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        
        # Camera Vectors
        self.offset = pygame.math.Vector2()
        self.zoom_scale = 1.0
        self.internal_surf_size = (2500, 2500)
        self.internal_surf = pygame.Surface(self.internal_surf_size, pygame.SRCALPHA)
        self.internal_rect = self.internal_surf.get_rect(center = (SCREEN_W // 2, SCREEN_H // 2))

    def custom_draw(self, player):
        # 1. Handle Zoom Input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]: self.zoom_scale += 0.05
        if keys[pygame.K_e]: self.zoom_scale -= 0.05
        
        # Clamp Zoom (Don't let it get too small or too big/flipped)
        if self.zoom_scale < 0.3: self.zoom_scale = 0.3
        if self.zoom_scale > 2.0: self.zoom_scale = 2.0

        # 2. Calculate Camera Center (Focus on Player)
        self.offset.x = player.rect.centerx - SCREEN_W // 2
        self.offset.y = player.rect.centery - SCREEN_H // 2

        # 3. Draw Background (Floor)
        # We draw logic on the screen directly using Vector Math
        
        # NOTE: For performance with Zoom, we iterate sprites.
        # Ideally, we would scale the whole surface, but scaling sprites teaches the vector math better.
        
        for sprite in sorted(self.sprites(), key=lambda s: s.rect.centery):
            # A. Get position relative to camera
            offset_pos = sprite.rect.topleft - self.offset
            
            # B. Apply Zoom Math
            # We want to zoom relative to the CENTER of the screen
            # 1. Shift positions so (0,0) is the center of the screen
            center_offset = offset_pos - pygame.math.Vector2(SCREEN_W//2, SCREEN_H//2)
            
            # 2. Scale that distance
            zoomed_offset = center_offset * self.zoom_scale
            
            # 3. Shift back to screen coordinates
            final_pos = zoomed_offset + pygame.math.Vector2(SCREEN_W//2, SCREEN_H//2)
            
            # C. Scale the Image
            # (Note: Scaling images every frame is slow in Python, but fine for learning)
            new_w = int(sprite.rect.width * self.zoom_scale)
            new_h = int(sprite.rect.height * self.zoom_scale)
            
            # Only draw if it's going to be visible (Optimization)
            if -100 < final_pos.x < SCREEN_W + 100 and -100 < final_pos.y < SCREEN_H + 100:
                 zoomed_image = pygame.transform.scale(sprite.image, (new_w, new_h))
                 self.display_surface.blit(zoomed_image, final_pos)

# --- GAME OBJECTS ---
class Player(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 0, 0)) # Red
        self.rect = self.image.get_rect(center=(1000, 1000))
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 400

    def update(self, dt):
        keys = pygame.key.get_pressed()
        input_vec = pygame.math.Vector2(0, 0)
        
        if keys[pygame.K_LEFT]: input_vec.x = -1
        if keys[pygame.K_RIGHT]: input_vec.x = 1
        if keys[pygame.K_UP]: input_vec.y = -1
        if keys[pygame.K_DOWN]: input_vec.y = 1
        
        if input_vec.length() > 0:
            input_vec = input_vec.normalize()
            self.pos += input_vec * self.speed * dt
            self.rect.center = round(self.pos)

class Star(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        size = random.randint(20, 50) # Made bigger to see zoom better
        self.image = pygame.Surface((size, size))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 2000)
        self.rect.y = random.randint(0, 2000)

# --- MAIN ---
camera_group = CameraGroup()
player = Player(camera_group)

for i in range(200):
    Star(camera_group)

while True:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((10, 10, 20)) # Space Blue

    camera_group.update(dt)
    camera_group.custom_draw(player)

    # UI Info
    info = pygame.font.SysFont(None, 30).render(f"Zoom: {camera_group.zoom_scale:.2f}", True, (0, 255, 0))
    screen.blit(info, (10, 10))
```

---

### 5) 20-Minute Drill

**Your Task:** Add a **Parallax Background**.

1. **Create a Background List:** Before the loop, create a list of 50 random rectangles (simulating distant galaxies). `bg_stars = [{'pos': Vector2(x,y), 'speed': 0.2}, ...]`
    
2. **Draw Loop:** Inside `custom_draw`, **before** drawing the sprites, loop through `bg_stars`.
    
3. **Apply Parallax Math:**
    
    - `draw_x = star.x - (self.offset.x * star.speed)`
        
    - `draw_y = star.y - (self.offset.y * star.speed)`
        
4. **Draw:** Draw these rectangles.
    
5. **Observe:** Notice how they move slower than the player, creating depth!
    

---

### 6) Quick Quiz

1. **If the Player is at X=2000 and the Camera is at X=1500, where is the Player drawn on the screen?**
    
2. **Why do we sort sprites by `rect.centery` inside the custom draw method?**
    
3. **Why do we draw the UI (Score/Text) manually instead of adding it to the CameraGroup?**
    

**Answers:**

1. X = 500 (`Player - Camera`).
    
2. To handle **Depth** (Y-Sort). Objects lower on the screen (higher Y) should be drawn _on top_ of objects higher on the screen to look like 3D perspective.
    
3. Because UI should stick to the screen and not move when the player walks away.
    

---

### 7) Homework for Tomorrow

Apply this to your **Platformer Project** (Day 9/10).

- Create a `CameraGroup` class.
    
- Move your level design (platforms) so the level is 2000 pixels wide.
    
- Make the camera follow the player as they jump through the level.
    

---

### 8) Progress to Mastery

🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩⬜ **36%**

---
### 9) Obsidian Note

## 🧠 CONCEPT SUMMARY

#### The Camera Concept:
The Camera isn't an object that captures light; it's a math offset.
> [!note] Formula
> `Screen Position = World Position - Camera Offset`

#### Custom Sprite Group:
We extend `pygame.sprite.Group` to create a `CameraGroup`. We override the `draw` method to calculate the offset for every sprite before blitting it.

#### Camera Zoom (Scaling Vectors):
Zooming is multiplying the distance between objects. To zoom in, we multiply the distance vector by a scale factor (> 1.0). To zoom out, we multiply by a fraction (< 1.0).
> [!important] Zoom Math
> 1. Calculate distance from screen center: `dist = obj_pos - screen_center`
> 2. Scale distance: `zoomed_dist = dist * zoom_scale`
> 3. Reposition: `final_pos = zoomed_dist + screen_center`

#### Y-Sort Rendering:
In top-down games, drawing sprites in order of their Y-coordinate ensures that players appearing "lower" on screen are drawn on top of players "higher" on screen, maintaining correct 3D perspective.

---

## 🛠️ WHAT I DID TODAY

* **Built a Camera Group:** Created a custom class inheriting from `pygame.sprite.Group`.
* **Implemented Camera Tracking:** Calculated the offset needed to keep the player centered (`player.center - screen_center`).
* **Created a Massive World:** Generated a play area larger than the window.
* **Implemented Zoom:** Added logic to scale sprite sizes and position vectors based on user input (Q/E keys).
* **Parallax Basics:** Learned that background layers should move at a fraction of the camera speed to create depth.

---

## 💻 SOURCE CODE

> [!example]- CAMERA GROUP WITH ZOOM
> ```python
> class CameraGroup(pygame.sprite.Group):
>     def __init__(self):
>         super().__init__()
>         self.display_surface = pygame.display.get_surface()
>         self.offset = pygame.math.Vector2()
>         self.zoom_scale = 1.0
> 
>     def custom_draw(self, target):
>         # 1. Update Zoom
>         keys = pygame.key.get_pressed()
>         if keys[pygame.K_q]: self.zoom_scale += 0.01
>         if keys[pygame.K_e]: self.zoom_scale -= 0.01
> 
>         # 2. Center Camera
>         self.offset.x = target.rect.centerx - SCREEN_W // 2
>         self.offset.y = target.rect.centery - SCREEN_H // 2
> 
>         # 3. Draw & Scale Sprites
>         for sprite in self.sprites():
>             # Math to center zoom on screen
>             offset_pos = sprite.rect.topleft - self.offset
>             center_offset = offset_pos - pygame.math.Vector2(SCREEN_W//2, SCREEN_H//2)
>             zoomed_pos = (center_offset * self.zoom_scale) + pygame.math.Vector2(SCREEN_W//2, SCREEN_H//2)
>             
>             # Scale Image
>             new_w = int(sprite.rect.width * self.zoom_scale)
>             new_h = int(sprite.rect.height * self.zoom_scale)
>             scaled_surf = pygame.transform.scale(sprite.image, (new_w, new_h))
>             
>             self.display_surface.blit(scaled_surf, zoomed_pos)
> ```

---

## 🧠 LEARNED TODAY

* **Offset Math:** Moving to the *right* increases World X. To draw it, we must shift the world *left* (Subtract X).
* **Zoom Origin:** If you just multiply position by zoom, everything scales away from (0,0). To zoom on the *player*, you must calculate positions relative to the screen center first.

---

## 🧪 PRACTICE / EXERCISES

**Exercise: Parallax Stars**
Goal: Draw background stars that move at 20% speed.

```python
# Inside custom_draw:
for star in bg_stars:
    # Multiply offset by small number (0.2) for depth
    x = star.x - (self.offset.x * 0.2)
    y = star.y - (self.offset.y * 0.2)
    pygame.draw.circle(display, WHITE, (x, y), 2)
## 🎯 GOALS FOR TOMORROW
```

> [!todo] ✨ **Day 12: Particle Effects**
> 
> - Learn to spawn lists of temporary objects.
>     
> - Create explosions, smoke, and trails.
>     
> - Manage memory by deleting particles when they fade out.
>