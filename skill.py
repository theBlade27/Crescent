import pygame as p
from sprite import *
from settings import *
from character import *
from wait import *
import random
vec = p.math.Vector2

class Skill(p.sprite.Sprite):

    # each character has a list of skills
    # skills are what are used to deal damage or heal other characters during combat

    def __init__(self, game, character):

        self.groups = game.skills_group
        p.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.name = '' # name of the skill
        self.desc = '' # description of the skill
        self.character = character # the character this skill belongs to
        self.targets = [] # the targets this skill is going to be used on

        self.range = [0, 0] # the minimum and maximum range in tiles this skill can target characters in
        self.multiplier = 1 # the damage/healing multiplier (for example some skills deal more or less damage for a tradeoff)
        self.targets_all_in_range = False # whether this skill targets every single character in its range
        self.splash = 0 # the amount of tiles around the target that are also affected by the skill
        self.heals = False # whether the skill damages or heals
        self.sanity_recovering = False # whether the skill increases sanity
        self.sanity_reducing = False # whether the skill decreases sanity
        self.debuffing = False # whether this skill applies debuffs

        self.effects_on_hit = [] # the effects this skill applies on targets it is used on
        self.effects_on_user = [] # the effects this skill applies on the character that uses it

        self.bonus_stun = 0 # bonus chance to stun
        self.bonus_debuff = 0 # bonus chance to add debuffs
        self.bonus_crit = 0 # bonus chance to crit
        self.bonus_precision = 0 # bonus chance to hit

        self.combat_animation = p.Surface((1, 1))
        self.combat_animation.fill(BLACK)

        self.mark_damage_multiplier = 1 # bonus damage to marked targets

        self.barks = [] # things the character may say after using this skill

    def update(self):

        if self == self.game.selected_character.selected_skill:
            menu = self.game.menus['BATTLE']
            for tile in menu.tiles:
                distance = vec(tile.grid_pos[0], tile.grid_pos[1]) - vec(self.game.selected_character.grid_pos[0], self.game.selected_character.grid_pos[1])
                if distance.length() >= self.range[0] and distance.length() < self.range[1]:
                    tile.targetable = True

    def use_skill(self, tiles):

        self.targets = []

        self.text = '' # this text will be displayed at the top of the screen

        crit = False
        dodged = False
        missed = False

        # these numbers will be displayed to the player on the combat animation to show how effective a skill is
        # for example, it would show how much damage an attack did after it is used
        damage_numbers = []
        heal_numbers = []
        sanity_heal_numbers = []
        sanity_damage_numbers = []

        if self.game.actingout:

            # if the character using this skill is acting out, say something from the characters list of 'actoutbarks'

            if self.character.barking == False:

                BarkTimer(self.game, self.character, random.choice(self.character.actoutbarks))

        for tile in tiles:

            # gets a list of every character who is standing on the tiles that are passed into this function

            for character in self.game.characters:
                if character.grid_pos == tile.grid_pos:
                    self.targets.append(character)

        # if this skill does damage

        if self.heals == False:

            # for every target that needs to be damaged

            for target in self.targets:

                # the damage they should take is found by choosing a random number from the user of this skills damage range and multiply it by the multiplier of this skill

                damage = random.randint(int(self.character.damage[0]), int(self.character.damage[1])) * self.multiplier

                # then the amount the targets health goes down by is calculated by the 'calculate_damage_dealt' function which is in the Character class
                # as well as this, information about exactly how much damage was dealt after everything was accounted for, whether it crit, whether it missed and whether the character dodged are returned

                damage, crit, missed, dodged = target.calculate_damage_dealt(damage, self.character)

                # if the character crit, increase their sanity
                if crit:
                    self.character.calculate_sanity_increase(5)

                # if the character got to deaths door

                if target.deaths_door == True:

                    # if the character is still alive, the text must change to indicate that character is almost dead

                    if target in self.game.battle.all_characters:
                        self.text += '{} IS ON THE BRINK OF DEATH!\n'.format(target.name)
                        target.effect_applied_images.append(DeathsDoor(self.game, None).image)
                    else:

                    # otherwise, say they aer dead
                        self.text += '{} MET THEIR END.\n'.format(target.name)

                # if the attack crit, add the word CRIT in front of the damage text that is displayed and make the character say something

                if (not missed) and (not dodged):

                    if crit:

                        damage_numbers.append('CRIT' + str(int(damage)))
                        if self.character.barking == False:

                            if self.game.actingout == False:

                                BarkTimer(self.game, self.character, random.choice(self.character.critbarks))

                    else:

                        # otherwise, just write the word normally

                        damage_numbers.append(str(int(damage)))

                # indicate to the player if the attack was missed or the target dodged

                elif missed:

                    damage_numbers.append('MISSED')

                elif dodged:

                    damage_numbers.append('DODGED')

        # same but for sanity recovering skills

        if self.sanity_recovering == True:

            for target in self.targets:
                sanity_recovery = random.randint(int(self.character.sanity_recovery_skills[0]), int(self.character.sanity_recovery_skills[1]))
                sanity = int(target.calculate_sanity_increase(sanity_recovery))

                sanity_heal_numbers.append(sanity)

        # same but for sanity reducing skills

        if self.sanity_reducing == True:

            for target in self.targets:
                sanity_reduction = random.randint(int(self.character.sanity_reduction_skills[0]), int(self.character.sanity_reduction_skills[1]))
                sanity = int(target.calculate_sanity_decrease(sanity_reduction))

                sanity_damage_numbers.append(sanity)

        # same but for healing skills

        if self.heals == True:

            for target in self.targets:
                healing = random.randint(int(self.character.healing[0]), int(self.character.healing[1])) * self.multiplier
                healing, crit = target.calculate_health_healed(healing, self.character)
                if crit:
                    self.character.calculate_sanity_increase(5)
                    target.calculate_sanity_increase(5)

                if crit:

                    heal_numbers.append('CRIT' + str(int(healing)))

                else:

                    heal_numbers.append(str(int(healing)))

        # for every effect in 'effects_on_user', apply that effect on the user

        for effect in self.effects_on_user:

            # if the effect is STRENGTH

            if effect == 'STRENGTH':

                # remove strength
        
                for effect in self.character.effects:
                    if type(effect) == Strength:
                        effect.remove_effect()

                # then apply it again to reset the timer

                self.character.effects.append(Strength(self.game, self.character))

                # then add an image of the effect to the combat animation so the player knows the strength effect has been applied to the user
                self.character.effect_applied_images.append(Strength(self.game, None).image)

            if effect == 'STRENGTH2':
        
                for effect in self.character.effects:
                    if type(effect) == Strength2:
                        effect.remove_effect()

                self.character.effects.append(Strength2(self.game, self.character))
                self.character.effect_applied_images.append(Strength2(self.game, None).image)

            if effect == 'STRENGTH3':
        
                for effect in self.character.effects:
                    if type(effect) == Strength3:
                        effect.remove_effect()

                self.character.effects.append(Strength3(self.game, self.character))
                self.character.effect_applied_images.append(Strength3(self.game, None).image)

            if effect == 'CRIT':
        
                for effect in self.character.effects:
                    if type(effect) == Crit:
                        effect.remove_effect()

                self.character.effects.append(Crit(self.game, self.character))
                self.character.effect_applied_images.append(Crit(self.game, None).image)

            if effect == 'CRIT2':
        
                for effect in self.character.effects:
                    if type(effect) == Crit2:
                        effect.remove_effect()

                self.character.effects.append(Crit2(self.game, self.character))
                self.character.effect_applied_images.append(Crit2(self.game, None).image)

            if effect == 'CRIT3':
        
                for effect in self.character.effects:
                    if type(effect) == Crit3:
                        effect.remove_effect()

                self.character.effects.append(Crit3(self.game, self.character))
                self.character.effect_applied_images.append(Crit3(self.game, None).image)

            if effect == 'PRECISION':
        
                for effect in self.character.effects:
                    if type(effect) == Precision:
                        effect.remove_effect()

                self.character.effects.append(Precision(self.game, self.character))
                self.character.effect_applied_images.append(Precision(self.game, None).image)

            if effect == 'PRECISION2':
        
                for effect in self.character.effects:
                    if type(effect) == Precision2:
                        effect.remove_effect()

                self.character.effects.append(Precision2(self.game, self.character))
                self.character.effect_applied_images.append(Precision2(self.game, None).image)

            if effect == 'PRECISION3':
        
                for effect in self.character.effects:
                    if type(effect) == Precision3:
                        effect.remove_effect()

                self.character.effects.append(Precision3(self.game, self.character))
                self.character.effect_applied_images.append(Precision3(self.game, None).image)

            if effect == 'SPEED':
        
                for effect in self.character.effects:
                    if type(effect) == Speed:
                        effect.remove_effect()

                self.character.effects.append(Speed(self.game, self.character))
                self.character.effect_applied_images.append(Speed(self.game, None).image)

            if effect == 'SPEED2':
        
                for effect in self.character.effects:
                    if type(effect) == Speed2:
                        effect.remove_effect()

                self.character.effects.append(Speed2(self.game, self.character))
                self.character.effect_applied_images.append(Speed2(self.game, None).image)

            if effect == 'SPEED3':
        
                for effect in self.character.effects:
                    if type(effect) == Speed3:
                        effect.remove_effect()

                self.character.effects.append(Speed3(self.game, self.character))
                self.character.effect_applied_images.append(Speed3(self.game, None).image)

            if effect == 'PROTECTION':
        
                for effect in self.character.effects:
                    if type(effect) == Protection:
                        effect.remove_effect()

                self.character.effects.append(Protection(self.game, self.character))
                self.character.effect_applied_images.append(Protection(self.game, None).image)

            if effect == 'PROTECTION2':
        
                for effect in self.character.effects:
                    if type(effect) == Protection2:
                        effect.remove_effect()

                self.character.effects.append(Protection2(self.game, self.character))
                self.character.effect_applied_images.append(Protection2(self.game, None).image)

            if effect == 'PROTECTION3':
        
                for effect in self.character.effects:
                    if type(effect) == Protection3:
                        effect.remove_effect()

                self.character.effects.append(Protection3(self.game, self.character))
                self.character.effect_applied_images.append(Protection3(self.game, None).image)

            if effect == 'DODGE':
        
                for effect in self.character.effects:
                    if type(effect) == Dodge:
                        effect.remove_effect()

                self.character.effects.append(Dodge(self.game, self.character))
                self.character.effect_applied_images.append(Dodge(self.game, None).image)

            if effect == 'DODGE2':
        
                for effect in self.character.effects:
                    if type(effect) == Dodge2:
                        effect.remove_effect()

                self.character.effects.append(Dodge2(self.game, self.character))
                self.character.effect_applied_images.append(Dodge2(self.game, None).image)

            if effect == 'DODGE3':
        
                for effect in self.character.effects:
                    if type(effect) == Dodge3:
                        effect.remove_effect()

                self.character.effects.append(Dodge3(self.game, self.character))
                self.character.effect_applied_images.append(Dodge3(self.game, None).image)

        # same but for effects applied on targets

        for target in self.targets:

            # reset the targets list of applied effects

            target.effect_applied_images.clear()

            # for every effect this skill applies

            for effect in self.effects_on_hit:

                # if the skill actually hit
                    
                if (not missed) and (not dodged):

                    # if the effect is BURNING
                
                    if effect == 'BURNING':

                        # using a random number, decide if the effect is actually applied, with this skills 'bonus_debuff' property increasing the chance
                        rand = random.randint(0, 100)

                        rand += self.bonus_debuff

                        # if the random number is greater than the targets resistance to debuffs, it is successful

                        if rand >= self.character.fire:
                            self.successful = True
                        else:
                            self.successful = False

                        # if it is successful, apply the effect

                        if self.successful:

                            for effect in target.effects:
                                if type(effect) == Burning:
                                    effect.remove_effect()

                            target.effects.append(Burning(self.game, target))
                            target.effect_applied_images.append(Burning(self.game, None).image)

                        # if not, a cross will be drawn to indicate to the player that the effect was not applied

                        else:

                            target.effect_applied_images.append(p.transform.scale(CROSS, [40, 40]))

                    if effect == 'BURNING2':

                        rand = random.randint(0, 100)

                        rand += self.bonus_debuff

                        if rand >= self.character.fire:
                            self.successful = True
                        else:
                            self.successful = False

                        if self.successful:

                            for effect in target.effects:
                                if type(effect) == Burning2:
                                    effect.remove_effect()

                            target.effects.append(Burning2(self.game, target))
                            target.effect_applied_images.append(Burning2(self.game, None).image)

                        else:

                            target.effect_applied_images.append(p.transform.scale(CROSS, [40, 40]))

                    if effect == 'BURNING3':

                        rand = random.randint(0, 100)

                        rand += self.bonus_debuff

                        if rand >= self.character.fire:
                            self.successful = True
                        else:
                            self.successful = False

                        if self.successful:

                            for effect in target.effects:
                                if type(effect) == Burning3:
                                    effect.remove_effect()

                            target.effects.append(Burning3(self.game, target))
                            target.effect_applied_images.append(Burning3(self.game, None).image)

                        else:

                            target.effect_applied_images.append(p.transform.scale(CROSS, [40, 40]))

                    if effect == 'BLEEDING':


                        rand = random.randint(0, 100)

                        rand += self.bonus_debuff

                        if rand >= self.character.bleed:
                            self.successful = True
                        else:
                            self.successful = False

                        if self.successful:

                            for effect in target.effects:
                                if type(effect) == Bleeding:
                                    effect.remove_effect()

                            target.effects.append(Bleeding(self.game, target))
                            target.effect_applied_images.append(Bleeding(self.game, None).image)

                        else:

                            target.effect_applied_images.append(p.transform.scale(CROSS, [40, 40]))

                    if effect == 'BLEEDING2':


                        rand = random.randint(0, 100)

                        rand += self.bonus_debuff

                        if rand >= self.character.bleed:
                            self.successful = True
                        else:
                            self.successful = False

                        if self.successful:

                            for effect in target.effects:
                                if type(effect) == Bleeding2:
                                    effect.remove_effect()

                            target.effects.append(Bleeding2(self.game, target))
                            target.effect_applied_images.append(Bleeding2(self.game, None).image)

                        else:

                            target.effect_applied_images.append(p.transform.scale(CROSS, [40, 40]))

                    if effect == 'BLEEDING3':


                        rand = random.randint(0, 100)

                        rand += self.bonus_debuff

                        if rand >= self.character.bleed:
                            self.successful = True
                        else:
                            self.successful = False

                        if self.successful:

                            for effect in target.effects:
                                if type(effect) == Bleeding3:
                                    effect.remove_effect()

                            target.effects.append(Bleeding3(self.game, target))
                            target.effect_applied_images.append(Bleeding3(self.game, None).image)

                        else:

                            target.effect_applied_images.append(p.transform.scale(CROSS, [40, 40]))

                    if effect == 'STUNNING':

                        rand = random.randint(0, 100)

                        rand += self.bonus_stun

                        if rand >= self.character.stun:
                            self.successful = True
                            for effect in target.effects:
                                if type(effect) == StunResist:
                                    self.successful = False
                        else:
                            self.successful = False

                        if self.successful:

                            for effect in target.effects:
                                if type(effect) == Stun:
                                    effect.remove_effect()

                            target.effects.append(Stun(self.game, target))
                            target.effect_applied_images.append(Stun(self.game, None).image)

                        else:

                            target.effect_applied_images.append(p.transform.scale(CROSS, [40, 40]))

                    if effect == 'MARKING':

                        for effect in target.effects:
                            if type(effect) == Mark:
                                effect.remove_effect()

                        target.effects.append(Mark(self.game, target))
                        target.effect_applied_images.append(Mark(self.game, None).image)

                    if effect == 'ANTIDODGE':

                        rand = random.randint(0, 100)

                        rand += self.bonus_debuff

                        if rand >= self.character.debuff:
                            self.successful = True
                        else:
                            self.successful = False

                        if self.successful:

                            for effect in target.effects:
                                if type(effect) == AntiDodge:
                                    effect.remove_effect()

                            target.effects.append(AntiDodge(self.game, target))
                            target.effect_applied_images.append(AntiDodge(self.game, None).image)

                        else:

                            target.effect_applied_images.append(p.transform.scale(CROSS, [40, 40]))

                    if effect == 'ANTIDODGE2':

                        rand = random.randint(0, 100)

                        rand += self.bonus_debuff

                        if rand >= self.character.debuff:
                            self.successful = True
                        else:
                            self.successful = False

                        if self.successful:

                            for effect in target.effects:
                                if type(effect) == AntiDodge2:
                                    effect.remove_effect()

                            target.effects.append(AntiDodge2(self.game, target))
                            target.effect_applied_images.append(AntiDodge2(self.game, None).image)

                        else:

                            target.effect_applied_images.append(p.transform.scale(CROSS, [40, 40]))

                    if effect == 'ANTIDODGE3':

                        rand = random.randint(0, 100)

                        rand += self.bonus_debuff

                        if rand >= self.character.debuff:
                            self.successful = True
                        else:
                            self.successful = False

                        if self.successful:

                            for effect in target.effects:
                                if type(effect) == AntiDodge3:
                                    effect.remove_effect()

                            target.effects.append(AntiDodge3(self.game, target))
                            target.effect_applied_images.append(AntiDodge3(self.game, None).image)

                        else:

                            target.effect_applied_images.append(p.transform.scale(CROSS, [40, 40]))

                    if effect == 'BLINDING':

                        rand = random.randint(0, 100)

                        rand += self.bonus_debuff

                        if rand >= self.character.debuff:
                            self.successful = True
                        else:
                            self.successful = False

                        if self.successful:

                            for effect in target.effects:
                                if type(effect) == Blindness:
                                    effect.remove_effect()

                            target.effects.append(Blindness(self.game, target))
                            target.effect_applied_images.append(Blindness(self.game, None).image)

                        else:

                            target.effect_applied_images.append(p.transform.scale(CROSS, [40, 40]))

                    if effect == 'BLINDING2':

                        rand = random.randint(0, 100)

                        rand += self.bonus_debuff

                        if rand >= self.character.debuff:
                            self.successful = True
                        else:
                            self.successful = False

                        if self.successful:

                            for effect in target.effects:
                                if type(effect) == Blindness2:
                                    effect.remove_effect()

                            target.effects.append(Blindness2(self.game, target))
                            target.effect_applied_images.append(Blindness2(self.game, None).image)

                        else:

                            target.effect_applied_images.append(p.transform.scale(CROSS, [40, 40]))

                    if effect == 'BLINDING3':

                        rand = random.randint(0, 100)

                        rand += self.bonus_debuff

                        if rand >= self.character.debuff:
                            self.successful = True
                        else:
                            self.successful = False

                        if self.successful:

                            for effect in target.effects:
                                if type(effect) == Blindness3:
                                    effect.remove_effect()

                            target.effects.append(Blindness3(self.game, target))
                            target.effect_applied_images.append(Blindness3(self.game, None).image)

                        else:

                            target.effect_applied_images.append(p.transform.scale(CROSS, [40, 40]))

                    if effect == 'STRENGTH':
        
                        for effect in target.effects:
                            if type(effect) == Strength:
                                effect.remove_effect()

                        target.effects.append(Strength(self.game, target))
                        target.effect_applied_images.append(Strength(self.game, None).image)

                    if effect == 'STRENGTH2':
        
                        for effect in target.effects:
                            if type(effect) == Strength2:
                                effect.remove_effect()

                        target.effects.append(Strength2(self.game, target))
                        target.effect_applied_images.append(Strength2(self.game, None).image)

                    if effect == 'STRENGTH3':
        
                        for effect in target.effects:
                            if type(effect) == Strength3:
                                effect.remove_effect()

                        target.effects.append(Strength3(self.game, target))
                        target.effect_applied_images.append(Strength3(self.game, None).image)

                    if effect == 'DODGE':
        
                        for effect in target.effects:
                            if type(effect) == Dodge:
                                effect.remove_effect()

                        target.effects.append(Dodge(self.game, target))
                        target.effect_applied_images.append(Dodge(self.game, None).image)

                    if effect == 'DODGE2':
        
                        for effect in target.effects:
                            if type(effect) == Dodge2:
                                effect.remove_effect()

                        target.effects.append(Dodge2(self.game, target))
                        target.effect_applied_images.append(Dodge2(self.game, None).image)

                    if effect == 'DODGE3':
        
                        for effect in target.effects:
                            if type(effect) == Dodge3:
                                effect.remove_effect()

                        target.effects.append(Dodge3(self.game, target))
                        target.effect_applied_images.append(Dodge3(self.game, None).image)

                    if effect == 'CRIT':
        
                        for effect in target.effects:
                            if type(effect) == Crit:
                                effect.remove_effect()

                        target.effects.append(Crit(self.game, target))
                        target.effect_applied_images.append(Crit(self.game, None).image)

                    if effect == 'CRIT2':
        
                        for effect in target.effects:
                            if type(effect) == Crit2:
                                effect.remove_effect()

                        target.effects.append(Crit2(self.game, target))
                        target.effect_applied_images.append(Crit2(self.game, None).image)

                    if effect == 'CRIT3':
        
                        for effect in target.effects:
                            if type(effect) == Crit3:
                                effect.remove_effect()

                        target.effects.append(Crit3(self.game, target))
                        target.effect_applied_images.append(Crit3(self.game, None).image)

                    if effect == 'PRECISION':
        
                        for effect in target.effects:
                            if type(effect) == Precision:
                                effect.remove_effect()

                        target.effects.append(Precision(self.game, target))
                        target.effect_applied_images.append(Precision(self.game, None).image)

                    if effect == 'PRECISION2':
        
                        for effect in target.effects:
                            if type(effect) == Precision2:
                                effect.remove_effect()

                        target.effects.append(Precision2(self.game, target))
                        target.effect_applied_images.append(Precision2(self.game, None).image)

                    if effect == 'PRECISION3':
        
                        for effect in target.effects:
                            if type(effect) == Precision3:
                                effect.remove_effect()

                        target.effects.append(Precision3(self.game, target))
                        target.effect_applied_images.append(Precision3(self.game, None).image)

                    if effect == 'PROTECTION':
        
                        for effect in target.effects:
                            if type(effect) == Protection:
                                effect.remove_effect()

                        target.effects.append(Protection(self.game, target))
                        target.effect_applied_images.append(Protection(self.game, None).image)

                    if effect == 'PROTECTION2':
        
                        for effect in target.effects:
                            if type(effect) == Protection2:
                                effect.remove_effect()

                        target.effects.append(Protection2(self.game, target))
                        target.effect_applied_images.append(Protection2(self.game, None).image)

                    if effect == 'PROTECTION3':
        
                        for effect in target.effects:
                            if type(effect) == Protection3:
                                effect.remove_effect()

                        target.effects.append(Protection3(self.game, target))
                        target.effect_applied_images.append(Protection3(self.game, None).image)

                    if effect == 'SPEED':
        
                        for effect in target.effects:
                            if type(effect) == Speed:
                                effect.remove_effect()

                        target.effects.append(Speed(self.game, target))
                        target.effect_applied_images.append(Speed(self.game, None).image)

                    if effect == 'SPEED2':
        
                        for effect in target.effects:
                            if type(effect) == Speed2:
                                effect.remove_effect()

                        target.effects.append(Speed2(self.game, target))
                        target.effect_applied_images.append(Speed2(self.game, None).image)

                    if effect == 'SPEED3':
        
                        for effect in target.effects:
                            if type(effect) == Speed3:
                                effect.remove_effect()

                        target.effects.append(Speed3(self.game, target))
                        target.effect_applied_images.append(Speed3(self.game, None).image)

                    if effect == 'WEAKNESS':

                        rand = random.randint(0, 100)

                        rand += self.bonus_debuff

                        if rand >= self.character.debuff:
                            self.successful = True
                        else:
                            self.successful = False

                        if self.successful:

                            for effect in target.effects:
                                if type(effect) == Weakness:
                                    effect.remove_effect()

                            target.effects.append(Weakness(self.game, target))
                            target.effect_applied_images.append(Weakness(self.game, None).image)

                        else:

                            target.effect_applied_images.append(p.transform.scale(CROSS, [40, 40]))

                    if effect == 'WEAKNESS2':

                        rand = random.randint(0, 100)

                        rand += self.bonus_debuff

                        if rand >= self.character.debuff:
                            self.successful = True
                        else:
                            self.successful = False

                        if self.successful:

                            for effect in target.effects:
                                if type(effect) == Weakness2:
                                    effect.remove_effect()

                            target.effects.append(Weakness2(self.game, target))
                            target.effect_applied_images.append(Weakness2(self.game, None).image)

                        else:

                            target.effect_applied_images.append(p.transform.scale(CROSS, [40, 40]))

                    if effect == 'WEAKNESS3':

                        rand = random.randint(0, 100)

                        rand += self.bonus_debuff

                        if rand >= self.character.debuff:
                            self.successful = True
                        else:
                            self.successful = False

                        if self.successful:

                            for effect in target.effects:
                                if type(effect) == Weakness3:
                                    effect.remove_effect()

                            target.effects.append(Weakness3(self.game, target))
                            target.effect_applied_images.append(Weakness3(self.game, None).image)

                        else:

                            target.effect_applied_images.append(p.transform.scale(CROSS, [40, 40]))

                    if effect == 'SLOWNESS':

                        rand = random.randint(0, 100)

                        rand += self.bonus_debuff

                        if rand >= self.character.debuff:
                            self.successful = True
                        else:
                            self.successful = False

                        if self.successful:

                            for effect in target.effects:
                                if type(effect) == Slowness:
                                    effect.remove_effect()

                            target.effects.append(Slowness(self.game, target))
                            target.effect_applied_images.append(Slowness(self.game, None).image)

                        else:

                            target.effect_applied_images.append(p.transform.scale(CROSS, [40, 40]))

                    if effect == 'SLOWNESS2':

                        rand = random.randint(0, 100)

                        rand += self.bonus_debuff

                        if rand >= self.character.debuff:
                            self.successful = True
                        else:
                            self.successful = False

                        if self.successful:

                            for effect in target.effects:
                                if type(effect) == Slowness2:
                                    effect.remove_effect()

                            target.effects.append(Slowness2(self.game, target))
                            target.effect_applied_images.append(Slowness2(self.game, None).image)

                        else:

                            target.effect_applied_images.append(p.transform.scale(CROSS, [40, 40]))

                    if effect == 'SLOWNESS3':

                        rand = random.randint(0, 100)

                        rand += self.bonus_debuff

                        if rand >= self.character.debuff:
                            self.successful = True
                        else:
                            self.successful = False

                        if self.successful:

                            for effect in target.effects:
                                if type(effect) == Slowness3:
                                    effect.remove_effect()

                            target.effects.append(Slowness3(self.game, target))
                            target.effect_applied_images.append(Slowness3(self.game, None).image)

                        else:

                            target.effect_applied_images.append(p.transform.scale(CROSS, [40, 40]))

                    if effect == 'BROKEN':

                        rand = random.randint(0, 100)

                        rand += self.bonus_debuff

                        if rand >= self.character.debuff:
                            self.successful = True
                        else:
                            self.successful = False

                        if self.successful:

                            for effect in target.effects:
                                if type(effect) == BrokenArmour:
                                    effect.remove_effect()

                            target.effects.append(BrokenArmour(self.game, target))
                            target.effect_applied_images.append(BrokenArmour(self.game, None).image)

                        else:

                            target.effect_applied_images.append(p.transform.scale(CROSS, [40, 40]))

                    if effect == 'BROKEN2':

                        rand = random.randint(0, 100)

                        rand += self.bonus_debuff

                        if rand >= self.character.debuff:
                            self.successful = True
                        else:
                            self.successful = False

                        if self.successful:

                            for effect in target.effects:
                                if type(effect) == BrokenArmour2:
                                    effect.remove_effect()

                            target.effects.append(BrokenArmour2(self.game, target))
                            target.effect_applied_images.append(BrokenArmour2(self.game, None).image)

                        else:

                            target.effect_applied_images.append(p.transform.scale(CROSS, [40, 40]))

                    if effect == 'BROKEN3':

                        rand = random.randint(0, 100)

                        rand += self.bonus_debuff

                        if rand >= self.character.debuff:
                            self.successful = True
                        else:
                            self.successful = False

                        if self.successful:

                            for effect in target.effects:
                                if type(effect) == BrokenArmour3:
                                    effect.remove_effect()

                            target.effects.append(BrokenArmour3(self.game, target))
                            target.effect_applied_images.append(BrokenArmour3(self.game, None).image)

                        else:

                            target.effect_applied_images.append(p.transform.scale(CROSS, [40, 40]))

        # reset things

        for tile in self.game.menus['BATTLE'].tiles:
            tile.being_targeted = False

        for menu in self.game.menus.values():
            menu.update_images()

        self.character.has_used_skill = True

        # play this skills sound if it went through

        if not dodged and not missed:

            self.sound.play()

        else:

            # or play the MISS_SOUND if it missed

            sound = p.mixer.Sound(MISS_SOUND)
            sound.play()

        # play combat animations, displaying how effective the skill was using the numbers calculated earlier

        self.game.play_combat_animations(self.character, self.targets, damage_numbers, heal_numbers, sanity_damage_numbers, sanity_heal_numbers)

        # after this timer is up, the combat animation is killed and the next character starts their turn

        ShowSkillEffectivenessTimer(self.game, self.character, self.text)

        # there is a 1 in 3 chance the character says something related to the skill they used

        rand = random.randint(1, 3)

        if rand == 3:

            if len(self.barks) > 0:

                if self.character.barking == False:

                    BarkTimer(self.game, self.character, random.choice(self.barks))

