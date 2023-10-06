import pygame as p
from settings import *

class Sprite:

    def __init__(self, spritesheet, scale = 1):

        self.spritesheet = spritesheet.convert()
        self.scale = scale

    def get_sprite(self, x, y, width, height):

        sprite = p.Surface((width, height))
        sprite.blit(self.spritesheet, (0, 0), (x, y, width, height))
        sprite = p.transform.scale(sprite, (width * self.scale, height * self.scale))
        sprite.convert()
        sprite.set_colorkey(BLACK)
        return sprite
    
def colour_swap(image, old_colour, new_colour):

    new_image = p.Surface(image.get_size())
    new_image.fill(new_colour)
    image.set_colorkey(old_colour)
    new_image.blit(image, (0, 0))
    return new_image