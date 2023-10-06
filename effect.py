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

    def __init__(self, game, character, duration = 3):
        super().__init__(game, character, duration)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 2).get_sprite(0, 120, 20, 20)

    def apply_effect(self):

        self.character.damage[0] = self.character.damage[0] * 1.2
        self.character.damage[1] = self.character.damage[1] * 1.2

        for menu in self.game.menus.values():
            menu.update_images()

    def remove_effect(self):

        self.character.damage[0] = self.character.damage[0] / 1.2
        self.character.damage[1] = self.character.damage[1] / 1.2

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