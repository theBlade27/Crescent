import pygame as p
from settings import *
from menu import *

class Battle(p.sprite.Sprite):

    def __init__(self, game, battle):

        self.game = game
        self.game.battle = self

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
        else:
            self.turn_order_counter = self.all_characters.index(self.game.selected_character)
            self.turn_order_counter += 1
            self.game.selected_character = self.all_characters[self.turn_order_counter % len(self.all_characters)]
            self.game.selected_character.start_turn()

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

        


