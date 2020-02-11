import random
import threading
import time

import pygame

from config import WINDOW_DIMENSION, WINDOW_UPDATE_PERIOD_MS, WINDOW_THREAD_NAME
from logic import Spaceship, World, Rectangle


def rectangle_to_pygame_rect(rectangle: Rectangle):
    pos = rectangle.top_left
    dim = rectangle.dimension
    r = pygame.Rect(pos.x, pos.y, dim.w, dim.h)
    return r


class SpaceshipPainter:

    def __init__(self):
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def paint(self, surf: pygame.Surface, spaceship: Spaceship):
        spaceshp_pyrect = rectangle_to_pygame_rect(spaceship.rectangle)
        pygame.draw.rect(surf, self.color, spaceshp_pyrect)


class WorldPainter:

    def __init__(self, world: World):
        self.world = world
        self.spaceship_painter = SpaceshipPainter()

    def paint(self, surf: pygame.Surface):
        self.spaceship_painter.paint(surf, self.world.spaceship)


class Window:

    def __init__(self, painter):
        self._create_window()

        self.painter = painter

        self._stop_event = threading.Event()
        self.thread = threading.Thread(target=self._loop, name=WINDOW_THREAD_NAME)
        self.thread.start()

    def _create_window(self):
        pygame.display.init()
        self.surface = pygame.display.set_mode(WINDOW_DIMENSION)

    def _loop(self):
        while True:

            if self._stop_event.is_set():
                break

            self.painter.paint(self.surface)

            pygame.display.flip()
            time.sleep(WINDOW_UPDATE_PERIOD_MS)

        pygame.display.quit()

    def stop(self):
        self._stop_event.set()
