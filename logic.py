class Position:

    def __init__(self, x, y):
        self.x = x
        self.y = y


class HorizontalMover:

    def move_left(self, pos: Position):
        pos.x -= 1

    def move_right(self, pos: Position):
        pos.x += 1


class Shooter:

    def fire(self):
        pass


class Destructor:

    def destroy(self):
        pass


class Spaceship:

    def __init__(self, position):
        self.pos = position
        self.h_mover = HorizontalMover()
        self.shooter = Shooter()
        self.destructor = Destructor()

    def move_left(self):
        self.h_mover.move_left(self.pos)

    def move_right(self):
        self.h_mover.move_right(self.pos)

    def fire(self):
        self.shooter.fire()

    def destroy(self):
        self.destructor.destroy()
