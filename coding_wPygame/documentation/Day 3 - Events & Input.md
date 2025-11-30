Tags: [[Programming]], [[PyGame]], [[Python]], [[Game]]

---
### LAST TIME

Since we have built a window (Day 1) and drawn shapes/images (Day 2). Today, we're going to be bring life into our codes game by making it interactive. We are going to learn how to control objects using the **Keyboard** and **Mouse**.

#### 1) Learning Goal

we will learn to detect specific user inputs (key presses, mouse movement, clicks) and use them to control the position and color of objects on the screen.

#### 2) Clear Overview

Up until now, our games have been like movies, they just run. To make them games, we need to listen for **Events**.

- **Keyboard Events:** `KEYDOWN` (press) and `KEYUP` (release).
- **Mouse Events:** `MOUSEMOTION` (movement) and `MOUSEBUTTONDOWN` (click).

#### 3) Deep Explanation

**A. The Event Loop Revisited** We already know `for event in pygame.event.get():`. This loop grabs every single thing the user did since the last frame. Today, we stop ignoring everything except `QUIT` and start looking for other specific event types.

**B. Keyboard Input (`KEYDOWN` vs. `KEYUP`)**

- **`KEYDOWN`**: Fired _once_ the moment a key is pushed down. Good for toggles (like pausing) or single actions (like jumping).
- **`KEYUP`**: Fired _once_ the moment a key is released. Good for stopping movement.  
- **`event.key`**: When a key event happens, we check `event.key` to see _which_ key it was (e.g., `K_LEFT`, `K_SPACE`, `K_a`).

**C. Mouse Input**

- **`MOUSEMOTION`**: Fired constantly as the mouse moves. It gives us `event.pos` (the x, y coordinates).
- **`MOUSEBUTTONDOWN`**: Fired when a button is clicked. It also gives us `event.pos`.

**D. Continuous Movement** If you want a character to move _while_ a key is held down, you can't just rely on `KEYDOWN` (which only fires once). Instead, you use `KEYDOWN` to set a variable (like `moving_left = True`) and `KEYUP` to unset it (`moving_left = False`). Then, in Our game loop, you move the character if the variable is true.

---

#### 4) Runnable Pygame Code Example

This code lets you move a **Blue Square** with the **Arrow Keys** and a **Red Circle** with the **Mouse**.


``` python
import pygame, sys
from pygame.locals import *

# 1. Setup
pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Day 3: Events & Input")

# 2. Variables for our Objects
# Player (Square) - Controlled by Keyboard
player_rect = pygame.Rect(300, 200, 50, 50) 
move_left = False
move_right = False
move_up = False
move_down = False
MOVESPEED = 5

# Cursor (Circle) - Controlled by Mouse
mouse_pos = (0, 0)

while True:
    # --- Event Loop ---
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # Keyboard Events: Key Pressed Down
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                move_left = True
            if event.key == K_RIGHT:
                move_right = True
            if event.key == K_UP:
                move_up = True
            if event.key == K_DOWN:
                move_down = True

        # Keyboard Events: Key Released
        if event.type == KEYUP:
            if event.key == K_LEFT:
                move_left = False
            if event.key == K_RIGHT:
                move_right = False
            if event.key == K_UP:
                move_up = False
            if event.key == K_DOWN:
                move_down = False

        # Mouse Events: Movement
        if event.type == MOUSEMOTION:
            mouse_pos = event.pos # Update tuple (x, y)

    # --- Game Logic (Movement) ---
    # Move the player if the flags are True
    if move_left:
        player_rect.x -= MOVESPEED
    if move_right:
        player_rect.x += MOVESPEED
    if move_up:
        player_rect.y -= MOVESPEED
    if move_down:
        player_rect.y += MOVESPEED

    # --- Drawing ---
    screen.fill((0, 0, 0)) # Clear screen

    # Draw Keyboard Player (Blue Square)
    pygame.draw.rect(screen, (0, 0, 255), player_rect)

    # Draw Mouse Cursor (Red Circle)
    pygame.draw.circle(screen, (255, 0, 0), mouse_pos, 20)

    pygame.display.update()
```

---

#### 5) 20-Minute Drill

**Your Task:** Modify the code above to add a "Teleport" feature.

1. When the user presses the **Spacebar**, the Blue Square should instantly jump to the center of the screen `(300, 200)`.

