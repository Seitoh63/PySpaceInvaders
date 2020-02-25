import pygame

import config
from config import *


class Score:

    def __init__(self, digit_sprites: list, score_sprite: pygame.Surface):
        self.score = 0
        self.digit_sprites = digit_sprites
        self.score_sprite = score_sprite

    def draw(self, surf: pygame.Surface):
        score_str = str(self.score)
        while len(score_str) < SCORE_DIGIT_COUNT:
            score_str = '0' + score_str

        x0, y0 = SCORE_POS
        step = SCORE_DIGIT_X_SPACE_PIXELS
        r = self.digit_sprites[0].get_rect()
        r.topleft = (x0, y0 - (r.h * 2))
        surf.blit(self.score_sprite, r)

        for digit in score_str:
            r.topleft = (x0, y0)
            surf.blit(self.digit_sprites[int(digit)], r)
            x0 += r.w + step

class HighScore:

    def __init__(self, digit_sprites: list, high_score_sprite: pygame.Surface):
        self.high_score = 0
        self.digit_sprites = digit_sprites
        self.high_score_sprite = high_score_sprite

    def draw(self, surf: pygame.Surface):
        score_str = str(self.high_score)
        while len(score_str) < SCORE_DIGIT_COUNT:
            score_str = '0' + score_str

        x0, y0 = HIGH_SCORE_POS
        step = SCORE_DIGIT_X_SPACE_PIXELS
        r = self.digit_sprites[0].get_rect()
        r.topleft = (x0, y0 - (r.h * 2))
        surf.blit(self.high_score_sprite, r)

        for digit in score_str:
            r.topleft = (x0, y0)
            surf.blit(self.digit_sprites[int(digit)], r)
            x0 += r.w + step

class LifeCounter:

    def __init__(self, life_count, life_sprite:pygame.Surface, digit_sprites : list):
        self.life_count = life_count
        self.life_sprite = life_sprite
        self.digit_sprites = digit_sprites

    def draw(self, surf:pygame.Surface):

        surf.blit(self.digit_sprites[self.life_count], pygame.Rect(LIFE_COUNT_POS,(0,0)))

        rect = self.life_sprite.get_rect()
        rect.topleft = LIFE_POS
        for life in range(self.life_count):
            surf.blit(self.life_sprite, rect)
            rect.left,rect.top = (rect.left + LIFE_POS_SHIFT[0] + rect.w , rect.top + LIFE_POS_SHIFT[1])



