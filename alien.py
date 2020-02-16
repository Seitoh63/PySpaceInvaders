import random

import pygame

from config import *
from tools import MovingDirection


class Laser:

    def __init__(self, rect: pygame.Rect):
        self.rect = rect
        self.moving_direction = MovingDirection.DOWN
        self.move_amount = 0

    def update(self, dt):
        self._move(dt)

    def _move(self, dt):
        self.move_amount += dt / 1000 * LASER_SPEED_PIXEL_PER_SECOND
        if self.move_amount > 1.:
            self.rect.y += int(self.move_amount)
            self.move_amount -= int(self.move_amount)

    def draw(self, surf: pygame.Surface):
        pygame.draw.rect(surf, LASER_RECT_COLOR, self.rect)


class Alien:

    def __init__(self, rect: pygame.Rect, sprites: list):
        self.sprites = sprites
        self.sprite_index = 0
        self.last_sprite_shift_delay = 0
        self.rect = rect
        self.move_amount = 0

    def update(self, dt):
        self._move(dt)
        self._sprite_shift(dt)

    def _move(self, dt):
        self.move_amount += dt / 1000 * ALIEN_SPEED_PIXEL_PER_SECOND
        if self.move_amount > 1.:
            self.rect.y += int(self.move_amount)
            self.move_amount -= int(self.move_amount)

    def fire(self):
        laser_rect = pygame.Rect(
            self.rect.centerx - (LASER_RECT_DIM[0] // 2),
            self.rect.bottom,
            LASER_RECT_DIM[0],
            LASER_RECT_DIM[1]
        )

        return Laser(laser_rect)

    def draw(self, surf: pygame.Surface):
        surf.blit(self.sprites[self.sprite_index], self.rect)

    def _sprite_shift(self, dt):
        self.last_sprite_shift_delay += dt
        if self.last_sprite_shift_delay > ALIEN_SPRITE_SHIFT_DELAY_MS :
            self.sprite_index += 1
            self.sprite_index %= len(self.sprites)
            self.last_sprite_shift_delay -= ALIEN_SPRITE_SHIFT_DELAY_MS


class Aliens:

    def __init__(self, aliens):
        self.aliens = aliens
        self.lasers = []
        self.last_firing_delay = 0


    def __iter__(self):
        return self.aliens.__iter__()

    def __next__(self):
        return self.aliens.__next__()

    def update(self, dt):

        self._fire(dt)

        for alien in self:
            alien.update(dt)

        for laser in self.lasers:
            laser.update(dt)
            if laser.rect.top > WORLD_DIM[1]:
                self.lasers.remove(laser)

    def draw(self, surf):
        for alien in self:
            alien.draw(surf)
        for laser in self.lasers:
            laser.draw(surf)

    def remove(self, alien):
        self.aliens.remove(alien)

    def _firing_aliens(self):

        # Group the alien by columns
        xs = set(alien.rect.centerx for alien in self.aliens)
        alien_dict = {x: [] for x in xs}
        for alien in self.aliens:
            alien_dict[alien.rect.centerx].append(alien)

        # identify lowest alien on column
        max_aliens = []
        for x in xs:
            max_alien = None
            max_alien_y = 0
            for alien in alien_dict[x]:
                if alien.rect.bottom > max_alien_y:
                    max_alien = alien
                    max_alien_y = alien.rect.bottom
            if max_alien: max_aliens.append(max_alien)

        return max_aliens

    def _fire(self, dt):
        self.last_firing_delay += dt

        while self.last_firing_delay > ALIEN_FIRING_PERIOD_MS:
            self.last_firing_delay -= ALIEN_FIRING_PERIOD_MS
            alien = random.choice(self._firing_aliens())
            self.lasers.append(alien.fire())


class AlienGenerator:

    def __init__(self):
        pass

    @staticmethod
    def generate():
        aliens = []

        alien_sprites = [
            [pygame.image.load(SPRITE_PATH + "alien1_frame1.png"),
             pygame.image.load(SPRITE_PATH + "alien1_frame2.png")],
            [pygame.image.load(SPRITE_PATH + "alien2_frame1.png"),
             pygame.image.load(SPRITE_PATH + "alien2_frame2.png")],
            [pygame.image.load(SPRITE_PATH + "alien3_frame1.png"),
             pygame.image.load(SPRITE_PATH + "alien3_frame2.png")],
        ]

        max_w = max([sprites[0].get_rect().w for sprites in alien_sprites])
        max_row_size = max([len(row) for row in ALIEN_FORMATION])
        step = WORLD_DIM[0]/max_row_size
        x0 = (step-max_w)//2
        xs = [ x0+ (step*i) for i in range(max_row_size) ]

        for row_index, alien_row in enumerate(ALIEN_FORMATION):
            for i, alien_index in enumerate(alien_row):

                sprites = alien_sprites[alien_index - 1]
                w, h = (sprites[0].get_rect().w, sprites[0].get_rect().h)

                center_x = xs[i]
                center_y = h + (2 * h * row_index)

                alien_rect = pygame.Rect(
                    center_x - w // 2,
                    center_y - h // 2,
                    w,
                    h,
                )

                aliens.append(Alien(alien_rect, sprites))

        return Aliens(aliens)
