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

        self.cost = 50

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

        self.healing = 8
        self.duration = 4
        self.sanity = 12

        self.cost = 50

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

        self.image = Sprite(MENU_SPRITESHEETS['ITEMS'], scale = 4).get_sprite(0, 40, 20, 20)
        self.desc = 'CHERISHED LETTER (BLADE ONLY)\nTHE LAST I HAVE LEFT OF HER...\nDAMAGE++ SANITY DAMAGE-\nDEATHBLOW-- PROTECTION-'

        self.equipable = True

        self.character = 'BLADE'

        self.cost = 250

    def equip_item(self, character):

        character.death -= 15
        character.protection -= 10
        character.sanity_damage_factor -= 20
        character.damage[0] *= 1.1
        character.damage[1] *= 1.1

    def remove_item(self, character):

        character.death += 15
        character.protection += 10
        character.sanity_damage_factor += 20
        character.damage[0] /= 1.1
        character.damage[1] /= 1.1

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

        self.cost = 250

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

        self.cost = 100

    def equip_item(self, character):

        character.damage[0] *= 1.05
        character.damage[1] *= 1.05
        character.precision += 5
        character.protection -= 5
        character.max_health *= 0.95

    def remove_item(self, character):

        character.damage[0] /= 1.05
        character.damage[1] /= 1.05
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

        character.damage[0] *= 1.1
        character.damage[1] *= 1.1
        character.precision += 10
        character.protection -= 10
        character.max_health *= 0.9

    def remove_item(self, character):

        character.damage[0] /= 1.1
        character.damage[1] /= 1.1
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

        character.damage[0] *= 1.2
        character.damage[1] *= 1.2
        character.precision += 15
        character.protection -= 15
        character.max_health *= 0.8

    def remove_item(self, character):

        character.damage[0] /= 1.2
        character.damage[1] /= 1.2
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

        character.protection += 15
        character.speed -= 1

    def remove_item(self, character):

        character.protection -= 15
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

        character.protection -= 15
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

        character.protection += 20
        character.precision -= 10


    def remove_item(self, character):

        character.protection -= 20
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

        character.precision += 10
        character.agility += 15
        character.sanity_damage_factor += 20

    def remove_item(self, character):

        character.precision -= 10
        character.agility -= 15
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

        character.crit += 10

    def remove_item(self, character):

        character.crit -= 10

class SerratedEdge(Item):

    def __init__(self, game):
        super().__init__(game)

        self.image = Sprite(MENU_SPRITESHEETS['ITEMS'], scale = 4).get_sprite(20, 80, 20, 20)
        self.desc = 'SERRATED EDGE (BREACH ONLY)\nBRUTALLY EFFICIENT TOOL OF MURDER\nDAMAGE++\nHEALTH-'

        self.equipable = True

        self.character = 'BREACH'

        self.cost = 250

    def equip_item(self, character):

        character.damage[0] *= 1.15
        character.damage[1] *= 1.15
        character.max_health *= 0.9

    def remove_item(self, character):

        character.damage[0] /= 1.15
        character.damage[1] /= 1.15
        character.max_health /= 0.9