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
        spaceship = world.spaceship
        self.assertEqual(SPACESHIP_DIMENSION, tuple(spaceship.rectangle.dimension))
        self.assertEqual(SPACESHIP_TOP_LEFT_STARTING_POINT, tuple(spaceship.rectangle.top_left))

        spaceship.h_mover.move_left(spaceship.rectangle,1)
        self.assertEqual(SPACESHIP_TOP_LEFT_STARTING_POINT[0]-1, spaceship.rectangle.top_left.x)

        spaceship.h_mover.move_right(spaceship.rectangle,1)
        spaceship.h_mover.move_right(spaceship.rectangle,1)
        self.assertEqual(SPACESHIP_TOP_LEFT_STARTING_POINT[0]+1, spaceship.rectangle.top_left.x)

        spaceship.h_mover.move_right(spaceship.rectangle,5000)
        self.assertEqual(world.h_mover.max_x - spaceship.rectangle.dimension.w, spaceship.rectangle.top_left.x)

        spaceship.h_mover.move_left(spaceship.rectangle,5000)
        self.assertEqual(world.h_mover.min_x, spaceship.rectangle.top_left.x)