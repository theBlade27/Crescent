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

            self.name = 'APPARITION'
            self.max_health = 10
            self.speed = 2
            self.frontliner = True
            self.damage = [3, 5]
            self.mobility = 4
            self.protection = 15
            self.agility = 3
            self.precision = 90
            self.crit = 5
            self.bleed = 60
            self.venom = 60
            self.fire = 60
            self.death = 0
            self.stun = 70
            self.debuff = 60

            self.skills = [
                GhostVanquish(self.game, self)
            ]

        if self.type == 'BANDIT1':

            self.name = 'SCIMITAR'
            self.max_health = 10
            self.speed = 5
            self.frontliner = True
            self.mobility = 5
            self.protection = 10
            self.agility = 10
            self.precision = 90
            self.crit = 15
            self.bleed = 30
            self.venom = 30
            self.fire = 30
            self.death = 0
            self.stun = 25
            self.debuff = 30

            self.skills = [
                ScimitarSlash(self.game, self)
            ]

            self.damage = [4, 6]

        if self.type == 'BANDIT2':

            self.name = 'FLINTLOCK'
            self.max_health = 8
            self.speed = 7
            self.frontliner = False
            self.mobility = 4
            self.protection = 0
            self.agility = 20
            self.precision = 95
            self.crit = 10
            self.bleed = 30
            self.venom = 30
            self.fire = 30
            self.death = 0
            self.stun = 15
            self.debuff = 30

            self.skills = [
                FlintShot(self.game, self)
            ]

            self.damage = [2, 5]

        if self.type == 'BANDIT3':

            self.name = 'TABARZIN'
            self.max_health = 20
            self.speed = 2
            self.frontliner = True
            self.mobility = 3
            self.protection = 10
            self.agility = 0
            self.precision = 85
            self.crit = 20
            self.bleed = 50
            self.venom = 50
            self.fire = 50
            self.death = 0
            self.stun = 50
            self.debuff = 60

            self.skills = [
                CrushingBlow(self.game, self)
            ]

            self.damage = [5, 8]

        self.grid_pos = grid_pos
        self.current_health = self.max_health
        self.selected_skill = None

        self.usable_skills = []
        self.targetable_characters = []
        self.ideal_target = None
        self.distance_from_ideal_target = vec(100, 100)
        self.can_use_skill = False
        self.target = None
        self.index = 0

    def update(self):

        self.play_animations()

    def play_animations(self):

        now = p.time.get_ticks()

        if now - self.last_update > 1000:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.image = p.transform.flip(self.images[self.current_frame], self.flipped, False)
            if self.game.inventory_open:
                self.combat_image = self.combat_images[self.current_frame]
                self.game.menus['INVENTORY'].images['COMBAT_IMAGE'].update()

    def calculate_skill(self):

        self.find_ideal_target()

        if self.ideal_target_in_range == False or self.can_use_skill == False:

            EnemyIsMovingTimer(self.game, self)

        else:

            self.determine_skill()
            

    def check_usable(self, tile):

        self.usable_skills = []
        self.can_use_skill = False
        menu = self.game.menus['BATTLE']
        self.ideal_target_in_range = False

        for skill in self.skills:
            if skill.targets_heroes == True:
                distance = vec(self.ideal_target.grid_pos) - vec(tile)
                if distance.length() >= skill.range[0] and distance.length() < skill.range[1]:
                    self.can_use_skill = True
                    if skill not in self.usable_skills:
                        self.usable_skills.append(skill)
                        self.ideal_target_in_range = True

            if skill.targets_heroes == False:
                for enemy in menu.enemies:
                    distance = vec(enemy.grid_pos) - vec(tile)
                    if distance.length() >= skill.range[0] and distance.length() < skill.range[1]:
                        self.can_use_skill = True
                        if skill not in self.usable_skills:
                            self.usable_skills.append(skill)

        if self.ideal_target_in_range == False:
            for skill in self.skills:
                for hero in menu.heroes:
                    distance = vec(hero.grid_pos) - vec(tile)
                    if distance.length() >= skill.range[0] and distance.length() < skill.range[1]:
                        self.can_use_skill = True
                        if skill not in self.usable_skills:
                            self.usable_skills.append(skill)

    def find_ideal_target(self):

        menu = self.game.menus['BATTLE']

        if self.frontliner == True:

            self.distance_from_ideal_target = vec(100, 100)

            for hero in menu.heroes:
                distance = vec(hero.grid_pos) - vec(self.grid_pos)
                if distance.length() < self.distance_from_ideal_target.length():
                    self.distance_from_ideal_target = distance
                    self.ideal_target = hero

        if self.frontliner == False:

            self.distance_from_ideal_target = vec(0, 0)

            for hero in menu.heroes:
                distance = vec(hero.grid_pos) - vec(self.grid_pos)
                if distance.length() > self.distance_from_ideal_target.length():
                    self.distance_from_ideal_target = distance
                    self.ideal_target = hero

        self.check_usable(self.grid_pos)

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

        self.check_usable(self.grid_pos)

        if self.can_use_skill == True:

            self.determine_skill()

        else:

            self.selected_skill = EnemySkip(self.game, self)
            self.selected_skill.use_skill()

    def determine_skill(self):

        menu = self.game.menus['BATTLE']

        self.selected_skill = random.choice(self.usable_skills)
        self.targetable_characters = []

        if self.selected_skill.targets_heroes == True:

            for hero in menu.heroes:

                distance = vec(hero.grid_pos) - vec(self.grid_pos)
                if distance.length() >= self.selected_skill.range[0] and distance.length() < self.selected_skill.range[1]:
                    if hero not in self.targetable_characters:
                        self.targetable_characters.append(hero)

        if self.selected_skill.targets_heroes == False:

            for enemy in menu.enemies:

                distance = vec(enemy.grid_pos) - vec(enemy.grid_pos)
                if distance.length() >= self.selected_skill.range[0] and distance.length() < self.selected_skill.range[1]:
                    if enemy not in self.targetable_characters:
                        self.targetable_characters.append(enemy)

        if len(self.targetable_characters) != 0:

            if self.ideal_target in self.targetable_characters:
                self.target = self.ideal_target
            else:
                self.target = random.choice(self.targetable_characters)
            
            EnemyIsAttackingTimer(self.game, self)

        else:
            self.selected_skill = EnemySkip(self.game, self)
            self.selected_skill.use_skill()

    def use_selected_skill(self):

        if self.selected_skill.targets_all_in_range == False:

            target = random.choice(self.targetable_characters)
            skill = self.selected_skill
            menu = self.game.menus['BATTLE']
            targets = []

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

            self.selected_skill.use_skill(targets)

        else:

            self.selected_skill.use_skill(self.targetable_characters)


    def start_turn(self):

        self.effect_applied_images.clear()

        self.selected_skill = None
        self.has_moved = False

        current_health = self.current_health

        for effect in self.effects:
            effect.tick()

        change_in_health = current_health - self.current_health

        sound = p.mixer.Sound(NEXT_SOUND)
        sound.play()

        for menu in self.game.menus.values():

            menu.update_images()

        if self.stunned == False:

            CalculateSkillTimer(self.game, self, change_in_health)

        else:

            StunnedTimer(self.game, self)

    def deathblow(self):

        rand = random.randint(0, 100)

        if rand >= self.death:
            self.die()

    def die(self):

        if self in self.game.battle.all_characters:

            sound = p.mixer.Sound(DEATH_SOUND)
            sound.play()

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
        pass

    def calculate_sanity_recovery(self, amount):
        pass


