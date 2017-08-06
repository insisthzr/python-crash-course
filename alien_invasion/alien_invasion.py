#!/usr/local/bin/python3.6

import pygame
from pygame.sprite import Group

import setting
from ship import Ship
import game_functions
import game_stats
import button
import scoreboard


def run_game():
    pygame.init()
    pygame.display.set_caption('Alien Invasion')

    ai_setting = setting.Setting()
    screen = pygame.display.set_mode(
        (ai_setting.screen_width, ai_setting.screen_height))
    ship = Ship(ai_setting, screen)
    bullets = Group()
    aliens = Group()
    stats = game_stats.GameStats(ai_setting)
    play_button = button.Button(ai_setting, screen, "Play")
    sb = scoreboard.Scoreboard(ai_setting, screen, stats)

    game_functions.create_fleet(ai_setting, screen, ship, aliens)

    while True:
        game_functions.check_events(ai_setting, screen, stats, sb,
                                    play_button, ship, aliens, bullets)
        if stats.game_active:
            ship.update()
            game_functions.update_bullets(ai_setting, screen, stats,
                                          sb, ship, aliens, bullets)
            game_functions.update_aliens(ai_setting, screen, stats,
                                         sb, ship, aliens, bullets)
        game_functions.update_screen(ai_setting, screen, stats, sb,
                                     ship, aliens, bullets, play_button)


run_game()
