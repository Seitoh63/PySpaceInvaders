import random

import pygame

from config import *
from tools import MovingDirection


class Saucer:

    def __init__(self):

        self.sprite = pygame.image.load(SPRITE_PATH + SAUCER_SPRITE_NAME)
        self.explosion_sprite = pygame.image.load(SPRITE_PATH + SAUCER_EXPLOSION_SPRITE_NAME)

        self.rect = self.sprite.get_rect()
        self.moving_direction = None
        self.move_amount = 0

        self.is_exploded = False
        self.time_since_explosion = 0
        self.explosion_duration = SAUCER_EXPLOSION_DURATION_MS

        self.saucer_sound = pygame.mixer.Sound(SOUND_PATH + SAUCER_SOUND)
        self.saucer_destruction_sound = pygame.mixer.Sound(SOUND_PATH + SAUCER_DESTRUCTION_SOUND)
        self.is_active = False

    def launch(self, top_left_pos, direction: MovingDirection):
        self.rect = self.sprite.get_rect(topleft=top_left_pos)
        self.moving_direction = direction
        self.saucer_sound.play(loops=-1)
        self.is_active = True

        self.is_exploded = False
        self.time_since_explosion = 0

    def update(self, dt):
        if self.is_exploded:
            self.time_since_explosion += dt
        self._move(dt)

    def _move(self, dt):
        if self.is_exploded:
            return
        self.move_amount += dt / 1000 * SAUCER_SPEED_PIXEL_PER_SECOND
        if self.move_amount > 1.:
            self.rect.x += int(self.move_amount) * self.moving_direction.value[0][0]
            self.move_amount -= int(self.move_amount)

    def draw(self, surf: pygame.Surface):

        if not self.is_active:
            return

        if self.is_exploded:
            surf.blit(self.explosion_sprite, self.rect)
        else:
            surf.blit(self.sprite, self.rect)

    def explode(self):
        self.is_exploded = True
        self.saucer_sound.stop()
        self.saucer_destruction_sound.play()

    def set_inactive(self):
        self.is_active = False
        self.saucer_sound.stop()
        self.saucer_destruction_sound.stop()

class Laser:

    def __init__(self, top_left_pos, type_index: int):

        self.moving_direction = MovingDirection.DOWN
        self.move_amount = 0

        self.sprites = [pygame.image.load(SPRITE_PATH + s) for s in LASER_SPRITE_NAMES[type_index]]
        self.sprite_index = 0

        self.rect = pygame.Rect(top_left_pos, self.sprites[self.sprite_index].get_rect().size)

        self.is_exploded = False
        self.time_since_explosion = 0
        self.explosion_sprite = pygame.image.load(SPRITE_PATH + LASER_EXPLOSION_SPRITE_NAME)


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
            surf.blit(self.explosion_sprite, self.explosion_sprite.get_rect(center=self.rect.center))

        else:
            sprite = self.sprites[self.sprite_index]
            surf.blit(sprite, sprite.get_rect(center=self.rect.center))
            self.sprite_index = (self.sprite_index + 1) % len(self.sprites)

    def explode(self):
        self.is_exploded = True


