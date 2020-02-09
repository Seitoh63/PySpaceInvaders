import sys

import pygame

from graphics import Window
from logic import World


class PySpaceInvaders:

    def __init__(self):
        pygame.init()
        self.window = Window()
        self.world = World()

        self._loop()

    def _loop(self):
        while True:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.window.stop()
                    sys.exit()


PySpaceInvaders()
