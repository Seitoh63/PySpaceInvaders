import pygame

from config import *


class Ground:

    def __init__(self):
        pass

    def draw(self, surf: pygame.Surface):
        pygame.draw.line(surf, (0, 255, 0), (0, WORLD_DIM[1] - 1), (WORLD_DIM[0] - 1, WORLD_DIM[1] - 1))


class Barricade:

    def __init__(self, rect: pygame.Rect, barricade_sprite: pygame.Surface):
        self.sprite = barricade_sprite
        self.rect = rect
        self.mask = pygame.mask.from_threshold(self.sprite, (0, 0, 0, 0), (1, 1, 1, 255))
        self.mask.invert()

    def draw(self, surf: pygame.Surface):
        surf.blit(self.sprite, self.rect)

    @staticmethod
    def generate_barricades():
        barricades = []

        for b_pos in BARRICADE_POSITIONS:
            surf = pygame.image.load(SPRITE_PATH + BARRICADE_SPRITE_NAME)
            rect = surf.get_rect()
            rect.center = b_pos
            barricades.append(Barricade(rect, surf))

        return barricades
