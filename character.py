import pygame as p
from sprite import *
from settings import *
from effect import *
from wait import *
import random
import math



class Character(p.sprite.Sprite):

    # characters are one of the most important and complex objects in this game, they contain the skills which the player/computer can use for combat to actually happen, as well as handling calculating damage
    # this specific class is never actually used, but instead forms a shell for the 'Hero' and 'Enemy' classes to copy and expand on, which both share most of their properties and functions

    def __init__(self, game, type):

        self.groups = game.characters
        p.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.type = type
        self.spritesheet = Sprite(CHARACTER_SPRITESHEETS[self.type], scale = 4)

        # this is the portrait that appears on the preview of each character

        self.portrait = self.spritesheet.get_sprite(80, 0, 20, 20)

        # this is the portrait that appears on the bottom menu

        self.large_portrait = p.transform.scale(self.portrait, (160, 160))


        # these images are used for the characters animation in a combat animation, which shows one character attacking another with one of their skills

        self.combat_images = [
            self.spritesheet.get_sprite(0, 20, 40, 40),
            self.spritesheet.get_sprite(40, 20, 40, 40)
        ]

        self.grid_pos = [0, 0]

        # these images are used for the characters animation when they are on the battle map whilst the player is selecting a skill

        self.images = [
            p.transform.scale(self.spritesheet.get_sprite(0, 0, 20, 20), (60, 60)),
            p.transform.scale(self.spritesheet.get_sprite(20, 0, 20, 20), (60, 60))
        ]

        # these properties are all used to keep track of the characters animation when on the map, and what direction they are facing

        self.last_update = 0
        self.current_frame = 0
        self.flipped = False

        self.image = self.images[0]
        self.combat_image = self.combat_images[0]

        self.effects = [
            
            ]
        
        self.has_moved = False # whether the character has moved
        self.has_used_skill = False # whether the character has used a skill
        self.deaths_door = False # whether the character is on deaths door
        self.stunned = False # whether the character is stunned, and needs to skip their next turn 
        self.marked = False # whether the character is marked, more likely to take attacks from enemies, as well as taking bonus damage from some attacks
        
        self.sanity_recovery_skills = [0, 0] # the range of values this characters skill will increase the targets sanity by
        self.sanity_reduction_skills = [0, 0] # the range of values this characters skill will decrease the targets sanity by
        self.healing = [0, 0] # the range of values this characters skill will heal the targets health by
        self.damage = [0, 0] # the range of values this characters skill will reduce the targets health by

        self.sanity_damage_factor = 0 # the amount of bonus sanity healing a hero will recieve
        self.sanity_recovery_factor = 0 # the amount of bonus sanity reduction a hero will recieve

        self.effect_applied_images = [] # the effects that are applied onto a character need to be displayed during combat animations, they are stored here

    def calculate_damage_dealt(self, damage, damage_dealer = None, debuff = False):

        # this function calculates the damage dealt/health healed when a character uses a skill on this character

        if self in self.game.characters:

            missed = False # whether the character that used the skill has missed
            dodged = False # whether this character has dodged
            crit = False # whether the character that used the skill has achieved a critical hit

            # if this damage does not come from a debuff (damage from things such as bleeding cannot be dodged)

            if debuff == False:

                # calculates the chance to dodge
                # if this character has lots of agility, and the attacker has low precision, the chance to for this character to dodge will be high

                chance_to_dodge = 100 + self.agility - damage_dealer.precision - damage_dealer.selected_skill.bonus_precision

                # calculates the chance to miss
                # if the attacker has low precision, the chance for them to miss will be high

                chance_to_miss = 100 - damage_dealer.precision - damage_dealer.selected_skill.bonus_precision

                # using a random number, whether there is a miss or a dodge is calculated here

                rand = random.randint(1, 100)

                if rand <= chance_to_dodge:

                    dodged = True

                rand = random.randint(1, 100)

                if rand <= chance_to_miss:

                    missed = True

                # if the attack has successfully hit

                if not missed and not dodged:

                    # whether the attack has crit is calculated

                    crit = self.calculate_crit(damage_dealer)

                    # if it has crit, increase the damage to the top of the range and then add 30%

                    if crit == True:
                        damage = damage_dealer.damage[1] * damage_dealer.selected_skill.multiplier
                        damage *= 1.3

                    marked = False

                    for effect in self.effects:
                        if type(effect) == Mark:
                            marked = True

                    # if this character is marked, add any bonus damage the attacker may deal

                    if marked == True:

                        damage = damage * damage_dealer.selected_skill.mark_damage_multiplier

                    # calculate the damage after this characters protection has been taken into account

                    protection = self.protection / 100

                    protection = 1 - protection

                    damage *= protection

                    # round the damage down

                    damage = math.floor(damage)

            if not missed and not dodged:

                # if the damage is greater than 0, this character recieves a deathblow check and might die

                if damage > 0 and self.current_health == 0:
                    self.deathblow()
                    self.deaths_door = True

                # decrease this characters health by the damage, making sure it never goes negative

                self.current_health = max(0, self.current_health - damage)

                # if this character is on zero health and has no deathblow resistance

                if self.current_health == 0 and self.death == 0 and self in self.game.battle.all_characters:

                    # if this character is an enemy
                    if self not in self.game.hero_party:
                        if debuff == False:

                            # make the hero that killed this character say something
                            if damage_dealer.barking == False:
                                BarkTimer(self.game, damage_dealer, random.choice(damage_dealer.killbarks))

                    # then die
                    self.die()

                if self.current_health == 0:
                    self.deaths_door = True

                # if this character is on deaths door and is a hero, make this character say something

                if self.deaths_door:
                    self.effects.append(DeathsDoor(self.game, self))
                    if self in self.game.hero_party:
                        if self.barking == False:
                            BarkTimer(self.game, self, random.choice(self.deathsdoorbarks))


            if debuff == False:

                return damage, crit, missed, dodged
    
    def deathblow(self):

        rand = random.randint(0, 100)

        # if the random number is greater than this characters deathblow resistance, die

        if rand >= self.death:
            self.die()

    def calculate_crit(self, character):

        rand = random.randint(0, 100)

        # if the character who used the skills crit chance plus any bonus crit from the skill they are using is above the random number, a critical hit has been achieved

        if rand <= character.crit + character.selected_skill.bonus_crit:
            return True
        else:
            return False
        
    def calculate_experience(self, experience):

        # increase this characters experience

        self.current_experience += experience

        level = self.experience_level

        # if this character isnt max level

        if level != len(EXPERIENCE_COSTS):

            # if the amount of experience this character has is greater than the amount needed to go to the next level

            if self.current_experience >= EXPERIENCE_COSTS[level]:

                # temporarily revert the effects provided by items

                for item in self.equipment:
                    if item != None:
                        item.remove_item(self)

                # increase this characters level

                self.experience_level += 1

                # improve this characters health and agility by accessing the dictionary using this characters type, and using the characters level as the index to access the correct list of stats for this level

                self.max_health = EXPERIENCE_VALUES[self.type][self.experience_level][0]
                self.agility = EXPERIENCE_VALUES[self.type][self.experience_level][1]

                # reset experience

                self.current_experience = 0

                # add the effects provided by items back on again

                for item in self.equipment:
                    if item != None:
                        item.equip_item(self)

    def calculate_health_healed(self, healing, healer):

        # this function is similiar to the 'calculate_damage_dealt' function except it deals with healing

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

        # removes the character from deaths door after they are healed

        if self.current_health > 0:
            self.deaths_door = False

        if self.deaths_door == False:

            for effect in self.effects:
                if type(effect) == DeathsDoor:
                    effect.remove_effect()

        return healing, crit