class Alien:

    def __init__(self, type: int, top_left_pos):

        # Type of alien, defining its sprite
        self.type = type
        self.sprites = [pygame.image.load(SPRITE_PATH + s) for s in ALIEN_SPRITE_NAMES[type - 1]]
        self.explosion_sprite = pygame.image.load(SPRITE_PATH + ALIEN_EXPLOSION_SPRITE_NAME)

        self.sprite_index = 0
        self.last_sprite_shift_delay = 0
        self.shift_sprite_period = ALIEN_SPRITE_SHIFT_PERIOD_MS

        self.rect = self.sprites[self.sprite_index].get_rect(topleft=top_left_pos)

        self.move_amount = 0

        self.delay_since_explosion = 0
        self.is_exploded = False

        self.destroy_sound = pygame.mixer.Sound(SOUND_PATH + ALIEN_DESTROYED_SOUND)

    def update(self, dt, movement):
        if self.is_exploded:
            self.delay_since_explosion += dt

        self._move(movement)
        self._sprite_shift(dt)

    def _move(self, movement):
        self.rect.y += movement[1]
        self.rect.x += movement[0]

    def fire(self):
        return Laser(
            (self.rect.centerx - (LASER_RECT_DIM[0] // 2), self.rect.bottom),
            random.randint(0, len(LASER_SPRITE_NAMES) - 1)
        )

    def draw(self, surf: pygame.Surface):

        if self.is_exploded:
            explosion_rect = self.explosion_sprite.get_rect()
            explosion_rect.center = self.rect.center
            surf.blit(self.explosion_sprite, explosion_rect)
        else:
            surf.blit(self.sprites[self.sprite_index], self.rect)

    def _sprite_shift(self, dt):
        self.last_sprite_shift_delay += dt
        if self.last_sprite_shift_delay > self.shift_sprite_period:
            self.sprite_index += 1
            self.sprite_index %= len(self.sprites)
            self.last_sprite_shift_delay -= self.shift_sprite_period

    def explode(self):
        self.is_exploded = True
        self.destroy_sound.play()


class Aliens:

    def __init__(self):

        self.alien_list = self._init_alien_list()
        self.rect = self._get_rect()
        self.lasers = []
        self.saucer = Saucer()

        self.movement_direction = MovingDirection.RIGHT
        self.last_movement_sequence_delay = 0
        self.movement_speed = ALIEN_SPEED_PIXEL_PER_SECOND
        self.move_amount = 0

        self.move_sounds = [pygame.mixer.Sound(SOUND_PATH + sound) for sound in ALIEN_MOVE_SOUNDS]
        self.sound_index = 0
        self.move_sounds[0].play(loops=-1)

        self.last_firing_delay = 0

        self.last_saucer_appearing_delay = 0

        self.starting_alien_count = len(self.alien_list)
        self.acceleration_step = 0

    def _init_alien_list(self):

        # Quite cryptic function but it does the job
        # TODO : improve readability
        aliens = []
        alien_sprites = [[pygame.image.load(SPRITE_PATH + s) for s in ss] for ss in ALIEN_SPRITE_NAMES]
        max_w = max([sprites[0].get_rect().w for sprites in alien_sprites])
        max_row_size = max([len(row) for row in ALIEN_FORMATION])
        step = ALIEN_FORMATION_WIDTH_PIXELS / max_row_size
        x0 = (-max_w) // 2 + (WORLD_DIM[0] - ALIEN_FORMATION_WIDTH_PIXELS) // 2
        xs = [x0 + (step * i) for i in range(max_row_size)]
        for row_index, alien_row in enumerate(ALIEN_FORMATION):
            for i, alien_index in enumerate(alien_row):
                sprites = alien_sprites[alien_index - 1]
                w, h = (sprites[0].get_rect().w, sprites[0].get_rect().h)
                center_x = xs[i]
                center_y = h + (2 * h * row_index) + ALIEN_STARTING_POS_Y
                aliens.append(Alien(alien_index, (center_x - w // 2, center_y - h // 2)))

        return aliens

    def __iter__(self):
        return self.alien_list.__iter__()

    def __next__(self):
        return next(self.__iter__())

    def reset(self):
        # We stop every sound
        for sound in self.move_sounds:
            sound.stop()

        self.alien_list = self._init_alien_list()
        self.rect = self._get_rect()
        self.lasers = []

        self.movement_direction = MovingDirection.RIGHT
        self.last_movement_sequence_delay = 0
        self.move_amount = 0
        self.movement_speed = ALIEN_SPEED_PIXEL_PER_SECOND

        self.sound_index = 0
        self.move_sounds[0].play(loops=-1)

        self.last_firing_delay = 0

        self.last_saucer_appearing_delay = 0

        self.acceleration_step = 0

    def update(self, dt):

        # Starting to play the move sound if it's the first update
        if self.sound_index == -1:
            self.move_sounds[0].play(loops=-1)
            self.sound_index = 0

        # Updating each inner entity
        self._update_aliens(dt)
        self._update_lasers(dt)
        self._update_saucer(dt)

        # If no more aliens, we reset them
        if not self.alien_list:
            self.reset()

    def _update_aliens(self, dt):
        self._fire(dt)
        self._accelerate()
        self._remove_aliens()
        self._update_alien(dt)

    def _fire(self, dt):

        # Incrementing delay since last firing time
        self.last_firing_delay += dt

        # Fire as many laser as needed
        while self.last_firing_delay > ALIEN_FIRING_PERIOD_MS:
            self.last_firing_delay -= ALIEN_FIRING_PERIOD_MS

            # Find all aliens that may fire
            firing_aliens = self._firing_aliens()

            # If no one can fire, leave
            if not firing_aliens:
                return

            # Choose a random alien, make it fire and add laser for updates
            alien = random.choice(firing_aliens)
            self.lasers.append(alien.fire())

    def _firing_aliens(self):

        # Group the alien by columns in a dict
        xs = set(alien.rect.centerx for alien in self.alien_list)
        alien_dict = {x: [] for x in xs}
        for alien in self.alien_list:
            alien_dict[alien.rect.centerx].append(alien)

        # identify lowest alien on each column
        lowest_aliens = []
        for x in xs:
            max_alien = None
            max_alien_y = 0
            for alien in alien_dict[x]:
                if alien.rect.bottom > max_alien_y:
                    max_alien = alien
                    max_alien_y = alien.rect.bottom
            if max_alien: lowest_aliens.append(max_alien)

        return lowest_aliens

    def _accelerate(self):

        # If already at max speed, we leave
        if self.acceleration_step >= len(self.move_sounds):
            return

        # Each time the total number of aliens is divided by 2, we accelerate
        if len(self.alien_list) <= self.starting_alien_count // (2 ** (self.acceleration_step + 1)):
            self.acceleration_step += 1
            self.movement_speed *= 2
            self.move_sounds[self.acceleration_step - 1].stop()
            self.move_sounds[self.acceleration_step].play(loops=-1)

            # We accelerate the sprite shift period of alien
            for alien in self.alien_list:
                alien.shift_sprite_period = alien.shift_sprite_period // 2

    def _remove_aliens(self):
        for alien in self:
            if alien.delay_since_explosion > ALIEN_EXPLOSION_DURATION_MS:
                self._remove_alien(alien)

    def _update_alien(self, dt):

        if not self.alien_list:
            return

        movement = self._get_alien_movement(dt)
        for alien in self:
            alien.update(dt, movement)

    def _get_alien_movement(self, dt):
        # get the x sign of the movement direction
        movement_direction_values = self.movement_direction.value[0]

        # Check how many pixels to move
        dt_s = dt / 1000
        self.move_amount += dt_s * self.movement_speed

        # if more than one pixel to move
        movement = (0, 0)
        if self.move_amount > 1.:
            ps = int(self.move_amount)
            movement = ps * movement_direction_values
            self.move_amount -= ps

        # Move alien rectangle
        self.rect = self._get_rect()
        self.rect.left += movement[0]
        self.rect.top += movement[1]

        # If too far right, we drop one line and go left
        if self.movement_direction == MovingDirection.RIGHT and self.rect.right >= WORLD_DIM[0]:
            movement = (movement[0] - (self.rect.right - WORLD_DIM[0]), movement[1] + self.alien_list[0].rect.h)
            self.movement_direction = MovingDirection.LEFT

        # If too far left, we drop one line and go right
        if self.movement_direction == MovingDirection.LEFT and self.rect.left <= 0:
            movement = (movement[0] - self.rect.left, movement[1] + self.alien_list[0].rect.h)
            self.movement_direction = MovingDirection.RIGHT

        return movement

    def draw(self, surf):
        for alien in self:
            alien.draw(surf)
        for laser in self.lasers:
            laser.draw(surf)
        self.saucer.draw(surf)

    def _remove_alien(self, alien):
        self.alien_list.remove(alien)

    def _update_lasers(self, dt):
        for laser in self.lasers:

            laser.update(dt)

            # If laser  out of screen, we explode it
            if laser.rect.bottom >= WORLD_DIM[1]:
                laser.explode()

            # If laser is destroyed for too long, we remove it from the list
            if laser.is_exploded and laser.time_since_explosion > ALIEN_EXPLOSION_DURATION_MS:
                self.lasers.remove(laser)
                continue

    def _update_saucer(self, dt):

        # increment the delay since the last apparition of saucer
        self.last_saucer_appearing_delay += dt
        if self.last_saucer_appearing_delay > SAUCER_POP_PERIOD_S * 1000:
            self.last_saucer_appearing_delay -= SAUCER_POP_PERIOD_S * 1000
            self._launch_saucer()

        # If saucer is inactive, nothing to do
        if not self.saucer.is_active:
            return

        self.saucer.update(dt)

        # if saucer out of screen, set it inactive
        if self.saucer.rect.x > WORLD_DIM[0] or self.saucer.rect.right < 0:
            self.saucer.set_inactive()

        # If is exploded for too long, set it inactive
        if self.saucer.is_exploded and self.saucer.time_since_explosion > self.saucer.explosion_duration:
            self.saucer.set_inactive()

    def _get_rect(self):

        if not self.alien_list:
            return pygame.Rect((0, 0), (0, 0))

        x0 = min(alien.rect.left for alien in self.alien_list)
        y0 = min(alien.rect.top for alien in self.alien_list)
        x1 = max(alien.rect.right for alien in self.alien_list)
        y1 = max(alien.rect.bottom for alien in self.alien_list)
        rect = pygame.Rect(x0, y0, x1 - x0, y1 - y0)
        return rect

    def _launch_saucer(self):

        xs = [0, WORLD_DIM[0] - self.saucer.rect.w]
        dirs = [MovingDirection.RIGHT, MovingDirection.LEFT]
        index = random.choice([0, 1])
        x = xs[index]
        y = SAUCER_STARTING_POS_Y
        direction = dirs[index]

        self.saucer.launch((x, y), direction)
