import pygame as p
from settings import *
from menu import *
from item import *
from cutscene import *

class Battle(p.sprite.Sprite):

    # this class deals with managing battles

    def __init__(self, game, battle):

        self.groups = game.all
        p.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.game.battle = self
        self.battle = battle

        # creates a battle menu, which contains all the tiles and obstacles and allows the player to click the tiles in order to use skills
        # when the battle menu is made, it loads a battle map, spawns all the characters in the right position, and adds each character to the correct list (heroes, enemies and all)
        self.game.menus['BATTLE'] = BattleMenu(self.game, battle)

        self.all_characters = [

        ]

        # adds every character in the battle menus list of characters to a list

        for character in self.game.menus['BATTLE'].characters:
            self.all_characters.append(character)

        # sorts the list by each characters speed
        self.all_characters.sort(key = lambda x : x.speed)

        # since characters with the highest speed go first, the list needs to be reversed, so larger numbers go at the fron
        self.all_characters.reverse()

        # the games selected character is set to the last character on the list (this is done because the turn counter is incremented before the turn starts, so if a character dies the position of the character who just had their turn can still be found and the turn order is not disrupted)
        self.game.selected_character = self.all_characters[len(self.all_characters)]

        self.start_next_character_turn()

    def start_next_character_turn(self):
        
        # the list of characters is reset and sorted again to account for any characters dying

        self.all_characters = [

        ]

        for character in self.game.menus['BATTLE'].characters:
            self.all_characters.append(character)

        self.all_characters.sort(key = lambda x : x.speed)
        self.all_characters.reverse()

        menu = self.game.menus['BATTLE']
        
        if len(menu.enemies) == 0:
            # if there are no enemies left, end the battle
            self.end_battle()
        elif len(menu.heroes) == 0:
            # if there are no heroes left, the player has failed and the game will restart, playing a cutscene
            self.game.reset_game()
            CutScene(self.game, 'gameover')
        else:
            # otherwise, the battle needs to continue

            # the position of the current character is found in the list of characters
            self.turn_order_counter = self.all_characters.index(self.game.selected_character)
            # the counter is incremented
            self.turn_order_counter += 1
            # the character after the one that has just taken their turn is selected
            self.game.selected_character = self.all_characters[self.turn_order_counter % len(self.all_characters)]
            # the character starts their turn
            self.game.selected_character.start_turn()



    def end_battle(self):

        # upon ending a battle, the menu is killed, the games camera focuses on the first member in the player party and some groups are emptied to save memory

        self.game.menus['BATTLE'].kill()

        self.game.selected_character = self.game.hero_party[0]
        self.game.camera_focus = self.game.hero_party[0].exploration_character

        self.game.tiles.empty()
        self.game.obstacles.empty()

        for character in self.game.characters:

            if type(character) == Enemy:
                # kills all enemy characters, they do not need to exist outside battle
                character.kill()
                # kills all the preview menus associated with each enemy as well
                self.game.menus['ENEMY' + str(character.index)].kill()
            if type(character) == Hero:
                if character != None:
                    character.selected_skill == None

                    # gives each hero some experience
                    character.calculate_experience(50)
                    # removes the stun debuff from each character
                    for effect in character.effects:
                        if isinstance(effect, Stun):
                            effect.remove_effect()


        # sometimes, the first hero in the player party might die
        # if this happens, the next hero in the players party must be found so the camera can focus on them
        hero_found = False
        i = 0

        # whilst a hero has not been found in the players party
        while hero_found == False:
            # if the hero is actually a hero and not the placehold None
            if type(self.game.hero_party[i] == Hero):
                # the games selected character and camera focus becomes the hero and the loop finishes
                self.game.selected_character = self.game.hero_party[i]
                self.game.camera_focus = self.game.hero_party[i].exploration_character
                hero_found = True

        # switches the game out of battle mode
        self.game.battle_mode = False

        # the tile object that is interacted with in order to start the battle is set to beaten
        self.game.last_interacted.beaten = True

        # loot is generated based on the type of battle which was beaten
        self.items, money = self.game.generate_loot(self.battle)

        # the game checks if every battle of the map has beaten to know if the next level can be unlocked yet
        self.game.check_stage_clear()

        # a menu opens showing the generated loot
        self.game.open_menu('LOOT', loot_list = self.items, money = money)

        # the players money is increased
        self.game.money += money

        for menu in self.game.menus.values():
            menu.update_images()

        


