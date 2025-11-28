import pygame, sys
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((500,400))
button_rect = pygame.Rect(100,100,200,50)
color = (255, 0, 0)

my_image = pygame.Surface((50, 50))
my_image.fill((0, 255, 0))

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == MOUSEBUTTONDOWN and button_rect.collidepoint(event.pos):
            print("Button was clicked!")

            if color == (0, 0, 255):
                color = (255, 0, 0)

            else:
                color = (0, 0, 255)

    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, color, button_rect)

    screen.blit(my_image,(200,200))

    pygame.draw.circle(screen,color,(350, 125),25)
    pygame.draw.line(screen,color,(0, 0),(500,400), 5)

    pygame.display.set_caption("TEST PYGAME  ")
    pygame.display.update()

