import pygame as p
from sprite import *
from settings import *
from skill import *
from effect import *

# this file just contains all the properties of the different skills heros have, there is no complex code here

class BladeActOut(HeroSkill):

    def __init__(self, game, character):
        super().__init__(game, character)

        self.name = 'ACT OUT'
        self.desc = 'USED WHEN INSANE'

        self.multiplier = 0.5

        self.range = [0, 4]

        self.sound = MEDIUM_SOUND

        self.sanity_reducing = True

        self.combat_animation = self.spritesheet.get_sprite(0, 80, 120, 40)
        self.combat_animation = p.transform.scale(self.combat_animation, (self.combat_animation.get_width() * 2, self.combat_animation.get_height() * 2))

class Vanquish(HeroSkill):

    def __init__(self, game, character):
        super().__init__(game, character)

        self.name = 'VANQUISH'
        self.desc = 'WITH A SWIFT AND DECISIVE STRIKE, THE BLADE STRIKES DOWN THE ENEMY, \nLEAVING THEM WOUNDED, REELING AND BROKEN\n+30% AGAINST MARKED'

        self.image = self.spritesheet.get_sprite(0, 60, 20, 20)
        self.image = p.transform.scale(self.image, (160, 160))

        self.range = [0, 4]

        self.sound = MEDIUM_SOUND

        self.barks = [
            'YOU SHALL BE VANQUISHED!'
            ]

        self.mark_damage_multiplier = 1.3

        self.combat_animation = self.spritesheet.get_sprite(0, 80, 120, 40)
        self.combat_animation = p.transform.scale(self.combat_animation, (self.combat_animation.get_width() * 2, self.combat_animation.get_height() * 2))

class Command(HeroSkill):

    def __init__(self, game, character):
        super().__init__(game, character)

        self.name = 'COMMAND'
        self.desc = 'THE BLADE RALLIES THE PARTY AGAINST A SINGLE TARGET, BRINGING A SHARPENED \nFOCUS TO THEIR ATTACKS'

        self.image = self.spritesheet.get_sprite(20, 60, 20, 20)
        self.image = p.transform.scale(self.image, (160, 160))

        self.range = [0, 12]

        self.multiplier = 0

        self.bonus_debuff = 100
        self.bonus_precision = 100

        self.effects_on_hit = ['MARKING', 'ANTIDODGE2']
        self.debuffing = True
        self.effects_on_user = ['CRIT2', 'PRECISION']

        self.barks = [
            'GET THEM!',
            'SHOW NO MERCY.'
            ]

        self.sound = MARK_SOUND

        self.combat_animation = self.spritesheet.get_sprite(0, 240, 120, 40)
        self.combat_animation = p.transform.scale(self.combat_animation, (self.combat_animation.get_width() * 2, self.combat_animation.get_height() * 2))

class SteelTempest(HeroSkill):

    def __init__(self, game, character):
        super().__init__(game, character)

        self.name = 'STEEL TEMPEST'
        self.desc = 'WITH A FIERCE WHIRLWIND OF SLASHES, THE BLADE BECOMES A TEMPEST OF STEEL, \nEACH STRIKE LEAVING BEHIND A TRAIL OF DEEP GASHES'

        self.image = self.spritesheet.get_sprite(40, 60, 20, 20)
        self.image = p.transform.scale(self.image, (160, 160))

        self.range = [0, 3]

        self.multiplier = 0.8

        self.targets_all_in_range = True

        self.effects_on_hit = ['BLEEDING', 'BLINDING']

        self.bonus_debuff = 30

        self.debuffing = True

        self.barks = [
            'YOUR BLOOD SHALL\nCLEANSE THE LAND'
            ]

        self.sound = MEDIUM_SOUND

        self.combat_animation = self.spritesheet.get_sprite(0, 120, 120, 40)
        self.combat_animation = p.transform.scale(self.combat_animation, (self.combat_animation.get_width() * 2, self.combat_animation.get_height() * 2))

