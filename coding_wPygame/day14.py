import pygame, sys

# 1. Setup
pygame.init()
SCREEN_W, SCREEN_H = 800, 600
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 40)

class GameStateManager:
    def __init__(self):
        self.state = 'intro'

        # Game Objects
        self.target_rect = pygame.Rect(400, 300, 50, 50)
        self.target_speed = 5

        # Create a Transparent Overlay Surface
        # We make a new surface the size of the screen
        self.overlay = pygame.Surface((SCREEN_W, SCREEN_H))
        self.overlay.fill((0, 0, 0))  # Fill black
        self.overlay.set_alpha(128)  # Set transparency (0=Invisible, 255=Opaque)

    # --- HELPER: JUST DRAW THE GAME ---
    # We pull this out so both 'main_game' and 'paused' can use it!
    def draw_game_elements(self):
        screen.fill((20, 20, 40))  # Clear screen
        pygame.draw.rect(screen, (0, 100, 255), self.target_rect)
        msg = font.render("CLICK THE SQUARE! (ESC to Pause)", True, (255, 255, 255))
        screen.blit(msg, (150, 50))

    # --- STATE 1: MENU ---
    def intro(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.state = 'main_game'

        screen.fill((50, 50, 50))
        title = font.render("START MENU", True, (255, 255, 255))
        instr = font.render("Press SPACE to Play", True, (0, 255, 0))
        screen.blit(title, (300, 200))
        screen.blit(instr, (250, 300))

    # --- STATE 2: PLAYING ---
    def main_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.target_rect.collidepoint(event.pos):
                    self.state = 'game_over'

            # PAUSE TRIGGER
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = 'paused'

        # 1. GAME LOGIC (Movement)
        # This ONLY runs in 'main_game', not 'paused'
        self.target_rect.x += self.target_speed
        if self.target_rect.right > 800 or self.target_rect.left < 0:
            self.target_speed *= -1

        # 2. DRAWING
        self.draw_game_elements()

    # --- STATE 3: PAUSED ---
    def paused(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # UNPAUSE TRIGGER
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = 'main_game'

        # 1. DRAW THE GAME (Frozen)
        # We call the draw helper, but we skipped the logic above!
        self.draw_game_elements()

        # 2. DRAW OVERLAY
        # Blit the semi-transparent black surface on top
        screen.blit(self.overlay, (0, 0))

        # 3. DRAW PAUSE TEXT
        text = font.render("PAUSED", True, (255, 255, 255))
        rect = text.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2))
        screen.blit(text, rect)

    # --- STATE 4: GAME OVER ---
    def game_over(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.state = 'intro'

        screen.fill((50, 0, 0))
        title = font.render("GAME OVER", True, (255, 255, 255))
        instr = font.render("Press R to Restart", True, (0, 255, 0))
        screen.blit(title, (300, 200))
        screen.blit(instr, (250, 300))

    def update(self):
        if self.state == 'intro':
            self.intro()
        elif self.state == 'main_game':
            self.main_game()
        elif self.state == 'paused':
            self.paused()
        elif self.state == 'game_over':
            self.game_over()


# --- MAIN LOOP ---
game_manager = GameStateManager()

while True:
    game_manager.update()
    pygame.display.update()
    clock.tick(60)