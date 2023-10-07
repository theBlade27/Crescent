import pygame as p
from sprite import *
from settings import *

class Effect(p.sprite.Sprite):

    def __init__(self, game, character, duration = 3):

        self.groups = game.effects_group
        p.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.character = character
        self.duration = duration

        if self.character == None:

            self.kill()

        else:

            if duration > -1:
                self.timed = True
            else:
                self.timed = False

            self.apply_effect()

    def apply_effect(self):

        pass

    def tick(self):

        if self.timed:

            self.duration -= 1
            if self.duration == 0:
                self.remove_effect()

            for menu in self.game.menus.values():
                menu.update_images()

    def remove_effect(self):

        if self in self.character.effects:

            self.character.effects.remove(self)
            for menu in self.game.menus.values():
                menu.update_images()

class Strength(Effect):

    def __init__(self, game, character, duration = 3, damage_multiplier = 1.2):
        self.damage_multiplier = damage_multiplier
        super().__init__(game, character, duration)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(0, 120, 20, 20)

    def apply_effect(self):

        self.character.damage[0] = self.character.damage[0] * self.damage_multiplier
        self.character.damage[1] = self.character.damage[1] * self.damage_multiplier

        for menu in self.game.menus.values():
            menu.update_images()

    def remove_effect(self):

        self.character.damage[0] = self.character.damage[0] / self.damage_multiplier
        self.character.damage[1] = self.character.damage[1] / self.damage_multiplier

class Strength2(Strength):

    def __init__(self, game, character, duration = 3):
        super().__init__(game, character, duration, 1.5)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(0, 140, 20, 20)

class Strength3(Strength):

    def __init__(self, game, character, duration = 3):
        super().__init__(game, character, duration, 2)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(0, 160, 20, 20)


class Weakness(Effect):

    def __init__(self, game, character, duration = 3, damage_multiplier = 1.2):

        self.damage_multiplier = damage_multiplier
        super().__init__(game, character, duration)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(20, 120, 20, 20)

    def apply_effect(self):

        self.character.damage[0] = self.character.damage[0] / self.damage_multiplier
        self.character.damage[1] = self.character.damage[1] / self.damage_multiplier

        for menu in self.game.menus.values():
            menu.update_images()

    def remove_effect(self):

        self.character.damage[0] = self.character.damage[0] * self.damage_multiplier
        self.character.damage[1] = self.character.damage[1] * self.damage_multiplier

class Weakness2(Weakness):

    def __init__(self, game, character, duration = 3):
        super().__init__(game, character, duration, 1.5)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(20, 140, 20, 20)

class Weakness3(Weakness):

    def __init__(self, game, character, duration = 3):
        super().__init__(game, character, duration, 2)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(20, 160, 20, 20)


        

class DeathsDoor(Effect):

    def __init__(self, game, character):
        super().__init__(game, character, -1)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(20, 280, 20, 20)

    def apply_effect(self):

        for effect in self.character.effects:
            if isinstance(effect, DeathsDoor):
                effect.remove_effect()
    
        self.character.sanity_recovery_factor -= 50
        self.character.sanity_damage_factor += 50

    def tick(self):

        self.character.calculate_sanity_decrease(10)

        for menu in self.game.menus.values():
            menu.update_images()

    def remove_effect(self):

        self.character.sanity_recovery_factor += 50
        self.character.sanity_damage_factor -= 50

        if self in self.character.effects:

            self.character.effects.remove(self)
            for menu in self.game.menus.values():
                menu.update_images()

class Burning(Effect):

    def __init__(self, game, character, duration = 3):
        super().__init__(game, character, duration)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(20, 360, 20, 20)

        self.damage = 2

    def tick(self):

        if self.timed:

            self.duration -= 1
            if self.character in self.game.battle.all_characters:
                self.character.calculate_damage_dealt(self.damage, debuff = True)
            if self.duration == 0:
                self.remove_effect()
            for menu in self.game.menus.values():
                menu.update_images()