class FalseHopes(HeroSkill):

    def __init__(self, game, character):
        super().__init__(game, character)

        self.name = 'FALSE HOPES'
        self.desc = 'THE BLADE OFFERS A GLIMMER OF HOPE TO THE PARTY, A RALLYING CRY IN THE \nFACE OF ADVERSITY; YET, DEEP WITHIN, HE CARRIES THE WEIGHT OF THE A \nBITTER TRUTH, A TRUTH THAT ONLY HE KNOWS'

        self.image = self.spritesheet.get_sprite(60, 60, 20, 20)
        self.image = p.transform.scale(self.image, (160, 160))

        self.range = [0, 12]

        self.targets_enemies = False

        self.targets_all_in_range = True

        self.effects_on_hit = ['CRIT', 'PROTECTION']

        self.heals = True
        self.sanity_recovering = True

        self.barks = [
            'THIS IS NO PLACE TO DIE.\nON YOUR FEET, SOLDIER',
            'THERE IS STILL HOPE!',
            'HAVE FAITH, FRIENDS!'
        ]

        self.sound = BUFF_SOUND

        self.combat_animation = self.spritesheet.get_sprite(0, 160, 120, 80)
        self.combat_animation = p.transform.scale(self.combat_animation, (self.combat_animation.get_width() * 2, self.combat_animation.get_height() * 2))

class ArcaneActOut(HeroSkill):

    def __init__(self, game, character):
        super().__init__(game, character)

        self.name = 'ACT OUT'
        self.desc = 'USED WHEN INSANE'

        self.range = [5, 10]

        self.multiplier = 0.5

        self.effects_on_hit = ['BURNING', 'BROKEN']

        self.sanity_reducing = True

        self.sound = MEDIUM_SOUND

        self.combat_animation = self.spritesheet.get_sprite(0, 240, 120, 40)
        self.combat_animation = p.transform.scale(self.combat_animation, (self.combat_animation.get_width() * 2, self.combat_animation.get_height() * 2))

class AzureEruption(HeroSkill):

    def __init__(self, game, character):
        super().__init__(game, character)

        self.name = 'AZURE ERUPTION'
        self.desc = 'THE ARCANE CHANNELS A TORRENT OF AZURE FIRE FROM THE EARTH ITSELF, \nENGULFING THE ENEMY IN A SEARING CONFLAGORATION'

        self.image = self.spritesheet.get_sprite(0, 60, 20, 20)
        self.image = p.transform.scale(self.image, (160, 160))

        self.range = [4, 8]

        self.multiplier = 0.7

        self.bonus_debuff = 30

        self.splash = 3

        self.barks = [
            'BURN. BURN! BURN!!'
            ]

        self.effects_on_hit = ['BURNING']

        self.debuffing = True

        self.sound = HEAVY_SOUND

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

        self.bonus_debuff = 30

        self.targets_enemies = True

        self.barks = [
            'ARE YOUR EYES BURNING YET?'
            ]

        self.targets_all_in_range = True

        self.effects_on_hit = ['BURNING2', 'STUNNING', 'BLINDING']

        self.debuffing = True

        self.sound = LIGHT_SOUND

        self.combat_animation = self.spritesheet.get_sprite(0, 280, 120, 40)
        self.combat_animation = p.transform.scale(self.combat_animation, (self.combat_animation.get_width() * 2, self.combat_animation.get_height() * 2))

class ArcaneAssault(HeroSkill):

    def __init__(self, game, character):
        super().__init__(game, character)

        self.name = 'ARCANE ASSAULT'
        self.desc = 'THE ARCANE DIRECTS HER MYSTICAL POWER INTO A SINGLE, DEVASTATING STRIKE, \nSEARING THEM WITH AN INTENSE HEAT'

        self.image = self.spritesheet.get_sprite(40, 60, 20, 20)
        self.image = p.transform.scale(self.image, (160, 160))

        self.range = [5, 10]

        self.bonus_debuff = 30

        self.effects_on_hit = ['BURNING', 'BROKEN']

        self.debuffing = True

        self.barks = [
            'SKIDOOSH!'
            ]

        self.sound = HEAVY_SOUND

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

        self.effects_on_hit = ['STRENGTH']

        self.targets_enemies = False

        self.sanity_recovering = True

        self.heals = True

        self.sound = BUFF_SOUND

        self.combat_animation = self.spritesheet.get_sprite(0, 160, 120, 80)
        self.combat_animation = p.transform.scale(self.combat_animation, (self.combat_animation.get_width() * 2, self.combat_animation.get_height() * 2))