# this is pretty much the same but for enemies instead

class EnemySkill(Skill):

    def __init__(self, game, character):
        super().__init__(game, character)

        self.targets_heroes = True

    def update(self):

        pass

    def use_skill(self, characters):

        self.text = ''

        dodged = False
        missed = False
        crit = False

        damage_numbers = []
        heal_numbers = []

        sanity_damage_numbers = []
        sanity_heal_numbers = []

        if self.heals == False:

            for character in characters:

                damage = random.randint(int(self.character.damage[0]), int(self.character.damage[1])) * self.multiplier
                damage, crit, missed, dodged = character.calculate_damage_dealt(damage, self.character)
                if crit:
                    character.calculate_sanity_decrease(10)

                if character.deaths_door == True:
                    if character in self.game.battle.all_characters:
                        self.text += '{} IS ON THE BRINK OF DEATH!\n'.format(character.name)
                        character.effect_applied_images.append(DeathsDoor(self.game, None).image)
                        character.calculate_sanity_decrease(10)
                    else:
                        self.text += '{} MET THEIR END.\n'.format(character.name)

                if (not missed) and (not dodged):

                    if crit:

                        damage_numbers.append('CRIT' + str(int(damage)))

                        if character.barking == False:

                            BarkTimer(self.game, character, random.choice(character.scaredbarks))

                    else:

                        damage_numbers.append(str(int(damage)))

                elif missed:

                    damage_numbers.append('MISSED')

                else:

                    damage_numbers.append('DODGED')

                

        if self.sanity_recovering == True:

            for character in characters:
                sanity_recovery = random.randint(int(self.character.sanity_recovery_skills[0]), int(self.character.sanity_recovery_skills[1]))
                sanity = int(character.calculate_sanity_increase(sanity_recovery))

                sanity_heal_numbers.append(sanity)

        if self.sanity_reducing == True:

            for character in characters:
                sanity_reduction = random.randint(int(self.character.sanity_reduction_skills[0]), int(self.character.sanity_reduction_skills[1]))
                sanity = int(character.calculate_sanity_decrease(sanity_reduction))

                sanity_damage_numbers.append(sanity)

                if character.barking == False:

                    BarkTimer(self.game, character, random.choice(character.scaredbarks))

        if self.heals == True:

            healing = random.randint(self.character.healing[0], self.character.healing[1]) * self.multiplier

            for character in characters:

                healing = random.randint(int(self.character.healing[0]), int(self.character.healing[1])) * self.multiplier
                healing, crit = character.calculate_health_healed(healing, self.character)

                if crit:

                    heal_numbers.append('CRIT' + str(int(healing)))

                else:

                    heal_numbers.append(str(int(healing)))

        for effect in self.effects_on_user:

            if effect == 'STRENGTH':
        
                for effect in self.character.effects:
                    if type(effect) == Strength:
                        effect.remove_effect()

                self.character.effects.append(Strength(self.game, self.character))
                self.character.effect_applied_images.append(Strength(self.game, None).image)

            if effect == 'STRENGTH2':
        
                for effect in self.character.effects:
                    if type(effect) == Strength2:
                        effect.remove_effect()

                self.character.effects.append(Strength2(self.game, self.character))
                self.character.effect_applied_images.append(Strength2(self.game, None).image)

            if effect == 'STRENGTH3':
        
                for effect in self.character.effects:
                    if type(effect) == Strength3:
                        effect.remove_effect()

                self.character.effects.append(Strength3(self.game, self.character))
                self.character.effect_applied_images.append(Strength3(self.game, None).image)

            if effect == 'CRIT':
        
                for effect in self.character.effects:
                    if type(effect) == Crit:
                        effect.remove_effect()

                self.character.effects.append(Crit(self.game, self.character))
                self.character.effect_applied_images.append(Crit(self.game, None).image)

            if effect == 'CRIT2':
        
                for effect in self.character.effects:
                    if type(effect) == Crit2:
                        effect.remove_effect()

                self.character.effects.append(Crit2(self.game, self.character))
                self.character.effect_applied_images.append(Crit2(self.game, None).image)

            if effect == 'CRIT3':
        
                for effect in self.character.effects:
                    if type(effect) == Crit3:
                        effect.remove_effect()

                self.character.effects.append(Crit3(self.game, self.character))
                self.character.effect_applied_images.append(Crit3(self.game, None).image)

            if effect == 'PRECISION':
        
                for effect in self.character.effects:
                    if type(effect) == Precision:
                        effect.remove_effect()

                self.character.effects.append(Precision(self.game, self.character))
                self.character.effect_applied_images.append(Precision(self.game, None).image)

            if effect == 'PRECISION2':
        
                for effect in self.character.effects:
                    if type(effect) == Precision2:
                        effect.remove_effect()

                self.character.effects.append(Precision2(self.game, self.character))
                self.character.effect_applied_images.append(Precision2(self.game, None).image)

            if effect == 'PRECISION3':
        
                for effect in self.character.effects:
                    if type(effect) == Precision3:
                        effect.remove_effect()

                self.character.effects.append(Precision3(self.game, self.character))
                self.character.effect_applied_images.append(Precision3(self.game, None).image)

            if effect == 'SPEED':
        
                for effect in self.character.effects:
                    if type(effect) == Speed:
                        effect.remove_effect()

                self.character.effects.append(Speed(self.game, self.character))
                self.character.effect_applied_images.append(Speed(self.game, None).image)

            if effect == 'SPEED2':
        
                for effect in self.character.effects:
                    if type(effect) == Speed2:
                        effect.remove_effect()

                self.character.effects.append(Speed2(self.game, self.character))
                self.character.effect_applied_images.append(Speed2(self.game, None).image)

            if effect == 'SPEED3':
        
                for effect in self.character.effects:
                    if type(effect) == Speed3:
                        effect.remove_effect()

                self.character.effects.append(Speed3(self.game, self.character))
                self.character.effect_applied_images.append(Speed3(self.game, None).image)

            if effect == 'PROTECTION':
        
                for effect in self.character.effects:
                    if type(effect) == Protection:
                        effect.remove_effect()

                self.character.effects.append(Protection(self.game, self.character))
                self.character.effect_applied_images.append(Protection(self.game, None).image)

            if effect == 'PROTECTION2':
        
                for effect in self.character.effects:
                    if type(effect) == Protection2:
                        effect.remove_effect()

                self.character.effects.append(Protection2(self.game, self.character))
                self.character.effect_applied_images.append(Protection2(self.game, None).image)

            if effect == 'PROTECTION3':
        
                for effect in self.character.effects:
                    if type(effect) == Protection3:
                        effect.remove_effect()

                self.character.effects.append(Protection3(self.game, self.character))
                self.character.effect_applied_images.append(Protection3(self.game, None).image)

            if effect == 'DODGE':
        
                for effect in self.character.effects:
                    if type(effect) == Dodge:
                        effect.remove_effect()

                self.character.effects.append(Dodge(self.game, self.character))
                self.character.effect_applied_images.append(Dodge(self.game, None).image)

            if effect == 'DODGE2':
        
                for effect in self.character.effects:
                    if type(effect) == Dodge2:
                        effect.remove_effect()

                self.character.effects.append(Dodge2(self.game, self.character))
                self.character.effect_applied_images.append(Dodge2(self.game, None).image)

            if effect == 'DODGE3':
        
                for effect in self.character.effects:
                    if type(effect) == Dodge3:
                        effect.remove_effect()

                self.character.effects.append(Dodge3(self.game, self.character))
                self.character.effect_applied_images.append(Dodge3(self.game, None).image)


        for character in characters:

            character.effect_applied_images.clear()
            i = 0

            for effect in self.effects_on_hit:
                    
                if (not missed) and (not dodged):

                    if effect == 'BLEEDING':

                        rand = random.randint(0, 100)

                        rand += self.bonus_debuff

                        if rand >= self.character.bleed:
                            self.successful = True
                        else:
                            self.successful = False

                        if self.successful:

                            for effect in character.effects:
                                if type(effect) == Bleeding:
                                    effect.remove_effect()

                            character.effects.append(Bleeding(self.game, character))
                            character.effect_applied_images.append(Bleeding(self.game, None).image)

                        else:

                            character.effect_applied_images.append(p.transform.scale(CROSS, [40, 40]))

                    if effect == 'BLEEDING2':

                        rand = random.randint(0, 100)

                        rand += self.bonus_debuff

                        if rand >= self.character.bleed:
                            self.successful = True
                        else:
                            self.successful = False

                        if self.successful:

                            for effect in character.effects:
                                if type(effect) == Bleeding2:
                                    effect.remove_effect()

                            character.effects.append(Bleeding2(self.game, character))
                            character.effect_applied_images.append(Bleeding2(self.game, None).image)

                        else:

                            character.effect_applied_images.append(p.transform.scale(CROSS, [40, 40]))

                    if effect == 'BLEEDING3':

                        rand = random.randint(0, 100)

                        rand += self.bonus_debuff

                        if rand >= self.character.bleed:
                            self.successful = True
                        else:
                            self.successful = False

                        if self.successful:

                            for effect in character.effects:
                                if type(effect) == Bleeding3:
                                    effect.remove_effect()

                            character.effects.append(Bleeding3(self.game, character))
                            character.effect_applied_images.append(Bleeding3(self.game, None).image)

                        else:

                            character.effect_applied_images.append(p.transform.scale(CROSS, [40, 40]))

                    if effect == 'STUNNING':

                        rand = random.randint(0, 100)

                        rand += self.bonus_stun

                        if rand >= self.character.stun:
                            self.successful = True
                            for effect in character.effects:
                                if type(effect) == StunResist:
                                    self.successful = False
                        else:
                            self.successful = False

                        if self.successful:

                            for effect in character.effects:
                                if type(effect) == Stun:
                                    effect.remove_effect()

                            character.effects.append(Stun(self.game, character))
                            character.effect_applied_images.append(Stun(self.game, None).image)

                        else:

                            character.effect_applied_images.append(p.transform.scale(CROSS, [40, 40]))

                    if effect == 'MARKING':

                        for effect in character.effects:
                            if type(effect) == Mark:
                                effect.remove_effect()

                        character.effects.append(Mark(self.game, character))
                        character.effect_applied_images.append(Mark(self.game, None).image)

                    if effect == 'ANTIDODGE':

                        rand = random.randint(0, 100)

                        rand += self.bonus_debuff

                        if rand >= self.character.debuff:
                            self.successful = True
                        else:
                            self.successful = False

                        if self.successful:

                            for effect in character.effects:
                                if type(effect) == AntiDodge:
                                    effect.remove_effect()

                            character.effects.append(AntiDodge(self.game, character))
                            character.effect_applied_images.append(AntiDodge(self.game, None).image)

                        else:

                            character.effect_applied_images.append(p.transform.scale(CROSS, [40, 40]))

                    if effect == 'ANTIDODGE2':

                        rand = random.randint(0, 100)

                        rand += self.bonus_debuff

                        if rand >= self.character.debuff:
                            self.successful = True
                        else:
                            self.successful = False

                        if self.successful:

                            for effect in character.effects:
                                if type(effect) == AntiDodge2:
                                    effect.remove_effect()

                            character.effects.append(AntiDodge2(self.game, character))
                            character.effect_applied_images.append(AntiDodge2(self.game, None).image)

                        else:

                            character.effect_applied_images.append(p.transform.scale(CROSS, [40, 40]))

                    if effect == 'ANTIDODGE3':

                        rand = random.randint(0, 100)

                        rand += self.bonus_debuff

                        if rand >= self.character.debuff:
                            self.successful = True
                        else:
                            self.successful = False

                        if self.successful:

                            for effect in character.effects:
                                if type(effect) == AntiDodge3:
                                    effect.remove_effect()

                            character.effects.append(AntiDodge3(self.game, character))
                            character.effect_applied_images.append(AntiDodge3(self.game, None).image)

                        else:

                            character.effect_applied_images.append(p.transform.scale(CROSS, [40, 40]))

                    if effect == 'BLINDING':

                        rand = random.randint(0, 100)

                        rand += self.bonus_debuff

                        if rand >= self.character.debuff:
                            self.successful = True
                        else:
                            self.successful = False

                        if self.successful:

                            for effect in character.effects:
                                if type(effect) == Blindness:
                                    effect.remove_effect()

                            character.effects.append(Blindness(self.game, character))
                            character.effect_applied_images.append(Blindness(self.game, None).image)

                        else:

                            character.effect_applied_images.append(p.transform.scale(CROSS, [40, 40]))

                    if effect == 'BLINDING2':

                        rand = random.randint(0, 100)

                        rand += self.bonus_debuff

                        if rand >= self.character.debuff:
                            self.successful = True
                        else:
                            self.successful = False

                        if self.successful:

                            for effect in character.effects:
                                if type(effect) == Blindness2:
                                    effect.remove_effect()

                            character.effects.append(Blindness2(self.game, character))
                            character.effect_applied_images.append(Blindness2(self.game, None).image)

                        else:

                            character.effect_applied_images.append(p.transform.scale(CROSS, [40, 40]))

                    if effect == 'BLINDING3':

                        rand = random.randint(0, 100)

                        rand += self.bonus_debuff

                        if rand >= self.character.debuff:
                            self.successful = True
                        else:
                            self.successful = False

                        if self.successful:

                            for effect in character.effects:
                                if type(effect) == Blindness3:
                                    effect.remove_effect()

                            character.effects.append(Blindness3(self.game, character))
                            character.effect_applied_images.append(Blindness3(self.game, None).image)

                        else:

                            character.effect_applied_images.append(p.transform.scale(CROSS, [40, 40]))

                    if effect == 'BURNING':


                        rand = random.randint(0, 100)

                        rand += self.bonus_debuff

                        if rand >= self.character.fire:
                            self.successful = True
                        else:
                            self.successful = False

                        if self.successful:

                            for effect in character.effects:
                                if type(effect) == Burning:
                                    effect.remove_effect()

                            character.effects.append(Burning(self.game, character))
                            character.effect_applied_images.append(Burning(self.game, None).image)

                        else:

                            character.effect_applied_images.append(p.transform.scale(CROSS, [40, 40]))

                    if effect == 'BURNING2':

                        rand = random.randint(0, 100)

                        rand += self.bonus_debuff

                        if rand >= self.character.fire:
                            self.successful = True
                        else:
                            self.successful = False

                        if self.successful:

                            for effect in character.effects:
                                if type(effect) == Burning2:
                                    effect.remove_effect()

                            character.effects.append(Burning2(self.game, character))
                            character.effect_applied_images.append(Burning2(self.game, None).image)

                        else:

                            character.effect_applied_images.append(p.transform.scale(CROSS, [40, 40]))

                    if effect == 'BURNING3':

                        rand = random.randint(0, 100)

                        rand += self.bonus_debuff

                        if rand >= self.character.fire:
                            self.successful = True
                        else:
                            self.successful = False

                        if self.successful:

                            for effect in character.effects:
                                if type(effect) == Burning3:
                                    effect.remove_effect()

                            character.effects.append(Burning3(self.game, character))
                            character.effect_applied_images.append(Burning3(self.game, None).image)

                        else:

                            character.effect_applied_images.append(p.transform.scale(CROSS, [40, 40]))

                    if effect == 'STRENGTH':
        
                        for effect in character.effects:
                            if type(effect) == Strength:
                                effect.remove_effect()

                        character.effects.append(Strength(self.game, character))
                        character.effect_applied_images.append(Strength(self.game, None).image)

                    if effect == 'STRENGTH2':
        
                        for effect in character.effects:
                            if type(effect) == Strength2:
                                effect.remove_effect()

                        character.effects.append(Strength2(self.game, character))
                        character.effect_applied_images.append(Strength2(self.game, None).image)

                    if effect == 'STRENGTH3':
        
                        for effect in character.effects:
                            if type(effect) == Strength3:
                                effect.remove_effect()

                        character.effects.append(Strength3(self.game, character))
                        character.effect_applied_images.append(Strength3(self.game, None).image)

                    if effect == 'DODGE':
        
                        for effect in character.effects:
                            if type(effect) == Dodge:
                                effect.remove_effect()

                        character.effects.append(Dodge(self.game, character))
                        character.effect_applied_images.append(Dodge(self.game, None).image)

                    if effect == 'DODGE2':
        
                        for effect in character.effects:
                            if type(effect) == Dodge2:
                                effect.remove_effect()

                        character.effects.append(Dodge2(self.game, character))
                        character.effect_applied_images.append(Dodge2(self.game, None).image)

                    if effect == 'DODGE3':
        
                        for effect in character.effects:
                            if type(effect) == Dodge3:
                                effect.remove_effect()

                        character.effects.append(Dodge3(self.game, character))
                        character.effect_applied_images.append(Dodge3(self.game, None).image)

                    if effect == 'CRIT':
        
                        for effect in character.effects:
                            if type(effect) == Crit:
                                effect.remove_effect()

                        character.effects.append(Crit(self.game, character))
                        character.effect_applied_images.append(Crit(self.game, None).image)

                    if effect == 'CRIT2':
        
                        for effect in character.effects:
                            if type(effect) == Crit2:
                                effect.remove_effect()

                        character.effects.append(Crit2(self.game, character))
                        character.effect_applied_images.append(Crit2(self.game, None).image)

                    if effect == 'CRIT3':
        
                        for effect in character.effects:
                            if type(effect) == Crit3:
                                effect.remove_effect()

                        character.effects.append(Crit3(self.game, character))
                        character.effect_applied_images.append(Crit3(self.game, None).image)

                    if effect == 'PRECISION':
        
                        for effect in character.effects:
                            if type(effect) == Precision:
                                effect.remove_effect()

                        character.effects.append(Precision(self.game, character))
                        character.effect_applied_images.append(Precision(self.game, None).image)

                    if effect == 'PRECISION2':
        
                        for effect in character.effects:
                            if type(effect) == Precision2:
                                effect.remove_effect()

                        character.effects.append(Precision2(self.game, character))
                        character.effect_applied_images.append(Precision2(self.game, None).image)

                    if effect == 'PRECISION3':
        
                        for effect in character.effects:
                            if type(effect) == Precision3:
                                effect.remove_effect()

                        character.effects.append(Precision3(self.game, character))
                        character.effect_applied_images.append(Precision3(self.game, None).image)

                    if effect == 'PROTECTION':
        
                        for effect in character.effects:
                            if type(effect) == Protection:
                                effect.remove_effect()

                        character.effects.append(Protection(self.game, character))
                        character.effect_applied_images.append(Protection(self.game, None).image)

                    if effect == 'PROTECTION2':
        
                        for effect in character.effects:
                            if type(effect) == Protection2:
                                effect.remove_effect()

                        character.effects.append(Protection2(self.game, character))
                        character.effect_applied_images.append(Protection2(self.game, None).image)

                    if effect == 'PROTECTION3':
        
                        for effect in character.effects:
                            if type(effect) == Protection3:
                                effect.remove_effect()

                        character.effects.append(Protection3(self.game, character))
                        character.effect_applied_images.append(Protection3(self.game, None).image)

                    if effect == 'SPEED':
        
                        for effect in character.effects:
                            if type(effect) == Speed:
                                effect.remove_effect()

                        character.effects.append(Speed(self.game, character))
                        character.effect_applied_images.append(Speed(self.game, None).image)

                    if effect == 'SPEED2':
        
                        for effect in character.effects:
                            if type(effect) == Speed2:
                                effect.remove_effect()

                        character.effects.append(Speed2(self.game, character))
                        character.effect_applied_images.append(Speed2(self.game, None).image)

                    if effect == 'SPEED3':
        
                        for effect in character.effects:
                            if type(effect) == Speed3:
                                effect.remove_effect()

                        character.effects.append(Speed3(self.game, character))
                        character.effect_applied_images.append(Speed3(self.game, None).image)

                    if effect == 'WEAKNESS':

                        rand = random.randint(0, 100)

                        rand += self.bonus_debuff

                        if rand >= self.character.debuff:
                            self.successful = True
                        else:
                            self.successful = False

                        if self.successful:

                            for effect in character.effects:
                                if type(effect) == Weakness:
                                    effect.remove_effect()

                            character.effects.append(Weakness(self.game, character))
                            character.effect_applied_images.append(Weakness(self.game, None).image)

                        else:

                            character.effect_applied_images.append(p.transform.scale(CROSS, [40, 40]))

                    if effect == 'WEAKNESS2':

                        rand = random.randint(0, 100)

                        rand += self.bonus_debuff

                        if rand >= self.character.debuff:
                            self.successful = True
                        else:
                            self.successful = False

                        if self.successful:

                            for effect in character.effects:
                                if type(effect) == Weakness2:
                                    effect.remove_effect()

                            character.effects.append(Weakness2(self.game, character))
                            character.effect_applied_images.append(Weakness2(self.game, None).image)

                        else:

                            character.effect_applied_images.append(p.transform.scale(CROSS, [40, 40]))

                    if effect == 'WEAKNESS3':

                        rand = random.randint(0, 100)

                        rand += self.bonus_debuff

                        if rand >= self.character.debuff:
                            self.successful = True
                        else:
                            self.successful = False

                        if self.successful:

                            for effect in character.effects:
                                if type(effect) == Weakness3:
                                    effect.remove_effect()

                            character.effects.append(Weakness3(self.game, character))
                            character.effect_applied_images.append(Weakness3(self.game, None).image)

                        else:

                            character.effect_applied_images.append(p.transform.scale(CROSS, [40, 40]))

                    if effect == 'SLOWNESS':

                        rand = random.randint(0, 100)

                        rand += self.bonus_debuff

                        if rand >= self.character.debuff:
                            self.successful = True
                        else:
                            self.successful = False

                        if self.successful:

                            for effect in character.effects:
                                if type(effect) == Slowness:
                                    effect.remove_effect()

                            character.effects.append(Slowness(self.game, character))
                            character.effect_applied_images.append(Slowness(self.game, None).image)

                        else:

                            character.effect_applied_images.append(p.transform.scale(CROSS, [40, 40]))

                    if effect == 'SLOWNESS2':

                        rand = random.randint(0, 100)

                        rand += self.bonus_debuff

                        if rand >= self.character.debuff:
                            self.successful = True
                        else:
                            self.successful = False

                        if self.successful:

                            for effect in character.effects:
                                if type(effect) == Slowness2:
                                    effect.remove_effect()

                            character.effects.append(Slowness2(self.game, character))
                            character.effect_applied_images.append(Slowness2(self.game, None).image)

                        else:

                            character.effect_applied_images.append(p.transform.scale(CROSS, [40, 40]))

                    if effect == 'SLOWNESS3':

                        rand = random.randint(0, 100)

                        rand += self.bonus_debuff

                        if rand >= self.character.debuff:
                            self.successful = True
                        else:
                            self.successful = False

                        if self.successful:

                            for effect in character.effects:
                                if type(effect) == Slowness3:
                                    effect.remove_effect()

                            character.effects.append(Slowness3(self.game, character))
                            character.effect_applied_images.append(Slowness3(self.game, None).image)

                        else:

                            character.effect_applied_images.append(p.transform.scale(CROSS, [40, 40]))

                    if effect == 'BROKEN':

                        rand = random.randint(0, 100)

                        rand += self.bonus_debuff

                        if rand >= self.character.debuff:
                            self.successful = True
                        else:
                            self.successful = False

                        if self.successful:

                            for effect in character.effects:
                                if type(effect) == BrokenArmour:
                                    effect.remove_effect()

                            character.effects.append(BrokenArmour(self.game, character))
                            character.effect_applied_images.append(BrokenArmour(self.game, None).image)

                        else:

                            character.effect_applied_images.append(p.transform.scale(CROSS, [40, 40]))

                    if effect == 'BROKEN2':

                        rand = random.randint(0, 100)

                        rand += self.bonus_debuff

                        if rand >= self.character.debuff:
                            self.successful = True
                        else:
                            self.successful = False

                        if self.successful:

                            for effect in character.effects:
                                if type(effect) == BrokenArmour2:
                                    effect.remove_effect()

                            character.effects.append(BrokenArmour2(self.game, character))
                            character.effect_applied_images.append(BrokenArmour2(self.game, None).image)

                        else:

                            character.effect_applied_images.append(p.transform.scale(CROSS, [40, 40]))

                    if effect == 'BROKEN3':

                        rand = random.randint(0, 100)

                        rand += self.bonus_debuff

                        if rand >= self.character.debuff:
                            self.successful = True
                        else:
                            self.successful = False

                        if self.successful:

                            for effect in character.effects:
                                if type(effect) == BrokenArmour3:
                                    effect.remove_effect()

                            character.effects.append(BrokenArmour3(self.game, character))
                            character.effect_applied_images.append(BrokenArmour3(self.game, None).image)

                        else:

                            character.effect_applied_images.append(p.transform.scale(CROSS, [40, 40]))
                i += 1

        for tile in self.game.menus['BATTLE'].tiles:
            tile.being_targeted = False

        for menu in self.game.menus.values():
            menu.update_images()

        if not dodged and not missed:

            self.sound.play()

        else:

            sound = p.mixer.Sound(MISS_SOUND)
            sound.play()

        self.game.play_combat_animations(self.character, characters, damage_numbers, heal_numbers, sanity_damage_numbers, sanity_heal_numbers)

        ShowSkillEffectivenessTimer(self.game, self.character, self.text)
        