2. When the user clicks the **Mouse Button**, the Red Circle should change color to **Green**. (Hint: You'll need a variable for color).

---

#### 6) Quick Quiz

1. **Which event type happens when you let go of a key?**
2. **Why do we use boolean variables (like `move_left`) instead of moving the character directly inside the `KEYDOWN` event?**
3. **How do you get the (x, y) coordinates of the mouse from a `MOUSEMOTION` event?**

**Answers:**

1. `KEYUP`
2. `KEYDOWN` only triggers _once_ when you first press the key. Boolean variables allow us to keep moving smoothly as long as the key is held down.
3. `event.pos`

---
#### 7) Homework for Tomorrow

Create a program where a square moves automatically (like a DVD screensaver).

- If it hits the edge of the screen, it should bounce back.    
- **Bonus:** Allow the user to reverse its direction by pressing `SPACE`.

---
#### 8) Progress to Mastery

🟩🟩🟩⬜⬜⬜⬜⬜⬜⬜ **10%**

---

#### 9) Obsidian Note

## 🧠 CONCEPT SUMMARY

#### Event Types:

Pygame generates specific events for user actions. We check `event.type` to differentiate them.

- `KEYDOWN`: Key is pressed (fires once).    
- `KEYUP`: Key is released (fires once).
- `MOUSEMOTION`: Mouse is moved.
- `MOUSEBUTTONDOWN`: Mouse button is clicked.

> [!note] NOTE
> We access _which_ key was pressed using `event.key` (e.g., `K_SPACE`) and _where_ the mouse is using `event.pos`.

#### Continuous Movement (Flags):

To move a character smoothly while a key is held, we don't move it inside the event loop. Instead, we use `KEYDOWN` to set a **flag** (e.g., `moving = True`) and `KEYUP` to unset it.

#### Boundary Checking & Collision:

To keep an object inside the window, we check its coordinates. If it goes past a wall (e.g., `left < 0`), we reset its position and apply a reaction (like a bounce or stop).

---

## 🛠️ WHAT I DID TODAY

- **Handled Keyboard Input:** Created a system to detect arrow key/WASD presses (`KEYDOWN`) and releases (`KEYUP`).    
- **Fixed Logic Bugs:** Learned that `if key == K_a or K_b:` is wrong; it must be `if key == K_a or key == K_b:`.
- **Implemented Smooth Movement:** Used boolean flags (`M_left`, `M_right`, etc.) to allow the square to move continuously.
- **Added Mouse Interaction:** Used `MOUSEMOTION` to track the cursor and `MOUSEBUTTON` to change colors.
- **Created Barriers:** Implemented logic to detect wall hits and push the player back (`BOUNCE`).

---
## SOURCE CODE

> [!example]- SOURCE CODE
> 
> ```python
> """
> Day 3 - Keyboard & Mouse Input + Bounce Movement
> Today I learned how to detect key presses, key releases,
> mouse movement, mouse clicks, and how to move a square on screen.
> """
> 
> import sys
> import pygame
> from pygame.locals import *
> 
> def main():
> 
>     # initializing pygame, this has to be called before anything else
>     pygame.init()
> 
>     # basically my window setup
>     # width = 600, height = 500
>     WINDOW_WIDTH = 600
>     WINDOW_HEIGHT = 500
>     DISPLAY = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
> 
>     # this is my blue square (player)
>     # it starts at x = 200, y = 200 and is 50x50 in size
>     PLAYER_RECT = pygame.Rect(200, 200, 50, 50)
> 
>     # these booleans are like switches I turn ON/OFF depending on
>     # what keys I'm pressing. I use them later to move the square.
>     M_left = False
>     M_right = False
>     M_up = False
>     M_down = False
> 
>     # how fast the player moves per frame
>     MOVEMENT_SPEED = 1
> 
>     # how strong the bounce is when the square hits a wall
>     # (just my idea to make it bounce back)
>     BOUNCE = 10
> 
>     # mouse related variables
>     # mouse_pos tracks where my mouse currently is
>     # cursor_color changes depending on if I'm clicking or not
>     mouse_pos = (0, 0)
>     cursor_color = (255, 0, 0)
> 
>     # the game loop, this is what keeps everything running forever
>     while True:
> 
>         # event handling section
>         # this checks every little thing the user does (keyboard, mouse, quit)
>         for event in pygame.event.get():
> 
>             # if the user presses the close button, quit the whole program
>             if event.type == QUIT:
>                 pygame.quit()
>                 sys.exit()
> 
>             # runs only ONCE when I initially press a key
>             if event.type == KEYDOWN:
> 
>                 # turning on the movement booleans (meaning I'm holding the key)
>                 if event.key == K_LEFT or event.key == K_a:
>                     M_left = True
>                 if event.key == K_RIGHT or event.key == K_d:
>                     M_right = True
>                 if event.key == K_UP or event.key == K_w:
>                     M_up = True
>                 if event.key == K_DOWN or event.key == K_s:
>                     M_down = True
> 
>                 # spacebar instantly teleports the square to the center
>                 if event.key == K_SPACE:
>                     PLAYER_RECT.center = (300, 250)
> 
>             # runs only ONCE when I release the key
>             # this stops the movement in that direction
>             if event.type == KEYUP:
> 
>                 if event.key == K_LEFT or event.key == K_a:
>                     M_left = False
>                 if event.key == K_RIGHT or event.key == K_d:
>                     M_right = False
>                 if event.key == K_UP or event.key == K_w:
>                     M_up = False
>                 if event.key == K_DOWN or event.key == K_s:
>                     M_down = False
> 
>             # when I move the mouse, I store its current position
>             if event.type == MOUSEMOTION:
>                 mouse_pos = event.pos
> 
>             # clicking the mouse button turns the circle green
>             if event.type == MOUSEBUTTONDOWN:
>                 cursor_color = (0, 255, 0)
> 
>             # releasing the mouse button makes it red again
>             elif event.type == MOUSEBUTTONUP:
>                 cursor_color = (255, 0, 0)
> 
>         # ================================================================
>        # MOVEMENT LOGIC (This part actually moves the square every frame)
>        # ================================================================
> 
>         if M_left:
>             PLAYER_RECT.x -= MOVEMENT_SPEED
>         if M_right:
>             PLAYER_RECT.x += MOVEMENT_SPEED
>         if M_up:
>             PLAYER_RECT.y -= MOVEMENT_SPEED
>         if M_down:
>             PLAYER_RECT.y += MOVEMENT_SPEED
> 
>         # ================================================================
>         # BOUNCE LOGIC (simple bounce system)
>         # idea: if the square hits the border, push it back inside
>         # ================================================================
> 
>         # hitting the left wall
>         if PLAYER_RECT.left < 0:
>             PLAYER_RECT.left = 0
>             PLAYER_RECT.x += BOUNCE
> 
>         # hitting the right wall
>         if PLAYER_RECT.right > WINDOW_WIDTH:
>             PLAYER_RECT.right = WINDOW_WIDTH
>             PLAYER_RECT.x -= BOUNCE
> 
>         # hitting the top wall
>         if PLAYER_RECT.top < 0:
>             PLAYER_RECT.top = 0
>             PLAYER_RECT.y += BOUNCE
> 
>         # hitting the bottom wall
>         if PLAYER_RECT.bottom > WINDOW_HEIGHT:
>             PLAYER_RECT.bottom = WINDOW_HEIGHT
>             PLAYER_RECT.y -= BOUNCE
> 
>         # ================================================================
>         # DRAWING SECTION
>         # This is where all visual things are drawn every frame
>         # ================================================================
> 
>         DISPLAY.fill((255, 255, 255))  # clear the screen to white
> 
>         # the blue square
>         pygame.draw.rect(DISPLAY, (0, 0, 255), PLAYER_RECT)
> 
>         # circle that follows the mouse
>         pygame.draw.circle(DISPLAY, cursor_color, mouse_pos, 20)
> 
>         pygame.display.update()  # refresh to show everything
> 
> # program starts here
> if __name__ == "__main__":
>     main()
> ```

---

## 🧠 LEARNED TODAY

- **Logical Operators:** When checking multiple keys, you must be explicit: `if key == A or key == B`. Python does not understand `if key == A or B`.
    
- **Event Logic:** `KEYDOWN` happens once. For movement, we use it to toggle a variable (`M_left = True`) so the game loop keeps moving the player until `KEYUP` sets it to `False`.
    
- **Physics vs Direct:** We learned about Velocity (speed + direction) as a way to handle smoother bouncing, versus Direct movement (teleporting the rect).
    

---

## 🧪 PRACTICE / EXERCISES

**Exercise: Teleport & Color Change** Goal: Spacebar resets position; Click changes color.

``` python
# Inside Event Loop:
if event.type == KEYDOWN:
    if event.key == K_SPACE:
        PLAYER_RECT.center = (300, 200) # Teleport

if event.type == MOUSEBUTTONDOWN:
    cursor_color = (0, 255, 0) # Change to Green
elif event.type == MOUSEBUTTONUP:
    cursor_color = (255, 0, 0) # Revert to Red
```

---

## 💡 NOTES TO SELF

> [!important] IMPORTANT
> 
> Keyboard Input: `KEYDOWN` fires only once per press. For continuous movement (walking), use flags/booleans or velocity logic.

> [!important] IMPORTANT
> 
> Mouse Input: `MOUSEMOTION` fires constantly when moving. `MOUSEBUTTONDOWN` fires once per click.

---

## 🎯 GOALS FOR TOMORROW

> [!todo] ⏱️ **Day 4: FPS, Time, & Delta Time**
> 
> - Learn to control the game speed using `pygame.time.Clock`.
>     
> - Understand Frame Rate (FPS).
>     
> - Learn why "Delta Time" is crucial for smooth movement on different computers.