class BreachActOut(HeroSkill):

    def __init__(self, game, character):
        super().__init__(game, character)

        self.name = 'ACT OUT'
        self.desc = 'USED WHEN INSANE'

        self.multiplier = 0.5

        self.range = [0, 6]

        self.sound = HEAVY_SOUND

        self.sanity_reducing = True

        self.combat_animation = self.spritesheet.get_sprite(0, 80, 120, 40)
        self.combat_animation = p.transform.scale(self.combat_animation, (self.combat_animation.get_width() * 2, self.combat_animation.get_height() * 2))



class DoubleTap(HeroSkill):

    def __init__(self, game, character):
        super().__init__(game, character)

        self.name = 'DOUBLE TAP'
        self.desc = 'TWO SHOTS, ONE PURPOSE - SWIFT AND EFFICIENT ELIMINATION\n+30% AGAINST MARKED'

        self.image = self.spritesheet.get_sprite(0, 60, 20, 20)
        self.image = p.transform.scale(self.image, (160, 160))

        self.range = [0, 6]

        self.mark_damage_multiplier = 1.3

        self.multiplier = 1

        self.effects_on_hit = ['BROKEN']

        self.debuffing = True

        self.bonus_debuff = 30

        self.barks = [
            'PEW PEW!'
            ]

        self.sound = HEAVY_SOUND

        self.combat_animation = self.spritesheet.get_sprite(0, 80, 120, 40)
        self.combat_animation = p.transform.scale(self.combat_animation, (self.combat_animation.get_width() * 2, self.combat_animation.get_height() * 2))

class KissOfFire(HeroSkill):

    def __init__(self, game, character):
        super().__init__(game, character)

        self.name = 'KISS OF FIRE'
        self.desc = 'A POINT BLANK SHOT THAT LEAVES FOES REELING AND BROKEN'

        self.image = self.spritesheet.get_sprite(20, 60, 20, 20)
        self.image = p.transform.scale(self.image, (160, 160))

        self.range = [0, 2]

        self.barks = [
            'THAT LOOKED LIKE IT HURT'
            ]
        
        self.debuffing = True

        self.multiplier = 1.7

        self.sound = HEAVY_SOUND

        self.combat_animation = self.spritesheet.get_sprite(0, 120, 120, 40)
        self.combat_animation = p.transform.scale(self.combat_animation, (self.combat_animation.get_width() * 2, self.combat_animation.get_height() * 2))

class BleedingBlade(HeroSkill):

    def __init__(self, game, character):
        super().__init__(game, character)

        self.name = 'BLEEDING BLADE'
        self.desc = 'A CALCULATED STRIKE THAT INFLICTS A LASTING AND DEBILITATING WOUND\n+50% AGAINST MARKED'

        self.image = self.spritesheet.get_sprite(40, 60, 20, 20)
        self.image = p.transform.scale(self.image, (160, 160))

        self.range = [0, 3]

        self.multiplier = 0.8

        self.mark_damage_multiplier = 1.5

        self.effects_on_hit = ['BLEEDING']

        self.bonus_debuff = 30

        self.debuffing = True

        self.sound = MEDIUM_SOUND

        self.combat_animation = self.spritesheet.get_sprite(0, 160, 120, 40)
        self.combat_animation = p.transform.scale(self.combat_animation, (self.combat_animation.get_width() * 2, self.combat_animation.get_height() * 2))

class Firestarter(HeroSkill):

    def __init__(self, game, character):
        super().__init__(game, character)

        self.name = 'FIRESTARTER'
        self.desc = 'IGNITE MAYHEM WITH A FIERY EXPLOSION'

        self.image = self.spritesheet.get_sprite(60, 60, 20, 20)
        self.image = p.transform.scale(self.image, (160, 160))

        self.range = [3, 8]

        self.splash = 2

        self.multiplier = 0.3

        self.bonus_debuff = 30

        self.debuffing = True

        self.barks = [
            'FIRE IN THE HOLE!'
            ]

        self.effects_on_hit = ['MARKING', 'BURNING']

        self.sound = DEBUFF_SOUND

        self.combat_animation = self.spritesheet.get_sprite(0, 200, 120, 40)
        self.combat_animation = p.transform.scale(self.combat_animation, (self.combat_animation.get_width() * 2, self.combat_animation.get_height() * 2))