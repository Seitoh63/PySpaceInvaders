import math
import random
import sys

import pygame

from alien import Aliens
from config import *
from controllers import LifeCounterController
from decor import Ground, Barricades
from spaceship import Spaceship
from ui import Score, LifeCounter, HighScore


class PySpaceInvaders:

    def __init__(self):

        # On crée la surface dans laquelle les sprites vont être affichés
        self.window_surface = pygame.display.set_mode(WINDOW_SIZE)

        # Variables pour la game loop
        self.update_time_delay = 0
        self.draw_time_delay = 0

        # On crée les entités du jeu
        self.spaceship = Spaceship()
        self.aliens = Aliens()
        self.ground = Ground()
        self.barricades = Barricades()
        self.score = Score()
        self.high_score = HighScore()
        self.life_counter = LifeCounter()

        # On crée les controllers
        self.life_counter_controller = LifeCounterController(self.spaceship, self.life_counter)

    def play(self):
        clock = pygame.time.Clock()
        while True:
            dt = clock.tick()

            update_count = self.get_update_count(dt)
            if update_count > 0:
                self.update(update_count * UPDATE_PERIOD_MS)

            frame_count = self.get_frame_count(dt)
            if frame_count > 0:
                self.draw()

    def update(self, dt):

        # On récupère les événements dont les inputs
        events = self.get_events()

        # On met à jour les entités
        self.spaceship.update(dt, events)
        self.aliens.update(dt)

        # On gère les interactions entre entités
        self.life_counter_controller.control()
        self.collide()

    def get_update_count(self, dt):
        # on incrémente le délai depuis la dernière update
        self.update_time_delay += dt

        # On compte combien on devrait avoir d'update. Si plus d'une, on affiche un warning.
        update_count = self.update_time_delay // UPDATE_PERIOD_MS
        if update_count > 1:
            print(str(update_count - 1) + " updates are late.")

        self.update_time_delay = self.update_time_delay % UPDATE_PERIOD_MS

        return update_count

    def get_events(self):
        events = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            events.append(event)
        return events

    def draw(self):

        # d'abord on efface tout ce qui est à l'écran
        self.window_surface.fill((0, 0, 0,))

        # On dessine toutes les entités
        self.ground.draw(self.window_surface)
        self.barricades.draw(self.window_surface)
        self.spaceship.draw(self.window_surface)
        self.aliens.draw(self.window_surface)
        self.score.draw(self.window_surface)
        self.high_score.draw(self.window_surface)
        self.life_counter.draw(self.window_surface)

        # on affiche à l'écran
        pygame.display.flip()

    def get_frame_count(self, dt):
        # on incrémente le délai depuis la dernière frame
        self.draw_time_delay += dt

        # On compte combien on devrait avoir de frame. Si plus d'une, on affiche un warning.
        frame_count = self.draw_time_delay // DRAW_PERIOD_MS
        if frame_count > 1:
            print("Skipping " + str(frame_count - 1) + " frames")

        self.draw_time_delay = self.draw_time_delay % DRAW_PERIOD_MS
        return frame_count

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

        if self._collide_with_barricades(self.spaceship.missile, MISSILE_BARRICADE_EXPLOSION_RADIUS):
            self.spaceship.missile = None

    def _collide_laser_and_barricades(self):

        for laser in self.aliens.lasers:
            if self._collide_with_barricades(laser, LASER_BARRICADE_EXPLOSION_RADIUS):
                self.aliens.lasers.remove(laser)

    def _collide_alien_and_barricades(self):

        for alien in self.aliens:
            self._collide_with_barricades(alien, LASER_BARRICADE_EXPLOSION_RADIUS)

    def _collide_with_barricades(self, shoot, radius):

        w, h = (shoot.rect.w, shoot.rect.h)
        x, y = (shoot.rect.x, shoot.rect.y)
        shoot_mask = pygame.Mask((w, h), fill=True)

        for barricade in self.barricades:
            offset = (x - barricade.rect.x, y - barricade.rect.y)
            collision_point = barricade.mask.overlap(shoot_mask, offset)

            if collision_point:
                cx, cy = collision_point
                for x in range(cx - radius, cx + radius + 1, 1):
                    for y in range(cy - radius, cy + radius + 1, 1):
                        if x < 0 or x >= barricade.rect.w or y < 0 or y >= barricade.rect.h:
                            continue
                        if math.sqrt((x - cx) ** 2 + (y - cy) ** 2) > radius:
                            continue

                        if x == cx and y == cy:
                            barricade.mask.set_at((x, y), 0)
                        elif random.random() < BARRICADE_DESTRUCTION_PROBABILITY:
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
    pygame.init()
    game = PySpaceInvaders()
    game.play()
