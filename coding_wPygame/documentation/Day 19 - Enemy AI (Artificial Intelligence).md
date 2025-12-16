Tags: [[Programming]], [[Python]], [[PyGame]], [[Game]]

---
### 1) Learning Goal

You will learn to implement **Proximity AI** (Aggro Range). The enemy will wander randomly, but if the player steps inside an invisible circle (the Aggro Radius), the enemy will switch modes and run directly at the player.
### 2) Clear Overview

- **The Math:** We calculate the distance between Player and Enemy using vectors.
- **The Threshold:** We define a number (e.g., 200 pixels).
    
    - `Distance > 200`: **Patrol Mode** (Move randomly or stand still).
    - `Distance < 200`: **Chase Mode** (Move toward player).
    
- **The Chase Vector:** `Direction = (Player_Pos - Enemy_Pos).normalize()`.

### 3) Deep Explanation

**A. Calculating Distance**

- Pygame vectors make this trivial.
- dist = (player.pos - enemy.pos).length()
- This gives you the exact pixel distance (hypotenuse) between the two.

**B. The State Machine**

Just like our Game State Manager (Day 14), an enemy needs states.

- **IDLE:** Wait for 2 seconds.
- **WANDER:** Pick a random point and walk there.
- **CHASE:** Ignore everything and run at the player.

**C. Line of Sight (Bonus Theory)**

Real AI checks for walls. "Can I see the player?"

We usually check this with pygame.draw.line (raycasting) or checking if the vector collides with a wall group. We'll stick to distance today for simplicity.

---
### 4) Runnable Pygame Code Example

Here is a **Zombie Simulator**.

- **Green:** You.    
- **Red:** The Zombie.
- **Yellow Circle:** The "Aggro Range" (Visualized).
- **Behavior:** Walk close to the zombie. Notice it turns bright red and chases you. Run away, and it gives up.

``` Python
import pygame, sys, random

# 1. Setup
pygame.init()
SCREEN_W, SCREEN_H = 800, 600
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)

# --- CLASSES ---
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((0, 255, 0)) # Green
        self.rect = self.image.get_rect(center=(400, 300))
        self.pos = pygame.math.Vector2(400, 300)
        self.speed = 250

    def update(self, dt):
        keys = pygame.key.get_pressed()
        input_vec = pygame.math.Vector2(0, 0)
        if keys[pygame.K_w]: input_vec.y -= 1
        if keys[pygame.K_s]: input_vec.y += 1
        if keys[pygame.K_a]: input_vec.x -= 1
        if keys[pygame.K_d]: input_vec.x += 1
        
        if input_vec.length() > 0:
            self.pos += input_vec.normalize() * self.speed * dt
            self.rect.center = round(self.pos)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, player_ref):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((200, 50, 50)) # Red
        self.rect = self.image.get_rect(center=(100, 100))
        
        self.pos = pygame.math.Vector2(100, 100)
        self.speed = 150 # Slower than player (so you can escape)
        
        self.player = player_ref # Reference to player to track them
        self.state = "IDLE" 
        self.aggro_radius = 200
        
        # Wander Logic
        self.wander_target = pygame.math.Vector2(100, 100)
        self.wander_timer = 0

    def update(self, dt):
        # 1. Calculate Distance to Player
        # Vector from Enemy -> Player
        to_player_vec = self.player.pos - self.pos
        dist = to_player_vec.length()
        
        # 2. STATE MACHINE
        if dist < self.aggro_radius:
            self.state = "CHASE"
        else:
            self.state = "WANDER"

        # 3. BEHAVIOR
        if self.state == "CHASE":
            self.image.fill((255, 0, 0)) # Bright Red (Angry)
            
            # Move towards player
            direction = to_player_vec.normalize()
            self.pos += direction * self.speed * dt
            
        elif self.state == "WANDER":
            self.image.fill((100, 50, 50)) # Dark Red (Calm)
            
            # Pick a random spot every 2 seconds
            self.wander_timer += dt
            if self.wander_timer > 2.0:
                self.wander_target = pygame.math.Vector2(
                    random.randint(0, SCREEN_W),
                    random.randint(0, SCREEN_H)
                )
                self.wander_timer = 0
            
            # Move towards wander target
            to_target = self.wander_target - self.pos
            if to_target.length() > 5: # If not arrived yet
                self.pos += to_target.normalize() * (self.speed * 0.5) * dt

        # Apply Position
        self.rect.center = round(self.pos)

# --- SETUP ---
player = Player()
enemy = Enemy(player)
all_sprites = pygame.sprite.Group(player, enemy)

# --- GAME LOOP ---
while True:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update
    all_sprites.update(dt)

    # Draw
    screen.fill((20, 20, 20))
    
    # Debug: Draw Aggro Radius
    pygame.draw.circle(screen, (50, 50, 0), enemy.rect.center, enemy.aggro_radius, 1)
    
    all_sprites.draw(screen)
    
    # Debug Text
    status = font.render(f"Enemy State: {enemy.state}", True, (255, 255, 255))
    screen.blit(status, (10, 10))

    pygame.display.update()
```

