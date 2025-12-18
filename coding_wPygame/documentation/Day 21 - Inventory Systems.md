Tags: [[Programming]], [[Python]], [[PyGame]], [[Game]]

---
### 1) Learning Goal

You will learn to manage **Game Data** (lists of items) separate from **Game Objects** (sprites on the ground), and how to render a **UI Overlay** that pauses the game logic while you manage your gear.

### 2) Clear Overview

- **The World Item:** A sprite on the ground. When you touch it, it disappears (`kill()`). 
- **The Backend (Data):** When the sprite dies, we add a string or dictionary to a list: `inventory.append("Gold Coin")`.
- **The Frontend (UI):** When you press **'I'**, we stop moving and draw a grid of gray boxes. Inside those boxes, we draw the names of the items in your list.

### 3) Deep Explanation

**A. The Data Structure**
An inventory is usually a list.

- **Simple:** `inv = ["Sword", "Potion", "Key"]`
- Advanced: inv = [{"name": "Sword", "dmg": 10}, {"name": "Potion", "heal": 50}]

We will stick to the Simple version today.    

**B. The Toggling Logic**
We need a boolean flag: show_inventory = False.

- In the event loop:

    ``` Python 
    if event.key == pygame.K_i:
        show_inventory = not show_inventory
    ```

- In the Update loop:
    
    ``` Python
    if show_inventory:
        draw_inventory()
    else:
            update_game()
    ```
    
_This acts like a pause screen!_
    

**C. The UI Loop**
To draw the inventory, we don't just print the list. We iterate through the list and draw them in slots.

- Slot 1: (100, 100)
- Slot 2: (100, 150)    
- Slot 3: (100, 200)

### 4) Runnable Pygame Code Example

Here is an **Inventory Demo**.

- **WASD:** Move.
- **Walk over Items:** Pick them up (Green = Potion, Yellow = Coin).
- **Press 'I':** Open Inventory (Game pauses).


``` Python
import pygame, sys, random

# 1. Setup
pygame.init()
SCREEN_W, SCREEN_H = 800, 600
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# --- CLASSES ---
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((0, 100, 255)) # Blue
        self.rect = self.image.get_rect(center=(400, 300))
        self.pos = pygame.math.Vector2(400, 300)
        self.speed = 300
        
        # THE BACKPACK
        self.inventory = [] 
        self.capacity = 5

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

class Item(pygame.sprite.Sprite):
    def __init__(self, name, color):
        super().__init__()
        self.name = name
        self.image = pygame.Surface((20, 20))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, 750)
        self.rect.y = random.randint(50, 550)

# --- SETUP ---
player = Player()
all_sprites = pygame.sprite.Group(player)
items_group = pygame.sprite.Group()

# Create some random items
for i in range(3):
    item = Item("Potion", (0, 255, 0)) # Green
    items_group.add(item)
    all_sprites.add(item)

for i in range(3):
    item = Item("Coin", (255, 255, 0)) # Yellow
    items_group.add(item)
    all_sprites.add(item)

# Game State
show_inventory = False

# --- UI DRAW FUNCTION ---
def draw_inventory_ui(surface, inventory):
    # 1. Dim the background
    overlay = pygame.Surface((SCREEN_W, SCREEN_H))
    overlay.set_alpha(150)
    overlay.fill((0, 0, 0))
    surface.blit(overlay, (0, 0))
    
    # 2. Draw the Box
    panel_rect = pygame.Rect(200, 100, 400, 400)
    pygame.draw.rect(surface, (50, 50, 50), panel_rect)
    pygame.draw.rect(surface, (200, 200, 200), panel_rect, 3) # Border
    
    # 3. Draw Title
    title = font.render("INVENTORY", True, (255, 255, 255))
    surface.blit(title, (340, 110))
    
    # 4. Draw Items
    y_offset = 160
    for i, item_name in enumerate(inventory):
        # Draw Text
        text = font.render(f"{i+1}. {item_name}", True, (255, 255, 255))
        surface.blit(text, (220, y_offset))
        y_offset += 40
        
    # 5. Draw "Empty" slots if needed
    if len(inventory) == 0:
        empty = font.render("(Empty)", True, (150, 150, 150))
        surface.blit(empty, (220, 160))

# --- GAME LOOP ---
while True:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # TOGGLE INVENTORY
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                show_inventory = not show_inventory

    # LOGIC (Only run if inventory is CLOSED)
    if not show_inventory:
        player.update(dt)
        
        # Check Item Pickup
        hit_list = pygame.sprite.spritecollide(player, items_group, True) # True = Kill sprite
        for item in hit_list:
            if len(player.inventory) < player.capacity:
                player.inventory.append(item.name)
                print(f"Picked up: {item.name}")
            else:
                print("Inventory Full!")
                # (Ideally you wouldn't kill the sprite here if full, but keeping it simple)

    # DRAWING
    screen.fill((30, 30, 30))
    all_sprites.draw(screen)
    
    # Draw UI on TOP
    if show_inventory:
        draw_inventory_ui(screen, player.inventory)
    else:
        hint = font.render("Press 'I' for Inventory", True, (255, 255, 255))
        screen.blit(hint, (10, 10))

    pygame.display.update()
```

