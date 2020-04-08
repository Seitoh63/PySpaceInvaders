from spaceship import Spaceship
from ui import LifeCounter


class LifeCounterController:

    def __init__(self, spaceship: Spaceship, life_counter: LifeCounter):
        self.spaceship = spaceship
        self.life_counter = life_counter

    def control(self):
        if not self.spaceship.is_active:
            if self.life_counter.life_count > 0:
                self.life_counter.life_count -= 1
                self.spaceship.reset()
