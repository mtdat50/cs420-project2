import pygame
from Cell import Cell

class Object(pygame.sprite.Sprite):
    def __init__(self, picture_path, cell: Cell | None = None, pos_x: int | None = None, pos_y: int | None = None):
        super().__init__()

        self.image = pygame.image.load(picture_path).convert_alpha()
        self.rect = self.image.get_rect()

        if cell:
            self.rect.center = cell.rect.center
        if pos_x != None and pos_y != None:
            self.rect.topleft = (pos_x, pos_y)