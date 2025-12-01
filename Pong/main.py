""""
PONG GAME — TO-DO LIST
----------------------

TODO:
    📌 STAGE 1 — BASE SETUP
        - Create the main game window (size, caption, FPS) [DONE]
        - Initialize Pygame, Clock(), and delta time (dt) 
        - Create the game loop structure (running = True) [DONE]
        - Clear screen + update display every frame [DONE]

    📌 STAGE 2 — OBJECT CREATION
        - Create paddle rectangles (left & right)
        - Create ball rectangle
        - Add variables for paddle speed (px/s)
        - Add variables for ball speed (px/s) + direction vector

    📌 STAGE 3 — PADDLE MOVEMENT
        - Implement player controls for left paddle (W/S or ↑/↓)
        - Make paddle movement use delta time (time-based)
        - Prevent paddles from leaving screen boundaries

    📌 STAGE 4 — BALL PHYSICS
        - Move the ball using dt (ball_pos_x, ball_pos_y as floats)
        - Detect collision with top and bottom walls → bounce
        - Detect collision with paddles → bounce horizontally
        - Add ball speed increase after each paddle hit (optional)

    📌 STAGE 5 — SCORING SYSTEM
        - Detect when ball exits left/right screen
        - Add score counters for Player 1 and Player 2
        - Reset ball to center when a point is scored
        - Serve the ball toward the player who was scored on

    📌 STAGE 6 — GAME POLISH
        - Add center dividing line
        - Add text rendering for scores
        - Add game restart on SPACE
        - Add simple sound effects (bounce, score) (optional)

    📌 STAGE 7 — EXTRA FEATURES (Optional)
        - Add difficulty settings (ball speed, paddle speed)
        - Add AI/bot for Player 2 (easy/medium/hard)
        - Add smooth paddle acceleration instead of instant movement
        - Add color themes (classic, neon, dark mode)
        - Add FPS + dt display for debugging
        - Add main menu screen
"""""

# ================================= MAIN CODE ===================================

# importing libraries
import pygame
import sys
import pygame.font
from pygame.locals import *
from pygame.time import Clock

def main():

    # initialize the pygame
    pygame.init()

    # font
    font = pygame.font.SysFont(None, 32)

    # display
    WINDOW_WIDTH = 600
    WINDOW_HEIGHT = 700
    DISPLAY = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

    # clock
    clock = Clock()
    FPS = 60

    # player object
    PLAYER_OBJ = pygame.Rect(200,600,200,25)

    # color
    PLAYER_COLOR = (0,0,0)

    # text render
    text_surface = font.render(f"FPS: {int(clock.get_fps())}", True, (0,0,0))
    text_rect = text_surface.get_rect()

    # movements
    M_left = False
    M_right = False

    # movement speed
    MOVEMENT_SPEED = 1

    # game loop
    while True:

        for event in pygame.event.get():

            # check for quit
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            # down
            if event.type == KEYDOWN:

                if event.key == K_LEFT or event.key == K_a:
                    M_left = True

                if event.key == K_RIGHT or event.key == K_d:
                    M_right = True

            # up
            if event.type == KEYUP:

                if event.key == K_LEFT or event.key == K_a:
                    M_left = False

                if event.key == K_RIGHT or event.key == K_d:
                    M_right = False


        # movement logic

        if M_left:
            PLAYER_OBJ.x -= MOVEMENT_SPEED

        if M_right:
            PLAYER_OBJ.x += MOVEMENT_SPEED

        if PLAYER_OBJ.left < 0:
            PLAYER_OBJ.left = 0

        DISPLAY.fill((255,255,255))
        DISPLAY.blit(text_surface, text_rect)

        pygame.draw.rect(DISPLAY,PLAYER_COLOR, PLAYER_OBJ)
        pygame.display.update()



if __name__ == "__main__":
    main()