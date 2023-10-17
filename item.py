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

        self.character = 'ANY'

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
        self.desc = 'BANDAGE\nUSED TO STAUNCH THE FLOW OF BLOOD.'

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

                

class Food1(Item):

    def __init__(self, game):
        super().__init__(game)

        self.image = Sprite(MENU_SPRITESHEETS['ITEMS'], scale = 4).get_sprite(40, 0, 20, 20)
        self.desc = 'RATIONS\nBEATS STARVING.'

        self.healing = 5
        self.duration = 4

    def use(self, index):

        character = self.game.selected_character

        if type(character) == Hero:

            for effect in character.effects:
                if type(effect) == Starving:
                    character.effects.remove(effect)

                    character.damage[0] *= 1.1
                    character.damage[1] *= 1.1
                    character.protection += 10
                    character.speed += 1
                    character.precision += 5
                    character.agility += 5
                    character.crit += 5

                    character.current_health += self.healing
                    character.effects.append(Stuffed(self.game, character, self.duration))

                    for effect in character.effects:
                        if type(effect) == DeathsDoor:
                            effect.remove_effect()
                        
                    self.game.inventory[index] = None
                    self.game.selected_item = None
                    self.kill()

                    for menu in self.game.menus.values():
                        menu.update_images()

                elif type(effect) == Satiated:
                    character.effects.remove(effect)

                    character.current_health += self.healing
                    character.effects.append(Stuffed(self.game, character, self.duration))

                    for effect in character.effects:
                        if type(effect) == DeathsDoor:
                            effect.remove_effect()

                    self.game.inventory[index] = None
                    self.game.selected_item = None
                    self.kill()

                    for menu in self.game.menus.values():
                        menu.update_images()

                

class Food2(Food1):

    def __init__(self, game):
        super().__init__(game)

        self.image = Sprite(MENU_SPRITESHEETS['ITEMS'], scale = 4).get_sprite(60, 0, 20, 20)
        self.desc = 'MEAL\nEVIL CANNOT BE VANQUISHED ON AN EMPTY STOMACH.'

        self.healing = 10
        self.duration = 8

class Food3(Food1):

    def __init__(self, game):
        super().__init__(game)

        self.image = Sprite(MENU_SPRITESHEETS['ITEMS'], scale = 4).get_sprite(80, 0, 20, 20)
        self.desc = 'FEAST\nTHERE ARE FEW THINGS A GOOD FEAST CANNOT FIX!'

        self.healing = 20
        self.duration = 16

class CherishedLetter(Item):

    def __init__(self, game):
        super().__init__(game)

        self.image = Sprite(MENU_SPRITESHEETS['ITEMS'], scale = 4).get_sprite(0, 40, 20, 20)
        self.desc = 'CHERISHED LETTER (BLADE ONLY)\nTHE LAST I HAVE LEFT OF HER...\nDAMAGE++ SANITY DAMAGE-\nDEATHBLOW-- PROTECTION-'

        self.equipable = True

        self.character = 'BLADE'

    def equip_item(self, character):

        character.death -= 30
        character.protection -= 10
        character.sanity_damage_factor -= 20
        character.damage[0] *= 1.2
        character.damage[1] *= 1.2

    def remove_item(self, character):

        character.death += 30
        character.protection += 10
        character.sanity_damage_factor += 20
        character.damage[0] /= 1.2
        character.damage[1] /= 1.2

class HolyBook(Item):

    def __init__(self, game):
        super().__init__(game)

        self.image = Sprite(MENU_SPRITESHEETS['ITEMS'], scale = 4).get_sprite(20, 40, 20, 20)
        self.desc = 'HOLY BOOK (BLADE ONLY)\nFAITH IS ALL I NEED.\nSANITY RECOVERY SKILLS+ CRIT+'

        self.equipable = True

        self.character = 'BLADE'

    def equip_item(self, character):

        character.sanity_recovery_skills[0] *= 1.2
        character.sanity_recovery_skills[1] *= 1.2

        character.sanity_recovery_factor += 20
        character.crit += 10

    def remove_item(self, character):

        character.sanity_recovery_skills[0] /= 1.2
        character.sanity_recovery_skills[1] /= 1.2

        character.sanity_recovery_factor -= 20
        character.crit -= 10

class LuckyRing(Item):

    def __init__(self, game):
        super().__init__(game)

        self.image = Sprite(MENU_SPRITESHEETS['ITEMS'], scale = 4).get_sprite(20, 20, 20, 20)
        self.desc = 'LUCKY RING\nIT\'S BEAUTY IS INSPIRING.\nPRECISION+ CRIT+\nHEALTH-'

        self.equipable = True

    def equip_item(self, character):

        character.precision += 10
        character.crit += 10
        character.max_health *= 0.9

    def remove_item(self, character):

        character.precision -= 10
        character.crit -= 10
        character.max_health /= 0.9

