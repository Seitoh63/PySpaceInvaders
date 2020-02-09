from config import SPACESHIP_TOP_LEFT_STARTING_POINT, SPACESHIP_DIMENSION, WORLD_DIMENSION


class Position:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __iter__(self):
        yield self.x
        yield self.y

class Dimension:

    def __init__(self, w, h):
        self.w = w
        self.h = h

    def __iter__(self):
        yield self.w
        yield self.h

class Rectangle:

    def __init__(self, top_left_position: Position, dimension: Dimension):
        self.top_left = top_left_position
        self.dimension = dimension


class HorizontalRectangleMover:

    def __init__(self, min_x, max_x):
        self.min_x = min_x
        self.max_x = max_x

    def move_left(self, rectangle: Rectangle):
        if self.min_x == rectangle.top_left.x:
            return

        rectangle.top_left.x -= 1

    def move_right(self, rectangle: Rectangle):
        if self.max_x == rectangle.top_left.x + rectangle.dimension.w:
            return

        rectangle.top_left.x += 1


class Shooter:

    def fire(self):
        pass


class Destructor:

    def destroy(self):
        pass


class World:

    def __init__(self):
        self.dimension = WORLD_DIMENSION
        self.h_mover = HorizontalRectangleMover(0, self.dimension[0]-1)

class Spaceship:

    def __init__(self, h_mover: HorizontalRectangleMover):
        self.rectangle = self._init_spaceship_rect()
        self.h_mover = h_mover
        self.shooter = Shooter()
        self.destructor = Destructor()

    def _init_spaceship_rect(self):
        spaceship_top_left = Position(*SPACESHIP_TOP_LEFT_STARTING_POINT)
        spaceship_dimension = Dimension(*SPACESHIP_DIMENSION)
        spaceship_rect = Rectangle(spaceship_top_left, spaceship_dimension)
        return spaceship_rect

    def move_left(self):
        self.h_mover.move_left(self.rectangle)

    def move_right(self):
        self.h_mover.move_right(self.rectangle)

    def fire(self):
        self.shooter.fire()

    def destroy(self):
        self.destructor.destroy()
