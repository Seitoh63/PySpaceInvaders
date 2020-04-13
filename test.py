import pygame

from config import LASER_SPRITE_NAMES, SPRITE_PATH

for sprite_row in LASER_SPRITE_NAMES:
    for sprite_name in sprite_row:
        sprite = pygame.image.load(SPRITE_PATH + sprite_name)

        sprite2 = pygame.transform.scale2x(sprite)

        pygame.image.save(sprite2, sprite_name)
