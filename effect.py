import pygame as p
from sprite import *
from settings import *

class Effect(p.sprite.Sprite):

    # all effects follow the same blueprint, so i am only going to comment on a few examples because the idea stays the same with the most of them

    def __init__(self, game, character, duration = 3):

        self.groups = game.effects_group, game.all
        p.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.character = character # the character the effect is applied to
        self.duration = duration # the amount of rounds the effect needs to last

        if self.character == None:

            self.kill()

        else:

            # if the duration is more than 0, it is an effect that only lasts a certain amount of rounds

            if duration > -1:
                self.timed = True

            # otherwise it is an effect that persists until some other condition has been met
            else:
                self.timed = False

            self.apply_effect()

    def apply_effect(self):

        # this is where the characters stats are changed

        pass

    def tick(self):

        # if this effect is a timed one

        if self.timed:

            # reduce the remaining duration by 1
            self.duration -= 1

            # once the remaining duration is 0, remove the effect
            if self.duration == 0:
                self.remove_effect()

            for menu in self.game.menus.values():
                menu.update_images()

    def remove_effect(self):

        # this is where the characters stats are reverted

        if self in self.character.effects:

            # remove this effect from the list of the characters effect

            self.character.effects.remove(self)
            for menu in self.game.menus.values():
                menu.update_images()

class Strength(Effect):

    def __init__(self, game, character, duration = 3, damage_multiplier = 1.2):
        self.damage_multiplier = damage_multiplier
        super().__init__(game, character, duration)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(0, 120, 20, 20)

    def apply_effect(self):

        # the characters damage is increased

        self.character.damage[0] = self.character.damage[0] * self.damage_multiplier
        self.character.damage[1] = self.character.damage[1] * self.damage_multiplier

        for menu in self.game.menus.values():
            menu.update_images()

    def remove_effect(self):

        # the characters damage is decreased to the same amount as it was before the effect was applied

        self.character.damage[0] = self.character.damage[0] / self.damage_multiplier
        self.character.damage[1] = self.character.damage[1] / self.damage_multiplier

        if self in self.character.effects:

            self.character.effects.remove(self)
            for menu in self.game.menus.values():
                menu.update_images()

class Strength2(Strength):

    def __init__(self, game, character, duration = 3):
        super().__init__(game, character, duration, 1.5)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(0, 140, 20, 20)

class Strength3(Strength):

    def __init__(self, game, character, duration = 3):
        super().__init__(game, character, duration, 2)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(0, 160, 20, 20)


class Crit(Effect):

    def __init__(self, game, character, duration = 3, crit_modifier = 10):
        self.crit_modifier = crit_modifier
        super().__init__(game, character, duration)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(0, 240, 20, 20)

    def apply_effect(self):

        self.character.crit += self.crit_modifier
        for menu in self.game.menus.values():
            menu.update_images()

    def remove_effect(self):

        self.character.crit -= self.crit_modifier

        if self in self.character.effects:

            self.character.effects.remove(self)
            for menu in self.game.menus.values():
                menu.update_images()

class Crit2(Crit):

    def __init__(self, game, character, duration = 3):
        super().__init__(game, character, duration, 25)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(0, 260, 20, 20)

class Crit3(Crit):

    def __init__(self, game, character, duration = 3):
        super().__init__(game, character, duration, 40)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(0, 280, 20, 20)


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

        if self in self.character.effects:

            self.character.effects.remove(self)
            for menu in self.game.menus.values():
                menu.update_images()

class Weakness2(Weakness):

    def __init__(self, game, character, duration = 3):
        super().__init__(game, character, duration, 1.5)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(20, 140, 20, 20)

class Weakness3(Weakness):

    def __init__(self, game, character, duration = 3):
        super().__init__(game, character, duration, 2)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(20, 160, 20, 20)


class Insanity(Effect):

    def __init__(self, game, character):
        super().__init__(game, character, -1)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(40, 240, 20, 20)

    def apply_effect(self):

        for effect in self.character.effects:
            if isinstance(effect, Insanity):
                effect.remove_effect()
    
        self.character.damage[0] /= 1.1
        self.character.damage[1] /= 1.1
        self.character.protection -= 10
        self.character.speed -= 1
        self.character.precision -= 5
        self.character.agility -= 5
        self.character.crit -= 5

        self.character.death -= 33

        for menu in self.game.menus.values():
            menu.update_images()

    def remove_effect(self):

        self.character.damage[0] *= 1.1
        self.character.damage[1] *= 1.1
        self.character.protection += 10
        self.character.speed += 1
        self.character.precision += 5
        self.character.agility += 5
        self.character.crit += 5

        self.character.death += 33

        if self in self.character.effects:
            self.character.effects.remove(self)

            for menu in self.game.menus.values():
                menu.update_images()

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

        self.character.damage[0] /= 1.2
        self.character.damage[1] /= 1.2
        self.character.protection -= 20
        self.character.speed -= 2
        self.character.precision -= 10
        self.character.agility -= 10
        self.character.crit -= 10

    def tick(self):

        self.character.calculate_sanity_decrease(10)

        for menu in self.game.menus.values():
            menu.update_images()

    def remove_effect(self):

        self.character.sanity_recovery_factor += 50
        self.character.sanity_damage_factor -= 50

        self.character.damage[0] *= 1.2
        self.character.damage[1] *= 1.2
        self.character.protection += 20
        self.character.speed += 2
        self.character.precision += 10
        self.character.agility += 10
        self.character.crit += 10

        if self in self.character.effects:

            self.character.effects.remove(self)
            for menu in list(self.game.menus.values()):
                menu.update_images()

