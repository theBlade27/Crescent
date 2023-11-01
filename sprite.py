import pygame as p
from settings import *

class Sprite:

    # this class deals with getting images from a larger spritesheet
    # it also deals with easily scaling images

    def __init__(self, spritesheet, scale = 1):

        # takes in an image
        # the convert() function makes it easier for python to deal with it

        self.spritesheet = spritesheet.convert()
        self.scale = scale

    def get_sprite(self, x, y, width, height):

        # creates a surface the same size as the width and height passed in

        sprite = p.Surface((width, height))

        # a part of the image self.spritesheet is taken
        # this part starts at 'x' and is 'width' pixels long in the x axis
        # this part starts at 'y' and is 'height' pixels long in the y axis

        # this part of the image is then drawn on to the surface created earlier starting at (0, 0)
        # this results in a new image of the correct width and height that consists only of the part that is specified by the parameters

        sprite.blit(self.spritesheet, (0, 0), (x, y, width, height))

        # the image is scaled to be the correct size
        sprite = p.transform.scale(sprite, (width * self.scale, height * self.scale))
        sprite.convert()

        # any black is removed (note that any images with transparent backgrounds are seen to have black backgrounds, so this is done to make sure images that are meant to be transparent are actually transparent and dont have a background)
        sprite.set_colorkey(BLACK)

        # returns the image
        return sprite
    
# this function does not belong to the sprite class but since it is to do with images i put it here
# it deals with changing the colour of an image

def colour_swap(image, old_colour, new_colour):

    # creates a surface the same size as the original image

    new_image = p.Surface(image.get_size())

    # fills the surface with the new colour
    new_image.fill(new_colour)

    # removes the old colour from the old surface
    image.set_colorkey(old_colour)

    # draw the old image on top of the new image
    # the gaps left by the removal of the old colour are filled by the new colour underneath
    new_image.blit(image, (0, 0))

    # return the colour swapped image
    return new_image