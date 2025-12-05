import pygame
import sys

from pygame.locals import *
from pygame.math import Vector2
from pygame.time import Clock

class Main:
    """
    Main game class:
    - Initializes display, clock, and player variables
    - Handles isometric conversion
    - Draws grid and players
    - Handles input and normalized movement
    """

    def __init__(self):
        """
        Initialize all game-related variables, display, and clock.
        This keeps setup in one clean place.
        """

        # ------------------------
        # DISPLAY SETUP
        # ------------------------
        self.DISPLAY_WIDTH = 800
        self.DISPLAY_HEIGHT = 600

        # Create the display window
        self.DISPLAY = pygame.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))
        pygame.display.set_caption("DAY8: 2D ISOMETRIC DRID & VECTOR DEMO")

        # ------------------------
        # CLOCK & FPS
        # ------------------------
        self.CLOCK = Clock()  # Clock object to control FPS
        self.FPS = 60         # Target frames per second

        # ------------------------
        # PLAYER SETUP
        # ------------------------
        self.PLAYER_SPEED = 200       # Movement speed in pixels per second

        # Green player uses Vector2 for proper normalized movement
        self.player_pos = Vector2(400, 300)

        # Red "bad" player as a simple list (non-normalized, moves faster diagonally)
        self.bad_pos = [400, 300]

        # ------------------------
        # GRID SETTINGS
        # ------------------------
        self.tile_size = 30           # Size of each diamond tile in pixels
        self.grid_rows = 20           # Number of rows in the grid
        self.grid_cols = 20           # Number of columns in the grid

        # ------------------------
        # COLORS
        # ------------------------
        self.bg_color = (0, 0, 0)     # Background color (black)
        self.grid_color = (255, 255, 255)  # Grid color (white)

    # ------------------------------
    # HELPER FUNCTIONS
    # ------------------------------

    def to_iso(self, x, y):
        """
        Convert Cartesian (top-down) coordinates to isometric screen coordinates.

        Parameters:
        - x: X-coordinate in grid/cartesian space
        - y: Y-coordinate in grid/cartesian space

        Returns:
        - iso_x, iso_y: screen coordinates in isometric projection

        Isometric conversion:
        - iso_x = x - y     (horizontal displacement)
        - iso_y = (x + y)/2 (vertical displacement with 50% vertical squish)
        """
        iso_x = (x - y)
        iso_y = (x + y) / 2
        return iso_x, iso_y

    def draw_iso_grid(self):
        """
        Draw a white isometric grid of diamond tiles.

        The grid is drawn by iterating through all rows and columns,
        calculating isometric positions, and drawing diamonds as polygons.
        """
        for r in range(self.grid_rows):     # Loop through rows
            for c in range(self.grid_cols): # Loop through columns
                # Cartesian coordinates for this grid point
                x = c * self.tile_size
                y = r * self.tile_size

                # Convert to isometric coordinates
                iso_x, iso_y = self.to_iso(x, y)

                # Center the grid horizontally and offset vertically
                iso_x += self.DISPLAY_WIDTH // 2
                iso_y += 50

                # Define the 4 points of the diamond (top, right, bottom, left)
                points = [
                    (iso_x, iso_y - self.tile_size / 4),      # Top vertex
                    (iso_x + self.tile_size / 2, iso_y),      # Right vertex
                    (iso_x, iso_y + self.tile_size / 4),      # Bottom vertex
                    (iso_x - self.tile_size / 2, iso_y)       # Left vertex
                ]

                # Draw the diamond outline
                pygame.draw.polygon(self.DISPLAY, self.grid_color, points, 1)

    # ------------------------------
    # MAIN GAME LOOP
    # ------------------------------

    def run(self):
        """Main game loop: handles input, movement, and drawing every frame."""
        while True:

            # ------------------------
            # DELTA TIME
            # ------------------------
            # Calculate time (in seconds) since last frame
            dt = self.CLOCK.tick(self.FPS) / 1000

            # ------------------------
            # EVENT HANDLING
            # ------------------------
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()  # Close pygame
                    sys.exit()     # Exit program

            # ------------------------
            # INPUT HANDLING
            # ------------------------
            keys = pygame.key.get_pressed()   # Get state of all keys
            input_vector = Vector2(0, 0)      # Reset input vector each frame

            # Move left
            if keys[K_LEFT]:
                input_vector.x -= 1
                self.bad_pos[0] -= self.PLAYER_SPEED * dt  # Red player moves faster diagonally
                print("left key is pressed")

            # Move right
            if keys[K_RIGHT]:
                input_vector.x += 1
                self.bad_pos[0] += self.PLAYER_SPEED * dt
                print("right key is pressed")

            # Move up
            if keys[K_UP]:
                input_vector.y -= 1
                self.bad_pos[1] -= self.PLAYER_SPEED * dt
                print("up key is pressed")

            # Move down
            if keys[K_DOWN]:
                input_vector.y += 1
                self.bad_pos[1] += self.PLAYER_SPEED * dt
                print("down key is pressed")


            # ------------------------
            # NORMALIZED MOVEMENT
            # ------------------------
            if input_vector.length() > 0:
                # Normalize vector so diagonal movement is not faster
                input_vector = input_vector.normalize()

                # Apply movement scaled by speed and delta time
                self.player_pos += input_vector * self.PLAYER_SPEED * dt

            # ------------------------
            # CONVERT PLAYER POSITIONS TO ISOMETRIC
            # ------------------------
            # Green player
            iso_px, iso_py = self.to_iso(self.player_pos.x, self.player_pos.y)
            iso_px += self.DISPLAY_WIDTH // 2
            iso_py += 50

            # Red player
            iso_bx, iso_by = self.to_iso(self.bad_pos[0], self.bad_pos[1])
            iso_bx += self.DISPLAY_WIDTH // 2
            iso_by += 50

            # ------------------------
            # DRAWING
            # ------------------------
            self.DISPLAY.fill(self.bg_color)   # Clear screen with black

            self.draw_iso_grid()               # Draw the white isometric grid

            # Draw red player (non-normalized)
            pygame.draw.rect(
                self.DISPLAY,
                (255, 0, 0),                  # Color red
                (iso_bx - 10, iso_by - 20, 20, 40)  # Rect(x, y, width, height)
            )

            # Draw green player (vector-normalized)
            pygame.draw.rect(
                self.DISPLAY,
                (0, 255, 0),                  # Color green
                (iso_px - 10, iso_py - 20, 20, 40)
            )

            # Update the display
            pygame.display.update()


# ------------------------------
# RUN THE GAME
# ------------------------------
if __name__ == "__main__":
    pygame.init()  # Initialize all pygame modules
    app = Main()   # Create an instance of the Main game class
    app.run()      # Start the main game loop
