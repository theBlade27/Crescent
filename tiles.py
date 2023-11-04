import pygame as p
from sprite import *
from settings import *
vec = p.math.Vector2

class Tile(p.sprite.Sprite):

    # these tiles are present only in battle, and track whether they have a hero or enemy on them, and can be clicked on when a skill is selected in order to choose a target

    def __init__(self, game, x, y, image, offset):
        self.groups = game.tiles, game.all
        p.sprite.Sprite.__init__(self, self.groups)

        self.game = game

        self.grid_pos = [x, y]

        self.image = image
        self.background = self.image.copy()

        self.traversable = False # whether this tile can be moved to
        self.targetable = False # whether this tile can be targetted by the skill that is selected by the selected character
        self.obstructed = False # whether this tile is being blocked by something
        self.has_enemy = False # whether this tile has a hero
        self.has_hero = False # whether this tile has an enemy
        self.being_targeted = False # whether this tile is currently being targetted by the skill that is selected by the selected character

        self.offset = offset

        self.hitbox = p.Rect(x * MAP_SCALE * TILE_SIZE + offset[0], y * MAP_SCALE * TILE_SIZE + offset[1], 60, 60)

    def update(self):

        # the image is reset to the default image this tile had when it was first created
        self.image = self.background.copy()
            
        # if the player has control over their character
        if self.game.actingout == False:

            # if the mouse is hovering over this tile

            if self.hitbox.collidepoint(self.game.mouse.pos):

                # if this tile has a character

                if self.has_enemy or self.has_hero:

                    # find the preview menu associated with this character and changes its border to white so the player knows which character their mouse is hovering over

                    for character in self.game.menus['BATTLE'].characters:

                        if character.grid_pos == self.grid_pos:

                            for menu in self.game.menus:
                                if menu == 'HERO1' or menu == 'HERO2' or menu == 'HERO3' or menu == 'HERO4':
                                    if self.game.menus[menu].hero == character:
                                        self.game.menus[menu].colour = WHITE
                                        self.game.menus[menu].update()
                                if menu == 'ENEMY1' or menu == 'ENEMY2' or menu == 'ENEMY3' or menu == 'ENEMY4' or menu == 'ENEMY5' or menu == 'ENEMY6':
                                    if self.game.menus[menu].enemy == character:
                                        self.game.menus[menu].colour = WHITE
                                        self.game.menus[menu].update()

                if self.game.mouse.pressed['M2']:

                    # open the inventory with the character as an argument, this will show all the characters stats

                    if self.has_enemy or self.has_hero:

                        for character in self.game.menus['BATTLE'].characters:

                            if character.grid_pos == self.grid_pos:

                                self.game.open_menu('INVENTORY', character)
                                self.game.menus['INVENTORY'].hero = character

            # if this tile can be moved to (whether or not this tile is traversable is changed by the selected character when the player has the move skill selected)

            if self.traversable:

                # if the player hasnt used a skill and hasnt moved

                if self.game.selected_character.has_used_skill == False:
                        
                        if self.game.selected_character.has_moved == False:

                            # draw a white overlay over this tile

                            self.image.blit(MOVEMENTINDICATOR, (0, 0))

                            # if the mouse is hovering over this tile

                            if self.hitbox.collidepoint(self.game.mouse.pos):

                                # if this tile isnt obstructed
                                
                                if self.obstructed == False:

                                    # draw a confirmation marker on top of this tile
                                    self.image.blit(CONFIRMATION, (0, 0))

                                    if self.game.mouse.pressed['M1']:

                                        # move the character to this tile
                                        self.game.selected_character.selected_skill.use_skill(self)

                                # otherwise, draw a red cross over this tile
                                else:
                                    self.game.selected_tile = self
                                    self.game.menus['BATTLE'].cross = True

            # reset whether this tile is traversable
            self.traversable = False

            # if the player has selected a skill

            if self.game.selected_character.selected_skill != None:

                # if the mouse is hovering over this tile, the games selected tile is this one

                if self.hitbox.collidepoint(self.game.mouse.pos):
                    self.game.selected_tile = self

                if self.being_targeted and self.targetable == False:
                    self.image.blit(CONFIRMATION, (0, 0))

                    self.being_targeted = False

                # if this tile is targetable (whether or not this tile is targetable is changed by the selected character when the player has a skill selected)

                if self.targetable:

                    if self.game.selected_character.selected_skill != None:

                        # if this skill targets enemies, draw a red overlay over this tile
                        if self.game.selected_character.selected_skill.targets_enemies == True:
                            self.image.blit(ATTACKINDICATOR, (0, 0))

                            # if the hero hasnt used a skill yet
                            if self.game.selected_character.has_used_skill == False:

                                if self.being_targeted:
                                    self.image.blit(CONFIRMATION, (0, 0))

                                self.being_targeted = False

                                # if their skill isnt one that targets every character in range

                                if self.game.selected_character.selected_skill.targets_all_in_range == False:

                                    if self.hitbox.collidepoint(self.game.mouse.pos):
                                        self.game.selected_tile = self

                                        # if this tile has an enemy
                                        if self.has_enemy:

                                            menu = self.game.menus['BATTLE']
                                            skill = self.game.selected_character.selected_skill

                                            # if the skills splash distance is less than the distance from this tile to the tile the mosue is hovering over, this tile is also being targeted

                                            for tile in menu.tiles:
                                                selected_tile = self.game.selected_tile
                                                distance = vec(tile.grid_pos) - vec(selected_tile.grid_pos)
                                                if distance.length() <= skill.splash:
                                                    tile.being_targeted = True

                                            # if the player presses M1

                                            if self.game.mouse.pressed['M1']:
                                                menu = self.game.menus['BATTLE']

                                                # get a list of every tile that is being targeted
                                                targeted_tiles = []
                                                for tile in menu.tiles:
                                                    if tile.being_targeted:
                                                        targeted_tiles.append(tile)
                                                self.game.selected_character.has_used_skill = True

                                                # use the skill on every tile that has been targeted
                                                self.game.selected_character.selected_skill.use_skill(targeted_tiles)

                                        # otherwise if this tile doesnt have an enemy, draw a cross over this tile
                                        elif self.has_hero:
                                            self.game.selected_tile = self
                                            self.game.menus['BATTLE'].cross = True
                                        elif self.obstructed:
                                            self.game.selected_tile = self
                                            self.game.menus['BATTLE'].cross = True
                                        else:
                                            self.image.blit(CONFIRMATION, (0, 0))

                                # otherwise, if their skill targets every enemy in its range
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

                        # same thing as the code above, but instead for skills that target heros
                        # a green overlay is drawn over the tiles instead
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


            # everything is reset again

            self.targetable = False
            self.has_enemy = False
            self.has_hero = False

class Obstacle(Tile):

    def __init__(self, game, x, y, image, menu):
        self.groups = game.obstacles, game.all
        p.sprite.Sprite.__init__(self, self.groups)

        self.game = game

        self.grid_pos = [x, y]

        self.image = image

        self.menu = menu

        # makes the tile this obstacle was placed on obstructed

        for tile in self.game.tiles:

            if tile.grid_pos == self.grid_pos:
                tile.obstructed = True