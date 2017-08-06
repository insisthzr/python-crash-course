#!/usr/local/bin/python3.6

import pygame
from pygame.sprite import Group

import setting
from ship import Ship
import game_functions as gf
import game_stats as gs
import button
import scoreboard


def run_game():
    pygame.init()
    ai_setting = setting.Setting()
    screen = pygame.display.set_mode(
        (ai_setting.screen_width, ai_setting.screen_height))
    pygame.display.set_caption('Alien Invasion')
    ship = Ship(ai_setting, screen)
    bullets = Group()
    aliens = Group()
    gf.create_fleet(ai_setting, screen, ship, aliens)
    stats = gs.GameStats(ai_setting)
    play_button = button.Button(ai_setting, screen, "Play")
    sb = scoreboard.Scoreboard(ai_setting, screen, stats)
    while True:
        gf.check_events(ai_setting, screen, stats, sb,
                        play_button, ship, aliens, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_setting, screen, stats,
                              sb, ship, aliens, bullets)
            gf.update_aliens(ai_setting, screen, stats,
                             sb, ship, aliens, bullets)
        gf.update_screen(ai_setting, screen, stats, sb,
                         ship, aliens, bullets, play_button)


run_game()
