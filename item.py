import pygame as p
from sprite import *
from settings import *
from hero import *

class Item(p.sprite.Sprite):

    def __init__(self, game):

        # all items follow the same blueprint, so i am only going to comment on a few examples because the idea stays the same with the most of them

        self.groups = game.items_group, game.all
        p.sprite.Sprite.__init__(self, self.groups)

        self.game = game

        # some items are equipable, and change a heros stats
        # others are not equipable, such as bandages, and have an immediate effect
        self.equipable = False

        # by default, any character can equip any item as long as 'equipable' is true
        # however, if 'character' is changed from 'ANY', to the name of a character, such as 'BLADE', only that character can equip it
        self.character = 'ANY'

        # the amount of money a player receives if they choose to remove the item from their inventory
        self.cost = 0

        # the description of the item that shows up at the top of the screen
        self.desc = ''

    def use(self, index):

        # the index is passed in so the inventory slot the item is in can be emptied when used

        pass

    def equip_item(self, character):

        # the character is passed in so that their stats can be changed

        pass

    def remove_item(self, character):

        # the character is passed in so that their stats can be changed

        pass


class Bandage(Item):

    def __init__(self, game):
        super().__init__(game)

        # this is an example of a non equipable item

        self.image = Sprite(MENU_SPRITESHEETS['ITEMS'], scale = 4).get_sprite(0, 0, 20, 20)
        self.desc = 'BANDAGE\nUSED TO STAUNCH THE FLOW OF BLOOD.'

        self.cost = 50

    def use(self, index):

        # non equipables are always used on the games selected character
        # this is so that a hero can only use items on their turn

        character = self.game.selected_character

        # checks the character is a hero so the player doesnt accidentally use it whilst it is the enemys turn

        if type(character) == Hero:

            # checks if the character is bleeding

            for effect in character.effects:

                # if they are bleeding
                if type(effect) == Bleeding or type(effect) == Bleeding2 or type(effect) == Bleeding3:
                    # bleeding is removed
                    effect.remove_effect()

                    # the index the item was in is emptied, and this item is killed
                    self.game.inventory[index] = None
                    self.game.selected_item = None
                    self.kill()

class Torch(Item):

    def __init__(self, game):
        super().__init__(game)

        self.image = Sprite(MENU_SPRITESHEETS['ITEMS'], scale = 4).get_sprite(20, 0, 20, 20)
        self.desc = 'TORCH\nREMOVES BLINDNESS'

        self.cost = 50

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

        # another non equipable item, but a bit more complex

        # the amount of health the character is healed for
        self.healing = 8

        # the amount of time the character is full for
        self.duration = 4

        # the amount of sanity the player recovers
        self.sanity = 12

        self.cost = 50

    def use(self, index):

        character = self.game.selected_character

        if type(character) == Hero:

            for effect in character.effects:

                # if the hero is starving
                if type(effect) == Starving:
                    # removes starving
                    character.effects.remove(effect)

                    # increases the players stats to cancel out the decrease in their stats they had due to starving

                    character.damage[0] *= 1.1
                    character.damage[1] *= 1.1
                    character.protection += 10
                    character.speed += 1
                    character.precision += 5
                    character.agility += 5
                    character.crit += 5

                    # increases the players health and sanity, making sure they do not go over their max health and sanity

                    character.current_health = min(character.max_health, character.current_health + self.healing)
                    character.current_sanity = min(character.max_sanity, character.current_sanity + self.sanity)

                    # adds the stuffed effect, which gives some buffs and makes it so the hero cannot eat again until a few turns have passed
                    character.effects.append(Stuffed(self.game, character, self.duration))

                    # removes deathsdoor since the hero has healed
                    for effect in character.effects:
                        if type(effect) == DeathsDoor:
                            effect.remove_effect()

                    # removes the item from the inventory
                        
                    self.game.inventory[index] = None
                    self.game.selected_item = None
                    self.kill()

                    # updates menus to display any changes

                    for menu in self.game.menus.values():
                        menu.update_images()

                # same thing, but if the hero is already satiated
                elif type(effect) == Satiated:
                    character.effects.remove(effect)

                    character.current_health = min(character.max_health, character.current_health + self.healing)
                    character.current_sanity = min(character.max_sanity, character.current_sanity + self.sanity)
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

        self.healing = 16
        self.duration = 5
        self.sanity = 24

        self.cost = 100

