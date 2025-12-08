# ui.py
import pygame

class Button:
    def __init__(self, rect, text, callback, cost_fn):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.callback = callback
        self.cost_fn = cost_fn

    def draw(self, surf, font, player_money):
        cost, val_str = self.cost_fn()
        can_afford = player_money >= cost

        col_bg = (50, 80, 50) if can_afford else (50, 50, 50)
        col_border = (100, 200, 100) if can_afford else (80, 80, 80)

        pygame.draw.rect(surf, col_bg, self.rect)
        pygame.draw.rect(surf, col_border, self.rect, 2)

        lbl_name = font.render(f"{self.text}", True, (255, 255, 255))
        lbl_cost = font.render(f"${cost} | {val_str}", True, (200, 200, 100))

        surf.blit(lbl_name, (self.rect.x + 10, self.rect.y + 5))
        surf.blit(lbl_cost, (self.rect.x + 10, self.rect.y + 25))

    def click(self, mx, my, player):
        if self.rect.collidepoint(mx, my):
            cost, _ = self.cost_fn()
            if player.money >= cost:
                player.money -= cost
                self.callback(player)
                return True
        return False