import sys

import pygame

from alien import AlienGenerator
from config import *
from spaceship import SpaceshipGenerator


class PySpaceInvaders:

    def __init__(self):
        pygame.init()
        self.window_surface = pygame.display.set_mode(WINDOW_SIZE)

        self.spaceship = SpaceshipGenerator.generate()
        self.aliens = AlienGenerator.generate()

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

        if self.spaceship: self.spaceship.update(update_count*UPDATE_PERIOD_MS, events)
        self.aliens.update(update_count*UPDATE_PERIOD_MS)

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

        if self.spaceship:  self.spaceship.draw(self.window_surface)
        self.aliens.draw(self.window_surface)

        pygame.display.flip()

        self.draw_time_delay = self.draw_time_delay %  DRAW_PERIOD_MS

    def collide(self):
        self._collide_missile_and_aliens()
        self._collide_spaceship_and_aliens()
        self._collide_spaceship_and_lasers()
        self._collide_missile_and_lasers()

    def _collide_missile_and_aliens(self):
        if self.spaceship is None or self.spaceship.missile is None:
            return
        missile_rect = self.spaceship.missile.rect
        for alien in self.aliens:
            if missile_rect.colliderect(alien.rect):
                self.aliens.remove(alien)
                self.spaceship.missile = None

    def _collide_spaceship_and_aliens(self):
        for alien in self.aliens:

            if self.spaceship is None:
                return

            if alien.rect.colliderect(self.spaceship.rect):
                self.spaceship = None

    def _collide_spaceship_and_lasers(self):

        if self.spaceship is None:
            return

        laser_rect_list = [laser.rect for laser in self.aliens.lasers]
        spaceship_rect = self.spaceship.rect
        if spaceship_rect.collidelist(laser_rect_list) != - 1:
            self.spaceship = None

    def _collide_missile_and_lasers(self):

        if self.spaceship is None or self.spaceship.missile is None:
            return

        laser_rect_list = [laser.rect for laser in self.aliens.lasers]
        missile_rect = self.spaceship.missile.rect
        laser_index = missile_rect.collidelist(laser_rect_list)
        if laser_index != -1:
            self.spaceship.missile = None
            self.aliens.lasers.pop(laser_index)


if __name__ == "__main__":
    game = PySpaceInvaders()
    game.play()