class Food3(Food1):

    def __init__(self, game):
        super().__init__(game)

        self.image = Sprite(MENU_SPRITESHEETS['ITEMS'], scale = 4).get_sprite(80, 0, 20, 20)
        self.desc = 'FEAST\nTHERE ARE FEW THINGS A GOOD FEAST CANNOT FIX!'

        self.healing = 24
        self.duration = 6
        self.sanity = 36

        self.cost = 200

class CherishedLetter(Item):

    def __init__(self, game):
        super().__init__(game)

        # this is an example of an equipable item

        self.image = Sprite(MENU_SPRITESHEETS['ITEMS'], scale = 4).get_sprite(0, 40, 20, 20)
        self.desc = 'CHERISHED LETTER (BLADE ONLY)\nTHE LAST I HAVE LEFT OF HER...\nDAMAGE++ SANITY DAMAGE-\nDEATHBLOW-- PROTECTION-'

        self.equipable = True

        # only equipable by BLADE

        self.character = 'BLADE'

        self.cost = 250

    def equip_item(self, character):

        # decreases and increases certain stats

        character.death -= 15
        character.protection -= 10
        character.sanity_damage_factor -= 20
        character.damage[0] *= 1.2
        character.damage[1] *= 1.2

    def remove_item(self, character):

        # does the opposite when the item is removed, returning the character to their original state

        character.death += 15
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

        self.cost = 250

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

        self.cost = 500

    def equip_item(self, character):

        character.precision += 15
        character.crit += 10
        character.max_health *= 0.9

    def remove_item(self, character):

        character.precision -= 15
        character.crit -= 10
        character.max_health /= 0.9

class GlisteningJambiya(Item):

    def __init__(self, game):
        super().__init__(game)

        self.image = Sprite(MENU_SPRITESHEETS['ITEMS'], scale = 4).get_sprite(0, 20, 20, 20)
        self.desc = 'GLISTENING JAMBIYA\nAN INTRICATE DAGGER.\nDAMAGE+ SPEED+\nPRECISION-'

        self.equipable = True

        self.cost = 250

    def equip_item(self, character):

        character.damage[0] *= 1.2
        character.damage[1] *= 1.2
        character.speed += 2
        character.precision -= 10

    def remove_item(self, character):

        character.damage[0] /= 1.2
        character.damage[1] /= 1.2
        character.speed -= 2
        character.precision += 10

class CrescentCoin(Item):

    def __init__(self, game):
        super().__init__(game)

        self.image = Sprite(MENU_SPRITESHEETS['ITEMS'], scale = 4).get_sprite(60, 20, 20, 20)
        self.desc = 'CRESCENT COIN\nJUST A COIN...\nDAMAGE+ PRECISION+\nPROTECTION- HEALTH-'

        self.equipable = True

        self.cost = 100

    def equip_item(self, character):

        character.damage[0] *= 1.15
        character.damage[1] *= 1.15
        character.precision += 5
        character.protection -= 5
        character.max_health *= 0.95

    def remove_item(self, character):

        character.damage[0] /= 1.15
        character.damage[1] /= 1.15
        character.precision -= 5
        character.protection += 5
        character.max_health /= 0.95

class CursedCoin(Item):

    def __init__(self, game):
        super().__init__(game)

        self.image = Sprite(MENU_SPRITESHEETS['ITEMS'], scale = 4).get_sprite(40, 20, 20, 20)
        self.desc = 'CURSED COIN\nSOMETHING\'S NOT RIGHT...\nDAMAGE++ PRECISION++\nPROTECTION-- HEALTH--'

        self.equipable = True

        self.cost = 250

    def equip_item(self, character):

        character.damage[0] *= 1.25
        character.damage[1] *= 1.25
        character.precision += 10
        character.protection -= 10
        character.max_health *= 0.9

    def remove_item(self, character):

        character.damage[0] /= 1.25
        character.damage[1] /= 1.25
        character.precision -= 10
        character.protection += 10
        character.max_health /= 0.9

