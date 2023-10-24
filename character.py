import pygame as p
from sprite import *
from settings import *
from effect import *
from wait import *
import random
import math



class Character(p.sprite.Sprite):

    def __init__(self, game, type):

        self.groups = game.characters
        p.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.type = type
        self.spritesheet = Sprite(CHARACTER_SPRITESHEETS[self.type], scale = 4)

        self.portrait = self.spritesheet.get_sprite(80, 0, 20, 20)

        self.large_portrait = p.transform.scale(self.portrait, (160, 160))

        self.combat_images = [
            self.spritesheet.get_sprite(0, 20, 40, 40),
            self.spritesheet.get_sprite(40, 20, 40, 40)
        ]

        self.grid_pos = [0, 0]

        self.images = [
            p.transform.scale(self.spritesheet.get_sprite(0, 0, 20, 20), (60, 60)),
            p.transform.scale(self.spritesheet.get_sprite(20, 0, 20, 20), (60, 60))
        ]

        self.last_update = 0
        self.current_frame = 0
        self.flipped = False

        self.image = self.images[0]
        self.combat_image = self.combat_images[0]

        self.effects = [
            
            ]
        
        self.has_moved = False
        self.has_used_skill = False
        self.deaths_door = False
        self.stunned = False
        self.marked = False
        
        self.sanity_recovery_skills = [0, 0]
        self.sanity_reduction_skills = [0, 0]
        self.healing = [0, 0]
        self.damage = [0, 0]

        self.sanity_damage_factor = 0
        self.sanity_recovery_factor = 0

        self.effect_applied_images = []

    def calculate_damage_dealt(self, damage, damage_dealer = None, debuff = False):

        if self in self.game.characters:

            missed = False
            dodged = False
            crit = False

            if debuff == False:

                chance_to_dodge = 100 + self.agility - damage_dealer.precision - damage_dealer.selected_skill.bonus_precision

                chance_to_miss = 100 - damage_dealer.precision - damage_dealer.selected_skill.bonus_precision

                rand = random.randint(1, 100)

                if rand <= chance_to_dodge:

                    dodged = True

                rand = random.randint(1, 100)

                if rand <= chance_to_miss:

                    missed = True

                if not missed and not dodged:

                    crit = self.calculate_crit(damage_dealer)

                    if crit == True:
                        damage = damage_dealer.damage[1] * damage_dealer.selected_skill.multiplier
                        damage *= 1.5

                    marked = False

                    for effect in self.effects:
                        if type(effect) == Mark:
                            marked = True

                    if marked == True:

                        damage = damage * damage_dealer.selected_skill.mark_damage_multiplier


                    protection = self.protection / 100

                    protection = 1 - protection

                    damage *= protection

                    damage = math.floor(damage)

            if not missed and not dodged:

                if damage > 0 and self.current_health == 0:
                    self.deathblow()
                    self.deaths_door = True

                self.current_health = max(0, self.current_health - damage)

                if self.current_health == 0 and self.death == 0 and self in self.game.battle.all_characters:
                    if self not in self.game.hero_party:
                        if debuff == False:
                            if damage_dealer.barking == False:
                                BarkTimer(self.game, damage_dealer, random.choice(damage_dealer.killbarks))
                    self.die()

                if self.current_health == 0:
                    self.deaths_door = True

                if self.deaths_door:
                    self.effects.append(DeathsDoor(self.game, self))
                    if self in self.game.hero_party:
                        if self.barking == False:
                            BarkTimer(self.game, self, random.choice(self.deathsdoorbarks))

            if debuff == False:

                return damage, crit, missed, dodged
    
    def deathblow(self):

        rand = random.randint(0, 100)

        if rand >= self.death:
            self.die()

    def calculate_crit(self, character):

        rand = random.randint(0, 100)

        if rand <= character.crit + character.selected_skill.bonus_crit:
            return True
        else:
            return False

    def calculate_health_healed(self, healing, healer):

        crit = self.calculate_crit(healer)

        if crit == True:
            healing = healer.healing[1]
            healing *= 1.5

        healing = int(healing)

        self.current_health = min(self.current_health + healing, self.max_health)

        if self.deaths_door and healing > 0 and healer != self and self in self.game.menus['BATTLE'].heroes:
            if self.barking == False:
                BarkTimer(self.game, self, random.choice(self.healbarks))

        if self.deaths_door and healing > 0 and healer != self and self in self.game.menus['BATTLE'].heroes:
            if healer.barking == False:
                BarkTimer(self.game, healer, random.choice(healer.healerbarks))

        if self.current_health > 0:
            self.deaths_door = False

        if self.deaths_door == False:

            for effect in self.effects:
                if type(effect) == DeathsDoor:
                    effect.remove_effect()

        return healing, crit

