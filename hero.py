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

        if self.type == 'BLADE':
            self.name = 'BLADE'
            self.max_health = 1
            self.speed = 3
            self.damage = [6, 9]
            self.healing = [1, 2]
            self.sanity_recovery_skills = [4, 7]
            self.mobility = 4
            self.protection = 15
            self.agility = 0
            self.precision = 90
            self.crit = 5
            self.bleed = 60
            self.venom = 60
            self.fire = 60
            self.death = 1
            self.stun = 70
            self.debuff = 60
            self.equipment = [None, None, None]

            self.skills = [
                Vanquish(self.game, self),
                GetHim(self.game, self),
                Slash(self.game, self),
                StrengthenResolve(self.game, self),
                HeroMove(self.game, self),
                HeroSkip(self.game, self),
                HeroRetreat(self.game, self)

            ]

            self.starting_grid_pos = [4, 1]

        if self.type == 'ARCANE':
            self.name = 'ARCANE'
            self.max_health = 1
            self.speed = 6
            self.damage = [5, 7]
            self.healing = [5, 7]
            self.sanity_recovery_skills = [0, 0]
            self.mobility = 6
            self.protection = 0
            self.agility = 20
            self.precision = 95
            self.crit = 10
            self.bleed = 30
            self.venom = 30
            self.fire = 30
            self.death = 1
            self.stun = 50
            self.debuff = 40
            self.equipment = [None, None, None]

            self.skills = [
                AzureEruption(self.game, self),
                Dazzle(self.game, self),
                ArcaneAssault(self.game, self),
                Rejuvinate(self.game, self),
                HeroMove(self.game, self),
                HeroSkip(self.game, self),
                HeroRetreat(self.game, self) 
            ]

            self.starting_grid_pos = [0, 0]

        self.current_health = self.max_health

        self.current_sanity = 100
        self.max_sanity = 100

        self.current_experience = 0
        self.max_experience = 100

        self.selected_skill = None
        self.has_used_skill = False
        self.has_moved = False

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
            if self.game.inventory_open:
                self.combat_image = self.combat_images[self.current_frame]
                self.game.menus['INVENTORY'].images['COMBAT_IMAGE'].update()

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

        current_health = self.current_health

        for effect in self.effects:
            effect.tick()

        change_in_health = current_health - self.current_health

        sound = p.mixer.Sound(NEXT_SOUND)
        sound.play()

        for menu in self.game.menus.values():

            menu.update_images()

        if self.stunned == False:
            PlayerTurnTimer(self.game, self, change_in_health)

        else:

            StunnedTimer(self.game, self)

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

        if self in self.game.battle.all_characters:

            self.game.hero_party.append(None)

            sound = p.mixer.Sound(DEATH_SOUND)
            sound.play()

            menu = self.game.menus['BATTLE']
            for tile in menu.tiles:
                if tile.grid_pos == self.grid_pos:
                    tile.obstructed = False

            self.game.hero_party.remove(self)

            if self in self.game.menus['BATTLE'].characters:
                self.game.menus['BATTLE'].heroes.remove(self)
                self.game.menus['BATTLE'].characters.remove(self)
                self.game.battle.all_characters.remove(self)

            for i in range(4):
                menu = self.game.menus['HERO' + str(i + 1)]
                if menu.hero == self:
                    menu.kill()

            i = 0

            for hero in self.game.hero_party:

                if hero != None:

                    self.game.menus['HERO' + str(i + 1)].hero = hero
                    i += 1

            for menu in self.game.menus.values():
                menu.update()
                menu.update_images()

            self.exploration_character.kill()


            self.kill()




        

        