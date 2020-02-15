import sys

import pygame

from alien import AlienGenerator
from config import *
from spaceship import SpaceshipGenerator
from tools import time_ms


class PySpaceInvaders:

    def __init__(self):
        pygame.init()
        self.window_surface = pygame.display.set_mode(WINDOW_SIZE)

        self.spaceship = SpaceshipGenerator.generate()
        self.aliens = AlienGenerator.generate()

        self.last_update_time = None
        self.last_draw_time = None

    def play(self):

        self.last_update_time = time_ms()
        self.last_draw_time = time_ms()

        while True:
            self.update()
            self.draw()

    def get_events(self):
        events = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            events.append(event)
        return events

    def update(self):
        elapsed_time_ms = time_ms() - self.last_update_time
        if elapsed_time_ms < UPDATE_PERIOD_MS:
            return

        update_count = elapsed_time_ms // UPDATE_PERIOD_MS
        if update_count > 1:
            print("Skipping " + str(update_count - 1) + " updates")

        events = self.get_events()

        if self.spaceship: self.spaceship.update(elapsed_time_ms, events)
        self.aliens.update(elapsed_time_ms)

        self.collide()

        self.last_update_time += elapsed_time_ms

    def draw(self):

        elapsed_time_ms = time_ms() - self.last_draw_time
        if elapsed_time_ms < DRAW_PERIOD_MS:
            return

        frame_count = elapsed_time_ms // DRAW_PERIOD_MS
        if frame_count > 1:
            print("Skipping " + str(frame_count - 1) + " frames")

        self.window_surface.fill((0, 0, 0,))

        if self.spaceship:  self.spaceship.draw(self.window_surface)
        self.aliens.draw(self.window_surface)

        pygame.display.flip()

        self.last_draw_time += elapsed_time_ms

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
