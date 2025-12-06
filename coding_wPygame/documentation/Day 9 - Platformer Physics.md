Tags: [[Programming]], [[Python]], [[PyGame]], [[Game]] 

---

Up until now, our characters floated around like ghosts. Today, we give them **MASS**. We are going to implement **Gravity** (pulling them down) and **Floor Collision** (stopping them from falling into the void).

#### 1) Learning Goal

We will learn to implement **Gravity** as a constant acceleration, **Jumping** as an instantaneous force, and **Vertical Collision** to detect the ground.

#### 2) Clear Overview

- **Gravity:** It's just a number we add to our Y-Velocity every single frame. It makes the player fall faster and faster.
    
- **The Floor:** An invisible line (or rectangle). If the player crosses it, we snap them back on top and set their Y-Velocity to 0.
    
- **Jumping:** A one-time subtraction from Y-Velocity (because Y goes _down_, so negative Y is _up_).
    

#### 3) Deep Explanation

**A. Gravity is Acceleration**

Remember Day 8? Position += Velocity * dt.
Gravity works one step higher: *Velocity += Acceleration * dt.*

- Every frame, we add `GRAVITY * dt` to `velocity.y`.
- This creates a smooth, accelerating fall (just like real life!).

**B. The "Grounded" State**

You can't jump if you are in the air (unless you want a double jump). We need a boolean flag: self.on_ground = False.

- If we touch the floor -> `on_ground = True`.
- If we jump or fall off a ledge -> `on_ground = False`.

**C. The Physics Loop**

1. **Apply Gravity** to Velocity.
2. **Move** the Player (apply Velocity to Position).
3. **Check Collisions** (Did we hit the floor?).
4. **Resolve Collisions** (Snap to top of floor, set Y velocity to 0).

---

#### 4) Runnable Pygame Code Example

Here is a complete simulation. You control the **Blue Square**.

- **Left/Right:** Move.
- **Space:** Jump!
- **Green Bar:** The Floor.

Notice how the player accelerates as they fall!

``` python
import pygame, sys
from pygame.locals import *

# 1. Setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
pygame.display.set_caption("Day 9: Platformer Physics")

# Constants
GRAVITY = 2000      # Pixels per second squared (How heavy it feels)
JUMP_STRENGTH = -800 # Negative is UP
MOVE_SPEED = 400
FLOOR_Y = 500       # The Y level of the ground

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((50, 100, 255))
        self.rect = self.image.get_rect(midbottom=(400, FLOOR_Y))
        
        # Physics Vectors
        self.pos = pygame.math.Vector2(400, FLOOR_Y)
        self.vel = pygame.math.Vector2(0, 0)
        
        self.on_ground = True

    def update(self, dt):
        # 1. Horizontal Movement (Standard)
        keys = pygame.key.get_pressed()
        self.vel.x = 0 # Reset X speed (snappy movement)
        if keys[K_LEFT]:  self.vel.x = -MOVE_SPEED
        if keys[K_RIGHT]: self.vel.x = MOVE_SPEED

        # 2. Apply Gravity (The Magic!)
        # We add gravity to velocity.y every single frame
        self.vel.y += GRAVITY * dt

        # 3. Apply Movement to Position
        self.pos += self.vel * dt

        # 4. Floor Collision (The "Thud")
        # In a real game, you check collisions with rects. 
        # Here, we use a simple "Floor Line" at FLOOR_Y.
        
        # If our feet (pos.y) go BELOW the floor...
        if self.pos.y >= FLOOR_Y:
            self.pos.y = FLOOR_Y    # Snap back to top of floor
            self.vel.y = 0          # Stop falling!
            self.on_ground = True
        else:
            self.on_ground = False

        # 5. Sync Rect
        self.rect.midbottom = round(self.pos)

    def jump(self):
        # Only jump if we are standing on something!
        if self.on_ground:
            self.vel.y = JUMP_STRENGTH
            self.on_ground = False

# Setup Objects
player = Player()
all_sprites = pygame.sprite.Group(player)

# Game Loop
while True:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                player.jump()

    # Update
    all_sprites.update(dt)

    # Draw
    screen.fill((30, 30, 30))
    
    # Draw Floor
    pygame.draw.rect(screen, (100, 200, 100), (0, FLOOR_Y, 800, 100))
    
    # Draw Player
    all_sprites.draw(screen)
    
    pygame.display.update()
```

---

#### 5) 20-Minute Drill

**Your Task:** Tweak the physics to feel different.

1. **Moon Gravity:** Change `GRAVITY` to `500`. Run it. How does it feel?
    
