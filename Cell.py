import pygame, random

class Cell(pygame.sprite.Sprite):
    def __init__(self, picture_path, pos_x, pos_y):
        super().__init__()
        # Random floor asset
        picture_path += str(random.randrange(0, 11)) + ".png"

        self.image = pygame.image.load(picture_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)