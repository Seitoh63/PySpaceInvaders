import pygame

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
