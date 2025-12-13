import pygame  # Import the main Pygame library for game development
import sys  # Import the system library to handle exiting the program cleanly
from pygame.locals import *  # Import all Pygame constants (like K_a, QUIT, etc.)

# --- CONFIGURATION ---
TILE_SIZE = 40  # Define the width and height of each block/tile in pixels
DISPLAY_WIDTH = 600  # Define the total width of the game window
DISPLAY_HEIGHT = 800  # Define the total height of the game window

# Define the level layout using a list of strings (a grid)
# X = Wall, B = Brick, P = Paddle, O = Ball, Space = Empty
LEVEL_MAP = [
    "XXXXXXXXXXXXXXX",  # Row 0: Top wall
    "XBBBBBBBBBBBBBX",  # Row 1: Bricks
    "XBBBBBBBBBBBBBX",  # Row 2: Bricks
    "XBBBBBBBBBBBBBX",  # Row 3: Bricks
    "XBBBBBBBBBBBBBX",  # Row 4: Bricks
    "XBBBBBBBBBBBBBX",  # Row 5: Bricks
    "X             X",  # Row 6: Empty space
    "X             X",  # Row 7
    "X             X",  # Row 8
    "X             X",  # Row 9
    "X             X",  # Row 10
    "X             X",  # Row 11
    "X             X",  # Row 12
    "X             X",  # Row 13
    "X             X",  # Row 14
    "X             X",  # Row 15
    "X      O      X",  # Row 16: Ball spawn point
    "X             X",  # Row 17
    "X     PPP     X",  # Row 18: Paddle spawn point
    "XXXXXXXXXXXXXXX",  # Row 19: Bottom wall
]


class Tile(pygame.sprite.Sprite):  # Define a class for static tiles (Walls/Bricks)
    def __init__(self, pos, type):  # Initialize the tile with a position and type
        super().__init__()  # Call the parent Sprite class constructor

        # Create a square surface (image) for the tile
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        # Create a rectangle for collision detection, positioned at 'pos'
        self.rect = self.image.get_rect(topleft=pos)
        self.type = type  # Save the type ("X" or "B") just in case we need it later

        if type == "X":  # If this tile is a Wall
            self.image.fill((180, 180, 180))  # Fill it with light gray

            # Draw a darker border around the wall for visual style
            pygame.draw.rect(
                self.image,
                (80, 80, 80),  # Border color (Dark Gray)
                (0, 0, TILE_SIZE, TILE_SIZE),  # Rectangle area
                3  # Border thickness
            )

        elif type == "B":  # If this tile is a Brick
            self.image.fill((0, 150, 255))  # Fill it with Blue

            # Draw a darker border around the brick
            pygame.draw.rect(
                self.image,
                (0, 80, 250),  # Border color (Darker Blue)
                self.image.get_rect(),  # Rectangle area
                2  # Border thickness
            )


class Player(pygame.sprite.Sprite):  # Define the Player/Paddle class
    def __init__(self, pos):  # Initialize with a starting position
        super().__init__()  # Call parent Sprite constructor

        # The paddle is 3 tiles wide (40 * 3 = 120 pixels)
        self.image = pygame.Surface((TILE_SIZE * 3, TILE_SIZE))
        self.image.fill((0, 255, 0))  # Fill the paddle with Green
        self.rect = self.image.get_rect(center=pos)  # Position the rect based on center
        self.speed = 500  # Movement speed in pixels per second

    def update(self, dt):  # Update loop, runs every frame
        keys = pygame.key.get_pressed()  # Get the state of all keyboard keys

        # Check if 'A' or Left Arrow is pressed
        if keys[K_a] or keys[K_LEFT]:
            self.rect.x -= self.speed * dt  # Move left (subtract from X)

        # Check if 'D' or Right Arrow is pressed
        if keys[K_d] or keys[K_RIGHT]:
            self.rect.x += self.speed * dt  # Move right (add to X)

        # --- Screen Boundaries ---
        # Prevent paddle from going past the left wall (1 tile thick)
        if self.rect.left < TILE_SIZE:
            self.rect.left = TILE_SIZE

        # Prevent paddle from going past the right wall
        if self.rect.right > DISPLAY_WIDTH - TILE_SIZE:
            self.rect.right = DISPLAY_WIDTH - TILE_SIZE


