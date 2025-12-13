Tags: [[Programming]], [[Python]], [[PyGame]], [[Game]]

----
### 1) Learning Goal

You will learn to implement **Projectiles** (Bullets). This involves spawning objects on demand, calculating their direction (Vector Math), managing **Fire Rate** (Cooldowns), and handling **Bullet-vs-Enemy Collisions**.

### 2) Clear Overview

- **The Bullet:** It's just a small Sprite that moves fast in one direction.
    
- **Spawning:** When you click, we calculate the direction from the Player to the Mouse.
    
- **Cooldown:** We check `current_time` to stop the player from firing 60 bullets a second (unless you want a minigun!).
    
- **Cleanup:** Bullets must die when they leave the screen, or your computer will crash.
    

### 3) Deep Explanation

**A. The Aiming Math (Vectors)**

Remember Day 8? Vectors are back.

To shoot toward the mouse:

1. Get Mouse Position.
    
2. `Direction = (Mouse_Pos - Player_Pos).normalize()`
    
3. `Bullet_Velocity = Direction * Bullet_Speed`
    

**B. The Cooldown Timer**

To prevent infinite spamming:

1. Variable `last_shot_time = 0`.
2. Variable `shoot_cooldown = 500` (milliseconds).
3. Check: `if (now - last_shot_time) > shoot_cooldown: SHOOT!`

**C. Collision (The groupcollide trick)**

We use pygame.sprite.groupcollide(bullets, enemies, True, True).

- The first `True`: Kill the bullet.
- The second True: Kill the enemy.

One line of code handles the entire war.

---

### 4) Runnable Pygame Code Example

Here is a Top-Down Shooter.

- **WASD:** Move Player.
- **Mouse:** Aim.
- **Left Click:** SHOOT!    
- **Enemies:** Red squares spawning randomly.

``` Python
import pygame, sys, random

# 1. Setup
pygame.init()
SCREEN_W, SCREEN_H = 800, 600
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
clock = pygame.time.Clock()

# --- CLASSES ---
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((0, 255, 0)) # Green
        self.rect = self.image.get_rect(center=(400, 300))
        self.pos = pygame.math.Vector2(400, 300)
        self.speed = 300
        
        # COMBAT STATS
        self.last_shot_time = 0
        self.shoot_delay = 250 # ms (4 shots per second)

    def get_input(self):
        keys = pygame.key.get_pressed()
        input_vec = pygame.math.Vector2(0, 0)
        if keys[pygame.K_w]: input_vec.y -= 1
        if keys[pygame.K_s]: input_vec.y += 1
        if keys[pygame.K_a]: input_vec.x -= 1
        if keys[pygame.K_d]: input_vec.x += 1
        
        if input_vec.length() > 0:
            self.pos += input_vec.normalize() * self.speed * dt
            self.rect.center = round(self.pos)
            
        # SHOOTING INPUT
        if pygame.mouse.get_pressed()[0]: # Left Click
            self.shoot()

    def shoot(self):
        current_time = pygame.time.get_ticks()
        
        # COOLDOWN CHECK
        if current_time - self.last_shot_time > self.shoot_delay:
            self.last_shot_time = current_time
            
            # 1. Calculate Direction to Mouse
            mouse_pos = pygame.mouse.get_pos()
            direction = (mouse_pos - self.pos)
            
            if direction.length() > 0: # Avoid crash if mouse is exactly on player
                direction = direction.normalize()
                
                # 2. Spawn Bullet
                bullet = Bullet(self.rect.center, direction)
                bullet_group.add(bullet)
                all_sprites.add(bullet)

    def update(self):
        self.get_input()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, start_pos, direction):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 255, 0)) # Yellow
        self.rect = self.image.get_rect(center=start_pos)
        
        self.pos = pygame.math.Vector2(start_pos)
        self.velocity = direction * 600 # Fast speed
        self.lifetime = 1000 # ms (Auto-delete after 1 second if it hits nothing)
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        self.pos += self.velocity * dt
        self.rect.center = round(self.pos)
        
        # Cleanup (Wall or Time)
        if (pygame.time.get_ticks() - self.spawn_time > self.lifetime or
            not screen.get_rect().colliderect(self.rect)):
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0)) # Red
        self.rect = self.image.get_rect()
        
        # Spawn random edge
        self.rect.x = random.randint(0, SCREEN_W)
        self.rect.y = random.randint(0, SCREEN_H)

# --- GROUPS ---
all_sprites = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

# Game Loop
spawn_timer = 0

while True:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # SPAWN ENEMIES
    spawn_timer += dt
    if spawn_timer > 1.0: # Every 1 second
        enemy = Enemy()
        enemy_group.add(enemy)
        all_sprites.add(enemy)
        spawn_timer = 0

    # UPDATE
    all_sprites.update()

    # COMBAT LOGIC (The Magic Line)
    # Check if ANY bullet hit ANY enemy. Kill both (True, True)
    hits = pygame.sprite.groupcollide(bullet_group, enemy_group, True, True)
    
    # DRAW
    screen.fill((20, 20, 30))
    all_sprites.draw(screen)
    pygame.display.update()
```

