import pygame as p
from sprite import *
from settings import *
from character import *
from explorationCharacter import *
from effect import *
from skill import *
from hero_skills import *

class Hero(Character):

    # this class is pretty much the same as the 'Enemy' class but is controlled by the player most of the time, and has a few extra things

    def __init__(self, game, type, pos):
        super().__init__(game, type)

        # each character has their own exploration character that moves around the map

        self.exploration_character = ExplorationCharacter(self.game, self.type, pos, self)

        self.barking = False

        # lists of things the character says in different situation

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

            # same properties as enemies
            
            self.name = 'AZIZ'
            self.mobility = 3
            self.bleed = 60
            self.venom = 60
            self.fire = 60
            self.death = 66
            self.stun = 40
            self.debuff = 60
            self.equipment = [None, None, None] # slots to keep equipable items in
            self.frontliner = True

            self.skills = [
                Vanquish(self.game, self),
                Command(self.game, self),
                SteelTempest(self.game, self),
                FalseHopes(self.game, self),
                HeroMove(self.game, self),
                HeroSkip(self.game, self),
                #HeroRetreat(self.game, self), # this skill was used to retreat from battle, but has been removed
                BladeActOut(self.game, self) # this skill can never be accessed by the player, and is only used when the character has gone insane and performs an action by themself

            ]

            self.starting_grid_pos = [4, 1] # the heros starting formation, so frontliners start closer to the enemy than backliners

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

            
            self.name = 'YASMINE'
            self.mobility = 4
            self.bleed = 30
            self.venom = 30
            self.fire = 30
            self.death = 66
            self.stun = 30
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
                #HeroRetreat(self.game, self),
                ArcaneActOut(self.game, self)
            ]

            self.starting_grid_pos = [0, 0]

        if self.type == 'BREACH':

            self.deathsdoorbarks = [
                'I GUESS THIS IS IT THEN.'
            ]

            self.killbarks = [
                'ELIMINATED.',
                'ANOTHER ONE BITES THE DUST!'
            ]

            self.healbarks = [
                'YOU WON\'T REGRET THIS'
            ]

            self.healerbarks = [

            ]

            self.critbarks = [
                'HEADSHOT!',
                'I DESERVE A PAYRISE!'
            ]

            self.scaredbarks = [
                'I DIDN\'T SIGN UP FOR THIS...'
            ]

            self.actoutbarks = [
                'WHERE\'S MY MONEY HUH!'
            ]

            self.meltdownbarks = [
                'USELESS... YOU\'RE ALL USELESS'
            ]

            self.giveupbarks = [
                'IV\'E HAD ENOUGH THANKS.'
            ]

            
            self.name = 'AUDREY'
            self.mobility = 5
            self.bleed = 40
            self.venom = 40
            self.fire = 40
            self.death = 66
            self.stun = 30
            self.debuff = 40
            self.equipment = [None, None, None]
            self.frontliner = False

            self.skills = [
                DoubleTap(self.game, self),
                KissOfFire(self.game, self),
                BleedingBlade(self.game, self),
                Firestarter(self.game, self),
                HeroMove(self.game, self),
                HeroSkip(self.game, self),
                #HeroRetreat(self.game, self),
                BreachActOut(self.game, self)
            ]

            self.starting_grid_pos = [0, 2]

        self.current_sanity = 100 # characters start with all of their sanity
        self.max_sanity = 100

        self.current_experience = 0 # characters start with no experience

        self.selected_skill = None
        self.has_used_skill = False
        self.has_moved = False

        # these properties keep track of events related to sanity

        self.insane = False
        self.meltingdown = False
        self.givingup = False

        # these keep track of this characters various upgrade levels for when they get upgraded

        self.armour_level = 0
        self.weapon_level = 0
        self.experience_level = 0

        # all of the characters stats are retrieved from the appropiate dictionary, with their type as the key, and their level being the correct list to retrieve the stat from
        # for example, health is tied to the characters experience, so the EXPERIENCE_VALUES dictionary is accessed
        # for BLADE, the key would be BLADE
        # since the character is experience level 0, the first list in the list of lists is retrieved
        # and max health is the first property on that list, so the first item on that list is retrieved and set to max_health

        self.max_health = EXPERIENCE_VALUES[self.type][self.experience_level][0]
        self.agility = EXPERIENCE_VALUES[self.type][self.experience_level][1]

        self.protection = ARMOUR_VALUES[self.type][self.armour_level][0]
        self.speed = ARMOUR_VALUES[self.type][self.armour_level][1]
        self.healing[0] = ARMOUR_VALUES[self.type][self.armour_level][2]
        self.healing[1] = ARMOUR_VALUES[self.type][self.armour_level][3]
        self.sanity_recovery_skills[0] = ARMOUR_VALUES[self.type][self.armour_level][2]
        self.sanity_recovery_skills[1] = ARMOUR_VALUES[self.type][self.armour_level][3]

        self.damage[0] = WEAPON_VALUES[self.type][self.weapon_level][0]
        self.damage[1] = WEAPON_VALUES[self.type][self.weapon_level][1]
        self.precision = WEAPON_VALUES[self.type][self.weapon_level][2]
        self.crit = WEAPON_VALUES[self.type][self.weapon_level][3]

        self.sanity_reduction_skills = [6, 12]

        self.current_health = self.max_health

        # characters start off satiated

        self.effects = [
            Satiated(self.game, self)
        ]

    def update(self):
            
        # if this character hasnt used a skill, allow the player to select one by pressing keys 1 to 6
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

        # same as every other animation function

        now = p.time.get_ticks()

        if now - self.last_update > 1000:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.image = p.transform.flip(self.images[self.current_frame], self.flipped, False)
            self.combat_image = self.combat_images[self.current_frame]

    def start_turn(self):

        # mostly the same as the Enemy 'start_turn' function

        self.game.close_menu()

        # values reset

        self.game.actingout = False

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

        # if sanity has become 0, this character is now insane

        if self.current_sanity == 0:
            self.insane = True
        
        if self.insane == True:
            if self.current_sanity > 50:
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

            # if this character is not insane or stunned, the player takes their turn normally

            if self.stunned == False:

                PlayerTurnTimer(self.game, self, change_in_health)

            else:

                StunnedTimer(self.game, self)

        else:

            if self.stunned == False:

                rand = random.randint(1, 6)

                # if they are insane, they have a 1/6 chance of attacking another hero, a 1/3 chance of saying something negative and reducing everyones sanity, a 1/6 chance of skipping their turn, and a 1/3 chance of a normal turn

                if rand == 1:

                    hero_party_length = 0

                    for hero in self.game.hero_party:
                        if hero != None:
                            hero_party_length += 1

                    # if there is another hero in the players party, attack them

                    if hero_party_length > 1:

                        self.game.actingout = True # this boolean being set to true indicates to the rest of the game that the player has lost control, so things such as buttons disappear and cannot be pressed temporarily
                        CalculateSkillTimer(self.game, self, change_in_health)

                    else:

                    # otherwise, skip your turn

                        self.game.actingout = False
                        self.givingup = True
                        PlayerTurnTimer(self.game, self, change_in_health)

                elif rand == 2 or rand == 3:

                    self.game.actingout = False
                    self.meltingdown = True # this boolean being set to true means this character will say something negative
                    PlayerTurnTimer(self.game, self, change_in_health)

                elif rand == 4:

                    self.game.actingout = True
                    self.givingup = True # this boolean being set to true means this character will skip their turn
                    PlayerTurnTimer(self.game, self, change_in_health)

                else:

                    self.game.actingout = False
                    PlayerTurnTimer(self.game, self, change_in_health)

            else:

                StunnedTimer(self.game, self)

        for menu in self.game.menus.values():
            menu.update_images()

    def giveup(self):

        # upon giving up this characters sanity decreases

        rand = random.randint(8, 15)
        sanity_reduction = rand
        sanity = int(self.calculate_sanity_decrease(sanity_reduction))

        # they then say something negative

        if self.barking == False:

            BarkTimer(self.game, self, random.choice(self.giveupbarks))

        # they will also have a 50% chance to apply a debuff on themselves

        applied_debuff = random.randint(1, 3)

        successful = False
                
        rand = random.randint(0, 100)

        if rand >= 50:
            successful = True

        # depending on the random number, a different debuff can be given

        if successful:

            if applied_debuff == 1:

                # removes blindess

                for effect in self.effects:
                    if type(effect) == Blindness:
                        effect.remove_effect()

                # then adds it again so the timer resets

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

        # same as giving up, but instead everyone in the pary is affected

        if self.barking == False:

            BarkTimer(self.game, self, random.choice(self.meltdownbarks))

        for hero in self.game.hero_party:
            if hero != None:
                rand = random.randint(8, 15)
                sanity_reduction = rand
                sanity = int(hero.calculate_sanity_decrease(sanity_reduction))

                applied_debuff = random.randint(1, 3)

                successful = False
                
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


    # every skill to do with this hero attacking another has basically the same code as the code used for object of the Enemy class to make decisions, but shorter

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

        # changes the amount this characters sanity would decrease by this characters sanity damage factor, which is changed by some effects and items

        sanity_factor = self.sanity_damage_factor / 100

        extra_sanity_damage = sanity_factor * amount

        amount += extra_sanity_damage

        amount = int(amount)

        self.current_sanity = max(0, self.current_sanity - amount)

        if self.current_sanity == 0:
            self.insane = True

        if self.insane:
            self.effects.append(Insanity(self.game, self))

        return amount

    def calculate_sanity_increase(self, amount):

        # changes the amount this characters sanity would increase by this characters sanity recovery factor, which is changed by some effects and items

        sanity_factor = self.sanity_recovery_factor / 100

        extra_sanity_healing = sanity_factor * amount

        amount += extra_sanity_healing

        amount = int(amount)

        self.current_sanity = min(self.max_sanity, self.current_sanity + amount)

        if self.current_sanity > 50:
            self.insane = False

        if self.insane == False:
            for effect in self.effects:
                if type(effect) == Insanity:
                    effect.remove_effect()

        return amount

    def die(self):

        if self in self.game.characters:

            # replaces this heros slot in the hero party with the None placeholder

            self.game.hero_party.append(None)

            sound = p.mixer.Sound(DEATH_SOUND)
            sound.play()

            if self.game.battle_mode:
                menu = self.game.menus['BATTLE']
                for tile in menu.tiles:
                    if tile.grid_pos == self.grid_pos:
                        tile.obstructed = False

            # removes self from all lists

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

            # kills the exploration character associated with this character

            self.exploration_character.kill()


            self.kill()

            self.game.tick_check()




        

        