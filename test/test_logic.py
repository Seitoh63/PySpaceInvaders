from unittest import TestCase

from config import WORLD_DIMENSION, SPACESHIP_DIMENSION, SPACESHIP_TOP_LEFT_STARTING_POINT
from logic import World, Spaceship


class TestLogic(TestCase):

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_world(self):
        world = World()
        self.assertEqual(WORLD_DIMENSION, tuple(world.dimension))

    def test_spaceship(self):
        world = World()
        spaceship = Spaceship(world.h_mover)

        self.assertEqual(SPACESHIP_DIMENSION, tuple(spaceship.rectangle.dimension))
        self.assertEqual(SPACESHIP_TOP_LEFT_STARTING_POINT, tuple(spaceship.rectangle.top_left))

        spaceship.move_left()
        self.assertEqual(SPACESHIP_TOP_LEFT_STARTING_POINT[0]-1, spaceship.rectangle.top_left.x)

        spaceship.move_right()
        spaceship.move_right()
        self.assertEqual(SPACESHIP_TOP_LEFT_STARTING_POINT[0]+1, spaceship.rectangle.top_left.x)

        for _ in range(5000) : spaceship.move_right()
        self.assertEqual(world.h_mover.max_x - spaceship.rectangle.dimension.w, spaceship.rectangle.top_left.x)

        for _ in range(5000) : spaceship.move_left()
        self.assertEqual(world.h_mover.min_x, spaceship.rectangle.top_left.x)