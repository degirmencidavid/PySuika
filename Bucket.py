# Bucket

import pygame as pg

class Bucket(pg.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.width = width
        self.height = height
        self.color = color
        self.image = pg.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft=(x, y))

        # Make an open top for the bucket
        pg.draw.line(self.image, (0, 0, 0), (0, 0), (self.width, 0), 2)

    def update(self):
        pass  # Add any bucket-specific update logic here
