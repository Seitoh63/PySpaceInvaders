import pygame

from config import *
from tools import MovingDirection


class Missile:
    def __init__(self, rect: pygame.Rect, explosion_sprite):
        self.rect = rect
        self.moving_direction = MovingDirection.UP
        self.move_amount = 0

        self.is_exploded = False
        self.time_since_explosion = 0
        self.explosion_sprite = explosion_sprite

    def update(self, dt):

        if self.is_exploded:
            self.time_since_explosion += dt
        else:
            self._move(dt)

    def _move(self, dt):
        if self.moving_direction == MovingDirection.IDLE:
            return

        self.move_amount += dt / 1000 * MISSILE_SPEED_PIXEL_PER_SECOND
        if self.move_amount > 1.:
            direction = -1 if self.moving_direction == MovingDirection.UP else 1
            self.rect.y += int(self.move_amount) * direction
            self.move_amount -= int(self.move_amount)

    def draw(self, surf: pygame.Surface):
        if self.is_exploded:
            surf.blit(self.explosion_sprite, self.rect)
        else:
            pygame.draw.rect(surf, MISSILE_RECT_COLOR, self.rect)

    def explode(self):
        self.is_exploded = True

class Spaceship:

    def __init__(self, rect: pygame.Rect, sprite: pygame.Surface, missile_explosion_sprite):
        self.rect = rect
        self.sprite = sprite
        self.missile_explosion_sprite = missile_explosion_sprite
        self.moving_direction = MovingDirection.IDLE
        self.move_amount = 0

        self.firing = False
        self.missile = None

    def update(self, dt, events):

        for event in events:
            self._handle_event(event)

        self._move(dt)

        if self.missile is not None:
            self.missile.update(dt)

            if self.missile.rect.bottom < 0 :
                self.missile.explode()
            if self.missile.time_since_explosion > EXPLOSION_DURATION_MS :
                self.missile = None

        self._fire()

    def draw(self, surf: pygame.Surface):
        surf.blit(self.sprite, self.rect)

        if self.missile is not None:
            self.missile.draw(surf)

    def _handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.moving_direction = MovingDirection.LEFT

            if event.key == pygame.K_RIGHT:
                self.moving_direction = MovingDirection.RIGHT

            if event.key == pygame.K_SPACE:
                self.firing = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and self.moving_direction == MovingDirection.LEFT:
                self.moving_direction = MovingDirection.IDLE

            if event.key == pygame.K_RIGHT and self.moving_direction == MovingDirection.RIGHT:
                self.moving_direction = MovingDirection.IDLE

            if event.key == pygame.K_SPACE:
                self.firing = False

    def _move(self, dt):
        if self.moving_direction == MovingDirection.IDLE:
            return

        self.move_amount += dt / 1000 * SPACESHIP_SPEED_PIXEL_PER_SECOND
        if self.move_amount > 1.:

            direction = -1 if self.moving_direction == MovingDirection.LEFT else 1
            self.rect.x += int(self.move_amount) * direction
            self.move_amount -= int(self.move_amount)

            if self.rect.left < 0: self.rect.x = 0
            if self.rect.right >= WORLD_DIM[0]: self.rect.right = WORLD_DIM[0] - 1

    def _fire(self):

        if not self.firing:
            return

        ### Firing only when there is no actual missile, only one missile at a time
        if self.missile is not None:
            return

        missile_rect = pygame.Rect(
            self.rect.centerx - (MISSILE_RECT_DIM[0] // 2),
            self.rect.top - MISSILE_RECT_DIM[1],
            MISSILE_RECT_DIM[0],
            MISSILE_RECT_DIM[1]
        )

        self.missile = Missile(missile_rect, self.missile_explosion_sprite)


class SpaceshipGenerator:

    @staticmethod
    def generate():
        missile_explosion_sprite = pygame.image.load(SPRITE_PATH + MISSILE_EXPLOSION_SPRITE_NAME)
        sprite = pygame.image.load(SPRITE_PATH + SPACESHIP_SPRITE_NAME)
        w, h = sprite.get_rect().w, sprite.get_rect().h
        spaceship_rect = pygame.Rect(
            0,
            0,
            w,
            h,
        )
        spaceship_rect.center = SPACESHIP_STARTING_POSITION

        return Spaceship(spaceship_rect, sprite, missile_explosion_sprite)
