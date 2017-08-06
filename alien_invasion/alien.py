#!/usr/local/bin/python3.6

import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    def __init__(self, ai_setting, screen):
        super().__init__()

        self.screen = screen
        self.ai_setting = ai_setting
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        dx = self.ai_setting.alien_speed_factor * self.ai_setting.fleet_direction
        self.x += dx
        self.rect.x = self.x

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        if self.rect.left <= screen_rect.left:
            return True
        return False
