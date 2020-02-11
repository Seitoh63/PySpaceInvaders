import sys
import time

import pygame

from config import UPDATE_PERIOD_S
from graphics import Window, WorldPainter
from input import KeyboardInput
from logic import World


class PySpaceInvaders:

    def __init__(self):
        pygame.init()

        self.world = World()
        self.world_painter = WorldPainter(self.world)
        self.window = Window(self.world_painter)
        self.keyboard_input = KeyboardInput()

        self._loop()

    def _loop(self):
        self.clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self._quit()

                if event.type in [pygame.KEYUP, pygame.KEYDOWN]:
                    self._handle_keyboard_event(event)

            self._update()

    def _handle_keyboard_event(self, event):
        self.keyboard_input.handle_keyboard_input(event, self.world)

    def _quit(self):
        self.window.stop()
        sys.exit()

    def _update(self):
        elapsed_time = self.clock.tick()
        self.world.update(elapsed_time)

        dt = UPDATE_PERIOD_S - elapsed_time
        time.sleep(dt if dt > 0 else 0)


PySpaceInvaders()
