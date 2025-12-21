Tags: [[Programming]], [[Python]], [[PyGame]], [[Game]]

---
### 1) Learning Goal

You will learn to create an **Interaction System** where the game detects when the player is close to an NPC, displays a prompt ("Press E"), and opens a **Dialog Box** when triggered.

### 2) Clear Overview

- **The NPC:** A sprite that stands still but holds data (text lines).
    
- **The Trigger:** We use **Vector Math** (Distance) to check proximity.
    
    - `Distance < 50 pixels` $\rightarrow$ Show "Press E".
        
- **The Dialog State:** A simple boolean flag (`show_dialog`).
    
    - `True`: Draw the Blue Box and Text.
    - `False`: Draw the game normally.

### 3) Deep Explanation

**A. Proximity Detection**

We don't need complex collision boxes for talking. We just need the distance between center points.

dist = (player.pos - npc.pos).length()

**B. Input Debouncing (The "Chatter" Bug)**

If you put if keys [K_e]: toggle_dialog() inside the main loop, the dialog will flash open and closed 60 times a second because the computer is too fast.

- **Fix:** Use the `KEYDOWN` event (fires once per press) instead of `pygame.key.get_pressed()` (fires while held).

**C. The UI Layer**

Just like the Health Bar, the Dialog Box is drawn last.

1. Draw World.
2. Draw Player/NPC.
3. Draw Dialog Overlay.

### 4) Runnable Pygame Code Example

This code features a **Player (Blue)** and an **NPC (Yellow)**.

- **Walk close** to the NPC to see the "!" prompt.
- **Press E** to open the chat.    
- **Press E** again to close it.

```  Python
import pygame, sys

# 1. Setup
pygame.init()
SCREEN_W, SCREEN_H = 800, 600
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)
tip_font = pygame.font.SysFont("Arial", 16, bold=True)

# --- CLASSES ---
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((0, 100, 255)) # Blue
        self.rect = self.image.get_rect(center=(200, 300))
        self.pos = pygame.math.Vector2(200, 300)
        self.speed = 300

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

class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y, text):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 200, 0)) # Yellow
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = pygame.math.Vector2(x, y)
        self.text = text # What this NPC says

# --- UI FUNCTIONS ---
def draw_dialog_box(surface, text):
    # 1. The Box Background
    box_rect = pygame.Rect(50, 450, 700, 100)
    pygame.draw.rect(surface, (0, 0, 0), box_rect) # Black bg
    pygame.draw.rect(surface, (255, 255, 255), box_rect, 3) # White border
    
    # 2. The Text
    # (Simple render, no wrapping for now)
    text_surf = font.render(text, True, (255, 255, 255))
    surface.blit(text_surf, (70, 470))
    
    # 3. Instruction
    hint = tip_font.render("[Press E to Close]", True, (150, 150, 150))
    surface.blit(hint, (600, 520))

# --- MAIN LOOP ---
player = Player()
npc = NPC(600, 300, "Greetings, traveler! Welcome to Pygame.")
all_sprites = pygame.sprite.Group(player, npc)

dialog_active = False
active_text = ""

while True:
    dt = clock.tick(60) / 1000

    # 1. Check Proximity
    dist = (player.pos - npc.pos).length()
    can_interact = dist < 70

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        # INTERACTION INPUT (Event-based, not Polling)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                if dialog_active:
                    dialog_active = False # Close it
                elif can_interact:
                    dialog_active = True  # Open it
                    active_text = npc.text

    # Update (Stop moving if reading!)
    if not dialog_active:
        player.update(dt)

    # Drawing
    screen.fill((30, 30, 30))
    all_sprites.draw(screen)
    
    # Draw Interaction Prompt
    if can_interact and not dialog_active:
        prompt = tip_font.render("[E] TALK", True, (255, 255, 255))
        # Draw above NPC head
        screen.blit(prompt, (npc.rect.centerx - 20, npc.rect.top - 20))

    # Draw Dialog UI
    if dialog_active:
        draw_dialog_box(screen, active_text)

    pygame.display.update()
```

### 5) 20-Minute Drill

**Task: Multi-Page Dialog (The "Next" Button)**

1. Change `npc.text` to a **List**: `["Hello!", "I have a quest.", "Find the Red Gem."]`
2. Add a variable `self.dialog_index = 0` to the Main Loop logic.
3. **Logic:** When **E** is pressed while `dialog_active` is True:
    
    - Increment `dialog_index`.
    - If `dialog_index < len(npc.text)`, show the next line.
    - Else (if we ran out of lines), close the dialog and reset index to 0.

### 6) Quick Quiz

1. **Why do we stop calling `player.update(dt)` when `dialog_active` is True?**
2. **Why use `KEYDOWN` event for 'E' instead of `pygame.key.get_pressed()`?**
3. **If `dist` calculates the distance in pixels, what does `dist < 70` represent?**

**Answers:**

1. To pause the game state so the player doesn't walk away while reading.
2. To prevent the box from flickering open/closed 60 times a second (Debouncing).
3. The "Interaction Radius" (invisible circle) around the NPC.

### 7) Homework for Tomorrow

**Create a "Quest Giver".**

- Add a variable `has_quest = False` to the Player.
- Talk to the NPC. On the last line of dialog, set `player.has_quest = True`.
- If you talk to them _again_, check `if player.has_quest`:
    
    - If True, say: "Good luck on your quest!"
    - If False, say: "Please help me."

### 8) Progress to Mastery

🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩⬜⬜⬜⬜⬜⬜ **76%**

### 9) Obsidian Note

## 🧠 CONCEPT SUMMARY

#### Proximity Checks
Instead of using collision (touching), interactions often use **Distance Checks**.
> [!note] Formula
> `if (player.pos - target.pos).length() < radius:`

#### Game States (Micro-States)
We used a simple boolean (`dialog_active`) to create a sub-state.
* **Normal State:** Player moves, prompt appears if close.
* **Dialog State:** Player input moves text forward, movement physics are paused.

#### Event vs. Polling
* **Polling (`get_pressed`)**: Good for continuous movement (holding W).
* **Events (`KEYDOWN`)**: Good for toggles (Press E to Open/Close). Using polling here causes the "Machine Gun Effect" (toggling on/off every frame).

---

## 🛠️ WHAT I DID TODAY
* **Built an NPC:** Created a static sprite class holding text data.
* **Implemented Interaction:** Used vector math to detect when the player is within "Talking Range."
* **Created a GUI Overlay:** Drew a text box on top of the game world that pauses gameplay logic when active.

---

## 💻 SOURCE CODE
> [!example]- INTERACTION LOGIC
> ```python
> # 1. Check Distance
> dist = (player.pos - npc.pos).length()
> 
> # 2. Input Handling
> if event.key == K_e:
>     if dialog_open:
>         dialog_open = False # Close
>     elif dist < 50:
>         dialog_open = True  # Open
> ```

---

## 🎯 GOALS FOR TOMORROW
> [!todo] ✨ **Day 24: Game Polish (Screenshake & Particles)**
> * Implement "Juice": Making interactions feel powerful.
> * Add Screenshake when taking damage.
> * Add Flash effects (white screen flash) on critical hits.