class Burning(Effect):

    def __init__(self, game, character, duration = 3):
        super().__init__(game, character, duration)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(20, 360, 20, 20)

        self.damage = 4

    def tick(self):

        if self.timed:

            self.duration -= 1
            if self.character in self.game.characters:
                self.character.calculate_damage_dealt(self.damage, debuff = True)
            if self.duration == 0:
                self.remove_effect()
            for menu in self.game.menus.values():
                menu.update_images()

class Burning2(Burning):

    def __init__(self, game, character, duration = 3):
        super().__init__(game, character, duration)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(40, 360, 20, 20)

        self.damage = 8

class Burning3(Burning):

    def __init__(self, game, character, duration = 3):
        super().__init__(game, character, duration)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(60, 360, 20, 20)

        self.damage = 16

class Bleeding(Burning):

    def __init__(self, game, character, duration = 3):
        super().__init__(game, character, duration)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(20, 300, 20, 20)

        self.damage = 4

class Bleeding2(Burning):

    def __init__(self, game, character, duration = 3):
        super().__init__(game, character, duration)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(40, 300, 20, 20)

        self.damage = 8

class Bleeding3(Burning):

    def __init__(self, game, character, duration = 3):
        super().__init__(game, character, duration)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(60, 300, 20, 20)

        self.damage = 16

class Starving(Effect):

    def __init__(self, game, character, duration = -1):
        super().__init__(game, character, duration)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(60, 280, 20, 20)

    def apply_effect(self):
        
        self.character.damage[0] /= 1.1
        self.character.damage[1] /= 1.1
        self.character.protection -= 10
        self.character.speed -= 1
        self.character.precision -= 5
        self.character.agility -= 5
        self.character.crit -= 5

        for menu in self.game.menus.values():
            menu.update_images()

    def tick(self):

        if self.character in self.game.hero_party:
            self.character.calculate_damage_dealt(1, debuff = True)

        for menu in self.game.menus.values():
            menu.update_images()


    def remove_effect(self):
        
        self.character.damage[0] *= 1.1
        self.character.damage[1] *= 1.1
        self.character.protection += 10
        self.character.speed += 1
        self.character.precision += 5
        self.character.agility += 5
        self.character.crit += 5

        if self in self.character.effects:
            self.character.effects.remove(self)

            for menu in self.game.menus.values():
                menu.update_images()

class Satiated(Effect):

    def __init__(self, game, character, duration = 24):
        super().__init__(game, character, duration)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(80, 280, 20, 20)

    def apply_effect(self):
        
        pass

    def remove_effect(self):

        if self in self.character.effects:
            self.character.effects.remove(self)

            for menu in self.game.menus.values():
                menu.update_images()

        self.character.effects.append(Starving(self.game, self.character))

class Stuffed(Effect):

    def __init__(self, game, character, duration = 4):
        super().__init__(game, character, duration)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(40, 280, 20, 20)

    def apply_effect(self):
        
        self.character.damage[0] *= 1.1
        self.character.damage[1] *= 1.1
        self.character.protection += 10
        self.character.speed += 1
        self.character.precision += 5
        self.character.agility += 5
        self.character.crit += 5

        for menu in self.game.menus.values():
            menu.update_images()

    def remove_effect(self):
        
        self.character.damage[0] /= 1.1
        self.character.damage[1] /= 1.1
        self.character.protection -= 10
        self.character.speed -= 1
        self.character.precision -= 5
        self.character.agility -= 5
        self.character.crit -= 5

        if self in self.character.effects:
            self.character.effects.remove(self)

            for menu in self.game.menus.values():
                menu.update_images()

        self.character.effects.append(Satiated(self.game, self.character))

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


