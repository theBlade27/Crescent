import pygame as p
from sprite import *
from settings import *

class Item(p.sprite.Sprite):

    def __init__(self, game):

        self.groups = game.items_group
        p.sprite.Sprite.__init__(self, self.groups)

        self.game = game

class Bandage(Item):

    def __init__(self, game):
        super().__init__(game)

        self.image = Sprite(MENU_SPRITESHEETS['ITEMS'], scale = 4).get_sprite(0, 0, 20, 20)

class Torch(Item):

    def __init__(self, game):
        super().__init__(game)

        self.image = Sprite(MENU_SPRITESHEETS['ITEMS'], scale = 4).get_sprite(20, 0, 20, 20)