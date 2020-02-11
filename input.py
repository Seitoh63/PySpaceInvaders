import pygame


class KeyboardInput:

    def __init__(self):
        pass

    def handle_keyboard_input(self, event, world):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                world.spaceship.move_left()

            if event.key == pygame.K_RIGHT:
                world.spaceship.move_right()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and world.spaceship.is_moving_left():
                world.spaceship.stop_moving()

            if event.key == pygame.K_RIGHT and world.spaceship.is_moving_right():
                world.spaceship.stop_moving()
