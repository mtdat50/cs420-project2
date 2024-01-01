import pygame
from Cell import Cell

class Player(pygame.sprite.Sprite):
    def __init__(self, picture_path, cell: Cell):
        super().__init__()

        self.image = pygame.image.load(picture_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = cell.rect.center