# this skill is used when an enemy wants to move to another tile
class EnemyMove(EnemySkill):

    def __init__(self, game, character):
        super().__init__(game, character)

        self.sound = p.mixer.Sound(MOVE_SOUND)

    def use_skill(self, target_tile):

        menu = self.game.menus['BATTLE']

        character = self.game.selected_character

        # makes the tile this character is standing in not obstructed, as this character is about to move away from it

        for tile in menu.tiles:
            if tile.grid_pos == character.grid_pos:
                tile.obstructed = False

        # changes the direction this character is facing dependent on whether the x component of the distance is positive or negative

        distance = vec(target_tile) - vec(character.grid_pos)
        if distance[0] > 0:
            character.flipped = False
        elif distance[0] < 0:
            character.flipped = True

        # changes the image to be flipped to the new direction

        character.image = p.transform.flip(character.images[character.current_frame], character.flipped, False)

        # the characters position is changed

        character.grid_pos = target_tile

        self.sound.play()

class EnemySkip(EnemySkill):

    def __init__(self, game, character):
        super().__init__(game, character)

    def use_skill(self):

        NextTurnTimer(self.game, self.character)

class HeroSkill(Skill):

    def __init__(self, game, character):
        super().__init__(game, character)

        self.spritesheet = self.character.spritesheet

        self.targets_enemies = True

