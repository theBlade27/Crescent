import pygame as p
from sprite import *
from settings import *
from skill import*

class ScimitarSlash(EnemySkill):

    def __init__(self, game, character):
        super().__init__(game, character)

        self.range = [0, 3]
        self.name = 'SCIMITAR SLASH'

        self.effects_on_hit = ['BLEEDING']

        self.sound = p.mixer.Sound(MEDIUM_SOUND)

        self.combat_animation = self.character.spritesheet.get_sprite(0, 60, 120, 40)
        self.combat_animation = p.transform.scale(self.combat_animation, (self.combat_animation.get_width() * 2, self.combat_animation.get_height() * 2))

class CrushingBlow(EnemySkill):

    def __init__(self, game, character):
        super().__init__(game, character)

        self.range = [0, 3]
        self.name = 'CRUSHING BLOW'

        self.effects_on_hit = ['STUNNING']

        self.sound = p.mixer.Sound(HEAVY_SOUND)

        self.combat_animation = self.character.spritesheet.get_sprite(0, 60, 120, 40)
        self.combat_animation = p.transform.scale(self.combat_animation, (self.combat_animation.get_width() * 2, self.combat_animation.get_height() * 2))

class RushedShot(EnemySkill):

    def __init__(self, game, character):
        super().__init__(game, character)

        self.range = [3, 6]
        self.name = 'RUSHED SHOT'

        self.sound = p.mixer.Sound(LIGHT_SOUND)

        self.combat_animation = self.character.spritesheet.get_sprite(0, 60, 120, 40)
        self.combat_animation = p.transform.scale(self.combat_animation, (self.combat_animation.get_width() * 2, self.combat_animation.get_height() * 2))