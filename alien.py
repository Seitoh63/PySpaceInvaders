import random

import pygame

from config import *
from tools import MovingDirection


class Laser :

    def __init__(self,rect: pygame.Rect):
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

    def __iter__(self):
        self.i = 0
        self.flat_list = []
        for alien_row in self.aliens :
            for alien in alien_row:
                self.flat_list.append(alien)
        return self

    def __len__(self):
        length = 0
        for alien_row in self.aliens :
            length += len(alien_row)
        return length

    def __next__(self):
        if self.i < len(self) :
            self.i += 1
            return self.flat_list[self.i-1]
        else :
            raise StopIteration


    def __getitem__(self, i):
        if self.flat_list is None :
            for alien_row in self.aliens:
                for alien in alien_row:
                    self.flat_list.append(alien)
        return self.flat_list[i]

    def update(self, dt):

        if random.random() > 0.99 :
            alien = random.choice(self)
            self.lasers.append(alien.fire())

        for alien in self:
            alien.update(dt)
        for laser in self.lasers :
            laser.update(dt)

    def draw(self, surf):
        for alien in self:
            alien.draw(surf)
        for laser in self.lasers :
            laser.draw(surf)

    def remove(self, alien):
        for alien_row in self.aliens:
            if alien in alien_row :
                alien_row.remove(alien)


class AlienGenerator:

    def __init__(self):
        pass

    @staticmethod
    def generate():
        aliens = []
        row = []

        for i in range(ALIEN_COUNT):

            if i > 0 and i % ALIEN_PER_ROW == 0:
                aliens.append(row)
                row = []

            # A kind of formation for the alien
            center_x = ALIEN_RECT_DIM[0] + WORLD_DIM[0] / ALIEN_PER_ROW * (i % ALIEN_PER_ROW)
            center_y = ALIEN_RECT_DIM[1] + (2 * ALIEN_RECT_DIM[1] * (i // ALIEN_PER_ROW))

            alien_rect = pygame.Rect(
                center_x - ALIEN_RECT_DIM[0] // 2,
                center_y - ALIEN_RECT_DIM[1] // 2,
                ALIEN_RECT_DIM[0],
                ALIEN_RECT_DIM[1],
            )

            row.append(Alien(alien_rect))

        return Aliens(aliens)