class Ball(pygame.sprite.Sprite):  # Define the Ball class
    def __init__(self, pos):  # Initialize with starting position
        super().__init__()  # Call parent Sprite constructor

        # Create a transparent surface for the ball (20x20 pixels)
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        # Draw a yellow circle on that transparent surface
        pygame.draw.circle(self.image, (255, 255, 0), (10, 10), 10)

        # Create the rect for collisions
        self.rect = self.image.get_rect(center=pos)

        # IMPORTANT: Store exact position as a Vector2 (floats) for smooth movement
        self.pos = pygame.math.Vector2(pos)
        # Set initial velocity: 0 Horizontal, 500 Vertical (Straight Down)
        self.velocity = pygame.math.Vector2(0, 500)

    def update(self, dt, paddle, bricks, walls):  # Main physics logic

        # --- PHASE 1: X-AXIS MOVEMENT ---
        self.pos.x += self.velocity.x * dt  # Apply horizontal speed to float pos
        self.rect.x = round(self.pos.x)  # Sync the integer rect to the float pos

        # Check for collision with walls on the X-axis
        hit_walls = pygame.sprite.spritecollide(self, walls, False)
        for wall in hit_walls:  # Iterate through any walls we hit

            if self.velocity.x > 0:  # If moving Right
                self.rect.right = wall.rect.left  # SNAP ball to left side of wall
                self.pos.x = self.rect.x  # Update float pos to match snap
                self.velocity.x *= -1  # Bounce (flip X velocity)

            elif self.velocity.x < 0:  # If moving Left
                self.rect.left = wall.rect.right  # SNAP ball to right side of wall
                self.pos.x = self.rect.x  # Update float pos to match snap
                self.velocity.x *= -1  # Bounce

        # Check for collision with bricks on X-axis (True = delete brick)
        if pygame.sprite.spritecollide(self, bricks, True):
            self.velocity.x *= -1  # Bounce horizontally

        # --- PHASE 2: Y-AXIS MOVEMENT ---
        self.pos.y += self.velocity.y * dt  # Apply vertical speed to float pos
        self.rect.y = round(self.pos.y)  # Sync the integer rect to float pos

        # Check for collision with walls on the Y-axis
        hit_walls = pygame.sprite.spritecollide(self, walls, False)
        for wall in hit_walls:

            if self.velocity.y > 0:  # If moving Down
                self.rect.bottom = wall.rect.top  # SNAP ball to top of wall
                self.pos.y = self.rect.y  # Update float pos
                self.velocity.y *= -1  # Bounce (flip Y velocity)

            elif self.velocity.y < 0:  # If moving Up
                self.rect.top = wall.rect.bottom  # SNAP ball to bottom of wall
                self.pos.y = self.rect.y  # Update float pos
                self.velocity.y *= -1  # Bounce

        # --- PADDLE COLLISION (STEERING) ---
        if self.rect.colliderect(paddle.rect):  # If ball hits paddle
            if self.velocity.y > 0:  # And ball is falling down
                self.rect.bottom = paddle.rect.top  # SNAP to top of paddle
                self.pos.y = self.rect.y  # Update float pos
                self.velocity.y *= -1  # Bounce up

                # Calculate how far off-center the ball hit
                offset = self.rect.centerx - paddle.rect.centerx
                # Add that offset to X velocity to "steer" the ball
                self.velocity.x += offset * 3

        # Check for collision with bricks on Y-axis (True = delete brick)
        if pygame.sprite.spritecollide(self, bricks, True):
            self.velocity.y *= -1  # Bounce vertically

        # --- SAFETY NETS (Screen Boundaries) ---
        # If ball goes too far left
        if self.rect.left < 0:
            self.rect.left = 0
            self.pos.x = 0
            self.velocity.x *= -1

        # If ball goes too far right
        if self.rect.right > DISPLAY_WIDTH:
            self.rect.right = DISPLAY_WIDTH
            self.pos.x = self.rect.x
            self.velocity.x *= -1

        # If ball goes too far up
        if self.rect.top < 0:
            self.rect.top = 0
            self.pos.y = 0
            self.velocity.y *= -1


class Main:  # The main game management class
    def __init__(self):
        pygame.init()  # Initialize Pygame engine
        self.CLOCK = pygame.time.Clock()  # Create a clock to manage FPS
        self.FPS = 60  # Set target Frames Per Second
        # Create the game window
        self.DISPLAY = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

        # Create Sprite Groups to organize objects
        self.all_sprites = pygame.sprite.Group()  # Holds everything (for drawing)
        self.wall_group = pygame.sprite.Group()  # Holds only walls (for collision)
        self.brick_group = pygame.sprite.Group()  # Holds only bricks (for collision)

        self.player = None  # Placeholder for player object
        self.ball = None  # Placeholder for ball object

        self.load_level()  # Run the level loader function

    def load_level(self):
        player_created = False  # Flag to ensure we only make 1 paddle

        # Loop through every row in the map
        for row_index, row in enumerate(LEVEL_MAP):
            # Loop through every character in the row
            for col_index, tile_char in enumerate(row):
                # Calculate pixel position (Grid X * Tile Size)
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE

                if tile_char == "X":  # Found a Wall
                    tile = Tile((x, y), "X")  # Create Tile object
                    self.wall_group.add(tile)  # Add to wall group
                    self.all_sprites.add(tile)  # Add to draw group

                elif tile_char == "B":  # Found a Brick
                    tile = Tile((x, y), "B")  # Create Tile object
                    self.brick_group.add(tile)  # Add to brick group
                    self.all_sprites.add(tile)  # Add to draw group

                elif tile_char == "P":  # Found a Paddle spawn
                    if not player_created:  # Only if we haven't made one yet
                        # Create Player object (offset slightly)
                        self.player = Player((x + 100, y + 20))
                        self.all_sprites.add(self.player)  # Add to draw group
                        player_created = True  # Mark as created

                elif tile_char == "O":  # Found a Ball spawn
                    self.ball = Ball((x + 20, y + 20))  # Create Ball
                    self.all_sprites.add(self.ball)  # Add to draw group

    def run(self):  # The main game loop
        while True:
            # Calculate Delta Time (seconds passed since last frame)
            dt = self.CLOCK.tick(self.FPS) / 1000

            # Event Handling Loop
            for event in pygame.event.get():
                if event.type == QUIT:  # If user clicks X button
                    pygame.quit()  # Shut down Pygame
                    sys.exit()  # Exit script

            # Update Game Objects
            self.player.update(dt)  # Move player
            # Move ball (passing in walls/bricks for collision checks)
            self.ball.update(dt, self.player, self.brick_group, self.wall_group)

            # Draw Everything
            self.DISPLAY.fill((0, 0, 0))  # Clear screen with Black
            self.all_sprites.draw(self.DISPLAY)  # Draw all sprites to screen

            # Update Window Title with FPS
            pygame.display.set_caption(f"BreakOut | FPS: {int(self.CLOCK.get_fps())}")

            # Flip the display buffer (show the new frame)
            pygame.display.update()


if __name__ == "__main__":  # Check if script is run directly
    app = Main()  # Create an instance of the Main class
    app.run()  # Start the game loop