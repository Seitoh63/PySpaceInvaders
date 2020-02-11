from unittest import TestCase

import pygame

from config import WORLD_DIMENSION
from input import KeyboardInput
from logic import World, Spaceship


class Event:

    def __init__(self, type, key):
        self.type = type
        self.key = key


class TestLogic(TestCase):

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_world(self):
        world = World()
        self.assertEqual(WORLD_DIMENSION, tuple(world.dimension))

    def test_move(self):
        world = World()
        spaceship = world.spaceship
        keyboard_input = KeyboardInput()
        event = Event(pygame.KEYDOWN, pygame.K_LEFT)
        keyboard_input.handle_keyboard_input(event,world)

        world.update(10**6)
        self.assertEqual(world.h_mover.min_x, spaceship.rectangle.top_left.x)

        event = Event(pygame.KEYUP, pygame.K_LEFT)
        keyboard_input.handle_keyboard_input(event,world)
        event = Event(pygame.KEYDOWN, pygame.K_RIGHT)
        keyboard_input.handle_keyboard_input(event,world)
        world.update(10**6)
        self.assertEqual(world.h_mover.max_x - spaceship.rectangle.dimension.w, spaceship.rectangle.top_left.x)
