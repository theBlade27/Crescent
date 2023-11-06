import pygame as p
from sprite import *
from settings import *
from skill import*

# this file just contains all properties of the different skills enemys have, there is no complex code here

class GhostVanquish(EnemySkill):

    def __init__(self, game, character):
        super().__init__(game, character)

        self.name = 'REMINDER'

        self.range = [0, 3]

        self.sound = MEDIUM_SOUND

        self.combat_animation = self.character.spritesheet.get_sprite(0, 60, 120, 40)
        self.combat_animation = p.transform.scale(self.combat_animation, (self.combat_animation.get_width() * 2, self.combat_animation.get_height() * 2))

class ScimitarSlash(EnemySkill):

    def __init__(self, game, character):
        super().__init__(game, character)

        self.range = [0, 3]
        self.name = 'SCIMITAR SLASH'

        self.effects_on_hit = ['BLEEDING']

        self.sound = MEDIUM_SOUND

        self.mark_damage_multiplier = 1.2

        self.combat_animation = self.character.spritesheet.get_sprite(0, 60, 120, 40)
        self.combat_animation = p.transform.scale(self.combat_animation, (self.combat_animation.get_width() * 2, self.combat_animation.get_height() * 2))

class CrushingBlow(EnemySkill):

    def __init__(self, game, character):
        super().__init__(game, character)

        self.range = [0, 3]
        self.name = 'CRUSHING BLOW'

        self.effects_on_hit = ['STUNNING', 'BROKEN']

        self.sound = HEAVY_SOUND

        self.mark_damage_multiplier = 1.2

        self.combat_animation = self.character.spritesheet.get_sprite(0, 60, 120, 40)
        self.combat_animation = p.transform.scale(self.combat_animation, (self.combat_animation.get_width() * 2, self.combat_animation.get_height() * 2))

class FlintShot(EnemySkill):

    def __init__(self, game, character):
        super().__init__(game, character)

        self.range = [5, 9]
        self.name = 'FLINT SHOT'

        self.effects_on_hit = ['BLINDING']

        self.sound = LIGHT_SOUND

        self.mark_damage_multiplier = 1.2

        self.combat_animation = self.character.spritesheet.get_sprite(0, 60, 120, 40)
        self.combat_animation = p.transform.scale(self.combat_animation, (self.combat_animation.get_width() * 2, self.combat_animation.get_height() * 2))

class AridStab(EnemySkill):

    def __init__(self, game, character):
        super().__init__(game, character)

        self.range = [0, 3]
        self.name = 'ARID STAB'

        self.multiplier = 0.8

        self.effects_on_hit = ['BLEEDING']

        self.sound = LIGHT_SOUND

        self.combat_animation = self.character.spritesheet.get_sprite(0, 100, 120, 40)
        self.combat_animation = p.transform.scale(self.combat_animation, (self.combat_animation.get_width() * 2, self.combat_animation.get_height() * 2))

class IntimidatingRoar(EnemySkill):

    def __init__(self, game, character):
        super().__init__(game, character)

        self.range = [3, 6]
        self.name = 'INTIMIDATING ROAR'

        self.sanity_reducing = True
        self.multiplier = 0.1

        self.effects_on_hit = ['WEAKNESS', 'MARKING']

        self.sound = DEBUFF_SOUND

        self.combat_animation = self.character.spritesheet.get_sprite(0, 100, 120, 40)
        self.combat_animation = p.transform.scale(self.combat_animation, (self.combat_animation.get_width() * 2, self.combat_animation.get_height() * 2))

class Boom(EnemySkill):

    def __init__(self, game, character):
        super().__init__(game, character)

        self.range = [6, 11]
        self.name = 'BOOOOOOM!!!'

        self.effects_on_hit = ['BLINDING']

        self.sanity_reducing = True

        self.splash = 2

        self.sound = HEAVY_SOUND

        self.combat_animation = self.character.spritesheet.get_sprite(0, 60, 120, 40)
        self.combat_animation = p.transform.scale(self.combat_animation, (self.combat_animation.get_width() * 2, self.combat_animation.get_height() * 2))

class RallyingWinds(EnemySkill):

    def __init__(self, game, character):
        super().__init__(game, character)

        self.range = [1, 10]
        self.name = 'RALLYING WINDS'

        self.heals = True
        self.multiplier = 0

        self.effects_on_hit = ['STRENGTH']
        self.effects_on_user = ['STRENGTH']

        self.targets_all_in_range = True
        self.targets_heroes = False

        self.sound = BUFF_SOUND

        self.combat_animation = self.character.spritesheet.get_sprite(0, 100, 120, 80)
        self.combat_animation = p.transform.scale(self.combat_animation, (self.combat_animation.get_width() * 2, self.combat_animation.get_height() * 2))

class Obliterate(EnemySkill):

    def __init__(self, game, character):
        super().__init__(game, character)

        self.range = [0, 4]
        self.name = 'OBLITERATE'

        self.effects_on_hit = ['BROKEN', 'BLEEDING', 'MARKING']

        self.mark_damage_multiplier = 1.2

        self.sound = HEAVY_SOUND

        self.combat_animation = self.character.spritesheet.get_sprite(0, 100, 120, 40)
        self.combat_animation = p.transform.scale(self.combat_animation, (self.combat_animation.get_width() * 2, self.combat_animation.get_height() * 2))

class GetThem(EnemySkill):

    def __init__(self, game, character):
        super().__init__(game, character)

        self.range = [4, 12]
        self.name = 'GET THEM!'

        self.sanity_reducing = True
        self.multiplier = 0.1

        self.effects_on_hit = ['MARKING', 'ANTIDODGE2', 'BROKEN2']
        self.effects_on_user = ['CRIT']

        self.sound = MARK_SOUND

        self.combat_animation = self.character.spritesheet.get_sprite(0, 60, 120, 40)
        self.combat_animation = p.transform.scale(self.combat_animation, (self.combat_animation.get_width() * 2, self.combat_animation.get_height() * 2))