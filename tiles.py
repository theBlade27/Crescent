import pygame as p
from sprite import *
from settings import *
vec = p.math.Vector2

class Tile(p.sprite.Sprite):

    def __init__(self, game, x, y, image, offset):
        self.groups = game.tiles
        p.sprite.Sprite.__init__(self, self.groups)

        self.game = game

        self.grid_pos = [x, y]

        self.image = image
        self.background = self.image.copy()

        self.traversable = False
        self.targetable = False
        self.obstructed = False
        self.has_enemy = False
        self.has_hero = False
        self.being_targeted = False

        self.offset = offset

        self.hitbox = p.Rect(x * MAP_SCALE * TILE_SIZE + offset[0], y * MAP_SCALE * TILE_SIZE + offset[1], 60, 60)

    def update(self):

        self.image = self.background.copy()
        if self.hitbox.collidepoint(self.game.mouse.pos):
            if self.game.mouse.pressed['M2']:

                if self.has_enemy or self.has_hero:

                    for character in self.game.menus['BATTLE'].characters:

                        if character.grid_pos == self.grid_pos:

                            self.game.open_menu('INVENTORY', character)
                            self.game.menus['INVENTORY'].hero = character
                            self.game.inventory_open = True

        if self.traversable:

            if self.game.selected_character.has_used_skill == False:
                    
                    if self.game.selected_character.has_moved == False:

                        self.image.blit(MOVEMENTINDICATOR, (0, 0))

                        if self.hitbox.collidepoint(self.game.mouse.pos):
                            if self.obstructed == False:
                                self.image.blit(CONFIRMATION, (0, 0))
                                if self.game.mouse.pressed['M1']:
                                    self.game.selected_character.selected_skill.use_skill(self)
                            else:
                                self.game.selected_tile = self
                                self.game.menus['BATTLE'].cross = True

        self.traversable = False

        if self.game.selected_character.selected_skill != None:

            if self.hitbox.collidepoint(self.game.mouse.pos):
                self.game.selected_tile = self

            if self.being_targeted and self.targetable == False:
                self.image.blit(CONFIRMATION, (0, 0))

                self.being_targeted = False

            if self.targetable:

                if self.game.selected_character.selected_skill != None:

                    if self.game.selected_character.selected_skill.targets_enemies == True:
                        self.image.blit(ATTACKINDICATOR, (0, 0))

                        if self.game.selected_character.has_used_skill == False:

                            if self.being_targeted:
                                self.image.blit(CONFIRMATION, (0, 0))

                            self.being_targeted = False

                            if self.game.selected_character.selected_skill.targets_all_in_range == False:

                                if self.hitbox.collidepoint(self.game.mouse.pos):
                                    self.game.selected_tile = self
                                    if self.has_enemy:
                                        menu = self.game.menus['BATTLE']
                                        skill = self.game.selected_character.selected_skill

                                        for tile in menu.tiles:
                                            selected_tile = self.game.selected_tile
                                            distance = vec(tile.grid_pos) - vec(selected_tile.grid_pos)
                                            if distance.length() <= skill.splash:
                                                tile.being_targeted = True

                                        if self.game.mouse.pressed['M1']:
                                            menu = self.game.menus['BATTLE']
                                            targeted_tiles = []
                                            for tile in menu.tiles:
                                                if tile.being_targeted:
                                                    targeted_tiles.append(tile)
                                            self.game.selected_character.has_used_skill = True
                                            self.game.selected_character.selected_skill.use_skill(targeted_tiles)
                                    elif self.has_hero:
                                        self.game.selected_tile = self
                                        self.game.menus['BATTLE'].cross = True
                                    elif self.obstructed:
                                        self.game.selected_tile = self
                                        self.game.menus['BATTLE'].cross = True
                                    else:
                                        self.image.blit(CONFIRMATION, (0, 0))

                            else:
                                if self.has_enemy:
                                    self.image.blit(CONFIRMATION, (0, 0))
                                    self.being_targeted = True
                                    if self.hitbox.collidepoint(self.game.mouse.pos):
                                        if self.game.mouse.pressed['M1']:
                                            menu = self.game.menus['BATTLE']
                                            targeted_tiles = []
                                            for tile in menu.tiles:
                                                if tile.being_targeted:
                                                    targeted_tiles.append(tile)
                                            self.game.selected_character.has_used_skill = True
                                            self.game.selected_character.selected_skill.use_skill(targeted_tiles)

                if self.game.selected_character.selected_skill != None:

                    if self.game.selected_character.selected_skill.targets_enemies == False:
                        self.image.blit(HEALINDICATOR, (0, 0))

                        if self.game.selected_character.has_used_skill == False:

                            if self.being_targeted:
                                self.image.blit(CONFIRMATION, (0, 0))

                            self.being_targeted = False

                            if self.game.selected_character.selected_skill.targets_all_in_range == False:

                                if self.hitbox.collidepoint(self.game.mouse.pos):
                                    if self.has_hero:
                                        self.image.blit(CONFIRMATION, (0, 0))
                                        self.being_targeted = True
                                        if self.game.mouse.pressed['M1']:

                                            menu = self.game.menus['BATTLE']
                                            targeted_tiles = []
                                            for tile in menu.tiles:
                                                if tile.being_targeted:
                                                    targeted_tiles.append(tile)
                                            self.game.selected_character.has_used_skill = True
                                            self.game.selected_character.selected_skill.use_skill(targeted_tiles)
                                    elif self.has_enemy:
                                        self.game.selected_tile = self
                                        self.game.menus['BATTLE'].cross = True
                                    elif self.obstructed:
                                        self.game.selected_tile = self
                                        self.game.menus['BATTLE'].cross = True
                                    else:
                                        self.image.blit(CONFIRMATION, (0, 0))

                            else:
                                if self.has_hero:
                                    self.image.blit(CONFIRMATION, (0, 0))
                                    self.being_targeted = True
                                    if self.hitbox.collidepoint(self.game.mouse.pos):
                                        if self.game.mouse.pressed['M1']:
                                            menu = self.game.menus['BATTLE']
                                            targeted_tiles = []
                                            for tile in menu.tiles:
                                                if tile.being_targeted:
                                                    targeted_tiles.append(tile)
                                            self.game.selected_character.has_used_skill = True
                                            self.game.selected_character.selected_skill.use_skill(targeted_tiles)


        self.targetable = False
        self.has_enemy = False
        self.has_hero = False

class Obstacle(Tile):

    def __init__(self, game, x, y, image, menu):
        self.groups = game.obstacles
        p.sprite.Sprite.__init__(self, self.groups)

        self.game = game

        self.grid_pos = [x, y]

        self.image = image

        self.menu = menu

        for tile in self.game.tiles:

            if tile.grid_pos == self.grid_pos:
                tile.obstructed = True