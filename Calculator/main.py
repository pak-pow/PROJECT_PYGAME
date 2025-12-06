# ==========================================
#  CALCULATOR — REFACTORED CLEAN VERSION
# ==========================================

import pygame, sys
from pygame.locals import *

# -------------------------------
# Button Class (Reusable with Hover)
# -------------------------------
class Button:
    """
    CHANGE: Added hover effect feature
    UNCHANGED: Stores text, rectangle, text color, background color
    """

    def __init__(self, text, rect, font, bg_color=(217,217,217), text_color=(0,0,0), hover_color=(200,200,200)):
        self.text = text
        self.rect = pygame.Rect(rect)
        self.bg_color = bg_color
        self.text_color = text_color
        self.hover_color = hover_color  # CHANGE: color when hovering

        # Render text once
        self.text_surf = font.render(text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, screen):
        """
        CHANGE: Draw hover color if mouse is over button
        UNCHANGED: Draw button rectangle and text
        """
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, self.hover_color, self.rect)  # hover color
        else:
            pygame.draw.rect(screen, self.bg_color, self.rect)
        screen.blit(self.text_surf, self.text_rect)

    def clicked(self, mouse_pos):
        """Unchanged: Check if mouse clicked inside button"""
        return self.rect.collidepoint(mouse_pos)


# -------------------------------
# Main Program
# -------------------------------
def main():
    pygame.init()
    font = pygame.font.SysFont(None, 40)
    display = pygame.display.set_mode((500, 700))

    current_input = ""

    display_box = pygame.Rect(25, 25, 450, 100)
    grey = (217, 217, 217)

    # -------------------------------
    # Buttons Definition
    # -------------------------------
    numbers = [
        ("1", (25,180,80,100)), ("2", (125,180,80,100)), ("3", (225,180,80,100)),
        ("4", (25,300,80,100)), ("5", (125,300,80,100)), ("6", (225,300,80,100)),
        ("7", (25,420,80,100)), ("8", (125,420,80,100)), ("9", (225,420,80,100)),
        ("0", (25,540,80,100)), ("00", (125,540,80,100)), ("000", (225,540,80,100)),
    ]

    ops = [
        ("+", (325,180,60,180)), ("-", (400,180,60,180)),
        ("*", (325,380,60,180)), ("/", (400,380,60,180)),
        ("=", (325,580,135,60)), ("C", (25,133,80,40)),
    ]

    # CHANGE: Buttons now have hover color
    buttons = [Button(text, rect, font, hover_color=(180, 180, 250)) for text, rect in numbers + ops]

    # -------------------------------
    # Input Handler
    # -------------------------------
    def handle_button(text, current):
        if text == "C":
            return ""
        if text == "=":
            if current == "5+5":
                return "Hello world"
            try:
                return str(eval(current))
            except:
                return "ERROR"
        return current + text

    # -------------------------------
    # Game Loop
    # -------------------------------
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for btn in buttons:
                    if btn.clicked(mouse_pos):
                        current_input = handle_button(btn.text, current_input)

        # ----------------------
        # Drawing
        # ----------------------
        display.fill((255,255,255))
        pygame.draw.rect(display, grey, display_box)
        pygame.draw.line(display, grey, (0,150), (500,150))

        # CHANGE: Draw all buttons with hover effect
        for btn in buttons:
            btn.draw(display)

        # Draw current input
        display_text = font.render(current_input, True, (0,0,0))
        display.blit(display_text, (display_box.x+20, display_box.y+30))

        pygame.display.update()


if __name__ == "__main__":
    main()
