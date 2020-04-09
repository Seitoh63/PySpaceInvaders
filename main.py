import math
import random
import sys

import pygame

from alien import Aliens
from config import *
from decor import Ground, Barricades
from spaceship import Spaceship
from ui import Score, LifeCounter, HighScore


class PySpaceInvaders:

    def __init__(self):

        # We create a surface in which sprites will be shown
        self.window_surface = pygame.display.set_mode(WINDOW_SIZE)

        # Variables for game loop
        self.update_time_delay = 0
        self.draw_time_delay = 0

        # We create the game entities
        self.spaceship = Spaceship()
        self.aliens = Aliens()
        self.ground = Ground()
        self.barricades = Barricades()
        self.score = Score()
        self.high_score = HighScore()
        self.life_counter = LifeCounter()

    def play(self):
        clock = pygame.time.Clock()
        while True:
            dt = clock.tick()

            update_count = self._get_update_count(dt)
            if update_count > 0:
                # This update the entities from the game
                self._update(update_count * UPDATE_PERIOD_MS)

                # Here, it's all the update that involves several entities, like collision
                self._update_life_count()
                self._collide()

            frame_count = self._get_frame_count(dt)
            if frame_count > 0:
                self._draw()

    def _update(self, dt):

        # Getting input events
        events = self._get_events()

        # Updating each entity
        self.spaceship.update(dt, events)
        self.aliens.update(dt)

    def _update_life_count(self):
        if not self.spaceship.is_active:
            if self.life_counter.life_count > 0:
                self.life_counter.life_count -= 1
                self.spaceship.reset()

    def _get_update_count(self, dt):
        # Incrementing the delay since previous update
        self.update_time_delay += dt

        # Count how many updates should be done. If more than one, a warning is shown
        update_count = self.update_time_delay // UPDATE_PERIOD_MS
        if update_count > 1:
            print(str(update_count - 1) + " updates are late.")

        self.update_time_delay = self.update_time_delay % UPDATE_PERIOD_MS

        return update_count

    def _get_events(self):
        events = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            events.append(event)
        return events

    def _draw(self):

        # First we clear everything from screen
        self.window_surface.fill((0, 0, 0,))

        # We draw each entity
        self.ground.draw(self.window_surface)
        self.barricades.draw(self.window_surface)
        self.spaceship.draw(self.window_surface)
        self.aliens.draw(self.window_surface)
        self.score.draw(self.window_surface)
        self.high_score.draw(self.window_surface)
        self.life_counter.draw(self.window_surface)

        # We show the screen
        pygame.display.flip()

    def _get_frame_count(self, dt):
        # Incrementing delay since previous frame
        self.draw_time_delay += dt

        # We count how many frames we should draw. If more than one, we show a warning.
        frame_count = self.draw_time_delay // DRAW_PERIOD_MS
        if frame_count > 1:
            print("Skipping " + str(frame_count - 1) + " frames")

        self.draw_time_delay = self.draw_time_delay % DRAW_PERIOD_MS
        return frame_count

    def _collide(self):
        self._collide_missile_and_aliens()
        self._collide_spaceship_and_aliens()
        self._collide_spaceship_and_lasers()
        self._collide_missile_and_lasers()
        self._collide_missile_and_barricades()
        self._collide_laser_and_barricades()
        self._collide_alien_and_barricades()
        self._collide_missile_and_saucer()

    def _collide_missile_and_aliens(self):

        # If no missile, no collision to check
        if not self.spaceship.missile.is_active:
            return

        # Get rectangle from missile
        missile_rect = self.spaceship.missile.rect

        # Get each alien rectangle and check collision
        for alien in self.aliens:
            if missile_rect.colliderect(alien.rect):
                # if collision, make the alien explode and remove missile
                alien.explode()
                self.spaceship.missile.is_active = False

                # increase score
                self.score.value += alien.type * 10

    def _collide_missile_and_saucer(self):

        # If no missile or no saucer
        if not self.spaceship.missile.is_active or self.aliens.saucer is None:
            return

        # Get rectangle from missile and saucer
        missile_rect = self.spaceship.missile.rect
        saucer_rect = self.aliens.saucer.rect

        # if collision, make the saucer explode and remove missile
        if missile_rect.colliderect(saucer_rect):
            self.aliens.saucer.explode()
            self.spaceship.missile.is_active = False

            # increase score
            self.score.value += 300

    def _collide_spaceship_and_aliens(self):

        # Get each alien rect and check collision with spaceship
        for alien in self.aliens:

            # If spaceship already destroyed, we stop.
            if self.spaceship.is_destroyed:
                return

            if alien.rect.colliderect(self.spaceship.rect):
                self.spaceship.destroy()

    def _collide_spaceship_and_lasers(self):

        # If spaceship already destroyed, we return
        if self.spaceship.is_destroyed:
            return

        # Get each laser rectangle and spaceship rectangle
        laser_rect_list = [laser.rect for laser in self.aliens.lasers]
        spaceship_rect = self.spaceship.rect

        if spaceship_rect.collidelist(laser_rect_list) != - 1:
            self.spaceship.destroy()

    def _collide_missile_and_lasers(self):

        # If no missile, no collision to check
        if not self.spaceship.missile.is_active:
            return

        # Get each laser rectangle and missile rectangle
        laser_rect_list = [laser.rect for laser in self.aliens.lasers]
        missile_rect = self.spaceship.missile.rect

        # If collision, we remove both
        laser_index = missile_rect.collidelist(laser_rect_list)
        if laser_index != -1:
            self.spaceship.missile.is_active = False
            self.aliens.lasers.pop(laser_index)

    def _collide_missile_and_barricades(self):

        # If no missile, no collision to check
        if not self.spaceship.missile.is_active:
            return

        # If collision, update barricade sprite and destroy missile
        if self._collide_with_barricades(self.spaceship.missile, MISSILE_BARRICADE_EXPLOSION_RADIUS):
            self.spaceship.missile.is_active = False

    def _collide_laser_and_barricades(self):

        # If collision, update barricade sprite and destroy laser
        for laser in self.aliens.lasers:
            if self._collide_with_barricades(laser, LASER_BARRICADE_EXPLOSION_RADIUS):
                self.aliens.lasers.remove(laser)

    def _collide_alien_and_barricades(self):

        # If collision, update barricade sprite only, alien continue to live
        for alien in self.aliens:
            self._collide_with_barricades(alien, LASER_BARRICADE_EXPLOSION_RADIUS)

    def _collide_with_barricades(self, shoot, radius):
        for barricade in self.barricades:

            # Find a colliding pixel
            collision_point = self._find_colliding_pixel(shoot, barricade)

            # Handle collision if there is one
            if collision_point:
                self._apply_explosion_on_mask(collision_point, radius, barricade)
                self._build_sprite_from_mask(barricade)

                return True

        return False

    def _find_colliding_pixel(self, shoot, barricade):

        # get distance vector between top left of barricade and colliding entity
        x, y = (shoot.rect.x, shoot.rect.y)
        offset = (x - barricade.rect.x, y - barricade.rect.y)

        # Using mask to get collision point
        w, h = (shoot.rect.w, shoot.rect.h)
        shoot_mask = pygame.Mask((w, h), fill=True)
        return barricade.mask.overlap(shoot_mask, offset)

    def _apply_explosion_on_mask(self, collision_point, radius, barricade):

        # At collision point, remove pixels
        cx, cy = collision_point
        barricade.mask.set_at((cx, cy), 0)

        # Loop on each pixel around collision point
        for x in range(cx - radius, cx + radius + 1, 1):
            for y in range(cy - radius, cy + radius + 1, 1):

                # If not in barricade sprite, continue
                if x < 0 or x >= barricade.rect.w or y < 0 or y >= barricade.rect.h:
                    continue

                # if not in the circle around collision, continue
                if math.sqrt((x - cx) ** 2 + (y - cy) ** 2) > radius:
                    continue

                # We remove the pixel under a given probability
                if random.random() < BARRICADE_DESTRUCTION_PROBABILITY:
                    barricade.mask.set_at((x, y), 0)

    def _build_sprite_from_mask(self, barricade):

        # create an surfarray and change pixel color according to mask
        surf_array = pygame.surfarray.array3d(barricade.sprite)
        for y in range(barricade.rect.h):
            for x in range(barricade.rect.w):
                if barricade.mask.get_at((x, y)) == 0:
                    surf_array[x, y] = (0, 0, 0)

        # make sprite from surfarray.
        barricade.sprite = pygame.surfarray.make_surface(surf_array)


if __name__ == "__main__":
    pygame.init()
    game = PySpaceInvaders()
    game.play()
