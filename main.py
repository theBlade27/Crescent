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
from random import *

class Game:

    def __init__(self):

        p.mixer.pre_init(44100, -16, 4, 2048)
        p.init()

        self.set_up_window()
        
        self.new()

    def new(self):

        self.set_up_groups()
        self.reset_game()

    def set_up_window(self):

        p.display.set_caption(TITLE)
        screen_size = (WIDTH, HEIGHT)
        self.screen = p.display.set_mode(screen_size, p.FULLSCREEN)
        self.clock = p.time.Clock()

    def reset_game(self):

        self.end_game(True)

        self.set_up_variables(True)

    def end_game(self, reset):

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
            
        self.map_background = p.Surface((1, 1))

    def next_level(self, map):

        self.end_game(False)

        self.set_up_variables(False, map)


    def set_up_groups(self):

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

    def check_stage_clear(self):

        self.stageclear = True

        for object in self.interactable_objects:

            if type(object) == BattleInteraction:

                if object.beaten == False:

                    self.stageclear = False

    def set_up_variables(self, reset, map = MAPS['RESET']):

        reset = reset

        self.mouse = Mouse(self)
        self.debug = False
        self.clear_view = False
        self.battle_mode = False
        self.stageclear = False

        self.selected_tile = None

        self.inventory_open = False
        self.loot_open = False
        self.deleting = False

        if reset == True:

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

        self.selected_item = None
        self.selecting_equipment = False

        self.textbox_text = ''
        self.textbox_portrait = p.Surface((160, 160))
        self.textbox_portrait.fill(DARKBLUE)

        self.set_up_map(map)

        if reset == True:
            self.set_up_party(True)
        else:
            self.set_up_party(False)

        self.set_up_camera()
        self.load_font()
        self.set_up_menus()
        

    def load_font(self):

        self.font_spritesheet = Sprite(FONT)
        self.letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '!', '\"', '%', '\'', '(', ')', '+', '-', '.', ',', '/', ':', ';', '=', '?', '[', ']', '\\', ' '] 
        self.font = {}
        for i in range(0, len(self.letters)):
            self.font[self.letters[i]] = self.font_spritesheet.get_sprite(i * FONT_WIDTH, 0, FONT_WIDTH, FONT_HEIGHT)

    def set_up_map(self, map):

        self.map = Map(self, map)
        self.map_background = self.map.draw_map()

    def set_up_party(self, reset):

        if reset:

            self.hero_party = [
                Hero(self, 'ARCANE', self.spawn_location),
                None,
                None,
                None,
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


            for hero in self.hero_party:

                if hero != None:

                    if hero.current_health > 0:

                        hero.deaths_door = False

                    if hero.deaths_door == False:

                        for effect in hero.effects:
                            if type(effect) == DeathsDoor:
                                effect.remove_effect()

    def set_up_camera(self):

        self.selected_character = self.hero_party[0]
        self.camera_focus = self.selected_character.exploration_character
        self.camera = Camera(self, self.map.width, self.map.height)

    def set_up_menus(self):

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

        self.battle = Battle(self, type)

    def open_menu(self, menu, character = None, loot_list = None, text = None):

        if menu == 'INVENTORY':

            if character == None:

                self.menus[menu] = Inventory(self, self.selected_character)

            else:

                self.menus[menu] = Inventory(self, character)

        if menu == 'LOOT':

            self.menus[menu] = Loot(self, loot_list)

        if menu == 'SELECT_SKILLS':

            self.menus[menu] = SkillInfo(self, character)

        if menu == 'BARK':

            self.menus[menu] = Bark(self, character, text)

    def close_menu(self, menu):

        if menu in self.menus:

            self.menus[menu].kill()



    def play_combat_animations(self, attacker, targets, damage_numbers, heal_numbers, sanity_damage_numbers, sanity_heal_numbers):

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

        for sprite in self.barks:
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

                    self.start_battle('L2B1')

                if event.key == p.K_b:

                    self.next_level(MAPS['DESERT2'])

                if event.key == p.K_e:

                    BarkTimer(self, self.hero_party[0], 'TEST')


    def quit(self):

        p.quit()
        sys.exit()

game = Game()

while True:

    game.run()
    game.clock.tick(FPS)


