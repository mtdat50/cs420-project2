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

class Arrow(pygame.sprite.Sprite):
    def __init__(self, player_rect, target_cell):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.original_image = pygame.image.load("Graphics\\orcish_arrow.png").convert_alpha()
        self.image = self.original_image
        self.image = pygame.transform.rotate(self.original_image, 45)
        self.rect = self.image.get_rect(center=player_rect.center)
        self.target_cell = target_cell
        self.reached_target = False

        self.hori = 0
        self.vert = 0

        print(target_cell.rect.x, player_rect.x)
        print(target_cell.rect.y, player_rect.y)
        if target_cell.rect.x < player_rect.x:
            self.hori = -1
            self.image = pygame.transform.rotate(self.original_image, 90)
        if target_cell.rect.x > player_rect.x:
            self.hori = 1
            self.image = pygame.transform.rotate(self.original_image, -90)
        if target_cell.rect.y < player_rect.y:
            self.vert = -1
        if target_cell.rect.y > player_rect.y:
            self.vert = 1
            self.image = pygame.transform.rotate(self.original_image, 180)
        print(self.hori, self.vert)

    def update(self):
        # Move the arrow horizontally, adjust the speed as needed
        self.rect.x += 1 * self.hori
        self.rect.y += 1 * self.vert

        # Check if the arrow has reached the target cell
        if self.rect.colliderect(self.target_cell.rect):
            self.reached_target = True