---

### 5) 20-Minute Drill

**Your Task:** Implement **Item Dropping**.

1. In the `draw_inventory_ui` function, add a note: "Press 1-5 to Drop".
    
2. In the Event Loop (inside `if show_inventory:`), listen for number keys (`K_1`, `K_2`, etc.).
    
3. If `K_1` is pressed:
    
    - Check if `len(player.inventory) >= 1`.
        
    - If yes, remove item: `dropped = player.inventory.pop(0)`.
        
    - Spawn a new `Item` sprite at the player's location with that name.
        

_This completes the cycle: World -> Backpack -> World._

---

### 6) Quick Quiz

1. **Why do we use `show_inventory = not show_inventory`?**
    
2. **Does the `player.inventory` list store the Sprite objects or just strings?**
    
3. **Why do we draw the UI _after_ `all_sprites.draw(screen)`?**
    

**Answers:**

1. It toggles the boolean. If True, it becomes False. If False, it becomes True. Perfect for on/off switches.
    
2. **Strings** (in this example). Storing the Sprite object is risky because Sprites usually have coordinates, which doesn't make sense inside a backpack.
    
3. Because of the **Painter's Algorithm**. If we drew the UI first, the game characters would be drawn on top of the menu!
    

---

### 7) Homework for Tomorrow

**Add "Consumables".**

- Create a Potion item.
    
- When you open the inventory and press the key to "Use" it:
    
    1. Remove it from the list.
        
    2. Add +50 to `player.health`.
        
    3. Don't drop it on the ground; delete it permanently.
        

---

### 8) Progress to Mastery

🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩⬜⬜⬜⬜⬜⬜⬜⬜⬜ **70%**

---

### 9) Obsidian Note

## 🧠 CONCEPT SUMMARY

#### Data vs. Visuals:
An item in the world is a **Sprite** (image + rect). An item in the inventory is usually just **Data** (string or dict).
> [!note] The Cycle
> 1.  **Pickup:** Sprite collides -> `kill()` sprite -> Add data to List.
> 2.  **Drop:** Remove data from List -> Spawn new Sprite -> Set position to Player.

#### UI State:
The inventory is a separate Game State, similar to "Paused".
* **Logic:** When open, we pause the world update (so enemies don't kill you while reading).
* **Rendering:** We draw a semi-transparent overlay to dim the game, then draw the menu on top.

#### List Management:
* `append(item)`: Adds to the end.
* `pop(index)`: Removes item at specific index (and returns it).
* `len(list)`: Used to check Capacity (e.g., `if len(inv) < 5`).

---

## 🛠️ WHAT I DID TODAY

* **Created an Inventory List:** Added `self.inventory = []` to the player.
* **Implemented Pickup:** Used `spritecollide` to detect items, remove them from the world, and store their names.
* **Built a UI Overlay:** Created a function that draws a gray box and iterates through the list to render text names.
* **Added Toggling:** Used the `I` key to switch between Gameplay and Menu states.

---

## 💻 SOURCE CODE

> [!example]- INVENTORY TOGGLE
> ```python
> # Event Loop
> if event.key == pygame.K_i:
>     show_inv = not show_inv
> 
> # Main Loop
> if show_inv:
>     draw_menu()
> else:
>     update_game()
> ```

---

## 🧠 LEARNED TODAY

* **Separation of Concerns:** The item in your backpack doesn't need an X/Y coordinate. It just needs a Name and Stats. We strip away the physics when we pick it up.
* **Layering:** UI must always be the last thing drawn in the frame loop.

---

## 🎯 GOALS FOR TOMORROW

> [!todo] 📊 **Day 22: RPG Stats & Health Bars**
> * Create a sleek GUI Health Bar (Green bar over Red background).
> * Implement XP and Leveling Up.
> * Display stats on screen (STR, DEX, HP).
