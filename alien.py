import random

import pygame

from config import *
from tools import MovingDirection


class Soucoup:

    def __init__(self, rect: pygame.Rect, sprite, explosion_sprite, direction: MovingDirection):
        self.rect = rect
        self.moving_direction = direction
        self.move_amount = 0

        self.is_exploded = False
        self.time_since_explosion = 0

        self.sprite = sprite
        self.explosion_sprite = explosion_sprite

    def update(self, dt):
        if self.is_exploded:
            self.time_since_explosion += dt
        self._move(dt)

    def _move(self, dt):
        if self.is_exploded:
            return
        self.move_amount += dt / 1000 * SOUCOUP_SPEED_PIXEL_PER_SECOND
        if self.move_amount > 1.:
            self.rect.x += int(self.move_amount) * self.moving_direction.value[0][0]
            self.move_amount -= int(self.move_amount)

    def draw(self, surf: pygame.Surface):
        if self.is_exploded:
            surf.blit(self.explosion_sprite, self.rect)
        else:
            surf.blit(self.sprite, self.rect)

    def explode(self):
        self.is_exploded = True

    @staticmethod
    def generate():
        sprite = pygame.image.load(SPRITE_PATH + SOUCOUP_SPRITE_NAME)
        explosion_sprite = pygame.image.load(SPRITE_PATH + ALIEN_EXPLOSION_SPRITE_NAME)
        rect = sprite.get_rect()
        rect.top = SOUCOUP_STARTING_POS_Y

        xs = [0, WORLD_DIM[0] - rect.w]
        dirs = [MovingDirection.RIGHT, MovingDirection.LEFT]
        index = random.choice([0, 1])
        rect.left = xs[index]
        direction = dirs[index]
        return Soucoup(rect, sprite, explosion_sprite, direction)


class Laser:

    def __init__(self, rect: pygame.Rect, explosion_sprite):
        self.rect = rect
        self.moving_direction = MovingDirection.DOWN
        self.move_amount = 0

        self.is_exploded = False
        self.time_since_explosion = 0
        self.explosion_sprite = explosion_sprite

    def update(self, dt):
        if self.is_exploded:
            self.time_since_explosion += dt
        self._move(dt)

    def _move(self, dt):
        if self.is_exploded:
            return
        self.move_amount += dt / 1000 * LASER_SPEED_PIXEL_PER_SECOND
        if self.move_amount > 1.:
            self.rect.y += int(self.move_amount)
            self.move_amount -= int(self.move_amount)

    def draw(self, surf: pygame.Surface):
        if self.is_exploded:
            surf.blit(self.explosion_sprite, self.rect)
        else:
            pygame.draw.rect(surf, LASER_RECT_COLOR, self.rect)

    def explode(self):
        self.is_exploded = True