---
### 5) 20-Minute Drill

**Your Task:** Add a **"Return Home"** mechanic.

1. In `Enemy.__init__`, save `self.home_pos = pygame.math.Vector2(100, 100)`. 
2. Modify the Logic:
    
    - If `dist < aggro_radius`: CHASE.
    - If `dist > aggro_radius`: **RETURN**.

3. In `RETURN` state: Move towards `self.home_pos`.    
4. Once it reaches home (dist < 5), switch to `IDLE`.

_This is exactly how mobs work in MMOs like World of Warcraft. If you kite them too far, they give up and walk back to their spawn point._

---

### 6) Quick Quiz

1. **What vector math function gives us the distance between two points?**
2. **Why do we need to pass `player` into the Enemy class `__init__`?**    
3. **If the enemy speed is higher than the player speed, what happens to the game balance?**

**Answers:**

1. `.length()` (e.g., `(vec_a - vec_b).length()`).
2. The enemy needs to know _where_ the player is. By passing the player object, the enemy can check `self.player.pos` every frame.
3. The player can never escape. This is usually bad design unless you have a "Dodge" or "Stun" mechanic.

---

### 7) Homework for Tomorrow

**Add AI to your Platformer.**

- Create a "Slime" enemy.    
- If the player is within 300 pixels horizontally, the slime moves Left/Right toward the player.
- **Challenge:** Don't let the slime walk off ledges! (Check if there is a floor tile at `slime.x + velocity` before moving).

---
### 8) Progress to Mastery

🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩 **63%**

---

### 9) Obsidian Note

## 🧠 CONCEPT SUMMARY

#### Proximity AI:
A simple behavior model where the enemy reacts based on distance to the target.
> [!note] Formula
> `distance = (player.pos - enemy.pos).length()`

#### AI States:
1.  **Idle/Patrol:** Player is far away. Enemy moves randomly or stands still.
2.  **Chase (Aggro):** Player is close (`distance < radius`). Enemy moves directly toward player vector.
3.  **Retreat/Reset:** Player ran too far. Enemy returns to spawn point.

#### Passing References:
For an enemy to chase the player, the Enemy class must have access to the Player object. We usually pass `player` as an argument when creating the enemy: `Enemy(player)`.

---
## 🛠️ WHAT I DID TODAY

* **Calculated Distance:** Used vector subtraction and magnitude `.length()` to detect player proximity.
* **Built a State Machine:** Implemented logic to switch between "Wander" and "Chase" modes.
* **Visualized Debugging:** Drew the "Aggro Radius" circle on screen to verify the math visually.

---

## 💻 SOURCE CODE

> [!example]- CHASE LOGIC
> ```python
> def update(self, dt):
>     # 1. Get Vector to Player
>     diff = self.player.pos - self.pos
>     dist = diff.length()
> 
>     # 2. Check Range
>     if dist < 200:
>         # Chase!
>         direction = diff.normalize()
>         self.pos += direction * self.speed * dt
>     else:
>         # Idle/Patrol logic...
> ```

---

## 🧠 LEARNED TODAY

* **Vector Utility:** Vectors aren't just for movement; they are for *sensing*. `(A - B).length()` is the most common sensor in game dev.
* **Game Balance:** AI speed matters. If `EnemySpeed > PlayerSpeed`, the game becomes a reaction test rather than a strategy game.

---

## 🎯 GOALS FOR TOMORROW

> [!todo] 📦 **Day 20: Polish & Exporting**
> * Learn to convert your `.py` file into a standalone `.exe` file.
> * Share your game with friends (who don't have Python installed).
> * The final step of the "Core Curriculum"!
