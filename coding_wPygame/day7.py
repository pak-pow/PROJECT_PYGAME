"""
DAY 7 rendering proper text and UI
"""

import pygame
import sys

from pygame.time import Clock
from pygame.sprite import Sprite
from pygame.font import SysFont

pygame.init()
DISPLAY = pygame.display.set_mode((600,400))
clock = Clock()
font = SysFont(None, 30)

class UIElement(Sprite):

    def __init__(self, text, x, y, width, height):
        super().__init__()

        self.image = pygame.Surface((width,height))
        self.image.fill((50,50,50))

        self.rect = self.image.get_rect(topleft=(x,y))

        self.text_surface = font.render(text, True, (255,255,255))
        self.text_rect = self.text_surface.get_rect(center = self.rect.center)

    def draw(self, surface):

        surface.blit(self.image, self.rect)
        surface.blit(self.text_surface, self.text_rect)


btn_start = UIElement("START GAME", 200, 100, 200, 50)
btn_options = UIElement("OPTIONS", 200, 180, 200, 50)
btn_quit = UIElement("QUIT", 200, 260, 200, 50)

ui_elements = [btn_start, btn_options, btn_quit]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            if btn_start.rect.collidepoint(mouse_pos):
                print("Start Game clicked!")

            elif btn_options.rect.collidepoint(mouse_pos):
                print("Options clicked!")

            elif btn_quit.rect.collidepoint(mouse_pos):
                print("Quitting...")
                pygame.quit()
                sys.exit()

    DISPLAY.fill((255, 255, 255))

    for element in ui_elements:
        element.draw(DISPLAY)

    pygame.display.update()
