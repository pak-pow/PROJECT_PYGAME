Tags: [[Programming]], [[Python]], [[PyGame]], [[Game]]

---

### 1) Learning Goal

You will learn to use **Pygame Blend Modes** (`BLEND_MULT` and `BLEND_ADD`) to create lighting engines. You will build a system where darkness covers the screen, and lights "cut holes" through it.

### 2) Clear Overview

- **The Problem:** Drawing a semi-transparent black rectangle just makes everything look gray. It doesn't look like a shadow.
    
- **The Solution:** **Multiplication Blending**.
    
    - Think of colors as numbers between 0 and 1.
        
    - **Black** is 0. **White** is 1.
        
    - If you multiply the Game Screen by **Black** (0), it becomes Black (Darkness).
        
    - If you multiply the Game Screen by **White** (1), it stays the same (Light).
        
- **The Trick:** We create a "Light Map" surface. We fill it with Black, draw White circles where the lights are, and then multiply it over the game.
    

### 3) Deep Explanation

A. The Light Map Surface

We create a separate Surface called light_mask that is the same size as the screen.

light_mask = pygame.Surface((800, 600))

**B. The Logic Loop**

1. **Fill** `light_mask` with `(20, 20, 20)` (Very dark gray, ambient light).
    
2. **Draw** a White circle on the `light_mask` at the player's position.
    
3. **Draw** your normal game world.
    
4. **Blit** the `light_mask` onto the screen using `special_flags=pygame.BLEND_MULT`.
    

C. BLEND_ADD (Glowing)

For things like lasers or fire, we use Additive Blending.

This adds the pixel values together.

Red (200, 0, 0) + Red (100, 0, 0) = Super Bright Red (255, 0, 0).

---

### 4) Runnable Pygame Code Example

Here is a **Flashlight Simulator**.

- **Move:** Mouse.
    
- **Click:** Toggle "Cyberpunk Mode" (Additive colored lights).
    
- **Effect:** Notice how the white circle reveals the grid background.
    

``` Python
import pygame, sys, random

# 1. Setup
pygame.init()
SCREEN_W, SCREEN_H = 800, 600
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
clock = pygame.time.Clock()

# Generate a cool background pattern
bg_surf = pygame.Surface((SCREEN_W, SCREEN_H))
bg_surf.fill((50, 50, 50))
for x in range(0, SCREEN_W, 40):
    pygame.draw.line(bg_surf, (100, 100, 100), (x, 0), (x, SCREEN_H))
for y in range(0, SCREEN_H, 40):
    pygame.draw.line(bg_surf, (100, 100, 100), (0, y), (SCREEN_W, y))
    
# Draw some random colored boxes to see the lighting better
for i in range(20):
    color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
    rect = (random.randint(0, 700), random.randint(0, 500), 50, 50)
    pygame.draw.rect(bg_surf, color, rect)

# --- LIGHTING SETUP ---
# This is the "Filter" layer
light_mask = pygame.Surface((SCREEN_W, SCREEN_H))

# Load or Create a Light Texture (Soft Circle)
# In a real game, you'd load a 'gradient_circle.png'
# Here, we make one manually with circles
def draw_gradient_circle(surf, pos, radius, color):
    # Draw multiple circles with decreasing alpha to simulate softness
    # Note: For true smooth lighting, loading a PNG image is WAY faster
    pygame.draw.circle(surf, color, pos, radius)

mode_cyberpunk = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mode_cyberpunk = not mode_cyberpunk

    # 1. DRAW GAME WORLD (Normal)
    screen.blit(bg_surf, (0, 0))
    
    mouse_pos = pygame.mouse.get_pos()
    
    # 2. LIGHTING LOGIC
    if not mode_cyberpunk:
        # --- MODE A: FLASHLIGHT (Multiply) ---
        
        # A. Fill mask with Darkness (Ambient Light)
        # (30, 30, 30) = Very Dark. (0,0,0) = Pitch Black.
        light_mask.fill((30, 30, 30)) 
        
        # B. Cut a hole (Draw White Light)
        # White (255, 255, 255) means "Show 100% of the game color"
        pygame.draw.circle(light_mask, (255, 255, 255), mouse_pos, 100)
        
        # C. Apply the Mask using MULTIPLY
        # Game * Mask = Final Result
        screen.blit(light_mask, (0, 0), special_flags=pygame.BLEND_MULT)
        
        txt = "Mode: FLASHLIGHT (Multiply). Click to switch."
        
    else:
        # --- MODE B: NEON GLOW (Add) ---
        
        # A. We don't fill with darkness here. We just darken the screen manually first
        # creating a 'night' feel
        night_overlay = pygame.Surface((SCREEN_W, SCREEN_H))
        night_overlay.fill((0, 0, 0))
        night_overlay.set_alpha(200) # Darken everything
        screen.blit(night_overlay, (0,0))
        
        # B. Draw Colored Lights using ADD
        # Create a temp surface for the light
        glow_surf = pygame.Surface((SCREEN_W, SCREEN_H))
        glow_surf.fill((0, 0, 0)) # Black adds nothing
        
        # Draw Red Light
        pygame.draw.circle(glow_surf, (255, 0, 0), mouse_pos, 80)
        # Draw Blue Light (Offset)
        pygame.draw.circle(glow_surf, (0, 0, 255), (mouse_pos[0]+50, mouse_pos[1]+50), 60)
        
        # C. Apply using ADD
        screen.blit(glow_surf, (0, 0), special_flags=pygame.BLEND_ADD)
        
        txt = "Mode: CYBERPUNK (Add). Click to switch."

    # UI
    font = pygame.font.SysFont(None, 30)
    screen.blit(font.render(txt, True, (255, 255, 255)), (10, 10))

    pygame.display.update()
    clock.tick(60)
```

