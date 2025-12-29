import pygame
import random

WIDTH, HEIGHT = 800, 600
FPS = 60
SCROLL_SPEED = 40

BLACK = (10, 10, 15)
GOLD = (255, 215, 0)
CYAN = (0, 255, 255)
WHITE = (200, 200, 200)
GREEN = (50, 205, 50)
GREY = (100, 100, 100)

CREDITS_TEXT = [
    ("CONGRATULATIONS", "TITLE"),
    ("YOU HAVE COMPLETED THE 30-DAY GAUNTLET", "SUBTITLE"),
    ("", "SPACER"),
    ("--- INITIATING PROJECT 52 ---", "HEADER"),
    ("One Project. Every Week. For 52 Weeks.", "NORMAL"),
    ("", "SPACER"),
    ("PHASE 1: FOUNDATION (Wks 1-12)", "HEADER"),
    ("WK 01: Personal Portfolio v1", "GREEN"),
    ("WK 02: Python CLI Task Manager", "NORMAL"),
    ("WK 03: CSS Animation Showcase", "NORMAL"),
    ("WK 04: Math Visualization Tool", "NORMAL"),
    ("WK 05: JS Interactive Quiz", "NORMAL"),
    ("WK 06: Web Scraper for News", "NORMAL"),
    ("WK 07: Landing Page (Tailwind)", "NORMAL"),
    ("WK 08: Algorithm Visualizer (Pygame!)", "GREEN"),
    ("WK 09: Form Validation Lib", "NORMAL"),
    ("WK 10: Data Analysis Script", "NORMAL"),
    ("WK 11: Responsive Dashboard", "NORMAL"),
    ("WK 12: Calculator with GUI", "NORMAL"),
    ("", "SPACER"),
    ("PHASE 2: INTEGRATION (Wks 13-36)", "HEADER"),
    ("WK 13: REST API for Todo App", "NORMAL"),
    ("WK 21: Real-time Chat App", "NORMAL"),
    ("WK 27: Portfolio v2 with Backend", "NORMAL"),
    ("WK 36: Analytics Dashboard", "NORMAL"),
    ("", "SPACER"),
    ("PHASE 3: PRODUCTION (Wks 37-52)", "HEADER"),
    ("WK 37: CI/CD Pipeline Setup", "NORMAL"),
    ("WK 47: Microservices Arch.", "NORMAL"),
    ("WK 52: SaaS Product Launch", "GOLD"),
    ("", "SPACER"),
    ("REPO: github.com/pak-pow/PROJECT52", "CYAN"),
    ("", "SPACER"),
    ("GOOD LUCK, DEV.", "TITLE"),
    ("", "SPACER"),
    ("", "SPACER"),
    ("(Press ESC to exit)", "NORMAL"),
]

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Day 30: Graduation & Roadmap")
clock = pygame.time.Clock()

font_title = pygame.font.SysFont("Arial", 50, bold=True)
font_header = pygame.font.SysFont("Arial", 36, bold=True)
font_normal = pygame.font.SysFont("Arial", 28)


def render_text_objects():
    rendered_lines = []

    for line, style in CREDITS_TEXT:

        if style == "TITLE":
            surf = font_title.render(line, True, GOLD)

        elif style == "SUBTITLE":
            surf = font_header.render(line, True, WHITE)

        elif style == "HEADER":
            surf = font_header.render(line, True, CYAN)

        elif style == "CYAN":
            surf = font_normal.render(line, True, CYAN)

        elif style == "GREEN":
            surf = font_normal.render(line, True, GREEN)

        elif style == "GOLD":
            surf = font_header.render(line, True, GOLD)

        else:
            surf = font_normal.render(line, True, WHITE)

        rendered_lines.append({"surf": surf, "y": 0})

    return rendered_lines


def draw_stars(surface):
    for _ in range(50):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        brightness = random.randint(100, 255)
        surface.set_at((x, y), (brightness, brightness, brightness))


lines = render_text_objects()
scroll_y = HEIGHT + 50

running = True
while running:
    dt = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:
                SCROLL_SPEED = 200
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                SCROLL_SPEED = 40

    scroll_y -= SCROLL_SPEED * dt
    screen.fill(BLACK)
    draw_stars(screen)

    current_y = scroll_y

    for line in lines:
        rect = line["surf"].get_rect(center=(WIDTH // 2, int(current_y)))
        screen.blit(line["surf"], rect)
        current_y += 60

    if current_y < 0:
        scroll_y = HEIGHT + 50

    pygame.display.flip()

pygame.quit()