class GlisteningJambiya(Item):

    def __init__(self, game):
        super().__init__(game)

        self.image = Sprite(MENU_SPRITESHEETS['ITEMS'], scale = 4).get_sprite(0, 20, 20, 20)
        self.desc = 'GLISTENING JAMBIYA\nAN INTRICATE DAGGER.\nDAMAGE+ SPEED+\nPRECISION-'

        self.equipable = True

    def equip_item(self, character):

        character.damage[0] *= 1.1
        character.damage[1] *= 1.1
        character.speed += 2
        character.precision -= 10

    def remove_item(self, character):

        character.damage[0] /= 1.1
        character.damage[1] /= 1.1
        character.speed -= 2
        character.precision += 10

class CrescentCoin(Item):

    def __init__(self, game):
        super().__init__(game)

        self.image = Sprite(MENU_SPRITESHEETS['ITEMS'], scale = 4).get_sprite(60, 20, 20, 20)
        self.desc = 'CRESCENT COIN\nJUST A COIN...\nDAMAGE+ PRECISION+\nPROTECTION- HEALTH-'

        self.equipable = True

    def equip_item(self, character):

        character.damage[0] *= 1.15
        character.damage[1] *= 1.15
        character.precision += 10
        character.protection -= 10
        character.max_health *= 0.85

    def remove_item(self, character):

        character.damage[0] /= 1.15
        character.damage[1] /= 1.15
        character.precision -= 10
        character.protection += 10
        character.max_health /= 0.85

class CursedCoin(Item):

    def __init__(self, game):
        super().__init__(game)

        self.image = Sprite(MENU_SPRITESHEETS['ITEMS'], scale = 4).get_sprite(40, 20, 20, 20)
        self.desc = 'CURSED COIN\nSOMETHING\'S NOT RIGHT...\nDAMAGE++ PRECISION++\nPROTECTION-- HEALTH--'

        self.equipable = True

    def equip_item(self, character):

        character.damage[0] *= 1.3
        character.damage[1] *= 1.3
        character.precision += 20
        character.protection -= 20
        character.max_health *= 0.7

    def remove_item(self, character):

        character.damage[0] /= 1.3
        character.damage[1] /= 1.3
        character.precision -= 20
        character.protection += 20
        character.max_health /= 0.7

class ForsakenCoin(Item):

    def __init__(self, game):
        super().__init__(game)

        self.image = Sprite(MENU_SPRITESHEETS['ITEMS'], scale = 4).get_sprite(80, 20, 20, 20)
        self.desc = 'FORSAKEN COIN\nIT HOLDS OTHERWORLDY POWER.\nDAMAGE+++ PRECISION+++\nPROTECTION--- HEALTH---'

        self.equipable = True

    def equip_item(self, character):

        character.damage[0] *= 1.5
        character.damage[1] *= 1.5
        character.precision += 30
        character.protection -= 30
        character.max_health *= 0.5

    def remove_item(self, character):

        character.damage[0] /= 1.3
        character.damage[1] /= 1.3
        character.precision -= 30
        character.protection += 30
        character.max_health /= 0.5

class MagicLamp(Item):

    def __init__(self, game):
        super().__init__(game)

        self.image = Sprite(MENU_SPRITESHEETS['ITEMS'], scale = 4).get_sprite(0, 60, 20, 20)
        self.desc = 'MAGIC LAMP (ARCANE ONLY)\nPOWER COMES AT A PRICE.\nDAMAGE+\nSANITY DAMAGE+'

        self.equipable = True

        self.character = 'ARCANE'

    def equip_item(self, character):

        character.damage[0] *= 1.15
        character.damage[1] *= 1.15
        character.sanity_damage_factor += 15

    def remove_item(self, character):

        character.damage[0] /= 1.15
        character.damage[1] /= 1.15
        character.sanity_damage_factor -= 15

class SapphireEarrings(Item):

    def __init__(self, game):
        super().__init__(game)

        self.image = Sprite(MENU_SPRITESHEETS['ITEMS'], scale = 4).get_sprite(20, 60, 20, 20)
        self.desc = 'SAPPHIRE EARRINGS (ARCANE ONLY)\nSO BEAUTIFUL...\nHEALING+\nHEALTH-'

        self.equipable = True

        self.character = 'ARCANE'

    def equip_item(self, character):

        character.healing[0] *= 1.20
        character.healing[1] *= 1.20
        character.max_health *= 0.85

    def remove_item(self, character):

        character.healing[0] /= 1.20
        character.healing[1] /= 1.20
        character.max_health /= 0.85