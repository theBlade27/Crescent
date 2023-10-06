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
        self.set_up_variables()

    def set_up_window(self):

        p.display.set_caption(TITLE)
        screen_size = (WIDTH, HEIGHT)
        self.screen = p.display.set_mode(screen_size, p.FULLSCREEN)
        self.clock = p.time.Clock()

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

    def set_up_variables(self):

        self.mouse = Mouse(self)
        self.debug = False
        self.clear_view = False
        self.battle_mode = False

        self.selected_tile = None

        self.inventory_open = False
        self.loot_open = False
        self.deleting = False
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

        self.inventory[0] = Bandage(self)
        self.inventory[1] = Torch(self)
        self.inventory[3] = Torch(self)

        self.selected_item = None
        self.selecting_equipment = False

        self.money = 0

        self.textbox_text = ''
        self.textbox_portrait = p.Surface((160, 160))
        self.textbox_portrait.fill(DARKBLUE)

        self.set_up_map()
        self.set_up_party()
        self.set_up_camera()
        self.load_font()
        self.set_up_menus()
        

    def load_font(self):

        self.font_spritesheet = Sprite(FONT)
        self.letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '!', '\"', '%', '\'', '(', ')', '+', '-', '.', ',', '/', ':', ';', '=', '?', '[', ']', '\\', ' '] 
        self.font = {}
        for i in range(0, len(self.letters)):
            self.font[self.letters[i]] = self.font_spritesheet.get_sprite(i * FONT_WIDTH, 0, FONT_WIDTH, FONT_HEIGHT)

    def set_up_map(self):

        self.map = Map(self, TUTORIAL_MAP)
        self.map_background = self.map.draw_map()

    def set_up_party(self):

        self.hero_party = [
            Hero(self, 'BLADE', self.spawn_location),
            Hero(self, 'ARCANE', (self.spawn_location[0] + 96, self.spawn_location[1])),
            #Hero(self, 'BREACH', (self.spawn_location[0], self.spawn_location[1] + 96)),
            #Hero(self, 'FORTRESS', (self.spawn_location[0] + 96, self.spawn_location[1] + 96)),
            #None,
            None,
            None,
        ]

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

    def open_menu(self, menu, character = None, loot_list = None):

        if menu == 'INVENTORY':

            if character == None:

                self.menus[menu] = Inventory(self, self.selected_character)

            else:

                self.menus[menu] = Inventory(self, character)

        if menu == 'LOOT':

            self.menus[menu] = Loot(self, loot_list)

        if menu == 'SELECT_SKILLS':

            self.menus[menu] = SkillInfo(self, character)

    def close_menu(self, menu):

        if menu == 'INVENTORY':

            self.menus[menu].kill()

        if menu == 'LOOT':

            self.menus[menu].kill()

        if menu == 'SELECT_SKILLS':

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

        self.all.update()
        self.characters.update()
        self.effects_group.update()

        if self.battle_mode == False:
            self.interactable_objects.update()
            self.exploration_characters.update()
        else:
            self.selected_tile = None
            self.menus['BATTLE'].cross = False
            self.skills_group.update()
            self.tiles.update()

        self.menus_group.update()

    def draw(self):

        self.screen.fill(BLACK)

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

                if event.key == p.K_RIGHT:
                    for effect in self.hero_party[0].effects:
                        effect.tick()

                if event.key == p.K_LEFT:
                    for hero in self.hero_party:
                        if hero != None:
                            self.hero_party[0].effects.append(Strength(self, self.hero_party[0]))
                            self.hero_party[0].effects.append(Burning(self, self.hero_party[0]))
                    for menu in self.menus.values():
                        menu.update_images()

                if event.key == p.K_u:

                    self.debug = not self.debug

                if event.key == p.K_c:

                    self.clear_view = not self.clear_view

                if event.key == p.K_b:

                    loot_list = [
                        Bandage(self),
                        Torch(self),
                        Bandage(self)
                    ]

                    if self.loot_open == False:
                        self.open_menu('LOOT', loot_list = loot_list)
                        self.loot_open = True
                    else:
                        self.close_menu('LOOT')
                        self.loot_open = False

    def quit(self):

        p.quit()
        sys.exit()

game = Game()

while True:

    game.run()
    game.clock.tick(FPS)


