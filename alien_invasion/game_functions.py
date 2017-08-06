#!/usr/local/bin/python3.6

import sys
import time

import pygame

import bullet
from alien import Alien


def check_keydown_events(event, ai_setting, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_setting, screen, ship, bullets)
    elif event.key == pygame.K_ESCAPE:
        sys.exit()


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_setting, screen, stats, sb, play_button, ship, aliens, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_setting, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_setting, screen, stats, sb, play_button,
                              ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_setting, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        ai_setting.initialize_dynamic_setting()
        pygame.mouse.set_visible(False)

        stats.reset_stats()
        stats.game_active = True

        sb.prep_high_score()
        sb.prep_level()
        sb.prep_score()

        aliens.empty()
        bullets.empty()

        create_fleet(ai_setting, screen, ship, aliens)
        ship.center_ship()


def update_screen(ai_setting, screen, stats, sb, ship, aliens, bullets, play_button):
    screen.fill(ai_setting.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)
    sb.show_score()

    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()


def update_bullets(ai_setting, screen, stats, sb, ship, aliens, bullets):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collision(
        ai_setting, screen, stats, sb, ship, aliens, bullets)


def update_aliens(ai_setting, screen, stats, sb, ship, aliens, bullets):
    check_fleet_edges(ai_setting, aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_setting, screen, stats, sb, ship, aliens, bullets)

    check_aliens_bottom(ai_setting,  stats, screen, sb, ship, aliens, bullets)


def check_aliens_bottom(ai_setting, stats, screen, sb, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_setting, screen, stats, sb, ship, aliens, bullets)
            break


def fire_bullet(ai_setting, screen, ship, bullets):
    if len(bullets) < ai_setting.bullet_allowed:
        new_bullet = bullet.Bullet(ai_setting, screen, ship)
        bullets.add(new_bullet)


def get_number_aliens_x(ai_setting, alien_width):
    avaliable_space_x = ai_setting.screen_width - 2 * alien_width
    number_alien_x = int(avaliable_space_x / (2 * alien_width))
    return number_alien_x


def get_number_row(ai_setting, ship_height, alien_height):
    avaliable_space_y = (ai_setting.screen_height -
                         (3 * alien_height)) - ship_height
    number_rows = int(avaliable_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_setting, screen, aliens, alien_number, row_number):
    alien = Alien(ai_setting, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.y = alien.rect.height + 2 * alien.rect.height * row_number
    alien.rect.y = alien.y
    aliens.add(alien)


def create_fleet(ai_setting, screen, ship, aliens):
    alien = Alien(ai_setting, screen)
    number_alien_x = get_number_aliens_x(ai_setting, alien.rect.width)
    number_rows = get_number_row(
        ai_setting, ship.rect.height, alien.rect.height)
    for i in range(number_alien_x):
        for j in range(number_rows):
            create_alien(ai_setting, screen, aliens, i, j)


def check_fleet_edges(ai_setting, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_setting, aliens)
            break


def change_fleet_direction(ai_setting, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_setting.fleet_drop_speed
    ai_setting.fleet_direction *= -1


def check_bullet_alien_collision(ai_setting, screen, stats, sb, ship, aliens, bullets):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_setting.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        bullets.empty()
        ai_setting.increase_speed()

        stats.level += 1
        sb.prep_level()

        create_fleet(ai_setting, screen, ship, aliens)


def ship_hit(ai_setting,  screen, stats, sb, ship, aliens, bullets):
    if stats.ships_left > 0:
        stats.ships_left -= 1
        sb.prep_ships()

        aliens.empty()
        bullets.empty()

        create_fleet(ai_setting, screen, ship, aliens)
        ship.center_ship()

        time.sleep(1)
    else:
        pygame.mouse.set_visible(True)
        stats.game_active = False


def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