class HeroRetreat(Skill):

    def __init__(self, game, character):
        super().__init__(game, character)

        self.image = Sprite(MENU_SPRITESHEETS['ICON_SPRITESHEET'], scale = 8).get_sprite(140, 0, 20, 20)

    def update(self):
        
        if self == self.game.selected_character.selected_skill:
            self.use_skill()

    def use_skill(self):

        self.game.battle.end_battle()

# pretty much the same as EnemyMove but also updates the battle map to show which tiles can be moved to whenever this is selected

class HeroMove(Skill):

    def __init__(self, game, character):
        super().__init__(game, character)

        self.image = Sprite(MENU_SPRITESHEETS['ICON_SPRITESHEET'], scale = 8).get_sprite(100, 0, 20, 20)

        self.sound = p.mixer.Sound(MOVE_SOUND)

    def update(self):

        # if this skill is selected

        if self == self.game.selected_character.selected_skill:
            menu = self.game.menus['BATTLE']

            # for every tile
            for tile in menu.tiles:

                # if the distance betwen this tile and the character trying to move is smaller than the characters mobility stat
                distance = vec(tile.grid_pos[0], tile.grid_pos[1]) - vec(self.game.selected_character.grid_pos[0], self.game.selected_character.grid_pos[1])
                if distance.length() < self.game.selected_character.mobility:
                    # the tile is traversable
                    tile.traversable = True
                else:
                    # otherwise it isnt
                    tile.traversable = False

    def use_skill(self, target_tile):

        menu = self.game.menus['BATTLE']

        character = self.game.selected_character

        for tile in menu.tiles:
            tile.being_targeted = False
            if tile.grid_pos == character.grid_pos:
                tile.obstructed = False

        distance = vec(target_tile.grid_pos) - vec(character.grid_pos)
        if distance[0] > 0:
            character.flipped = False
        elif distance[0] < 0:
            character.flipped = True

        character.image = p.transform.flip(character.images[character.current_frame], character.flipped, False)

        character.grid_pos = target_tile.grid_pos
        character.has_moved = True
        character.selected_skill = None

        menu = self.game.menus['BOTTOM']
        menu.update_images()

        self.sound.play()
        

class HeroSkip(Skill):

    def __init__(self, game, character):
        super().__init__(game, character)

        self.image = Sprite(MENU_SPRITESHEETS['ICON_SPRITESHEET'], scale = 8).get_sprite(120, 0, 20, 20)

    def update(self):
        
        if self == self.game.selected_character.selected_skill:
            self.use_skill()

    def use_skill(self):

        if self.character.has_used_skill == False:

            self.game.battle.start_next_character_turn()


