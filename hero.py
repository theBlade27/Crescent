import pygame as p
from sprite import *
from settings import *
from character import *
from explorationCharacter import *
from effect import *
from skill import *
from hero_skills import *

class Hero(Character):

    def __init__(self, game, type, pos):
        super().__init__(game, type)

        self.exploration_character = ExplorationCharacter(self.game, self.type, pos, self)

        self.barking = False

        if self.type == 'BLADE':

            self.deathsdoorbarks = [
                'IS IT FINALLY OVER?',
                'BUT I\'M NOT DONE YET...'
            ]

            self.killbarks = [
                'YOUR KIND IS NO LONGER WELCOME HERE.',
                'BEGONE, FIEND.'
            ]

            self.healbarks = [
                'IT\'S NOT OVER YET.'
            ]

            self.healerbarks = [
                'STAY WITH ME FRIEND\nOUR TASK IS NOT YET COMPLETE.'
            ]

            self.critbarks = [
                'WE CAN DO THIS!',
                'THE LIGHT HAS CLAIMED YOU!'
            ]

            self.scaredbarks = [
                'IT... IT\'S HOPELESS...'
            ]
            
            self.actoutbarks = [
                'YOU...\nYOU\'RE ONE OF THEM!'
            ]

            self.meltdownbarks = [
                'THERE\'S NO HOPE.'
            ]

            self.giveupbarks = [
                'WHAT\'S THE POINT.'
            ]
            

            self.name = 'BLADE'
            self.mobility = 3
            self.bleed = 60
            self.venom = 60
            self.fire = 60
            self.death = 66
            self.stun = 70
            self.debuff = 60
            self.equipment = [None, None, None]
            self.frontliner = True

            self.skills = [
                Vanquish(self.game, self),
                Command(self.game, self),
                SteelTempest(self.game, self),
                FalseHopes(self.game, self),
                HeroMove(self.game, self),
                HeroSkip(self.game, self),
                HeroRetreat(self.game, self),
                BladeActOut(self.game, self)

            ]

            self.starting_grid_pos = [4, 1]

        if self.type == 'ARCANE':

            self.deathsdoorbarks = [
                'NO NOT YET!\nIV\'E SO MUCH TO LIVE FOR!'
            ]

            self.killbarks = [
                'MORE ASHES SCATTER THE LAND.',
                'SOME CANNOT BE REASONED WITH.'
            ]

            self.healbarks = [
                'THANKS FRIEND :)'
            ]

            self.healerbarks = [
                'SHHH SHHH....\nYOU\'RE OKAY :)',
            ]

            self.critbarks = [
                'DO YOU FEEL IT?\nDO YOU FEEL THE POWER!',
                'HAHAHAH BUUUURRNNNN!!!'
            ]

            self.scaredbarks = [
                'NO... NOT AGAIN...'
            ]

            self.actoutbarks = [
                'GET. AWAY. FROM. ME.'
            ]

            self.meltdownbarks = [
                '(STARTS SOBBING)'
            ]

            self.giveupbarks = [
                'I... CAN\'T'
            ]

            
            self.name = 'ARCANE'
            self.mobility = 5
            self.bleed = 30
            self.venom = 30
            self.fire = 30
            self.death = 66
            self.stun = 50
            self.debuff = 40
            self.equipment = [None, None, None]
            self.frontliner = False

            self.skills = [
                AzureEruption(self.game, self),
                Illuminate(self.game, self),
                ArcaneAssault(self.game, self),
                Rekindle(self.game, self),
                HeroMove(self.game, self),
                HeroSkip(self.game, self),
                HeroRetreat(self.game, self),
                ArcaneActOut(self.game, self)
            ]

            self.starting_grid_pos = [0, 0]

        self.current_sanity = 100
        self.max_sanity = 100

        self.current_experience = 0
        self.max_experience = 100

        self.selected_skill = None
        self.has_used_skill = False
        self.has_moved = False

        self.insane = False
        self.meltingdown = False
        self.givingup = False

        self.armour_level = 0
        self.weapon_level = 0

        self.max_health = ARMOUR_VALUES[self.type][self.armour_level][0]
        self.protection = ARMOUR_VALUES[self.type][self.armour_level][1]
        self.speed = ARMOUR_VALUES[self.type][self.armour_level][2]
        self.agility = ARMOUR_VALUES[self.type][self.armour_level][3]
        self.healing[0] = ARMOUR_VALUES[self.type][self.armour_level][4]
        self.healing[1] = ARMOUR_VALUES[self.type][self.armour_level][5]
        self.sanity_recovery_skills[0] = ARMOUR_VALUES[self.type][self.armour_level][4]
        self.sanity_recovery_skills[1] = ARMOUR_VALUES[self.type][self.armour_level][5]

        self.damage[0] = WEAPON_VALUES[self.type][self.weapon_level][0]
        self.damage[1] = WEAPON_VALUES[self.type][self.weapon_level][1]
        self.precision = WEAPON_VALUES[self.type][self.weapon_level][2]
        self.crit = WEAPON_VALUES[self.type][self.weapon_level][3]

        self.sanity_reduction_skills = [8, 15]

        self.current_health = self.max_health

        self.effects = [
            Satiated(self.game, self)
        ]

    def update(self):
            

        if self.has_used_skill == False:

            pressed_keys = p.key.get_pressed()
            if pressed_keys[p.K_1]:
                self.selected_skill = self.skills[0]
                self.game.menus['BOTTOM'].update_images()
            if pressed_keys[p.K_2]:
                self.selected_skill = self.skills[1]
                self.game.menus['BOTTOM'].update_images()
            if pressed_keys[p.K_3]:
                self.selected_skill = self.skills[2]
                self.game.menus['BOTTOM'].update_images()
            if pressed_keys[p.K_4]:
                self.selected_skill = self.skills[3]
                self.game.menus['BOTTOM'].update_images()
            if pressed_keys[p.K_5]:
                if self.has_moved == False:
                    self.selected_skill = self.skills[4]
                    self.game.menus['BOTTOM'].update_images()
            if pressed_keys[p.K_6]:
                self.selected_skill = self.skills[5]
                self.game.menus['BOTTOM'].update_images()

        self.play_animations()

    def play_animations(self):

        now = p.time.get_ticks()

        if now - self.last_update > 1000:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.image = p.transform.flip(self.images[self.current_frame], self.flipped, False)
            self.combat_image = self.combat_images[self.current_frame]

    def start_turn(self):

        self.effect_applied_images.clear()

        self.selected_skill = None

        self.has_moved = False
        self.has_used_skill = False

        self.game.selected_character = self

        if self.current_health == 0:
            self.deaths_door = True
        else:
            self.deaths_door = False

        if self.deaths_door == True:
            self.effects.append(DeathsDoor(self.game, self))
        else:
            for effect in self.effects:
                if type(effect) == DeathsDoor:
                    effect.remove_effect()

        if self.current_sanity == 0:
            self.insane = True
        
        if self.insane == True:
            if self.current_sanity > 66:
                self.insane = False

        if self.insane == True:
            self.effects.append(Insanity(self.game, self))
        else:
            for effect in self.effects:
                if type(effect) == Insanity:
                    effect.remove_effect()

        current_health = self.current_health

        for effect in self.effects:
            effect.tick()

        change_in_health = current_health - self.current_health

        sound = p.mixer.Sound(NEXT_SOUND)
        sound.play()

        for menu in self.game.menus.values():

            menu.update_images()

        if self.insane == False:


            if self.stunned == False:

                rand = random.randint(0, 100)

                if rand < self.current_sanity:

                    PlayerTurnTimer(self.game, self, change_in_health)

                else:

                    self.game.actingout = False
                    self.meltingdown = True
                    PlayerTurnTimer(self.game, self, change_in_health)

            else:

                StunnedTimer(self.game, self)

        else:

            if self.stunned == False:

                rand = random.randint(1, 6)

                if rand == 1:

                    hero_party_length = 0

                    for hero in self.game.hero_party:
                        if hero != None:
                            hero_party_length += 1

                    if hero_party_length > 1:

                        self.game.actingout = True
                        CalculateSkillTimer(self.game, self, change_in_health)

                    else:

                        self.game.actingout = False
                        self.meltingdown = True
                        PlayerTurnTimer(self.game, self, change_in_health)

                elif rand == 2 or rand == 3:

                    self.game.actingout = False
                    self.meltingdown = True
                    PlayerTurnTimer(self.game, self, change_in_health)

                elif rand == 4:

                    self.game.actingout = True
                    self.givingup = True
                    PlayerTurnTimer(self.game, self, change_in_health)

                else:
                    self.game.actingout = False
                    PlayerTurnTimer(self.game, self, change_in_health)

            else:

                StunnedTimer(self.game, self)

        for menu in self.game.menus.values():
            menu.update_images()

    def giveup(self):

        rand = random.randint(8, 15)
        sanity_reduction = rand
        sanity = int(self.calculate_sanity_decrease(sanity_reduction))

        self.selected_skill = EnemySkip(self.game, self)

        if self.barking == False:

            BarkTimer(self.game, self, random.choice(self.giveupbarks))

        applied_debuff = random.randint(1, 4)

        successful = False

        if applied_debuff <= 3:
                
            rand = random.randint(0, 100)

            if rand >= 50:
                successful = True

            if successful:

                if applied_debuff == 1:

                    for effect in self.effects:
                        if type(effect) == Blindness:
                            effect.remove_effect()

                    self.effects.append(Blindness(self.game, self))

                if applied_debuff == 2:

                    for effect in self.effects:
                        if type(effect) == Weakness:
                            effect.remove_effect()

                    self.effects.append(Weakness(self.game, self))

                if applied_debuff == 3:

                    for effect in self.effects:
                        if type(effect) == BrokenArmour:
                            effect.remove_effect()

                    self.effects.append(BrokenArmour(self.game, self))

        for menu in self.game.menus.values():
            menu.update_images()

    def meltdown(self):

        if self.barking == False:

            BarkTimer(self.game, self, random.choice(self.meltdownbarks))

        for hero in self.game.hero_party:
            if hero != None:
                rand = random.randint(8, 15)
                sanity_reduction = rand
                sanity = int(hero.calculate_sanity_decrease(sanity_reduction))

                applied_debuff = random.randint(1, 4)

                successful = False

                if applied_debuff <= 3:
                
                    rand = random.randint(0, 100)

                    if rand >= 50:
                        successful = True

                    if successful:

                        if applied_debuff == 1:

                            for effect in hero.effects:
                                if type(effect) == Blindness:
                                    effect.remove_effect()

                            hero.effects.append(Blindness(self.game, hero))

                        if applied_debuff == 2:

                            for effect in hero.effects:
                                if type(effect) == Weakness:
                                    effect.remove_effect()

                            hero.effects.append(Weakness(self.game, hero))

                        if applied_debuff == 3:

                            for effect in hero.effects:
                                if type(effect) == BrokenArmour:
                                    effect.remove_effect()

                            hero.effects.append(BrokenArmour(self.game, hero))

        for menu in self.game.menus.values():
            menu.update_images()

    def calculate_skill(self):

        self.find_ideal_target()

        if self.ideal_target_in_range == False or self.can_use_skill == False:

            HeroIsMovingTimer(self.game, self)

        else:

            self.determine_skill()

    def find_ideal_target(self):

        menu = self.game.menus['BATTLE']

        self.distance_from_ideal_target = vec(100, 100)

        for hero in menu.heroes:

            if hero != self:
                distance = vec(hero.grid_pos) - vec(self.grid_pos)
                if distance.length() < self.distance_from_ideal_target.length():
                    self.distance_from_ideal_target = distance
                    self.ideal_target = hero

        self.check_usable(self.grid_pos)

    def check_usable(self, tile):

        self.can_use_skill = False
        menu = self.game.menus['BATTLE']
        self.ideal_target_in_range = False

        skill = self.skills[7]

        distance = vec(self.ideal_target.grid_pos) - vec(tile)
        if distance.length() >= skill.range[0] and distance.length() < skill.range[1]:
            self.can_use_skill = True
            self.ideal_target_in_range = True

        if self.ideal_target_in_range == False:
            for hero in menu.heroes:
                if hero != self:
                    distance = vec(hero.grid_pos) - vec(tile)
                    if distance.length() >= skill.range[0] and distance.length() < skill.range[1]:
                        self.can_use_skill = True

    def move_tile(self):

        menu = self.game.menus['BATTLE']
        self.selected_skill = EnemyMove(self.game, self)
        
        if self.frontliner == True:
        
            closest_tile = vec(100, 100)
            smallest_distance_from_target = vec(100, 100)
            distance_from_target = vec(0, 0)

            for x in range(self.mobility, ((-self.mobility) - 1), -1):

                for y in range(self.mobility, ((-self.mobility) - 1), -1):

                    temp_grid_pos = self.grid_pos + vec(x, y)

                    distance_from_target = self.ideal_target.grid_pos - temp_grid_pos
                    if distance_from_target.length() < smallest_distance_from_target.length():
                        for tile in menu.tiles:
                            if tile.grid_pos == temp_grid_pos:
                                menu.check_obstructed()
                                if tile.obstructed == False:
                                    self.check_usable(tile.grid_pos)
                                    if self.can_use_skill:
                                        closest_tile = temp_grid_pos
                                        smallest_distance_from_target = distance_from_target 

            if self.can_use_skill == False:

                for x in range(self.mobility, ((-self.mobility) - 1), -1):

                    for y in range(self.mobility, ((-self.mobility) - 1), -1):

                        temp_grid_pos = self.grid_pos + vec(x, y)

                        distance_from_target = self.ideal_target.grid_pos - temp_grid_pos
                        if distance_from_target.length() < smallest_distance_from_target.length():
                            for tile in menu.tiles:
                                if tile.grid_pos == temp_grid_pos:
                                    menu.check_obstructed()
                                    if tile.obstructed == False:
                                        closest_tile = temp_grid_pos
                                        smallest_distance_from_target = distance_from_target
                                    
            self.selected_skill.use_skill(closest_tile)

        if self.frontliner == False:
        
            closest_tile = vec(100, 100)
            smallest_distance_from_target = vec(100, 100)
            furthest_tile = vec(0, 0)
            largest_distance_from_target = vec(0, 0)
            distance_from_target = vec(0, 0)
            target_tile = vec(100, 100)

            for x in range(self.mobility, ((-self.mobility) - 1), -1):

                for y in range(self.mobility, ((-self.mobility) - 1), -1):

                    temp_grid_pos = self.grid_pos + vec(x, y)

                    distance_from_target = self.ideal_target.grid_pos - temp_grid_pos
                    if distance_from_target.length() > largest_distance_from_target.length():
                        for tile in menu.tiles:
                            if tile.grid_pos == temp_grid_pos:
                                menu.check_obstructed()
                                if tile.obstructed == False:
                                    self.check_usable(tile.grid_pos)
                                    if self.can_use_skill:
                                        furthest_tile = temp_grid_pos
                                        largest_distance_from_target = distance_from_target 

                                        target_tile = furthest_tile

            if self.can_use_skill == False:

                distance_from_target = vec(0, 0)

                for x in range(self.mobility, ((-self.mobility) - 1), -1):

                    for y in range(self.mobility, ((-self.mobility) - 1), -1):

                        temp_grid_pos = self.grid_pos + vec(x, y)

                        distance_from_target = self.ideal_target.grid_pos - temp_grid_pos
                        if distance_from_target.length() < smallest_distance_from_target.length():
                            for tile in menu.tiles:
                                if tile.grid_pos == temp_grid_pos:
                                    menu.check_obstructed()
                                    if tile.obstructed == False:
                                        closest_tile = temp_grid_pos
                                        smallest_distance_from_target = distance_from_target
                                    
                                        target_tile = closest_tile
                                    
            self.selected_skill.use_skill(target_tile)

        if self.can_use_skill == True:

            self.determine_skill()

        else:

            self.selected_skill = EnemySkip(self.game, self)
            self.selected_skill.use_skill()

    def determine_skill(self):

        menu = self.game.menus['BATTLE']
        self.selected_skill = self.skills[7]

        self.targetable_characters = []

        for hero in menu.heroes:

            if hero != self:

                distance = vec(hero.grid_pos) - vec(self.grid_pos)
                if distance.length() >= self.selected_skill.range[0] and distance.length() < self.selected_skill.range[1]:
                    if hero not in self.targetable_characters:
                        self.targetable_characters.append(hero)

        if len(self.targetable_characters) != 0:

            if self.ideal_target in self.targetable_characters:
                self.target = self.ideal_target
            else:
                self.target = random.choice(self.targetable_characters)

            HeroIsAttackingTimer(self.game, self)

        else:
            self.selected_skill = EnemySkip(self.game, self)
            self.selected_skill.use_skill()

    def use_selected_skill(self):

        target = random.choice(self.targetable_characters)
        skill = self.selected_skill
        menu = self.game.menus['BATTLE']
        targets = []


        for hero in menu.heroes:
            if hero != self:
                distance = vec(hero.grid_pos) - vec(target.grid_pos)
                if distance.length() <= skill.splash:
                    targets.append(hero)


        self.selected_skill.use_skill(targets)
        
    def calculate_sanity_decrease(self, amount):

        sanity_factor = self.sanity_damage_factor / 100

        extra_sanity_damage = sanity_factor * amount

        amount += extra_sanity_damage

        amount = int(amount)

        self.current_sanity = max(0, self.current_sanity - amount)

        return amount

    def calculate_sanity_increase(self, amount):

        sanity_factor = self.sanity_recovery_factor / 100

        extra_sanity_healing = sanity_factor * amount

        amount += extra_sanity_healing

        amount = int(amount)

        self.current_sanity = min(self.max_sanity, self.current_sanity + amount)

        return amount

    def die(self):

        if self in self.game.characters:

            self.game.hero_party.append(None)

            sound = p.mixer.Sound(DEATH_SOUND)
            sound.play()

            if self.game.battle_mode:
                menu = self.game.menus['BATTLE']
                for tile in menu.tiles:
                    if tile.grid_pos == self.grid_pos:
                        tile.obstructed = False

            self.game.hero_party.remove(self)

            if self.game.battle_mode:

                if self in self.game.menus['BATTLE'].characters:
                    self.game.menus['BATTLE'].heroes.remove(self)
                    self.game.menus['BATTLE'].characters.remove(self)
                    self.game.battle.all_characters.remove(self)

            for i in range(4):
                menu = self.game.menus['HERO' + str(i + 1)]
                menu.hero = self.game.hero_party[i]

            for menu in self.game.menus.values():
                menu.update()
                menu.update_images()

            self.exploration_character.kill()


            self.kill()




        

        