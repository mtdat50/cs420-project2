import pygame, random
from constants import *

class Cell(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, initial_scale=1.0):
        super().__init__()
        # Random floor asset
        picture_path = "Graphics\\catacombs_" + str(random.randrange(0, 11)) + ".png"

        # Set scale
        self.scale = initial_scale

        # Load image
        self.original_image = pygame.image.load(picture_path).convert_alpha()
        self.image = self.original_image

        # Scale the image based on the current zoom level
        new_width = int(self.original_image.get_width() * self.scale)
        new_height = int(self.original_image.get_height() * self.scale)
        self.image = pygame.transform.scale(self.original_image, (new_width, new_height))

        # Set Rect
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos_x, pos_y)
        print(self.rect.topleft)
        
        # Set fog
        self.fog = Object("Graphics\\unseen.png", self, initial_scale=INIT_ZOOM)

    def remove_fog(self):
        self.fog = None

class Object(pygame.sprite.Sprite):
    def __init__(self, picture_path, cell: Cell | None = None, cell_center: tuple[int, int] | None = None, initial_scale=1.0):
        super().__init__()

        # Set scale
        self.scale = initial_scale

        # Load image
        self.original_image = pygame.image.load(picture_path).convert_alpha()
        self.image = self.original_image

        # Scale the image based on the current zoom level
        new_width = int(self.original_image.get_width() * self.scale)
        new_height = int(self.original_image.get_height() * self.scale)
        self.image = pygame.transform.scale(self.original_image, (new_width, new_height))

        if cell:
            self.rect = self.image.get_rect()
            self.rect.center = cell.rect.center
        elif cell_center:
            self.rect = self.image.get_rect(center=cell_center)
            self.rect.center = cell_center