class Alien:

    def __init__(
            self,
            type: int,
            rect: pygame.Rect,
            alien_sprites: list,
            explosion_sprite: pygame.Surface,
            laser_explosion_sprite: pygame.Surface,
            destroy_sound: pygame.mixer.Sound
    ):
        self.sprites = alien_sprites
        self.sprite_index = 0
        self.last_sprite_shift_delay = 0
        self.rect = rect
        self.move_amount = 0

        self.type = type

        self.delay_since_explosion = 0
        self.is_exploded = False
        self.explosion_sprite = explosion_sprite
        self.laser_explosion_sprite = laser_explosion_sprite

        self.destroy_sound = destroy_sound

    def update(self, dt, movement):
        if self.is_exploded:
            self.delay_since_explosion += dt

        self._move(dt, movement)
        self._sprite_shift(dt)

    def _move(self, dt, movement):
        self.rect.y += movement[1]
        self.rect.x += movement[0]

    def fire(self):
        laser_rect = pygame.Rect(
            self.rect.centerx - (LASER_RECT_DIM[0] // 2),
            self.rect.bottom,
            LASER_RECT_DIM[0],
            LASER_RECT_DIM[1]
        )

        return Laser(laser_rect, self.laser_explosion_sprite)

    def draw(self, surf: pygame.Surface):

        if self.is_exploded:
            explosion_rect = self.explosion_sprite.get_rect()
            explosion_rect.center = self.rect.center
            surf.blit(self.explosion_sprite, explosion_rect)
        else:
            surf.blit(self.sprites[self.sprite_index], self.rect)

    def _sprite_shift(self, dt):
        self.last_sprite_shift_delay += dt
        if self.last_sprite_shift_delay > ALIEN_SPRITE_SHIFT_DELAY_MS:
            self.sprite_index += 1
            self.sprite_index %= len(self.sprites)
            self.last_sprite_shift_delay -= ALIEN_SPRITE_SHIFT_DELAY_MS

    def explode(self):
        self.is_exploded = True
        self.destroy_sound.play()


class Aliens:

    def __init__(self, aliens, move_sound: pygame.mixer.Sound):
        self.aliens = aliens
        self.lasers = []

        self.soucoup = None
        self.soucoup_sound = pygame.mixer.Sound(SOUND_PATH + SOUCOUP_SOUND)

        self.last_soucoup_appearing_delay = 0

        self.last_firing_delay = 0
        self.movement_index = 0
        self.last_movement_sequence_delay = 0
        self.move_amount = 0

        self.move_sound = move_sound
        self.sound_index = 0

        self.move_sound.play(loops=-1)

    def __iter__(self):
        return self.aliens.__iter__()

    def __next__(self):
        return self.aliens.__next__()

    def update(self, dt):

        self._fire(dt)

        self._update_movement_direction(dt)
        movement = self._get_movement(dt)

        self._update_aliens(dt, movement)
        self._update_lasers(dt)

        if self.soucoup:
            self.soucoup.update(dt)

            if self.soucoup.rect.x > WORLD_DIM[0] or self.soucoup.rect.right < 0:
                self.soucoup = None
                self.soucoup_sound.stop()

        if self.soucoup and self.soucoup.is_exploded and self.soucoup.time_since_explosion > EXPLOSION_DURATION_MS:
            self.soucoup = None
            self.soucoup_sound.stop()

        self.last_soucoup_appearing_delay += dt
        if self.last_soucoup_appearing_delay > SOUCOUP_POP_PERIOD_S * 1000:
            self.last_soucoup_appearing_delay -= SOUCOUP_POP_PERIOD_S * 1000
            self.soucoup = Soucoup.generate()
            self.soucoup_sound.play(loops=-1)

    def draw(self, surf):
        for alien in self:
            alien.draw(surf)
        for laser in self.lasers:
            laser.draw(surf)

        if self.soucoup:
            self.soucoup.draw(surf)

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

        while self.last_firing_delay > ALIEN_FIRING_PERIOD_MS :

            self.last_firing_delay -= ALIEN_FIRING_PERIOD_MS
            firing_aliens = self._firing_aliens()
            if not firing_aliens:
                return
            alien = random.choice(self._firing_aliens())
            self.lasers.append(alien.fire())

    def _update_movement_direction(self, dt):
        self.last_movement_sequence_delay += dt
        while self.last_movement_sequence_delay // (ALIEN_MOVE_SEQUENCE_PERIOD_SECOND * 1000) > 1:
            self.movement_index += 1
            self.movement_index %= len(ALIEN_MOVE_SEQUENCE)
            self.last_movement_sequence_delay -= (ALIEN_MOVE_SEQUENCE_PERIOD_SECOND * 1000)

    def _get_movement(self, dt):
        movement = ALIEN_MOVE_SEQUENCE[self.movement_index]
        self.move_amount += dt / 1000 * ALIEN_SPEED_PIXEL_PER_SECOND
        move = (0, 0)
        if self.move_amount > 1.:
            move = (int(self.move_amount) * movement[0], int(self.move_amount) * movement[1])
            self.move_amount -= int(self.move_amount)

        return move

    def _update_aliens(self, dt, movement):

        for alien in self:
            if alien.delay_since_explosion > EXPLOSION_DURATION_MS:
                self.remove(alien)
            alien.update(dt, movement)

    def _update_lasers(self, dt):
        for laser in self.lasers:
            if laser.is_exploded and laser.time_since_explosion > EXPLOSION_DURATION_MS:
                self.lasers.remove(laser)

            laser.update(dt)
            if laser.rect.top > WORLD_DIM[1]:
                laser.rect.left -= laser.explosion_sprite.get_rect().w // 2
                laser.rect.top = WORLD_DIM[1] - laser.explosion_sprite.get_rect().h
                laser.explode()


class AlienGenerator:

    def __init__(self):
        pass

    @staticmethod
    def generate():
        aliens = []

        alien_sprites = [[pygame.image.load(SPRITE_PATH + s) for s in ss] for ss in ALIEN_SPRITE_NAMES]
        explosion_sprite = pygame.image.load(SPRITE_PATH + ALIEN_EXPLOSION_SPRITE_NAME)
        laser_explosion_sprite = pygame.image.load(SPRITE_PATH + LASER_EXPLOSION_SPRITE_NAME)

        max_w = max([sprites[0].get_rect().w for sprites in alien_sprites])
        max_row_size = max([len(row) for row in ALIEN_FORMATION])
        step = ALIEN_FORMATION_WIDTH / max_row_size
        x0 = (-max_w) // 2 + (WORLD_DIM[0] - ALIEN_FORMATION_WIDTH) // 2
        xs = [x0 + (step * i) for i in range(max_row_size)]

        destroy_sound = pygame.mixer.Sound(SOUND_PATH + ALIEN_DESTROYED_SOUND)
        move_sound = pygame.mixer.Sound(SOUND_PATH + ALIEN_MOVE_SOUND)
        for row_index, alien_row in enumerate(ALIEN_FORMATION):
            for i, alien_index in enumerate(alien_row):
                sprites = alien_sprites[alien_index - 1]
                w, h = (sprites[0].get_rect().w, sprites[0].get_rect().h)

                center_x = xs[i]
                center_y = h + (2 * h * row_index) + ALIEN_STARTING_POS_Y

                alien_rect = pygame.Rect(
                    center_x - w // 2,
                    center_y - h // 2,
                    w,
                    h,
                )

                aliens.append(
                    Alien(alien_index, alien_rect, sprites, explosion_sprite, laser_explosion_sprite, destroy_sound))

        return Aliens(aliens, move_sound)
