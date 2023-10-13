import pygame as p
from sprite import *
from settings import *
from hero import *

class Item(p.sprite.Sprite):

    def __init__(self, game):

        self.groups = game.items_group, game.all
        p.sprite.Sprite.__init__(self, self.groups)

        self.game = game

        self.equipable = False

    def use(self, index):

        pass

    def equip_item(self, character):

        pass

    def remove_item(self, character):

        pass


class Bandage(Item):

    def __init__(self, game):
        super().__init__(game)

        self.image = Sprite(MENU_SPRITESHEETS['ITEMS'], scale = 4).get_sprite(0, 0, 20, 20)
        self.desc = 'BANDAGE\nUSED TO STAUNCH THE FLOW OF BLOOD'

    def use(self, index):

        character = self.game.selected_character

        if type(character) == Hero:

            for effect in character.effects:
                if type(effect) == Bleeding or type(effect) == Bleeding2 or type(effect) == Bleeding3:
                    effect.remove_effect()

            self.game.inventory[index] = None
            self.game.selected_item = None
            self.kill()

class Torch(Item):

    def __init__(self, game):
        super().__init__(game)

        self.image = Sprite(MENU_SPRITESHEETS['ITEMS'], scale = 4).get_sprite(20, 0, 20, 20)
        self.desc = 'TORCH\nREMOVES BLINDNESS'

    def use(self, index):

        character = self.game.selected_character

        if type(character) == Hero:

            for effect in character.effects:
                if type(effect) == Blindness or type(effect) == Blindness2 or type(effect) == Blindness3:
                    effect.remove_effect()

            self.game.inventory[index] = None
            self.game.selected_item = None
            self.kill()