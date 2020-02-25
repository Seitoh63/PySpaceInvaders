import sys

import pygame

from alien import AlienGenerator
from config import *
from decor import Ground, Barricade
from spaceship import SpaceshipGenerator
from ui import Score, LifeCounter, HighScore


class PySpaceInvaders:

    def __init__(self):
        pygame.init()
        self.window_surface = pygame.display.set_mode(WINDOW_SIZE)

        self.spaceship = SpaceshipGenerator.generate()
        self.aliens = AlienGenerator.generate()
        self.ground = Ground()
        self.barricades = Barricade.generate_barricades()

        digit_sprites = [pygame.image.load(SPRITE_PATH + str(i) + ".png") for i in range(0, 10)]
        score_sprite = pygame.image.load(SPRITE_PATH + "score.png")
        high_score_sprite = pygame.image.load(SPRITE_PATH + "high_score.png")
        self.score = Score(digit_sprites, score_sprite)
        self.high_score = HighScore(digit_sprites, high_score_sprite)
        self.life_counter = LifeCounter(STARTING_LIFE_COUNT, pygame.image.load(SPRITE_PATH+SPACESHIP_SPRITE_NAME), digit_sprites)


        self.update_time_delay = 0
        self.draw_time_delay = 0

    def play(self):

        clock = pygame.time.Clock()
        while True:
            dt = clock.tick()

            self.update(dt)
            self.draw(dt)

    def get_events(self):
        events = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            events.append(event)
        return events

    def update(self, dt):
        self.update_time_delay += dt

        if self.update_time_delay < UPDATE_PERIOD_MS:
            return

        update_count = self.update_time_delay // UPDATE_PERIOD_MS
        if update_count > 1:
            print("Skipping " + str(update_count - 1) + " updates")

        events = self.get_events()

        if self.spaceship:
            self.spaceship.update(update_count * UPDATE_PERIOD_MS, events)
            if self.spaceship.is_destroyed and self.spaceship.delay_since_explosion > SPACESHIP_EXPLOSION_DURATION_MS:
                self.spaceship = None

        else :

            if self.life_counter.life_count > 0 :
                self.life_counter.life_count -= 1
                self.spaceship = SpaceshipGenerator.generate()

        self.aliens.update(update_count * UPDATE_PERIOD_MS)

        self.collide()

        self.update_time_delay = self.update_time_delay % UPDATE_PERIOD_MS

    def draw(self, dt):
        self.draw_time_delay += dt

        if self.draw_time_delay < DRAW_PERIOD_MS:
            return

        frame_count = self.draw_time_delay // DRAW_PERIOD_MS
        if frame_count > 1:
            print("Skipping " + str(frame_count - 1) + " frames")

        self.window_surface.fill((0, 0, 0,))

        self.ground.draw(self.window_surface)
        for barricade in self.barricades:
            barricade.draw(self.window_surface)

        if self.spaceship:  self.spaceship.draw(self.window_surface)
        self.aliens.draw(self.window_surface)

        self.score.draw(self.window_surface)
        self.high_score.draw(self.window_surface)
        self.life_counter.draw(self.window_surface)

        pygame.display.flip()

        self.draw_time_delay = self.draw_time_delay % DRAW_PERIOD_MS

    def collide(self):
        self._collide_missile_and_aliens()
        self._collide_spaceship_and_aliens()
        self._collide_spaceship_and_lasers()
        self._collide_missile_and_lasers()
        self._collide_missile_and_barricades()
        self._collide_laser_and_barricades()
        self._collide_alien_and_barricades()
        self._collide_missile_and_soucoup()

    def _collide_missile_and_aliens(self):
        if self.spaceship is None or self.spaceship.missile is None:
            return
        missile_rect = self.spaceship.missile.rect
        for alien in self.aliens:
            if missile_rect.colliderect(alien.rect):
                alien.explode()
                self.score.score += alien.type * 10
                self.spaceship.missile = None

    def _collide_missile_and_soucoup(self):
        if self.spaceship is None or self.spaceship.missile is None or self.aliens.soucoup is None:
            return

        missile_rect = self.spaceship.missile.rect
        soucoup_rect = self.aliens.soucoup.rect
        if missile_rect.colliderect(soucoup_rect):
            self.aliens.soucoup.explode()
            self.spaceship.missile = None
            self.score.score += 300

    def _collide_spaceship_and_aliens(self):
        for alien in self.aliens:

            if self.spaceship is None:
                return

            if alien.rect.colliderect(self.spaceship.rect):
                self.spaceship.destroy()

    def _collide_spaceship_and_lasers(self):

        if self.spaceship is None:
            return

        laser_rect_list = [laser.rect for laser in self.aliens.lasers]
        spaceship_rect = self.spaceship.rect
        if spaceship_rect.collidelist(laser_rect_list) != - 1:
            self.spaceship.destroy()

    def _collide_missile_and_lasers(self):

        if self.spaceship is None or self.spaceship.missile is None:
            return

        laser_rect_list = [laser.rect for laser in self.aliens.lasers]
        missile_rect = self.spaceship.missile.rect
        laser_index = missile_rect.collidelist(laser_rect_list)
        if laser_index != -1:
            self.spaceship.missile = None
            self.aliens.lasers.pop(laser_index)

    def _collide_missile_and_barricades(self):

        if self.spaceship is None or self.spaceship.missile is None:
            return

        if self._collide_with_barricades(self.spaceship.missile):
            self.spaceship.missile = None

    def _collide_laser_and_barricades(self):

        for laser in self.aliens.lasers:
            if self._collide_with_barricades(laser):
                self.aliens.lasers.remove(laser)

    def _collide_alien_and_barricades(self):

        for alien in self.aliens:
            self._collide_with_barricades(alien)

    def _collide_with_barricades(self, shoot):

        w, h = (shoot.rect.w, shoot.rect.h)
        x, y = (shoot.rect.x, shoot.rect.y)
        shoot_mask = pygame.Mask((w, h), fill=True)
        r = BARRICADE_EXPLOSION_RADIUS

        for barricade in self.barricades:
            offset = (x - barricade.rect.x, y - barricade.rect.y)
            collision_point = barricade.mask.overlap(shoot_mask, offset)

            if collision_point:
                cx, cy = collision_point
                for x in range(cx - r, cx + r + 1, 1):
                    for y in range(cy - r, cy + r + 1, 1):
                        if x < 0 or x >= barricade.rect.w or y < 0 or y >= barricade.rect.h:
                            continue
                        barricade.mask.set_at((x, y), 0)

                surf_array = pygame.surfarray.array3d(barricade.sprite)
                for y in range(barricade.rect.h):
                    for x in range(barricade.rect.w):
                        if barricade.mask.get_at((x, y)) == 0:
                            surf_array[x, y] = (0, 0, 0)
                barricade.sprite = pygame.surfarray.make_surface(surf_array)

                return True

        return False


if __name__ == "__main__":
    game = PySpaceInvaders()
    game.play()
