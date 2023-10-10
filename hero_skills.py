import pygame as p
from sprite import *
from settings import *
from skill import *
from effect import *

class Vanquish(HeroSkill):

    def __init__(self, game, character):
        super().__init__(game, character)

        self.name = 'VANQUISH'
        self.desc = 'WITH A SWIFT AND DECISIVE STRIKE, THE BLADE STRIKES DOWN THE ENEMY, \nLEAVING THEM WOUNDED, REELING AND BROKEN'

        self.image = self.spritesheet.get_sprite(0, 60, 20, 20)
        self.image = p.transform.scale(self.image, (160, 160))

        self.range = [0, 3]

        self.sound = p.mixer.Sound(HEAVY_SOUND)

        self.combat_animation = self.spritesheet.get_sprite(0, 80, 120, 40)
        self.combat_animation = p.transform.scale(self.combat_animation, (self.combat_animation.get_width() * 2, self.combat_animation.get_height() * 2))

class Command(HeroSkill):

    def __init__(self, game, character):
        super().__init__(game, character)

        self.name = 'COMMAND'
        self.desc = 'THE BLADE RALLIES THE PARTY AGAINST A SINGLE TARGET, BRINGING A SHARPENED \nFOCUS TO THEIR ATTACKS'

        self.image = self.spritesheet.get_sprite(20, 60, 20, 20)
        self.image = p.transform.scale(self.image, (160, 160))

        self.range = [0, 8]

        self.multiplier = 0

        self.bonus_debuff = 100
        self.bonus_precision = 100

        self.effects_on_hit = ['MARKING', 'ANTIDODGE']
        self.debuffing = True
        self.effects_on_user = ['CRIT3']

        self.sound = p.mixer.Sound(MARK_SOUND)

        self.combat_animation = self.spritesheet.get_sprite(0, 240, 120, 40)
        self.combat_animation = p.transform.scale(self.combat_animation, (self.combat_animation.get_width() * 2, self.combat_animation.get_height() * 2))

class SteelTempest(HeroSkill):

    def __init__(self, game, character):
        super().__init__(game, character)

        self.name = 'STEEL TEMPEST'
        self.desc = 'WITH A FIERCE WHIRLWIND OF SLASHES, THE BLADE BECOMES A TEMPEST OF STEEL, \nEACH STRIKE LEAVING BEHIND A TRAIL OF DEEP GASHES'

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

class FalseHopes(HeroSkill):

    def __init__(self, game, character):
        super().__init__(game, character)

        self.name = 'FALSE HOPES'
        self.desc = 'THE BLADE OFFERS A GLIMMER OF HOPE TO THE PARTY, A RALLYING CRY IN THE \nFACE OF ADVERSITY; YET, DEEP WITHIN, HE CARRIES THE WEIGHT OF THE A \nBITTER TRUTH, A TRUTH THAT ONLY HE KNOWS'

        self.image = self.spritesheet.get_sprite(60, 60, 20, 20)
        self.image = p.transform.scale(self.image, (160, 160))

        self.range = [0, 14]

        self.targets_enemies = False

        self.targets_all_in_range = True

        self.effects_on_hit = ['CRIT']

        self.heals = True
        self.sanity_recovering = True

        self.sound = p.mixer.Sound(SANITY_SOUND)

        self.combat_animation = self.spritesheet.get_sprite(0, 160, 120, 80)
        self.combat_animation = p.transform.scale(self.combat_animation, (self.combat_animation.get_width() * 2, self.combat_animation.get_height() * 2))

class AzureEruption(HeroSkill):

    def __init__(self, game, character):
        super().__init__(game, character)

        self.name = 'AZURE ERUPTION'
        self.desc = 'THE ARCANE CHANNELS A TORRENT OF AZURE FIRE FROM THE EARTH ITSELF, \nENGULFING THE ENEMY IN A SEARING CONFLAGORATION'

        self.image = self.spritesheet.get_sprite(0, 60, 20, 20)
        self.image = p.transform.scale(self.image, (160, 160))

        self.range = [7, 14]

        self.multiplier = 0.7

        self.splash = 2

        self.effects_on_hit = ['BURNING']
        self.debuffing = True

        self.sound = p.mixer.Sound(MEDIUM_SOUND)

        self.combat_animation = self.spritesheet.get_sprite(0, 80, 120, 80)
        self.combat_animation = p.transform.scale(self.combat_animation, (self.combat_animation.get_width() * 2, self.combat_animation.get_height() * 2))

class Illuminate(HeroSkill):

    def __init__(self, game, character):
        super().__init__(game, character)

        self.name = 'ILLUMINATE'
        self.desc = 'WITH A RADIANT BURST OF POWER, THE ARCANE CALLS UPON THE BRILLIANCE OF \nPURE LIGHT. IN A BLINDING FLASH, AN OVERWHELMING RADIANCE ENGULFS THE \nENEMY, LEAVING THEM STUNNED AND BLINDED'

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
        self.desc = 'THE ARCANE DIRECTS HER MYSTICAL POWER INTO A SINGLE, DEVASTATING STRIKE, \nSEARING THEM WITH AN INTENSE HEAT'

        self.image = self.spritesheet.get_sprite(40, 60, 20, 20)
        self.image = p.transform.scale(self.image, (160, 160))

        self.range = [4, 10]

        self.effects_on_hit = ['BURNING']
        self.debuffing = True

        self.sound = p.mixer.Sound(HEAVY_SOUND)

        self.combat_animation = self.spritesheet.get_sprite(0, 240, 120, 40)
        self.combat_animation = p.transform.scale(self.combat_animation, (self.combat_animation.get_width() * 2, self.combat_animation.get_height() * 2))
        
class Rekindle(HeroSkill):

    def __init__(self, game, character):
        super().__init__(game, character)

        self.name = 'REKINDLE'
        self.desc = 'CHANNELING HER INNER FIRE, THE ARCANE ENVELOPS HER COMPANIONS IN A \nSOOTHING AURA OF VERDANT FLAMES, REVITALIZING THEIR HEALTH, A REMINDER THAT \nEVEN IN THE MIDST OF BATTLE, THE WARMTH OF CAMARADERIE CAN HEAL WOUNDS \nAND REKINDLE THE FIGHTING SPIRIT'

        self.image = self.spritesheet.get_sprite(60, 60, 20, 20)
        self.image = p.transform.scale(self.image, (160, 160))

        self.range = [0, 10]

        self.targets_enemies = False

        self.heals = True

        self.sound = p.mixer.Sound(HEAL_SOUND)

        self.combat_animation = self.spritesheet.get_sprite(0, 160, 120, 80)
        self.combat_animation = p.transform.scale(self.combat_animation, (self.combat_animation.get_width() * 2, self.combat_animation.get_height() * 2))