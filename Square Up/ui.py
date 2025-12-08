# ui.py
import pygame


class Button:
    def __init__(self, rect, text, callback, cost_fn, condition_fn=None):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.callback = callback
        self.cost_fn = cost_fn
        self.condition_fn = condition_fn  # New: Function to check if button is clickable

    def draw(self, surf, font, player_money):
        cost, val_str = self.cost_fn()

        # Check condition (e.g., is Health full?)
        condition_met = True
        if self.condition_fn:
            condition_met = self.condition_fn()

        can_afford = player_money >= cost
        is_active = can_afford and condition_met

        if is_active:
            col_bg = (50, 80, 50)
            col_border = (100, 200, 100)
            col_text = (255, 255, 255)
        else:
            col_bg = (50, 50, 50)
            col_border = (80, 80, 80)
            col_text = (150, 150, 150)  # Grayed out text

        pygame.draw.rect(surf, col_bg, self.rect)
        pygame.draw.rect(surf, col_border, self.rect, 2)

        lbl_name = font.render(f"{self.text}", True, col_text)
        lbl_cost = font.render(f"${cost} | {val_str}", True, (200, 200, 100) if is_active else (100, 100, 100))

        surf.blit(lbl_name, (self.rect.x + 10, self.rect.y + 5))
        surf.blit(lbl_cost, (self.rect.x + 10, self.rect.y + 25))

    def click(self, mx, my, player):
        # Check condition before clicking
        if self.condition_fn and not self.condition_fn():
            return False

        if self.rect.collidepoint(mx, my):
            cost, _ = self.cost_fn()
            if player.money >= cost:
                player.money -= cost
                self.callback(player)
                return True
        return False