import random

import pygame

from config import *
from tools import MovingDirection, time_ms


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

    def __init__(self, rect: pygame.Rect):
        self.rect = rect
        self.move_amount = 0

    def update(self, dt):
        self._move(dt)

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

    def draw(self, surf):
        pygame.draw.rect(surf, ALIEN_RECT_COLOR, self.rect)


class Aliens:

    def __init__(self, aliens):
        self.aliens = aliens
        self.lasers = []
        self.last_firing = time_ms()

    def __iter__(self):
        return self.aliens.__iter__()

    def __next__(self):
        return self.aliens.__next__()

    def update(self, dt):

        self._fire()

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

    def _fire(self):
        elapsed_time = time_ms() - self.last_firing
        if elapsed_time > LASER_FIRING_PERIOD_MS:
            self.last_firing += elapsed_time
            alien = random.choice(self._firing_aliens())
            self.lasers.append(alien.fire())


class AlienGenerator:

    def __init__(self):
        pass

    @staticmethod
    def generate():
        aliens = []

        for i in range(ALIEN_COUNT):
            # A kind of formation for the alien
            center_x = ALIEN_RECT_DIM[0] + WORLD_DIM[0] / ALIEN_PER_ROW * (i % ALIEN_PER_ROW)
            center_y = ALIEN_RECT_DIM[1] + (2 * ALIEN_RECT_DIM[1] * (i // ALIEN_PER_ROW))

            alien_rect = pygame.Rect(
                center_x - ALIEN_RECT_DIM[0] // 2,
                center_y - ALIEN_RECT_DIM[1] // 2,
                ALIEN_RECT_DIM[0],
                ALIEN_RECT_DIM[1],
            )

            aliens.append(Alien(alien_rect))

        return Aliens(aliens)
