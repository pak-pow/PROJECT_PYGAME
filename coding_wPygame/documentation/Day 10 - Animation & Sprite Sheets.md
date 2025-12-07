Tags: [[Programming]], [[Python]], [[PyGame]], [[Game]] 

---
**Topic:** Animation & Sprite Sheets.
#### 1) Learning Goal

We will learn how to animate a sprite by cycling through a list of images (frames) and how to use a **Sprite Sheet** (one big image containing all animation frames) to manage assets efficiently.
#### 2) Clear Overview

- **The Illusion:** Animation is just showing different images really fast.

- **The Problem:** Loading 50 separate image files (`run1.png`, `run2.png`...) is messy and slow.
    
- **The Solution:** A **Sprite Sheet**. One single image file that looks like a film strip. We tell Pygame to "cut out" specific rectangles from it to create our animation frames.

#### 3) Deep Explanation

**A. Frame-by-Frame Logic**

Instead of self.image = one_surface, we have a list: self.frames = [image1, image2, image3].

We need a float variable (e.g., self.frame_index).

- Every update: `self.frame_index += animation_speed * dt`.
- We allow it to grow (0.1, 0.5, 1.2, 2.9...).
- We convert it to an integer to pick the image: `self.image = self.frames[int(self.frame_index)]`.
- If it goes too high (past the list length), we reset it to 0 (Loop).

**B. Cutting up a Sprite Sheet**

To get the frames from one big sheet, we use sheet.subsurface(rect). This grabs a specific chunk of the original image.

**C. Flipping (Left/Right)**

We don't need separate images for Left and Right. We use pygame.transform.flip(image, True, False) to mirror the image horizontally.

---
#### 4) Runnable Pygame Code Example

Watch the square change colors/shapes as it moves!

``` Python
import pygame, sys

# 1. Setup
pygame.init()
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()

# --- HELPER: GENERATE FAKE SPRITE SHEET ---
# In a real game, you would just load a .png file here.
# We are making a 128x32 surface (4 frames, each 32x32)
def generate_sprite_sheet():
    sheet = pygame.Surface((128, 32))
    sheet.fill((0, 0, 0)) # Transparent-ish background
    
    # Frame 1: Red Square
    pygame.draw.rect(sheet, (255, 0, 0), (0, 0, 32, 32))
    # Frame 2: Green Circle
    pygame.draw.circle(sheet, (0, 255, 0), (48, 16), 16)
    # Frame 3: Blue Rect
    pygame.draw.rect(sheet, (0, 0, 255), (64, 0, 32, 32))
    # Frame 4: Yellow Circle
    pygame.draw.circle(sheet, (255, 255, 0), (112, 16), 16)
    
    return sheet

# --- PLAYER CLASS ---
class Player(pygame.sprite.Sprite):
    def __init__(self, sheet):
        super().__init__()
        
        # 1. Load Frames
        self.frames = []
        frame_width = 32
        frame_height = 32
        
        # Cut up the sheet into 4 frames
        for i in range(4):
            # Create a rect for the chunk we want
            # x position moves over by 32 pixels each time (0, 32, 64, 96)
            frame_location = (i * frame_width, 0, frame_width, frame_height)
            # Grab the chunk (subsurface)
            frame_image = sheet.subsurface(frame_location)
            self.frames.append(frame_image)
            
        # 2. Setup Animation Variables
        self.frame_index = 0.0
        self.animation_speed = 8 # Frames per second
        
        # 3. Standard Setup
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(300, 200))
        self.pos = pygame.math.Vector2(300, 200)
        self.velocity = pygame.math.Vector2(0, 0)
        self.speed = 200
        self.facing_right = True

    def get_input(self):
        keys = pygame.key.get_pressed()
        self.velocity.x = 0
        if keys[pygame.K_LEFT]:
            self.velocity.x = -self.speed
            self.facing_right = False
        if keys[pygame.K_RIGHT]:
            self.velocity.x = self.speed
            self.facing_right = True

    def animate(self, dt):
        # Only animate if moving
        if self.velocity.x != 0:
            # Increase the index
            self.frame_index += self.animation_speed * dt
            
            # Loop back to 0 if we run out of frames
            if self.frame_index >= len(self.frames):
                self.frame_index = 0
        else:
            # Idle: Reset to first frame
            self.frame_index = 0

        # Update the actual image
        # int() chops off the decimal (2.8 -> 2) so we get a valid list index
        current_image = self.frames[int(self.frame_index)]
        
        # Handle Flipping
        if not self.facing_right:
            # flip(surface, x_bool, y_bool)
            self.image = pygame.transform.flip(current_image, True, False)
        else:
            self.image = current_image

    def update(self, dt):
        self.get_input()
        self.pos += self.velocity * dt
        self.rect.center = round(self.pos)
        self.animate(dt)

# Setup
sprite_sheet = generate_sprite_sheet() # Make our fake art
player = Player(sprite_sheet)
all_sprites = pygame.sprite.Group(player)

# Loop
while True:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((50, 50, 50))
    
    all_sprites.update(dt)
    all_sprites.draw(screen)
    
    # Draw the full sprite sheet at the top so you can see where frames come from
    screen.blit(sprite_sheet, (10, 10))
    
    pygame.display.update()
```