2. **Super Mario:** Change `GRAVITY` to `3000` and `JUMP_STRENGTH` to `-1200`. It should feel snappy and heavy.
    
3. **Double Jump:** Modify the `jump()` function. Add a variable `self.double_jump_ready`.
    
    - When you touch the ground, set `double_jump_ready = True`.
        
    - Allow a jump IF `on_ground` OR `double_jump_ready`.
        
    - If you jump while in the air, set `double_jump_ready = False`.
        

_Code this double jump logic now! It's a classic mechanic._

---

#### 6) Quick Quiz

1. **In Pygame, which direction is Positive Y? (Up or Down)**
    
2. **Why do we set `self.vel.y = 0` when we hit the floor?**
    
3. **To jump, do we add or subtract from Y velocity?**
    

**Answers:**

1. **Down** (so Gravity _adds_ to Y).
    
2. To stop the accumulation of gravity. If we didn't, gravity would keep adding up, and if we walked off a cliff, we would shoot down at light speed instantly.
    
3. **Subtract** (Negative Y moves up).
    

---

#### 7) Homework for Tomorrow

Create a "Platform" class (just a green rectangle).

- Spawn 3 platforms at different heights.
    
- Update your collision logic: Instead of checking `if self.pos.y >= FLOOR_Y`, check `pygame.sprite.spritecollide(player, platforms, False)`.
    
- _Hint:_ This is tricky! If you hit a platform, you need to check if you were _falling_ onto it.
    

---

#### 8) Progress to Mastery

🟩🟩🟩🟩🟩🟩🟩🟩🟩⬜ **30%**

---

#### 9) Obsidian Note

## 🧠 CONCEPT SUMMARY

#### Gravity:
A constant downward force. In code, it is **Acceleration**.
> [!note] 
> `velocity.y += GRAVITY * dt`
> We add this *every frame*, regardless of whether we are moving or standing still.

#### Jumping:
An instantaneous upward force.
> [!note] 
> `velocity.y = -JUMP_STRENGTH` (Negative because Up is Y-).
> We typically only allow this if `on_ground` is True.

#### Ground Collision:
When the player falls, we check if they crossed the floor line.
1.  **Detect:** `if player.y > floor_y`
2.  **Snap:** `player.y = floor_y` (Start standing ON the floor, not IN it).
3.  **Stop:** `velocity.y = 0` (Cancel the accumulated gravity).

---

## 🛠️ WHAT I DID TODAY

* **Implemented Gravity:** Created a physics simulation where objects fall faster over time.
* **Built a Jump Mechanic:** Added logic to apply instantaneous upward velocity.
* **Handled Ground State:** Created an `on_ground` flag to prevent infinite mid-air jumping.
* **Experimented with "Feel":** Tweaked Gravity and Jump Force numbers to simulate Moon gravity vs. Heavy gravity.

---

## 💻 SOURCE CODE

> [!example]- PHYSICS PLAYER CLASS
> ```python
> class Player(pygame.sprite.Sprite):
>     def __init__(self):
>         super().__init__()
>         self.pos = pygame.math.Vector2(100, 300)
>         self.vel = pygame.math.Vector2(0, 0)
>         self.on_ground = False
>         
>     def update(self, dt):
>         # 1. Apply Gravity
>         self.vel.y += 2000 * dt
>         
>         # 2. Move
>         self.pos += self.vel * dt
>         
>         # 3. Floor Collision (Simple)
>         if self.pos.y >= 500:
>             self.pos.y = 500
>             self.vel.y = 0
>             self.on_ground = True
>         else:
>             self.on_ground = False
>             
>         self.rect.midbottom = round(self.pos)
> 
>     def jump(self):
>         if self.on_ground:
>             self.vel.y = -800
> ```

---

## 🧠 LEARNED TODAY

* **Gravity is Accumulative:** You don't set Y speed to "down"; you *add* to Y speed constantly.
* **Floor Reset:** It is vital to set `vel.y = 0` when hitting the floor. If you don't, gravity keeps building up in the background. If you then walked off a ledge, you would teleport to the bottom of the screen instantly.

---

## 🧪 PRACTICE / EXERCISES

**Exercise: Double Jump**
Goal: Allow one extra jump in mid-air.

```python
# In __init__
self.jumps_left = 2

# In Jump
if self.jumps_left > 0:
    self.vel.y = -800
    self.jumps_left -= 1

# In Collision (Touching ground)
self.jumps_left = 2
````

---

## 🎯 GOALS FOR TOMORROW

> [!todo] 🏃 **Day 10: Animation**
> 
> - Learn to use **Sprite Sheets**.
>     
> - Animate the player walking (cycle through images).
>     
> - Flip images when facing Left vs Right.

