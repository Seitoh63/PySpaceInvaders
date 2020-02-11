import sys

import pygame

from graphics import Window, WorldPainter
from logic import World


class PySpaceInvaders:

    def __init__(self):
        pygame.init()

        self.world = World()
        self.world_painter = WorldPainter(self.world)
        self.window = Window(self.world_painter)
        self._loop()

    def _loop(self):
        while True:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.window.stop()
                    sys.exit()


PySpaceInvaders()
