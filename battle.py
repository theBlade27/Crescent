import pygame as p
from settings import *
from menu import *
from item import *

class Battle(p.sprite.Sprite):

    def __init__(self, game, battle):

        self.groups = game.all
        p.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.game.battle = self
        self.battle = battle

        self.game.menus['BATTLE'] = BattleMenu(self.game, battle)

        self.all_characters = [

        ]

        for character in self.game.menus['BATTLE'].characters:
            self.all_characters.append(character)

        self.all_characters.sort(key = lambda x : x.speed)
        self.all_characters.reverse()

        self.game.selected_character = self.all_characters[len(self.all_characters) - 1]

        self.start_next_character_turn()

    def start_next_character_turn(self):

        self.all_characters = [

        ]

        for character in self.game.menus['BATTLE'].characters:
            self.all_characters.append(character)

        self.all_characters.sort(key = lambda x : x.speed)
        self.all_characters.reverse()

        menu = self.game.menus['BATTLE']
        if len(menu.enemies) == 0:
            self.end_battle()
        elif len(menu.heroes) == 0:
            self.game.quit()
        else:
            self.turn_order_counter = self.all_characters.index(self.game.selected_character)
            self.turn_order_counter += 1
            self.game.selected_character = self.all_characters[self.turn_order_counter % len(self.all_characters)]
            self.game.selected_character.start_turn()

    def generate_loot(self):

        self.loot_list = []
        self.items = []

        number_of_common = random.randint(2, 3)
        number_of_rare = random.randint(1, 2)
        number_of_very_rare = random.randint(0, 1)

        for i in range(number_of_common):
            self.loot_list.append(random.choice(LOOT_TABLE[self.battle][0]))

        for i in range(number_of_rare):
            self.loot_list.append(random.choice(LOOT_TABLE[self.battle][1]))

        for i in range(number_of_very_rare):
            self.loot_list.append(random.choice(LOOT_TABLE[self.battle][2]))

        for item in self.loot_list:

            if item == 'BANDAGE':

                self.items.append(Bandage(self.game))

            if item == 'TORCH':

                self.items.append(Torch(self.game))


    def end_battle(self):

        self.game.menus['BATTLE'].kill()

        self.game.selected_character = self.game.hero_party[0]
        self.game.camera_focus = self.game.hero_party[0].exploration_character

        self.game.tiles.empty()
        self.game.obstacles.empty()

        for effect in self.game.effects_group:
            if effect.timed:
                effect.kill()

        for character in self.game.characters:

            if type(character) == Enemy:
                character.kill()
                self.game.menus['ENEMY' + str(character.index)].kill()

        hero_found = False
        i = 0

        while hero_found == False:
            if type(self.game.hero_party[i] == Hero):
                self.game.selected_character = self.game.hero_party[i]
                self.game.camera_focus = self.game.hero_party[i].exploration_character
                hero_found = True

        self.game.battle_mode = False

        for menu in self.game.menus.values():
            menu.update_images()

        self.game.last_interacted.beaten = True

        self.generate_loot()
        self.game.check_stage_clear()

        self.game.open_menu('LOOT', loot_list = self.items)
        self.loot_open = True

        


