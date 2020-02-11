from config import SPACESHIP_TOP_LEFT_STARTING_POINT, SPACESHIP_DIMENSION, WORLD_DIMENSION, \
    SPACESHIP_SPEED_PIXEL_PER_SECOND


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

    def move_left(self, rectangle: Rectangle, distance):
        rectangle.top_left.x -= distance
        if self.min_x > rectangle.top_left.x:
            rectangle.top_left.x =  self.min_x

    def move_right(self, rectangle: Rectangle, distance):
        rectangle.top_left.x += distance
        if self.max_x < rectangle.top_left.x + rectangle.dimension.w:
            rectangle.top_left.x = self.max_x- rectangle.dimension.w


class Shooter:

    def fire(self):
        pass


class Destructor:

    def destroy(self):
        pass


class World:

    def __init__(self):
        self.dimension = WORLD_DIMENSION
        self.h_mover = HorizontalRectangleMover(0, self.dimension[0] - 1)
        self.spaceship = Spaceship(self.h_mover)

    def update(self, dt_ms):
        self.spaceship.update(dt_ms)

class Spaceship:

    MOVING_LEFT = -1
    MOVING_RIGHT = 1
    NOT_MOVING = 0

    def __init__(self, h_mover: HorizontalRectangleMover):
        self.rectangle = self._init_spaceship_rect()
        self.h_mover = h_mover
        self.shooter = Shooter()
        self.destructor = Destructor()
        self.move = Spaceship.NOT_MOVING
        self.move_amount_in_pixels = 0

    def _init_spaceship_rect(self):
        spaceship_top_left = Position(*SPACESHIP_TOP_LEFT_STARTING_POINT)
        spaceship_dimension = Dimension(*SPACESHIP_DIMENSION)
        spaceship_rect = Rectangle(spaceship_top_left, spaceship_dimension)
        return spaceship_rect

    def move_left(self):
        self.move = Spaceship.MOVING_LEFT

    def move_right(self):
        self.move = Spaceship.MOVING_RIGHT

    def is_moving_left(self):
        return self.move == Spaceship.MOVING_LEFT

    def is_moving_right(self):
        return self.move == Spaceship.MOVING_RIGHT

    def is_moving(self):
        return self.is_moving_right() or self.is_moving_left()

    def stop_moving(self):
        self.move = Spaceship.NOT_MOVING

    def fire(self):
        self.shooter.fire()

    def destroy(self):
        self.destructor.destroy()

    def update(self, dt_ms):

        if not self.is_moving() :
            return

        self.move_amount_in_pixels += dt_ms / 1000 * SPACESHIP_SPEED_PIXEL_PER_SECOND

        move_amount_in_pixels_int = int(self.move_amount_in_pixels)
        if self.move == Spaceship.MOVING_LEFT :
            self.h_mover.move_left(self.rectangle,move_amount_in_pixels_int )
        if self.move == Spaceship.MOVING_RIGHT:
            self.h_mover.move_right(self.rectangle,move_amount_in_pixels_int)
        self.move_amount_in_pixels -= move_amount_in_pixels_int