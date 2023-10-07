import pygame as p
from sprite import *
from settings import *
from skill import *
from effect import *

class Vanquish(HeroSkill):

    def __init__(self, game, character):
        super().__init__(game, character)

        self.name = 'VANQUISH'

        self.image = self.spritesheet.get_sprite(0, 60, 20, 20)
        self.image = p.transform.scale(self.image, (160, 160))

        self.range = [0, 3]

        self.sound = p.mixer.Sound(HEAVY_SOUND)

        self.combat_animation = self.spritesheet.get_sprite(0, 80, 120, 40)
        self.combat_animation = p.transform.scale(self.combat_animation, (self.combat_animation.get_width() * 2, self.combat_animation.get_height() * 2))

class GetHim(HeroSkill):

    def __init__(self, game, character):
        super().__init__(game, character)

        self.name = 'GET HIM!'

        self.image = self.spritesheet.get_sprite(20, 60, 20, 20)
        self.image = p.transform.scale(self.image, (160, 160))

        self.range = [0, 5]

        self.multiplier = 0

        self.effects_on_hit = ['MARKING', 'ANTIDODGE']
        self.effects_on_user = ['STRENGTH']

        self.sound = p.mixer.Sound(MARK_SOUND)

        self.combat_animation = self.spritesheet.get_sprite(0, 240, 120, 40)
        self.combat_animation = p.transform.scale(self.combat_animation, (self.combat_animation.get_width() * 2, self.combat_animation.get_height() * 2))

class Slash(HeroSkill):

    def __init__(self, game, character):
        super().__init__(game, character)

        self.name = 'SLASH'

        self.image = self.spritesheet.get_sprite(40, 60, 20, 20)
        self.image = p.transform.scale(self.image, (160, 160))

        self.range = [0, 2]

        self.multiplier = 0.7

        self.targets_all_in_range = True

        self.effects_on_hit = ['BLEEDING']
        self.debuffing = True

        self.sound = p.mixer.Sound(MEDIUM_SOUND)

        self.combat_animation = self.spritesheet.get_sprite(0, 120, 120, 40)
        self.combat_animation = p.transform.scale(self.combat_animation, (self.combat_animation.get_width() * 2, self.combat_animation.get_height() * 2))

class StrengthenResolve(HeroSkill):

    def __init__(self, game, character):
        super().__init__(game, character)

        self.name = 'STRENGTHEN RESOLVE'

        self.image = self.spritesheet.get_sprite(60, 60, 20, 20)
        self.image = p.transform.scale(self.image, (160, 160))

        self.range = [0, 8]

        self.targets_enemies = False

        self.targets_all_in_range = True

        self.heals = True
        self.sanity_recovering = True

        self.sound = p.mixer.Sound(SANITY_SOUND)

        self.combat_animation = self.spritesheet.get_sprite(0, 160, 120, 80)
        self.combat_animation = p.transform.scale(self.combat_animation, (self.combat_animation.get_width() * 2, self.combat_animation.get_height() * 2))

class AzureEruption(HeroSkill):

    def __init__(self, game, character):
        super().__init__(game, character)

        self.name = 'AZURE ERUPTION'

        self.image = self.spritesheet.get_sprite(0, 60, 20, 20)
        self.image = p.transform.scale(self.image, (160, 160))

        self.range = [5, 9]

        self.multiplier = 0.7

        self.splash = 2

        self.effects_on_hit = ['BURNING']
        self.debuffing = True

        self.sound = p.mixer.Sound(MEDIUM_SOUND)

        self.combat_animation = self.spritesheet.get_sprite(0, 80, 120, 80)
        self.combat_animation = p.transform.scale(self.combat_animation, (self.combat_animation.get_width() * 2, self.combat_animation.get_height() * 2))

class Dazzle(HeroSkill):

    def __init__(self, game, character):
        super().__init__(game, character)

        self.name = 'DAZZLE'

        self.image = self.spritesheet.get_sprite(20, 60, 20, 20)
        self.image = p.transform.scale(self.image, (160, 160))

        self.range = [0, 4]

        self.multiplier = 0.1

        self.targets_enemies = True

        self.targets_all_in_range = True

        self.effects_on_hit = ['BURNING', 'STUNNING', 'BLINDING']
        self.debuffing = True

        self.sound = p.mixer.Sound(LIGHT_SOUND)

        self.combat_animation = self.spritesheet.get_sprite(0, 280, 120, 40)
        self.combat_animation = p.transform.scale(self.combat_animation, (self.combat_animation.get_width() * 2, self.combat_animation.get_height() * 2))

class ArcaneAssault(HeroSkill):

    def __init__(self, game, character):
        super().__init__(game, character)

        self.name = 'ARCANE ASSAULT'

        self.image = self.spritesheet.get_sprite(40, 60, 20, 20)
        self.image = p.transform.scale(self.image, (160, 160))

        self.range = [4, 8]

        self.effects_on_hit = ['BURNING']
        self.debuffing = True

        self.sound = p.mixer.Sound(HEAVY_SOUND)

        self.combat_animation = self.spritesheet.get_sprite(0, 240, 120, 40)
        self.combat_animation = p.transform.scale(self.combat_animation, (self.combat_animation.get_width() * 2, self.combat_animation.get_height() * 2))
        
class Rejuvinate(HeroSkill):

    def __init__(self, game, character):
        super().__init__(game, character)

        self.name = 'REJUVINATE'

        self.image = self.spritesheet.get_sprite(60, 60, 20, 20)
        self.image = p.transform.scale(self.image, (160, 160))

        self.range = [0, 10]

        self.targets_enemies = False

        self.heals = True

        self.sound = p.mixer.Sound(HEAL_SOUND)

        self.combat_animation = self.spritesheet.get_sprite(0, 160, 120, 80)
        self.combat_animation = p.transform.scale(self.combat_animation, (self.combat_animation.get_width() * 2, self.combat_animation.get_height() * 2))