---
#### 5) 20-Minute Drill

**Your Task:**

1. Run the code. Move the character using Left/Right.
    
2. **Experiment:** Change `self.animation_speed` to `2` (slow motion) and `20` (hyper speed). See how it feels.
    
3. **Challenge:** Add a "Jump" animation state.
    
    - Currently, we only check `if self.velocity.x != 0`.
        
    - Add a check: `if keys[pygame.K_SPACE]:`.
        
    - If space is held, force the image to be **Frame 2** (Index 1) immediately, overriding the walking animation.

---
#### 6) Quick Quiz

1. **What does `subsurface` do?**
2. **Why do we use a `float` for `frame_index` instead of an `int`?**   
3. **If I have 4 frames, and `frame_index` becomes 4.1, what error will happen if I don't reset it to 0?**

**Answers:**

1. It creates a new Surface that references a specific rectangular area of a larger Surface (cuts it out).
    
2. To track time smoothly. If we add `0.1` every frame, we stay on the same image for 10 frames before switching. An `int` would jump instantly.
    
3. `IndexError: list index out of range` (because the last valid index is 3).
    

---

#### 7) Homework for Tomorrow

Take your **Platformer Physics** (Day 9) code.

- Find a real sprite sheet online (search "2D platformer sprite sheet png").
    
- Use the `subsurface` logic to load the "Walk" frames into a list.
    
- Make your physics player animate while walking!
    

---

#### 8) Progress to Mastery

🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩 **33%** (1/3 of the way there!)

---

#### 9) Obsidian Note

## 🧠 CONCEPT SUMMARY

#### Animation Logic:
Animation is the rapid cycling of images.
> [!note] 
> We use a timer (float) to increment an index: `index += speed * dt`. We cast this to an `int` to pick an image from a list.

#### Sprite Sheets:
A single image file containing multiple animation frames. This saves memory and keeps assets organized.

#### Subsurface:
The Pygame method used to "cut out" a frame from a sheet.
> [!note] 
> `frame = full_sheet_image.subsurface((x, y, width, height))`

#### Flipping:
Use `pygame.transform.flip(surface, True, False)` to create a mirror image (e.g., facing Left) without needing a separate art file.

---

## 🛠️ WHAT I DID TODAY

* **Generated Assets:** Created a "programmatic" sprite sheet in memory to test animation without external files.
* **Sliced Sheets:** Used `subsurface` to divide one large image into a list of 4 smaller frames.
* **Implemented Cycling:** Created an update loop that cycles through the frame list based on Delta Time.
* **Added States:** Implemented logic to switch between "Idle" (frame 0) and "Walking" (cycling frames) based on velocity.

---

## 💻 SOURCE CODE

> [!example]- ANIMATED SPRITE CLASS
> ```python
> class AnimatedPlayer(pygame.sprite.Sprite):
>     def __init__(self, sheet, frame_count, width, height):
>         super().__init__()
>         self.frames = []
>         # Slice sheet
>         for i in range(frame_count):
>             loc = (i * width, 0, width, height)
>             self.frames.append(sheet.subsurface(loc))
>             
>         self.frame_index = 0.0
>         self.image = self.frames[0]
>         self.rect = self.image.get_rect()
> 
>     def animate(self, dt):
>         self.frame_index += 10 * dt # 10 FPS
>         if self.frame_index >= len(self.frames):
>             self.frame_index = 0
>             
>         self.image = self.frames[int(self.frame_index)]
> ```

---

## 🧠 LEARNED TODAY

* **State Animation:** Logic flow is key. `if jumping: image = jump_frame` must take priority over `if walking: image = walk_frame`.
* **Subsurface:** This is efficient because it shares pixel data with the original parent surface. It doesn't duplicate memory.

---

## 🧪 PRACTICE / EXERCISES

**Exercise: Animation States**
Goal: Switch animations based on action.

```python
# Inside update
if self.velocity.y != 0:
    self.image = self.jump_frame
elif self.velocity.x != 0:
    self.animate_walk(dt)
else:
    self.image = self.idle_frame
````

---

## 🎯 GOALS FOR TOMORROW

> [!todo] 🎥 **Day 11: Camera & Scrolling**
> 
> - Learn to render a world larger than the screen.
>     
> - Implement a Camera offset vector.
>     
> - Create a Parallax background effect.
>