class ForsakenCoin(Item):

    def __init__(self, game):
        super().__init__(game)

        self.image = Sprite(MENU_SPRITESHEETS['ITEMS'], scale = 4).get_sprite(80, 20, 20, 20)
        self.desc = 'FORSAKEN COIN\nIT HOLDS OTHERWORLDY POWER.\nDAMAGE+++ PRECISION+++\nPROTECTION--- HEALTH---'

        self.equipable = True

        self.cost = 500

    def equip_item(self, character):

        character.damage[0] *= 1.35
        character.damage[1] *= 1.35
        character.precision += 15
        character.protection -= 15
        character.max_health *= 0.8

    def remove_item(self, character):

        character.damage[0] /= 1.35
        character.damage[1] /= 1.35
        character.precision -= 15
        character.protection += 15
        character.max_health /= 0.8

class MagicLamp(Item):

    def __init__(self, game):
        super().__init__(game)

        self.image = Sprite(MENU_SPRITESHEETS['ITEMS'], scale = 4).get_sprite(0, 60, 20, 20)
        self.desc = 'MAGIC LAMP (ARCANE ONLY)\nPOWER COMES AT A PRICE.\nDAMAGE+\nSANITY DAMAGE+'

        self.equipable = True

        self.character = 'ARCANE'

        self.cost = 250

    def equip_item(self, character):

        character.damage[0] *= 1.2
        character.damage[1] *= 1.2
        character.sanity_damage_factor += 15

    def remove_item(self, character):

        character.damage[0] /= 1.2
        character.damage[1] /= 1.2
        character.sanity_damage_factor -= 15

class SapphireEarrings(Item):

    def __init__(self, game):
        super().__init__(game)

        self.image = Sprite(MENU_SPRITESHEETS['ITEMS'], scale = 4).get_sprite(20, 60, 20, 20)
        self.desc = 'SAPPHIRE EARRINGS (ARCANE ONLY)\nSO BEAUTIFUL...\nHEALING+\nHEALTH-'

        self.equipable = True

        self.character = 'ARCANE'

        self.cost = 250

    def equip_item(self, character):

        character.healing[0] *= 1.20
        character.healing[1] *= 1.20
        character.max_health *= 0.85

    def remove_item(self, character):

        character.healing[0] /= 1.20
        character.healing[1] /= 1.20
        character.max_health /= 0.85

class LifeCrystal(Item):

    def __init__(self, game):
        super().__init__(game)

        self.image = Sprite(MENU_SPRITESHEETS['ITEMS'], scale = 4).get_sprite(100, 20, 20, 20)
        self.desc = 'LIFE CRYSTAL\nIT HOLDS OTHERWORLDLY POWER\nHEALTH+'

        self.equipable = True

        self.cost = 250

    def equip_item(self, character):

        character.max_health *= 1.2

    def remove_item(self, character):

        character.max_health /= 1.2

class WarShield(Item):

    def __init__(self, game):
        super().__init__(game)

        self.image = Sprite(MENU_SPRITESHEETS['ITEMS'], scale = 4).get_sprite(120, 20, 20, 20)
        self.desc = 'WAR SHIELD\nA SIMPLE DEFENSIVE TOOL\nPROTECTION+\nSPEED-'

        self.equipable = True

        self.cost = 250

    def equip_item(self, character):

        character.protection += 10
        character.speed -= 1

    def remove_item(self, character):

        character.protection -= 10
        character.speed += 1

class SturdyRing(Item):

    def __init__(self, game):
        super().__init__(game)

        self.image = Sprite(MENU_SPRITESHEETS['ITEMS'], scale = 4).get_sprite(140, 20, 20, 20)
        self.desc = 'STURDY RING\nANCIENT, BUT INTACT\nPROTECTION+ HEALTH+\nDAMAGE-'

        self.equipable = True

        self.cost = 250

    def equip_item(self, character):

        character.protection += 10
        character.max_health *= 1.1
        character.damage[0] *= 0.95
        character.damage[1] *= 0.95


    def remove_item(self, character):

        character.protection -= 10
        character.max_health /= 1.1
        character.damage[0] /= 0.95
        character.damage[1] /= 0.95

