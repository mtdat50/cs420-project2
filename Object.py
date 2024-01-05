import pygame, random

class Cell(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, cell_info):
        super().__init__()
        # Random floor asset
        picture_path = "Graphics\\catacombs_" + str(random.randrange(0, 11)) + ".png"

        self.image = pygame.image.load(picture_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)
        self.fog = Object("Graphics\\unseen.png", self)

    def remove_fog(self):
        self.fog = None

class Object(pygame.sprite.Sprite):
    def __init__(self, picture_path, cell: Cell | None = None, pos_x: int | None = None, pos_y: int | None = None):
        super().__init__()

        self.image = pygame.image.load(picture_path).convert_alpha()
        self.rect = self.image.get_rect()

        if cell:
            self.rect.center = cell.rect.center
        if pos_x != None and pos_y != None:
            self.rect.topleft = (pos_x, pos_y)