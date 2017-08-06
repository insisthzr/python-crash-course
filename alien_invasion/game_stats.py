#!/usr/local/bin/python3.6


class GameStats():
    def __init__(self, ai_setting):
        self.game_active = False
        self.ai_setting = ai_setting
        self.reset_stats()
        self.high_score = 0

    def reset_stats(self):
        self.ships_left = self.ai_setting.ship_limit
        self.score = 0
        self.level = 1
