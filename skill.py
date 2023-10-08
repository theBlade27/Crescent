import pygame as p
from sprite import *
from settings import *
from character import *
from wait import *
import random
vec = p.math.Vector2

class Skill(p.sprite.Sprite):

    def __init__(self, game, character):

        self.groups = game.skills_group
        p.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.name = ''
        self.desc = ''
        self.character = character
        self.targets = []

        self.range = [0, 0]
        self.multiplier = 1
        self.targets_all_in_range = False
        self.splash = 0
        self.heals = False
        self.sanity_recovering = False
        self.sanity_reducing = False
        self.debuffing = False

        self.effects_on_hit = []
        self.effects_on_user = []

        self.bonus_stun = 0
        self.bonus_debuff = 0

        self.bonus_crit = 0

        self.bonus_precision = 0

        self.combat_animation = p.Surface((1, 1))
        self.combat_animation.fill(BLACK)

    def update(self):

        if self == self.game.selected_character.selected_skill:
            menu = self.game.menus['BATTLE']
            for tile in menu.tiles:
                distance = vec(tile.grid_pos[0], tile.grid_pos[1]) - vec(self.game.selected_character.grid_pos[0], self.game.selected_character.grid_pos[1])
                if distance.length() >= self.range[0] and distance.length() < self.range[1]:
                    tile.targetable = True

    def use_skill(self, tiles):

        self.targets = []

        self.text = ''

        crit = False
        dodged = False
        missed = False

        damage_numbers = []
        heal_numbers = []
        sanity_heal_numbers = []
        sanity_damage_numbers = []

        for tile in tiles:

            for character in self.game.characters:
                if character.grid_pos == tile.grid_pos:
                    self.targets.append(character)

        if self.heals == False:

            for target in self.targets:
                damage = random.randint(int(self.character.damage[0]), int(self.character.damage[1])) * self.multiplier
                damage, crit, missed, dodged = target.calculate_damage_dealt(damage, self.character)
                if crit:
                    self.character.calculate_sanity_increase(5)

                if not missed and not dodged:

                    if crit:

                        damage_numbers.append('CRIT' + str(damage))

                    else:

                        damage_numbers.append(damage)

                elif missed:

                    damage_numbers.append('MISSED')

                else:

                    damage_numbers.append('DODGED')

        if self.sanity_recovering == True:

            for target in self.targets:
                sanity_recovery = random.randint(self.character.sanity_recovery_skills[0], self.character.sanity_recovery_skills[1]) * self.multiplier
                sanity = target.calculate_sanity_increase(sanity_recovery)

                sanity_heal_numbers.append(sanity)

        if self.sanity_reducing == True:

            for target in self.targets:
                sanity_reduction = random.randint(self.character.sanity_reduction_skills[0], self.character.sanity_reduction_skills[1]) * self.multiplier
                sanity = target.calculate_sanity_decrease(sanity_reduction)

                sanity_damage_numbers.append(sanity)

        if self.heals == True:

            for target in self.targets:
                healing = random.randint(self.character.healing[0], self.character.healing[1]) * self.multiplier
                healing, crit = target.calculate_health_healed(healing, self.character)
                if crit:
                    self.character.calculate_sanity_increase(5)
                    target.calculate_sanity_increase(5)

                if crit:

                    heal_numbers.append('CRIT' + str(healing))

                else:

                    heal_numbers.append(healing)


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



        for target in self.targets:

            target.effect_applied_images.clear()

            i = 0

            for effect in self.effects_on_hit:
                    
                if not missed and not dodged:
                
                    if effect == 'BURNING':


                        rand = random.randint(0, 100)

                        rand += self.bonus_debuff

                        if rand >= self.character.fire:
                            self.successful = True
                        else:
                            self.successful = False

                        if self.successful:

                            for effect in target.effects:
                                if type(effect) == Burning:
                                    effect.remove_effect()

                            target.effects.append(Burning(self.game, target))
                            target.effect_applied_images.append(Burning(self.game, None).image)

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



                i += 1

        for tile in self.game.menus['BATTLE'].tiles:
            tile.being_targeted = False

        for menu in self.game.menus.values():
            menu.update_images()

        self.character.has_used_skill = True

        if not dodged and not missed:

            self.sound.play()

        else:

            sound = p.mixer.Sound(MISS_SOUND)
            sound.play()

        self.game.play_combat_animations(self.character, self.targets, damage_numbers, heal_numbers, sanity_damage_numbers, sanity_heal_numbers)

        ShowSkillEffectivenessTimer(self.game, self.character, self.text)


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

                damage = random.randint(self.character.damage[0], self.character.damage[1]) * self.multiplier
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

                if not missed and not dodged:

                    if crit:

                        damage_numbers.append('CRIT' + str(damage))

                    else:

                        damage_numbers.append(damage)

                elif missed:

                    damage_numbers.append('MISSED')

                else:

                    damage_numbers.append('DODGED')

                

        if self.sanity_recovering == True:

            for character in characters:
                sanity_recovery = random.randint(self.character.sanity_recovery_skills[0], self.character.sanity_recovery_skills[1]) * self.multiplier
                sanity = character.calculate_sanity_increase(sanity_recovery)

                sanity_heal_numbers.append(sanity)

        if self.sanity_reducing == True:

            for character in characters:
                sanity_reduction = random.randint(self.character.sanity_reduction_skills[0], self.character.sanity_reduction_skills[1]) * self.multiplier
                sanity = character.calculate_sanity_decrease(sanity_reduction)

                sanity_damage_numbers.append(sanity)

        if self.heals == True:

            healing = random.randint(self.character.healing[0], self.character.healing[1]) * self.multiplier

            for character in characters:

                healing = random.randint(self.character.healing[0], self.character.healing[1]) * self.multiplier
                healing = character.calculate_health_healed(healing, self.character)

                if crit:

                    heal_numbers.append('CRIT' + str(healing))

                else:

                    heal_numbers.append(healing)

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

        for character in characters:

            character.effect_applied_images.clear()
            i = 0

            for effect in self.effects_on_hit:
                    
                if not missed and not dodged:
                
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
        

class EnemyMove(EnemySkill):

    def __init__(self, game, character):
        super().__init__(game, character)

        self.sound = p.mixer.Sound(MOVE_SOUND)

    def use_skill(self, target_tile):

        menu = self.game.menus['BATTLE']

        character = self.game.selected_character

        for tile in menu.tiles:
            if tile.grid_pos == character.grid_pos:
                tile.obstructed = False

        distance = vec(target_tile) - vec(character.grid_pos)
        if distance[0] > 0:
            character.flipped = False
        elif distance[0] < 0:
            character.flipped = True

        character.image = p.transform.flip(character.images[character.current_frame], character.flipped, False)

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

class HeroMove(Skill):

    def __init__(self, game, character):
        super().__init__(game, character)

        self.image = Sprite(MENU_SPRITESHEETS['ICON_SPRITESHEET'], scale = 8).get_sprite(100, 0, 20, 20)

        self.sound = p.mixer.Sound(MOVE_SOUND)

    def update(self):

        if self == self.game.selected_character.selected_skill:
            menu = self.game.menus['BATTLE']
            for tile in menu.tiles:
                distance = vec(tile.grid_pos[0], tile.grid_pos[1]) - vec(self.game.selected_character.grid_pos[0], self.game.selected_character.grid_pos[1])
                if distance.length() < self.game.selected_character.mobility:
                    tile.traversable = True
                else:
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


