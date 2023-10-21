import pygame as p
from os import path
import sys
from settings import *
from mouse import *
from map import *
from camera import *
from menu import *
from sprite import *
from effect import *
from battle import *
from item import *
from scene import *
from cutscene import *
import random

# this class manages the entire game. it deals with starting up the game for the first time, resetting the game, changing levels, and finally updating and drawing every object

class Game:

    def __init__(self):

        p.mixer.pre_init(44100, -16, 4, 2048)
        p.init()

        self.set_up_window()
        
        self.new()

    def new(self):

        # when the game starts, all the groups that all the objects are in are created, and the game is reset
        # then, the introduction cutscene is played

        self.set_up_groups()
        self.menus = {}

        self.reset_game()

        CutScene(self, 'intro')

    def set_up_window(self):

        # initialises the window in fullscreen and initialises the clock

        p.display.set_caption(TITLE)
        screen_size = (WIDTH, HEIGHT)
        self.screen = p.display.set_mode(screen_size, p.FULLSCREEN)
        self.clock = p.time.Clock()

    def reset_game(self):

        # ticks are what are used to track how much the player has moved around
        # this system is used instead of simply just looking at the time so that events dont happen whilst the player isnt doing anything
        # it is increased whenever the player moves around

        self.ticks = 0

        self.end_game(True)

        self.set_up_variables(True)

    def end_game(self, reset):

        # depending on whether the game needs to reset completely or the game just needs to switch to the next level, this function can do two things
        # if the level just needs to be changed, the 'reset' parameter is False, so it clears the 'all' group - this contains everything except stuff that needs to be saved between stages, such as characters
        # otherwise, the 'reset' parameter is True, so every object is killed

        if reset == True:

            for sprite in self.all:

                sprite.kill()

            for sprite in self.characters:
                
                sprite.kill()

            for sprite in self.exploration_characters:

                sprite.kill()

        else:

            for sprite in self.all:

                sprite.kill()

        # resets the background
            
        self.map_background = p.Surface((1, 1))

    def next_level(self, map):

        # this function is used to change levels, and takes in the map that the level is being changed to as a parameter

        self.end_game(False)

        self.set_up_variables(False, map)


    def set_up_groups(self):

        # sets up all the groups

        self.all = p.sprite.LayeredUpdates()

        self.mouse_group = p.sprite.LayeredUpdates()
        self.characters = p.sprite.LayeredUpdates()
        self.exploration_characters = p.sprite.LayeredUpdates()
        self.tile_objects = p.sprite.LayeredUpdates()
        self.collision_hitboxes = p.sprite.LayeredUpdates()
        self.menus_group = p.sprite.LayeredUpdates()
        self.images_group = p.sprite.LayeredUpdates()
        self.effects_group = p.sprite.LayeredUpdates()
        self.skills_group = p.sprite.LayeredUpdates()
        self.interactable_objects = p.sprite.LayeredUpdates()
        self.obstacles = p.sprite.LayeredUpdates()
        self.tiles = p.sprite.LayeredUpdates()
        self.items_group = p.sprite.LayeredUpdates()
        self.battles = p.sprite.LayeredUpdates()
        self.numbers = p.sprite.LayeredUpdates()
        self.camera_group = p.sprite.LayeredUpdates()
        self.timers = p.sprite.LayeredUpdates()
        self.barks = p.sprite.LayeredUpdates()
        self.scenes_group = p.sprite.LayeredUpdates()
        self.cutscenes_group = p.sprite.LayeredUpdates()

    def check_stage_clear(self):

        # this function checks that every battle on a given stage has been beaten

        self.stageclear = True

        # 'interactable_objects' is a group that would contain any objects that start battles, so it is looped through
        # when a battle is beaten, the 'interactable' that it is associated with has its 'beaten' property set to True
        # if no object is found to be beaten, the stage has been cleared

        for object in self.interactable_objects:

            if type(object) == BattleInteraction:

                if object.beaten == False:

                    self.stageclear = False

    def set_up_variables(self, reset, map = MAPS['RESET']):

        # this function is called whenever the level is changed or the game is reset
        # this is an important function that sets up all the variables needed for the game to function
        # it resets many variables such as 'stageclear' back to False

        reset = reset

        # creates a mouse object
        self.mouse = Mouse(self)

        # this variable is used for debugging, and when true, all hitboxes are highlighted
        self.debug = False

        # this variable enables the player to hide the menus on the sides that shows character health so they can see more the map if they wish
        self.clear_view = False

        # this variable keeps track of whether the player is in a battle or not
        # this is important as the player shouldnt be able to move around the map and access chests whilst they are mid battle
        self.battle_mode = False

        # keeps track of whether this stage has been cleared
        self.stageclear = False

        # battle is grid based, and this keeps track of the tile the player is selecting
        self.selected_tile = None

        # these keep track of whether the inventory or loot menu is open
        # this is important so the player doesnt open loads of menus on top of each other
        self.loot_open = False

        # keeps track of whether a character is acting out
        # this is important so the game knows when to take away control from the player
        self.actingout = False

        # if the game is being reset, the players inventory and money is reset

        if reset == True:

            self.inventory = [
                ForsakenCoin(self),
                ForsakenCoin(self),
                ForsakenCoin(self),
                ForsakenCoin(self),
                ForsakenCoin(self),
                ForsakenCoin(self),
                ForsakenCoin(self),
                ForsakenCoin(self),
                ForsakenCoin(self),
                ForsakenCoin(self),
                ForsakenCoin(self),
                ForsakenCoin(self),
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
            ]

            self.inventory = [
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
            ]

            self.money = 0

        # keeps track of the item the player has selected in the inventory
        self.selected_item = None

        # keeps track of whether the player is selecting an item to equip
        self.selecting_equipment = False


        # calls a function to set up the map based on the parameter passed in
        self.set_up_map(map)

        # calls the 'set_up_party' function with the reset parameter set to True or False depending on whether the game is being reset

        if reset == True:
            self.set_up_party(True)
        else:
            self.set_up_party(False)

        # resets the textbox at the top of the screen

        self.textbox_text = ''
        self.textbox_portrait = p.Surface((160, 160))
        self.textbox_portrait.fill(DARKBLUE)

        # more vital objects are set up, such as the camera, menus
        # the font is also loaded

        self.set_up_camera()
        self.load_font()
        self.set_up_menus()
        

    def load_font(self):

        # this function loads up the font
        # first, it loads the font image
        # then it creates a list of all the possible characters
        # the order of the characters in the list is the same as the order of the characters in the image
        # a dictionary is created for the font
        # for every character in the list, the character is added to the dictionary, with the image of the character as its key
        # it does this by increasing the x position of where the image is grabbed from by the width of the character each time

        self.font_spritesheet = Sprite(FONT)
        self.letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '!', '\"', '%', '\'', '(', ')', '+', '-', '.', ',', '/', ':', ';', '=', '?', '[', ']', '\\', ' ', '$'] 
        self.font = {}
        for i in range(0, len(self.letters)):
            self.font[self.letters[i]] = self.font_spritesheet.get_sprite(i * FONT_WIDTH, 0, FONT_WIDTH, FONT_HEIGHT)

    def set_up_map(self, map):

        # creates a map object
        # sets the games background to a picture of the map

        self.map = Map(self, map)
        self.map_background = self.map.draw_map()

    def set_up_party(self, reset):

        # depending on whether the game is reset or not
        # the function either resets the party to just one character with no accessories
        # or it just changes their position to the new maps spawn location, as well as healing their health by a third
        # the spawn location is a variable that varies level to level, and is used to determine where on the map they spawn

        if reset:

            self.hero_party = [
                Hero(self, 'BLADE', self.spawn_location),
                None,
                None,
                #None,
                Hero(self, 'ARCANE', (self.spawn_location[0], self.spawn_location[1] + 100)),
                #Hero(self, 'ARCANE', (self.spawn_location[0] + 100, self.spawn_location[1])),
                #Hero(self, 'ARCANE', (self.spawn_location[0] + 100, self.spawn_location[1] + 100)),
            ]

        else:

            if self.hero_party[0] != None:

                self.hero_party[0].exploration_character.pos = self.spawn_location
                self.hero_party[0].current_health = min(self.hero_party[0].current_health + self.hero_party[0].max_health / 3, self.hero_party[0].max_health)

            if self.hero_party[1] != None:

                self.hero_party[1].exploration_character.pos = (self.spawn_location[0] + 96, self.spawn_location[1])
                self.hero_party[1].current_health = min(self.hero_party[1].current_health + self.hero_party[1].max_health / 3, self.hero_party[1].max_health)

            if self.hero_party[2] != None:

                self.hero_party[2].exploration_character.pos = (self.spawn_location[0], self.spawn_location[1] + 96)
                self.hero_party[2].current_health = min(self.hero_party[2].current_health + self.hero_party[2].max_health / 3, self.hero_party[2].max_health)

            if self.hero_party[3] != None:

                self.hero_party[3].exploration_character.pos = (self.spawn_location[0] + 96, self.spawn_location[1] + 96)
                self.hero_party[3].current_health = min(self.hero_party[3].current_health + self.hero_party[3].max_health / 3, self.hero_party[3].max_health)

            # since every hero is healed, their 'deaths door' debuff needs to be removed as they no longer meet the requirements

            for hero in self.hero_party:

                if hero != None:

                    if hero.current_health > 0:

                        hero.deaths_door = False

                    if hero.deaths_door == False:

                        for effect in hero.effects:
                            if type(effect) == DeathsDoor:
                                effect.remove_effect()

    def set_up_camera(self):

        # the selected character is set to be the first character in the players party
        # the 'camera_focus' variable tracks what the camera should be focusing on
        # it is set to be the selected character

        # the camera object is created


        self.selected_character = self.hero_party[0]
        self.camera_focus = self.selected_character.exploration_character
        self.camera = Camera(self, self.map.width, self.map.height)

    def set_up_menus(self):

        # sets up the menus required for the game
        # TOP is the menu that has all the buttons for doing thigns such as opening the inventory, as well as containing the information textbox
        # the HERO menus each correlate to one of the heroes in the party, and show their health and sanity

        self.menus = {
            'TOP': TopMenu(self),
            'HERO1': HeroPreview(self, 0),
            'HERO2': HeroPreview(self, 1),
            'HERO3': HeroPreview(self, 2),
            'HERO4': HeroPreview(self, 3),
            'BOTTOM': BottomMenu(self)
        }

        for image in self.images_group:
            image.update()

    def start_battle(self, type):

        self.battle_mode = True

        # creates a battle object based on the string that is passed in as a parameter
        self.battle = Battle(self, type)

    def open_menu(self, menu, character = None, loot_list = None, text = None, money = None):

        # this function opens up menus and ensures they have the correct parameters

        if menu == 'INVENTORY':

            self.close_menu('INVENTORY')
            self.close_menu('SELECT_SKILLS')

            if character == None:

                self.menus[menu] = Inventory(self, self.selected_character)

            else:

                self.menus[menu] = Inventory(self, character)

        if menu == 'LOOT':

            self.menus[menu] = Loot(self, loot_list, money)

        if menu == 'SELECT_SKILLS':

            self.close_menu('INVENTORY')
            self.close_menu('SELECT_SKILLS')

            self.menus[menu] = SkillInfo(self, character)

        if menu == 'BARK':

            self.menus[menu] = Bark(self, character, text)

    def close_menu(self, menu):

        # closes menus

        if menu in self.menus:

            self.menus[menu].kill()

    def generate_loot(self, type):

        loot_list = []
        inventory = []

        number_of_common = random.randint(1, 2)
        number_of_rare = random.randint(1, 1)
        number_of_very_rare = random.randint(0, 1)

        if len(LOOT_TABLE[type][0]) > 0:
            for i in range(number_of_common):
                loot_list.append(random.choice(LOOT_TABLE[type][0]))

        if len(LOOT_TABLE[type][1]) > 0:
            for i in range(number_of_rare):
                loot_list.append(random.choice(LOOT_TABLE[type][1]))

        if len(LOOT_TABLE[type][2]) > 0:
            for i in range(number_of_very_rare):
                loot_list.append(random.choice(LOOT_TABLE[type][2]))

        money = random.randint(LOOT_TABLE[type][3][0], LOOT_TABLE[type][3][1])

        money *= 50

        for item in loot_list:

            if item == 'BANDAGE':

                inventory.append(Bandage(self))

            if item == 'TORCH':

                inventory.append(Torch(self))

            if item == 'CHERISHED_LETTER':

                inventory.append(CherishedLetter(self))

            if item == 'HOLY_BOOK':

                inventory.append(HolyBook(self))

            if item == 'LUCKY_RING':

                inventory.append(LuckyRing(self))

            if item == 'GLISTENING_JAMBIYA':

                inventory.append(GlisteningJambiya(self))

            if item == 'CRESCENT_COIN':

                inventory.append(CrescentCoin(self))

            if item == 'CURSED_COIN':

                inventory.append(CursedCoin(self))

            if item == 'FORSAKEN_COIN':

                inventory.append(ForsakenCoin(self))

            if item == 'SAPPHIRE_EARRINGS':

                inventory.append(SapphireEarrings(self))

            if item == 'MAGIC_LAMP':

                inventory.append(MagicLamp(self))

            if item == 'FOOD':

                inventory.append(Food1(self))

            if item == 'FOOD2':

                inventory.append(Food2(self))

            if item == 'FOOD3':

                inventory.append(Food3(self))

        return inventory, money

    def play_combat_animations(self, attacker, targets, damage_numbers, heal_numbers, sanity_damage_numbers, sanity_heal_numbers):

        # this function creates the menu that shows the animations for combat, as well as showing things like the damage number, and whether the character dodged

        self.menus['COMBAT_ANIMATIONS'] = CombatAnimation(self, attacker, targets, damage_numbers, heal_numbers, sanity_damage_numbers, sanity_heal_numbers)

    def check_inventory_full(self):

        first_slot_found = False
        first_slot = 0

        i = 0

        for item in self.inventory:
            if item == None:
                if first_slot_found == False:
                    first_slot = i
                    first_slot_found = True

            i += 1

        return first_slot_found, first_slot



    def run(self):

        self.events()
        self.update()
        self.draw()

    def update(self):

        self.textbox_text = ''
        self.textbox_portrait = p.Surface((160, 160))
        self.textbox_portrait.fill(DARKBLUE)

        self.menus['TOP'].images['TEXT'].update()
        self.menus['TOP'].images['PORTRAIT'].update()

        self.mouse_group.update()
        self.characters.update()
        self.effects_group.update()
        self.timers.update()

        if self.battle_mode == False:
            self.tile_objects.update()
            self.interactable_objects.update()
            self.exploration_characters.update()
            self.camera_group.update()
        else:
            self.selected_tile = None
            self.menus['BATTLE'].cross = False
            self.skills_group.update()
            self.tiles.update()

        self.menus_group.update()

        self.menus['TOP'].images['TEXT'].update()

        self.cutscenes_group.update()

        self.scenes_group.update()
        self.cutscenes_group.update()

    def tick_check(self):

        if self.ticks >= 100:
            for hero in self.hero_party:
                if hero != None:
                    for effect in hero.effects:
                        effect.tick()
            self.ticks = 0

        if len(self.hero_party) == 0:
            self.reset_game()
            CutScene(self, 'gameover')

    def draw(self):

        self.screen.fill(FAKEBLACK)

        if self.battle_mode == False:

            self.screen.blit(self.map_background, self.camera.apply(self.map))

            for sprite in self.exploration_characters:
                self.screen.blit(sprite.image, self.camera.apply(sprite))
                if self.debug:
                    p.draw.rect(self.screen, RED, self.camera.apply_hitbox(sprite.hitbox), 1)

            for sprite in self.tile_objects:
                self.screen.blit(sprite.image, self.camera.apply(sprite))

        for sprite in self.collision_hitboxes:
            if self.debug:
                p.draw.rect(self.screen, RED, self.camera.apply_hitbox(sprite.hitbox), 1)

        for sprite in self.menus_group:
            if sprite.visible:
                self.screen.blit(sprite.image, sprite.pos)
            if self.debug:
                p.draw.rect(self.screen, RED, sprite.hitbox, 1)
                if self.battle_mode:
                    for sprite in self.tiles:
                        p.draw.rect(self.screen, RED, sprite.hitbox, 1)

        for sprite in self.menus['TOP'].images.values():
            self.screen.blit(sprite.image, sprite.pos)

        if 'PLAY' in self.menus:
            self.screen.blit(self.menus['PLAY'].image, (0, 0))

        for sprite in self.barks:
            self.screen.blit(sprite.image, sprite.pos)

        for sprite in self.scenes_group:
            self.screen.blit(sprite.image, sprite.pos)

        for sprite in self.mouse_group:
            self.screen.blit(sprite.image, sprite.pos)

        p.display.flip()

    def events(self):

        for event in p.event.get():

            if event.type == p.QUIT:
                self.quit()

            if event.type == p.KEYDOWN:
                if event.key == p.K_ESCAPE:
                    self.quit()

                if event.key == p.K_UP:
                    for hero in self.hero_party:
                        if hero != None:
                            hero.current_health = min(hero.max_health, hero.current_health + 1)
                    for menu in self.menus.values():
                        menu.update_images()

                if event.key == p.K_DOWN:
                    for hero in self.hero_party:
                        if hero != None:
                            hero.current_health = max(0, hero.current_health - 1)
                    for menu in self.menus.values():
                        menu.update_images()

                if event.key == p.K_u:

                    self.debug = not self.debug

                if event.key == p.K_c:

                    self.clear_view = not self.clear_view

                if event.key == p.K_q:

                    self.start_battle('L3B1')

                if event.key == p.K_b:

                    self.next_level(MAPS['DESERT3'])

                if event.key == p.K_e:

                    BarkTimer(self, self.hero_party[0], 'TEST')

                if event.key == p.K_l:
                    CutScene(self, 'gameover')

                if event.key == p.K_t:

                    for hero in self.hero_party:
                        if hero != None:
                            for effect in hero.effects:
                                effect.tick()


    def quit(self):

        p.quit()
        sys.exit()

game = Game()

while True:

    game.run()
    game.clock.tick(FPS)


