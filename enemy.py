import pygame as p
from sprite import *
from settings import *
from character import *
from explorationCharacter import *
from effect import *
from skill import *
from enemy_skills import *
from hero_skills import *
import random
from wait import *

class Enemy(Character):

    def __init__(self, game, type, grid_pos):
        super().__init__(game, type)

        if self.type == 'GHOSTBLADE':

            self.name = 'APPARITION' # name that appears
            self.max_health = 10 # amount of damage that can be taken before dying
            self.speed = 3 # determines turn order, higher numbers go first
            self.frontliner = True # determines which heroes this character chooses to targer
            self.damage = [4, 5] # range of damage that can be dealt
            self.mobility = 3 # radius for the amount of tiles this character can move
            self.protection = 15 # amount incoming damage is reduced by
            self.agility = 5 # chance to dodge
            self.precision = 95 # chance to hit
            self.crit = 5 # chance to crit
            self.bleed = 60 # chance to resist bleed
            self.venom = 60 # chance to resist venom
            self.fire = 60 # chance to resist fire
            self.death = 0 # chance to resist deathblow
            self.stun = 70 # chance to resist stun
            self.debuff = 60 # chance to resist debuffs

            self.skills = [
                GhostVanquish(self.game, self) # list of usable skills
            ]

        if self.type == 'BANDIT1':

            self.name = 'SCIMITAR'
            self.max_health = 20
            self.speed = 5
            self.frontliner = True
            self.mobility = 3
            self.protection = 10
            self.agility = 5
            self.precision = 90
            self.crit = 15
            self.bleed = 30
            self.venom = 30
            self.fire = 30
            self.death = 0
            self.stun = 35
            self.debuff = 30

            self.skills = [
                ScimitarSlash(self.game, self),
                RallyingWinds(self.game, self)
            ]

            self.damage = [5, 8]

        if self.type == 'BANDIT2':

            self.name = 'FLINTLOCK'
            self.max_health = 16
            self.speed = 7
            self.frontliner = False
            self.mobility = 3
            self.protection = 0
            self.agility = 10
            self.precision = 95
            self.crit = 10
            self.bleed = 15
            self.venom = 15
            self.fire = 15
            self.death = 0
            self.stun = 15
            self.debuff = 15

            self.skills = [
                FlintShot(self.game, self),
                AridStab(self.game, self)
            ]

            self.damage = [4, 7]

        if self.type == 'BANDIT3':

            self.name = 'TABARZIN'
            self.max_health = 32
            self.speed = 2
            self.frontliner = True
            self.mobility = 3
            self.protection = 10
            self.agility = 0
            self.precision = 90
            self.crit = 20
            self.bleed = 30
            self.venom = 30
            self.fire = 30
            self.death = 0
            self.stun = 30
            self.debuff = 30

            self.skills = [
                CrushingBlow(self.game, self),
                IntimidatingRoar(self.game, self)
            ]

            self.damage = [7, 11]

            self.sanity_reduction_skills = [8, 16] # range of numbers that sanity reducing attacks reduce a heros sanity by

        if self.type == 'BANDIT4':

            self.name = 'ARTILLERY'
            self.max_health = 16
            self.speed = 0
            self.frontliner = False
            self.mobility = 2
            self.protection = 0
            self.agility = 10
            self.precision = 90
            self.crit = 30
            self.bleed = 15
            self.venom = 15
            self.fire = 15
            self.death = 0
            self.stun = 15
            self.debuff = 15

            self.skills = [
                Boom(self.game, self)
            ]

            self.damage = [8, 12]

            self.sanity_reduction_skills = [8, 16]

        if self.type == 'BANDIT5':

            self.name = 'COMMANDER'
            self.max_health = 60
            self.speed = 5
            self.frontliner = True
            self.mobility = 4
            self.protection = 40
            self.agility = 0
            self.precision = 120
            self.crit = 30
            self.bleed = 70
            self.venom = 70
            self.fire = 70
            self.death = 66
            self.stun = 70
            self.debuff = 70

            self.skills = [
                Obliterate(self.game, self),
                GetThem(self.game, self)
            ]

            self.damage = [12, 20]

            self.sanity_reduction_skills = [16, 24]

        self.grid_pos = grid_pos
        self.current_health = self.max_health
        self.selected_skill = None

        self.usable_skills = [] # list of skills this character can use from their position
        self.targetable_characters = [] # list of characters this character can target from their position
        self.ideal_target = None # the target character this character wants to target
        self.distance_from_ideal_target = vec(100, 100) # the distance between this character and their target
        self.can_use_skill = False # whether this character can use any skills
        self.target = None # the character this character will actually end up attacking once everything is accounted for
        self.index = 0 # the index of this character in the enemy part

        self.primary_skill = self.skills[0] # the primary skill is the skill that enemies will always use as long as they are in range of their target, otherwise, they will use another skill

    def update(self):

        self.play_animations()

    def play_animations(self):

        now = p.time.get_ticks()

        if now - self.last_update > 1000:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.image = p.transform.flip(self.images[self.current_frame], self.flipped, False)
            self.combat_image = self.combat_images[self.current_frame]

    def calculate_skill(self):

        # this is called when an enemy character starts their turn

        # first they will find their ideal target
        # 'find_ideal_target' calls another function which checks if this character can use their primary skill on their ideal target

        self.find_ideal_target()

        # if they cant use their primary skill on their ideal target, they will move to a more ideal location

        if self.ideal_target_in_range == False or self.can_use_skill == False or self.primary_skill not in self.usable_skills:

            # when this timer is up, the 'move_tile' function is called

            EnemyIsMovingTimer(self.game, self)

        # otherwise, if this character is already in a favourable position, use a skill

        else:

            self.determine_skill()
            

    def check_usable(self, tile):

        # this function checks if a characters skills are usable from a certain tile

        # the list of skills that are usable are initially empty

        self.usable_skills = []
        self.can_use_skill = False
        menu = self.game.menus['BATTLE']
        self.ideal_target_in_range = False

        # for every skill this character has

        for skill in self.skills:

            # if this skill targets heroes

            if skill.targets_heroes == True:

                # distance is a vector between the position of this characters ideal target and the tile that is being checked

                distance = vec(self.ideal_target.grid_pos) - vec(tile)

                # if the length of distance is greater than the skills minimum range and less than the skills maximum

                if distance.length() >= skill.range[0] and distance.length() < skill.range[1]:

                    # this character can use a skill

                    self.can_use_skill = True

                    # add this skill to the list of usable skills
                    # the ideal target is in range

                    if skill not in self.usable_skills:
                        self.usable_skills.append(skill)
                        self.ideal_target_in_range = True

            # same but for skills that target enemies

            if skill.targets_heroes == False:
                for enemy in menu.enemies:
                    distance = vec(enemy.grid_pos) - vec(tile)
                    if distance.length() >= skill.range[0] and distance.length() < skill.range[1]:
                        self.can_use_skill = True
                        if skill not in self.usable_skills:
                            self.usable_skills.append(skill)

        # if the ideal target is not in range, check for other possible targets

        if self.ideal_target_in_range == False:
            for skill in self.skills:
                for hero in menu.heroes:
                    distance = vec(hero.grid_pos) - vec(tile)
                    if distance.length() >= skill.range[0] and distance.length() < skill.range[1]:
                        self.can_use_skill = True
                        if skill not in self.usable_skills:
                            self.usable_skills.append(skill)

    def find_ideal_target(self):

        # this function is called as soon as the enemy starts to calculate what skills they are going to use

        menu = self.game.menus['BATTLE']

        mark_found = False
        marked_heroes = []

        # first, a list of every marked hero is created, as these characters need to draw more attacks from enemies so the enemies can work together more effectively

        for hero in menu.heroes:
            for effect in hero.effects:
                if type(effect) == Mark:
                    marked_heroes.append(hero)
                    mark_found = True

        # if there are no marked characters

        if mark_found == False:

            # if this character is a frontliner, they need to target heroes close to them because frontliners have shorter range skills

            if self.frontliner == True:

                # initially distance from the ideal target is very high because we need to find the closest hero

                self.distance_from_ideal_target = vec(100, 100)

                # for every hero

                for hero in menu.heroes:

                    # if the distance between the two is smaller than the current smallest distance
                    # the smallest distance is updated so it can be compared with the distance of the next character
                    # the ideal target is updated to the closest hero

                    distance = vec(hero.grid_pos) - vec(self.grid_pos)
                    if distance.length() < self.distance_from_ideal_target.length():
                        self.distance_from_ideal_target = distance
                        self.ideal_target = hero

            # if this character is not a frontliner, they need to target heros further back as their skills have longer ranges
            # so, the same process happens again, but instead of the closest target, the furthest one is found, by having the distance start off small

            if self.frontliner == False:

                self.distance_from_ideal_target = vec(0, 0)

                for hero in menu.heroes:
                    distance = vec(hero.grid_pos) - vec(self.grid_pos)
                    if distance.length() > self.distance_from_ideal_target.length():
                        self.distance_from_ideal_target = distance
                        self.ideal_target = hero

        # the same process but for marked characters if a marked character was found

        if mark_found == True:

            if self.frontliner == True:

                self.distance_from_ideal_target = vec(100, 100)

                for hero in marked_heroes:
                    distance = vec(hero.grid_pos) - vec(self.grid_pos)
                    if distance.length() < self.distance_from_ideal_target.length():
                        self.distance_from_ideal_target = distance
                        self.ideal_target = hero

            if self.frontliner == False:

                self.distance_from_ideal_target = vec(0, 0)

                for hero in marked_heroes:
                    distance = vec(hero.grid_pos) - vec(self.grid_pos)
                    if distance.length() > self.distance_from_ideal_target.length():
                        self.distance_from_ideal_target = distance
                        self.ideal_target = hero

        # now that we have an ideal target, we can now check how many skills can be used on the ideal target from this characters position

        self.check_usable(self.grid_pos)

    def move_tile(self):

        # this function is called when the enemy needs to reposition

        menu = self.game.menus['BATTLE']

        # select the movement skill
        self.selected_skill = EnemyMove(self.game, self)

        # if this character is a frontliner, they will attempt to get as close to the ideal target as possible

        if self.frontliner == True:

            # the closest tile is set to be very far away
        
            closest_tile = vec(100, 100)

            # the smallest distance is set to be very large
            smallest_distance_from_target = vec(100, 100)

            distance_from_target = vec(0, 0)

            # for every tile in a square around this character, with the size of this square being determined by this characters mobility

            for x in range(self.mobility, ((-self.mobility) - 1), -1):

                for y in range(self.mobility, ((-self.mobility) - 1), -1):

                    temp_grid_pos = self.grid_pos + vec(x, y)

                    # find the distance from this potential tile to the ideal target

                    distance_from_target = self.ideal_target.grid_pos - temp_grid_pos

                    # if this distance is smaller than the current smallest distance

                    if distance_from_target.length() < smallest_distance_from_target.length():
                        for tile in menu.tiles:
                            if tile.grid_pos == temp_grid_pos:
                                menu.check_obstructed()
                                # if this tile isnt obstructed
                                if tile.obstructed == False:
                                    # check if skills can be used from this potential tile
                                    self.check_usable(tile.grid_pos)
                                    # if skills can be used, set the closest tile to this potential tile, as well as updating the new smallest distance
                                    if self.can_use_skill:
                                        closest_tile = temp_grid_pos
                                        smallest_distance_from_target = distance_from_target 

            # if the character cannot use any skills from any of the tiles they can move to, they still need to move closer to the target so they might be able to move next turn
            # so the process is repeated except it is not checked whether they can use the skill from that tile, the closest one is simply chosen

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
                                        self.check_usable(tile.grid_pos)
                                        closest_tile = temp_grid_pos
                                        smallest_distance_from_target = distance_from_target


            # after the closest tile is found, this character uses their movement skill to move to this tile
                                    
            self.selected_skill.use_skill(closest_tile)

        # if this character is not a frontliner, then it is mostly the same process, except the character attempts to move as far as possible from their target, unless they cannot use any skills from the tile they move to, in which case theyll move closer

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
                                        self.check_usable(tile.grid_pos)
                                        closest_tile = temp_grid_pos
                                        smallest_distance_from_target = distance_from_target
                                    
                                        target_tile = closest_tile
            
            self.selected_skill.use_skill(target_tile)

        # if this character can use a skill from the tile they have moved to, then they will choose a skill to use

        if self.can_use_skill == True:

            self.determine_skill()

        # otherwise, they will skip their turn

        else:

            self.selected_skill = EnemySkip(self.game, self)
            self.selected_skill.use_skill()

    def determine_skill(self):

        menu = self.game.menus['BATTLE']

        # if this characters primary skill is usable, select it
        # otherwise, choose a random one

        if self.primary_skill in self.usable_skills:
            self.selected_skill = self.primary_skill
        else:
            self.selected_skill = random.choice(self.usable_skills)

        self.targetable_characters = []

        # if this skill targets heros

        if self.selected_skill.targets_heroes == True:

            # for every hero

            for hero in menu.heroes:

                # find the distance from the hero to this character

                distance = vec(hero.grid_pos) - vec(self.grid_pos)

                # if this distance falls in the range of this characters skill
                if distance.length() >= self.selected_skill.range[0] and distance.length() < self.selected_skill.range[1]:
                    # add them to the list of targetable characters
                    if hero not in self.targetable_characters:
                        self.targetable_characters.append(hero)

        # same but for skills that target enemies

        if self.selected_skill.targets_heroes == False:

            for enemy in menu.enemies:

                distance = vec(enemy.grid_pos) - vec(self.grid_pos)
                if distance.length() >= self.selected_skill.range[0] and distance.length() < self.selected_skill.range[1]:
                    if enemy not in self.targetable_characters:
                        self.targetable_characters.append(enemy)

        # if there are characters in the list of targetable characters

        if len(self.targetable_characters) != 0:

            # if the ideal target is in this list, that is the target

            if self.ideal_target in self.targetable_characters:
                self.target = self.ideal_target

            # otherwise, choose a random one

            else:
                self.target = random.choice(self.targetable_characters)

            # this timer will cause this character to use their selected skill on their target once the timer is over
            
            EnemyIsAttackingTimer(self.game, self)

        # if there are no characters in the list of targetable characters, skip turn

        else:
            self.selected_skill = EnemySkip(self.game, self)
            self.selected_skill.use_skill()

    def use_selected_skill(self):

        # this is called when the 'EnemyIsAttackingTimer' timer has run out of time

        # if this skill doesnt target every target in range

        if self.selected_skill.targets_all_in_range == False:

            target = self.target
            skill = self.selected_skill
            menu = self.game.menus['BATTLE']
            targets = []

            # for any character close enough to be included in the splash range of the skills splash radius, add them to list of characters that will be affected

            if skill.targets_heroes:
                for hero in menu.heroes:
                    distance = vec(hero.grid_pos) - vec(target.grid_pos)
                    if distance.length() <= skill.splash:
                        targets.append(hero)
            else:
                for enemy in menu.enemies:
                    distance = vec(enemy.grid_pos) - vec(target.grid_pos)
                    if distance.length() <= skill.splash:
                        targets.append(enemy)

            # finally, the skill is used on the targets, causing an animation to play, their health to change, effects to be applied, and the next characters turn

            self.selected_skill.use_skill(targets)

        # if this skill targets every target in range, use the skill on every single targetable character

        else:

            self.selected_skill.use_skill(self.targetable_characters)


    def start_turn(self):

        # this is called by the 'Battle' object directly after the last character has finished their turn

        # various values are reset

        self.game.close_menu()

        self.effect_applied_images.clear()

        self.selected_skill = None
        self.has_moved = False

        # the health before and after all effects (such as bleeding) tick is found

        current_health = self.current_health

        for effect in self.effects:
            effect.tick()

        change_in_health = current_health - self.current_health

        # a sound plays indicating a new turn has started

        self.game.play_sound_effect(NEXT_SOUND)

        for menu in self.game.menus.values():

            menu.update_images()

        # if this character isnt stunned, have a normal turn

        if self.stunned == False:

            # this timer calls 'calculate_skill' after its time runs out

            CalculateSkillTimer(self.game, self, change_in_health)

        # otherwise, they are stunned

        else:

            # this timer starts the next turn after its time runs out

            StunnedTimer(self.game, self)

    def deathblow(self):

        rand = random.randint(0, 100)

        if rand >= self.death:
            self.die()

    def die(self):

        # upon death, removes this character from any lists, makes sure the tile this character was on is free to move to, and then kills itself

        if self in self.game.battle.all_characters:

            self.game.play_sound_effect(DEATH_SOUND)

            menu = self.game.menus['BATTLE']
            for tile in menu.tiles:
                if tile.grid_pos == self.grid_pos:
                    tile.obstructed = False

            self.game.menus['ENEMY' + str(self.index)].kill()

            if self in self.game.menus['BATTLE'].characters:
                self.game.menus['BATTLE'].enemies.remove(self)
                self.game.menus['BATTLE'].characters.remove(self)
                self.game.battle.all_characters.remove(self)
            

            self.kill()

    def calculate_sanity_decrease(self, amount):

        # enemies dont have sanity
        pass

    def calculate_sanity_recovery(self, amount):
        # enemies dont have sanity
        pass