class Dodge(Effect):

    def __init__(self, game, character, duration = 3, dodge_modifier = 10):

        self.dodge_modifier = dodge_modifier

        super().__init__(game, character, duration)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(0, 180, 20, 20)

    def apply_effect(self):

        self.character.agility += self.dodge_modifier

        for menu in self.game.menus.values():
            menu.update_images()

    def remove_effect(self):

        self.character.agility -= self.dodge_modifier

        if self in self.character.effects:

            self.character.effects.remove(self)
            for menu in self.game.menus.values():
                menu.update_images()

class Dodge2(Dodge):

    def __init__(self, game, character, duration = 3):
        super().__init__(game, character, duration, 25)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(0, 200, 20, 20)

class Dodge3(Dodge):

    def __init__(self, game, character, duration = 3):
        super().__init__(game, character, duration, 50)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(0, 220, 20, 20)

class AntiDodge(Dodge):

    def __init__(self, game, character, duration = 3):
        super().__init__(game, character, duration, -10)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(40, 180, 20, 20)

class AntiDodge2(Dodge):

    def __init__(self, game, character, duration = 3):
        super().__init__(game, character, duration, -25)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(40, 200, 20, 20)

class AntiDodge3(Dodge):

    def __init__(self, game, character, duration = 3):
        super().__init__(game, character, duration, -50)

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

        if self in self.character.effects:

            self.character.effects.remove(self)
            for menu in self.game.menus.values():
                menu.update_images()

class Blindness2(Blindness):

    def __init__(self, game, character, duration = 3):
        super().__init__(game, character, duration, 50)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(20, 200, 20, 20)

class Blindness3(Blindness):

    def __init__(self, game, character, duration = 3):
        super().__init__(game, character, duration, 100)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(20, 220, 20, 20)

class Precision(Blindness):
    
    def __init__(self, game, character, duration = 3):
        super().__init__(game, character, duration, -20)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(60, 180, 20, 20)

class Precision2(Blindness):
    
    def __init__(self, game, character, duration = 3):
        super().__init__(game, character, duration, -50)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(60, 200, 20, 20)

class Precision3(Blindness):
    
    def __init__(self, game, character, duration = 3):
        super().__init__(game, character, duration, -100)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(60, 220, 20, 20)


class Protection(Effect):

    def __init__(self, game, character, duration = 3, protection_modifier = 20):

        self.protection = protection_modifier
        super().__init__(game, character, duration)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(0, 60, 20, 20)

    def apply_effect(self):

        self.character.protection += self.protection

        for menu in self.game.menus.values():
            menu.update_images()

    def remove_effect(self):

        self.character.protection -= self.protection

        if self in self.character.effects:

            self.character.effects.remove(self)
            for menu in self.game.menus.values():
                menu.update_images()

class Protection2(Protection):
    
    def __init__(self, game, character, duration = 3):
        super().__init__(game, character, duration, 60)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(0, 80, 20, 20)

class Protection3(Protection):
    
    def __init__(self, game, character, duration = 3):
        super().__init__(game, character, duration, 100)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(0, 100, 20, 20)

class BrokenArmour(Protection):
    
    def __init__(self, game, character, duration = 3):
        super().__init__(game, character, duration, -20)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(20, 60, 20, 20)

class BrokenArmour2(Protection):
    
    def __init__(self, game, character, duration = 3):
        super().__init__(game, character, duration, -60)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(20, 80, 20, 20)

class BrokenArmour3(Protection):
    
    def __init__(self, game, character, duration = 3):
        super().__init__(game, character, duration, -100)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(20, 100, 20, 20)

class Speed(Effect):

    def __init__(self, game, character, duration = 3, speed_modifier = 2):

        self.speed = speed_modifier
        super().__init__(game, character, duration)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(0, 0, 20, 20)

    def apply_effect(self):

        self.character.speed += self.speed

        for menu in self.game.menus.values():
            menu.update_images()

    def remove_effect(self):

        self.character.speed -= self.speed

        if self in self.character.effects:

            self.character.effects.remove(self)
            for menu in self.game.menus.values():
                menu.update_images()

class Speed2(Speed):
    
    def __init__(self, game, character, duration = 3):
        super().__init__(game, character, duration, 4)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(0, 20, 20, 20)

class Speed3(Speed):
    
    def __init__(self, game, character, duration = 3):
        super().__init__(game, character, duration, 6)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(0, 40, 20, 20)

class Slowness(Speed):
    
    def __init__(self, game, character, duration = 3):
        super().__init__(game, character, duration, -2)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(20, 0, 20, 20)

class Slowness2(Speed):
    
    def __init__(self, game, character, duration = 3):
        super().__init__(game, character, duration, -4)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(20, 20, 20, 20)

class Slowness3(Speed):
    
    def __init__(self, game, character, duration = 3):
        super().__init__(game, character, duration, -6)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(20, 40, 20, 20)