class Burning2(Burning):

    def __init__(self, game, character, duration = 3):
        super().__init__(game, character, duration)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(40, 360, 20, 20)

        self.damage = 5

class Burning3(Burning):

    def __init__(self, game, character, duration = 3):
        super().__init__(game, character, duration)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(60, 360, 20, 20)

        self.damage = 10

class Bleeding(Burning):

    def __init__(self, game, character, duration = 3):
        super().__init__(game, character, duration)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(20, 300, 20, 20)

        self.damage = 2

class Bleeding2(Burning):

    def __init__(self, game, character, duration = 3):
        super().__init__(game, character, duration)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(40, 300, 20, 20)

        self.damage = 5

class Bleeding3(Burning):

    def __init__(self, game, character, duration = 3):
        super().__init__(game, character, duration)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(60, 300, 20, 20)

        self.damage = 10

class Stun(Effect):

    def __init__(self, game, character):
        super().__init__(game, character, -1)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(20, 380, 20, 20)

    def apply_effect(self):
        
        self.character.stunned = True

    def remove_effect(self):

        self.character.stunned = False

        if self in self.character.effects:

            self.character.effects.remove(self)
            for menu in self.game.menus.values():
                menu.update_images()

class Mark(Effect):

    def __init__(self, game, character, duration = 3):
        super().__init__(game, character, duration)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(20, 260, 20, 20)

    def apply_effect(self):
        
        self.character.marked = True

    def remove_effect(self):

        self.character.marked = False

        if self in self.character.effects:

            self.character.effects.remove(self)
            for menu in self.game.menus.values():
                menu.update_images()

class StunResist(Effect):

    def __init__(self, game, character, duration = 1):
        super().__init__(game, character, duration)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(80, 380, 20, 20)

    def apply_effect(self):

        self.character.stun += 50

    def remove_effect(self):

        self.character.stun -= 50

        if self in self.character.effects:

            self.character.effects.remove(self)
            for menu in self.game.menus.values():
                menu.update_images()


class Dodge(Effect):

    def __init__(self, game, character, duration = 3, dodge_modifier = 5):

        self.dodge_modifier = dodge_modifier

        super().__init__(game, character, duration)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(0, 180, 20, 20)

    def apply_effect(self):

        self.character.agility += self.dodge_modifier

        for menu in self.game.menus.values():
            menu.update_images()

    def remove_effect(self):

        self.character.agility -= self.dodge_modifier

class Dodge2(Dodge):

    def __init__(self, game, character, duration = 3):
        super().__init__(game, character, duration, 15)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(0, 200, 20, 20)

class Dodge3(Dodge):

    def __init__(self, game, character, duration = 3):
        super().__init__(game, character, duration, 30)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(0, 220, 20, 20)

class AntiDodge(Dodge):

    def __init__(self, game, character, duration = 3):
        super().__init__(game, character, duration, -5)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(40, 180, 20, 20)

class AntiDodge2(Dodge):

    def __init__(self, game, character, duration = 3):
        super().__init__(game, character, duration, -15)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(40, 200, 20, 20)

class AntiDodge3(Dodge):

    def __init__(self, game, character, duration = 3):
        super().__init__(game, character, duration, -30)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(40, 220, 20, 20)


class Blindness(Effect):

    def __init__(self, game, character, duration = 3, precision_modifier = 20):

        self.precision_modifier = precision_modifier
        super().__init__(game, character, duration)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(20, 180, 20, 20)

    def apply_effect(self):

        self.character.precision -= self.precision_modifier

        for menu in self.game.menus.values():
            menu.update_images()

    def remove_effect(self):

        self.character.precision += self.precision_modifier

class Blindness2(Blindness):

    def __init__(self, game, character, duration = 3):
        super().__init__(game, character, duration, 50)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(20, 200, 20, 20)

class Blindness3(Blindness):

    def __init__(self, game, character, duration = 3):
        super().__init__(game, character, duration, 100)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(20, 220, 20, 20)

