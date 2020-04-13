import pygame

from config import *


class Score:

    def __init__(self):
        self.value = 0
        self.digit_sprites = [pygame.image.load(SPRITE_PATH + str(i) + ".png") for i in range(0, 10)]
        self.score_sprite = pygame.image.load(SPRITE_PATH + "score.png")

    def draw(self, surf: pygame.Surface):
        score_str = str(self.value)
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

    def __init__(self):
        digit_sprites = [pygame.image.load(SPRITE_PATH + str(i) + ".png") for i in range(0, 10)]
        high_score_sprite = pygame.image.load(SPRITE_PATH + "high_score.png")

        self.value = 0
        self.digit_sprites = digit_sprites
        self.high_score_sprite = high_score_sprite

    def draw(self, surf: pygame.Surface):
        score_str = str(self.value)
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

    def __init__(self):
        self.life_gain_count = 0
        self.life_count = STARTING_LIFE_COUNT
        self.life_sprite = pygame.image.load(SPRITE_PATH + SPACESHIP_SPRITE_NAME)
        self.digit_sprites = [pygame.image.load(SPRITE_PATH + str(i) + ".png") for i in range(0, 10)]
        self.one_life_up_sound = pygame.mixer.Sound(SOUND_PATH + ONE_LIFE_UP_SOUND)

    def draw(self, surf: pygame.Surface):
        surf.blit(self.digit_sprites[self.life_count], pygame.Rect(LIFE_COUNT_POS, (0, 0)))

        rect = self.life_sprite.get_rect()
        rect.topleft = LIFE_POS
        for life in range(self.life_count):
            surf.blit(self.life_sprite, rect)
            rect.left, rect.top = (rect.left + LIFE_POS_SHIFT[0] + rect.w, rect.top + LIFE_POS_SHIFT[1])

    def one_up(self):
        self.life_count += 1
        self.life_gain_count += 1
        self.one_life_up_sound.play()


class GameOver:

    def __init__(self):
        self.game_over_sprite = pygame.image.load(SPRITE_PATH + "game_over.png")

    def draw(self, surf: pygame.Surface):
        w, h = WORLD_DIM
        center = (w // 2, h // 2)
        surf.blit(self.game_over_sprite, self.game_over_sprite.get_rect(center=center))