class BucketHelmet(Item):

    def __init__(self, game):
        super().__init__(game)

        self.image = Sprite(MENU_SPRITESHEETS['ITEMS'], scale = 4).get_sprite(160, 20, 20, 20)
        self.desc = 'BUCKET HELMET\nTHIS. IS A BUCKET.\nPROTECTION++\nPRECISION-'

        self.equipable = True

        self.cost = 100

    def equip_item(self, character):

        character.protection += 10
        character.precision -= 10


    def remove_item(self, character):

        character.protection -= 10
        character.precision += 10

class DeathPact(Item):

    def __init__(self, game):
        super().__init__(game)

        self.image = Sprite(MENU_SPRITESHEETS['ITEMS'], scale = 4).get_sprite(180, 20, 20, 20)
        self.desc = 'DEATH PACT\nDID LIFE EVER HAVE MEANING ANYWAYS?\nCRIT+++++\nHEALTH-----'

        self.equipable = True

        self.cost = 500

    def equip_item(self, character):

        character.crit += 100
        character.max_health *= 0.1

    def remove_item(self, character):

        character.crit -= 100
        character.max_health /= 0.1

class SeersStone(Item):

    def __init__(self, game):
        super().__init__(game)

        self.image = Sprite(MENU_SPRITESHEETS['ITEMS'], scale = 4).get_sprite(200, 20, 20, 20)
        self.desc = 'SEERS STONE\nI SEE IT NOW. I SEE IT ALL\nPRECISION+ DODGE++\nSANITY DAMAGE+'

        self.equipable = True

        self.cost = 500

    def equip_item(self, character):

        character.precision += 15
        character.agility += 20
        character.sanity_damage_factor += 20

    def remove_item(self, character):

        character.precision -= 15
        character.agility -= 20
        character.sanity_damage_factor -= 20

class RecoveryPendant(Item):

    def __init__(self, game):
        super().__init__(game)

        self.image = Sprite(MENU_SPRITESHEETS['ITEMS'], scale = 4).get_sprite(220, 20, 20, 20)
        self.desc = 'RECOVERY PENDANT\nMERELY WEARING IT BRINGS PEACE\nHEALTH+ SANITY RECOVERY SKILLS+ HEALING+\nSPEED- DAMAGE-'

        self.equipable = True

        self.cost = 500

    def equip_item(self, character):

        character.max_health *= 1.1
        character.healing[0] *= 1.1
        character.healing[1] *= 1.1
        character.sanity_recovery_skills[0] *= 1.1
        character.sanity_recovery_skills[1] *= 1.1
        character.speed -= 1
        character.damage[0] *= 0.9
        character.damage[1] *= 0.9

    def remove_item(self, character):

        character.max_health /= 1.1
        character.healing[0] /= 1.1
        character.healing[1] /= 1.1
        character.sanity_recovery_skills[0] /= 1.1
        character.sanity_recovery_skills[1] /= 1.1
        character.speed += 1
        character.damage[0] /= 0.9
        character.damage[1] /= 0.9

class SpentMatch(Item):

    def __init__(self, game):
        super().__init__(game)

        self.image = Sprite(MENU_SPRITESHEETS['ITEMS'], scale = 4).get_sprite(0, 80, 20, 20)
        self.desc = 'SPENT MATCH (BREACH ONLY)\nDWINDLING. LIKE HOPE.\nCRIT+'

        self.equipable = True

        self.character = 'BREACH'

        self.cost = 250

    def equip_item(self, character):

        character.crit += 15

    def remove_item(self, character):

        character.crit -= 15

class SerratedEdge(Item):

    def __init__(self, game):
        super().__init__(game)

        self.image = Sprite(MENU_SPRITESHEETS['ITEMS'], scale = 4).get_sprite(20, 80, 20, 20)
        self.desc = 'SERRATED EDGE (BREACH ONLY)\nBRUTALLY EFFICIENT TOOL OF MURDER\nDAMAGE++\nHEALTH-'

        self.equipable = True

        self.character = 'BREACH'

        self.cost = 250

    def equip_item(self, character):

        character.damage[0] *= 1.2
        character.damage[1] *= 1.2
        character.max_health *= 0.9

    def remove_item(self, character):

        character.damage[0] /= 1.2
        character.damage[1] /= 1.2
        character.max_health /= 0.9