---

### 5) 20-Minute Drill

**Your Task:** Make the flashlight **pulse** (flicker).

1. Use the `FLASHLIGHT` mode (not cyberpunk).
    
2. In the loop, generate a random radius for the circle every frame: `r = random.randint(95, 105)`.
    
3. **Advanced:** Make it look like a dying battery.
    
    - Normally radius is 100.
        
    - Every 100 frames, make the radius drop to 0 for 2 frames (blink off), then return.
        

_This teaches you how dynamic lighting can add tension to a horror game._

---

### 6) Quick Quiz

1. **In `BLEND_MULT` mode, what happens if I fill the light mask with White `(255, 255, 255)`?**
    
2. **In `BLEND_MULT` mode, what happens if I fill the light mask with Black `(0, 0, 0)`?**
    
3. **Why do we draw the lighting mask _after_ drawing the game world?**
    

**Answers:**

1. Nothing changes. The game looks normal (Multiplied by 1).
    
2. The screen goes pitch black (Multiplied by 0).
    
3. Because the mask modifies the pixels that are already on the screen. If you drew the mask first, the game sprites would just draw on top of the darkness.
    

---

### 7) Homework for Tomorrow

**Add "Fog of War" to your Tilemap Game.**

- Create a `light_mask` surface.
    
- In the loop, fill it with dark gray.
    
- Draw a white circle at `player.rect.center`.
    
- Draw another white circle for every torch/lamp in your level.
    
- Blit the mask with `BLEND_MULT`.
    

---

### 8) Progress to Mastery

🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩 **60%**

---

### 9) Obsidian Note

## 🧠 CONCEPT SUMMARY

#### Blend Modes:
Normally, Pygame just pastes one image on top of another (replacing the pixels). Blend modes change the math of how pixels combine.

#### `BLEND_MULT` (Multiply):
Used for **Shadows and Fog**.
* Math: `TargetPixel * BlendPixel`
* White (1) -> No Change.
* Black (0) -> Pitch Black.
* Technique: Fill a surface with Dark Gray, draw White circles where you want "Light", then Multiply over the screen.

#### `BLEND_ADD` (Additive):
Used for **Glow, Fire, Lasers**.
* Math: `TargetPixel + BlendPixel`
* Black (0) -> No Change.
* Color -> Brightens the image.
* Technique: Draw colored shapes on a Black background, then Add to screen.

---

## 🛠️ WHAT I DID TODAY

* **Created a Light Mask:** Made a surface dedicated to lighting information.
* **Implemented Flashlight Effect:** Used `BLEND_MULT` to hide the world in darkness and reveal only a specific area.
* **Implemented Neon Glow:** Used `BLEND_ADD` to make colors pop and look bright/hot.

---

## 💻 SOURCE CODE

> [!example]- LIGHTING ENGINE
> ```python
> # 1. Create Mask
> light_mask = pygame.Surface((800, 600))
> 
> # 2. Reset Mask (Ambient Darkness)
> light_mask.fill((20, 20, 20))
> 
> # 3. Draw Lights (White = Visible)
> pygame.draw.circle(light_mask, (255, 255, 255), player.pos, 100)
> 
> # 4. Apply to Screen
> screen.blit(game_sprites, (0,0))
> screen.blit(light_mask, (0,0), special_flags=pygame.BLEND_MULT)
> ```

---

## 🧠 LEARNED TODAY

* **Order Matters:** Lighting is a post-processing effect. It must be drawn LAST, after backgrounds, players, and enemies are already on the screen.
* **Performance:** Drawing simple shapes (circles) is fast. Drawing complex gradients pixel-by-pixel is slow. For best performance, load a "light ball" PNG image and blit that onto the mask instead of drawing circles manually.

---

## 🎯 GOALS FOR TOMORROW

> [!todo] 🤖 **Day 19: Enemy AI (Artificial Intelligence)**
> * Make enemies chase the player.
> * Implement "Line of Sight" (only chase if they see you).
> * Add simple states (Patrol vs. Attack).
