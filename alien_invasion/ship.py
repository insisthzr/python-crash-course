#!/usr/local/bin/python3.6

import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, ai_setting, screen):
        super().__init__()

        self.ai_setting = ai_setting

        self.screen = screen
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.centerx = float(self.rect.centerx)

        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        if self.moving_right:
            self.centerx += self.ai_setting.ship_speed_factor
        if self.moving_left:
            self.centerx -= self.ai_setting.ship_speed_factor

        if self.centerx < self.screen_rect.left + self.rect.width / 2:
            self.centerx = self.screen_rect.left + self.rect.width / 2
        if self.centerx > self.screen_rect.right - self.rect.width / 2:
            self.centerx = self.screen_rect.right - self.rect.width / 2

        self.rect.centerx = self.centerx

    def center_ship(self):
        self.centerx = self.screen_rect.centerx