---

### 5) 20-Minute Drill

**Your Task:** Add an **Ammo System**.

1. **Add Variable:** In Player `__init__`, add `self.ammo = 10`.
2. **Add Logic:** In `shoot()`, add a check: `and self.ammo > 0`.
3. **Decrement:** Every time you shoot, `self.ammo -= 1`.
4. **Reload:** Add a check in `get_input()`: If user presses **R**, set `self.ammo = 10` (maybe add a small delay so it's not instant!).

_This teaches you Resource Management._

---

### 6) Quick Quiz

1. **What happens if we don't normalize the direction vector?**
2. **Why do we need `groupcollide` instead of just `colliderect`?**
3. **If I want the bullet to destroy the enemy but keep flying (piercing shot), what arguments do I change in `groupcollide`?**

**Answers:**

1. The bullet speed would change depending on how far away the mouse is (Far mouse = Super fast bullet). Normalizing keeps speed constant.
2. `groupcollide` checks every bullet against every enemy efficiently. Writing nested loops (`for b in bullets: for e in enemies:`) is slow and messy.
3. `groupcollide(bullets, enemies, False, True)` (False for bullet kill, True for enemy kill).
    

---

### 7) Homework for Tomorrow

**Add Shooting to your Platformer.**

- Instead of aiming with the mouse, make the bullet travel in the direction the player is facing.
    
- If `facing_right`: `vel.x = 600`.
    
- If `not facing_right`: `vel.x = -600`.
    

---

### 8) Progress to Mastery

🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩 **53%**

---

### 9) Obsidian Note

## 🧠 CONCEPT SUMMARY

#### Projectiles (Bullets):
Sprites that are spawned dynamically, move in a specific vector direction, and delete themselves upon collision or time-out.

#### Vector Aiming:
To shoot from A (Player) to B (Mouse):
> [!note] Formula
> `Vector = Mouse_Pos - Player_Pos`
> `Direction = Vector.normalize()`
> `Velocity = Direction * Speed`

#### Cooldowns (Fire Rate):
Using time to limit actions.
> [!note] Logic
> `if current_time - last_shot_time > cooldown_duration:`
>     `Fire()`
>     `last_shot_time = current_time`

#### Group Collision:
`pygame.sprite.groupcollide(groupA, groupB, killA, killB)` is the standard way to handle warfare. It returns a dictionary of hits so you can play sounds or add score.

---

## 🛠️ WHAT I DID TODAY

* **Implemented Aiming:** Used Vector math to calculate the angle between player and mouse.
* **Created Bullets:** Built a prefab class that spawns at the player's location.
* **Added Fire Rate:** Prevented bullet spam using `pygame.time.get_ticks()`.
* **Handled Destruction:** Used `groupcollide` to destroy enemies and bullets simultaneously upon impact.

---

## 💻 SOURCE CODE

> [!example]- SHOOTING LOGIC
> ```python
> def shoot(self):
>     now = pygame.time.get_ticks()
>     if now - self.last_shot > self.cooldown:
>         self.last_shot = now
>         
>         # Math
>         dir_vec = (mouse_pos - self.pos).normalize()
>         bullet = Bullet(self.pos, dir_vec)
>         all_sprites.add(bullet)
> ```

---

## 🧠 LEARNED TODAY

* **Prefab Instantiation:** Creating objects inside the game loop (like `Bullet()`) is normal. Just make sure you delete them later (`kill()`) or you'll leak memory.
* **Sprite Management:** Adding a bullet to `all_sprites` (for drawing) AND `bullets_group` (for collision) is the correct pattern.

---

## 🎯 GOALS FOR TOMORROW

> [!todo] 💾 **Day 17: Saving & Loading Highscores**
> * Learn File I/O (Input/Output).
> * Save your High Score to a `.txt` or `.json` file.
> * Load it back when the game starts so data persists after closing the game.
