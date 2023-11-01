import pygame as p
import pytmx
from settings import *
from hero import *
from tileObject import *
from tiles import *
from enemy import *



class Map(p.sprite.Sprite):

    # this class is used to draw the background the player walks on, as well as placing every single map object the player can interact with

    def __init__(self, game, filename, menu = None):

        self.game = game

        self.groups = game.all
        p.sprite.Sprite.__init__(self, self.groups)

        # the file is loaded
        
        self.file = pytmx.load_pygame(filename)

        # the dimensions of the map is calculated by multiplying the amount of tiles by the size of each tile by the MAP_SCALE
        # MAP_SCALE is a constant that determines how much each tile is scaled by
        # this is done because by default the tiles are quite small
        self.width = self.file.width * TILE_SIZE * MAP_SCALE
        self.height = self.file.height * TILE_SIZE * MAP_SCALE

        self.hitbox = p.Rect(0, 0, self.width, self.height)
        self.menu = menu
    
    def generate_layer(self, surface, layer):

        # this for loop iterates through every single tile in the layer passed in


        for x, y, tile_id, in self.file.get_layer_by_name(layer):

            # gets the tile image based on the tile id of the current tile

            tile = self.file.get_tile_image_by_gid(tile_id)

            # multiplies x and y by the map scale so tiles are placed at the correct coordinates

            x *= MAP_SCALE
            y *= MAP_SCALE

            # if there is a tile

            if tile:

                # get the correct image for the tile by scaling it to the size of a tile multiplied by the MAP_SCALE

                tile = p.transform.scale(tile, (TILE_SIZE * MAP_SCALE, TILE_SIZE * MAP_SCALE))

                # get the properties of the tile from its id

                properties = self.file.get_tile_properties_by_gid(tile_id)

                # based on the layer that is passed in, different tile objects are placed
                # this is why placing tiles in the correct layer on 'tiled' (the program used to make maps) is important

                # for example, every tile in the 'walls' layer will have a tile object placed at those coordinates that act as a wall that cannot be moved through

                if layer == 'walls':
                    TileObject(self.game, tile, x * TILE_SIZE, y * TILE_SIZE, collidable = properties['collidable'])

                elif layer == 'interactables':
                    # some special tiles, like doors, have their very own object, which is specified by their 'type' property, which is blank for other less unique objects like rocks
                    if properties['type'] == 'door':
                        DoorTile(self.game, tile, x * TILE_SIZE, y * TILE_SIZE)
                    elif properties['type'] == 'hero':
                        CharacterTile(self.game, tile, x * TILE_SIZE, y * TILE_SIZE)
                    else:
                        TileObject(self.game, tile, x * TILE_SIZE, y * TILE_SIZE, True, collidable = properties['collidable'])

                elif layer == 'decor':
                    TileObject(self.game, tile, x * TILE_SIZE, y * TILE_SIZE)

                elif layer == 'alerts':
                    AlertTile(self.game, tile, x * TILE_SIZE, y * TILE_SIZE)

                else:
                    # if the tile does not belong to a layer that needs tile objects to be placed, the tile is simply drawn to the surface that is passed into this function
                    self.draw_tile(surface, tile, x, y)

    def generate_object_layer(self):

        # this function deals with placing events that aren't associated with a tile, such as as spawn points, and places where you can access menus, such as the upgrade menu or trader menu
        
        for event in self.file.objects:

            # for example, if there is an event called 'spawn'

            if event.name == 'spawn':

                # the games spawn location is set to the events coordinates multiplied by MAP_SCALE
                self.game.spawn_location = (event.x * MAP_SCALE, event.y * MAP_SCALE)

            if event.name == 'character':
                GetNewCharacter(self.game, event.x * MAP_SCALE, event.y * MAP_SCALE, event.character, event.description)

            if event.name == 'interaction':
                Interaction(self.game, event.x * MAP_SCALE, event.y * MAP_SCALE, event.description)

            if event.name == 'battle':
                BattleInteraction(self.game, event.x * MAP_SCALE, event.y * MAP_SCALE, event.description, event.encounter, event.proximity)

            if event.name == 'loot':
                Loot(self.game, event.x * MAP_SCALE, event.y * MAP_SCALE, event.description, event.loot)

            if event.name == 'level':
                Level(self.game, event.x * MAP_SCALE, event.y * MAP_SCALE, event.description, event.level, event.stageclear)

            if event.name == 'blacksmith':
                Blacksmith(self.game, event.x * MAP_SCALE, event.y * MAP_SCALE)

            if event.name == 'trader':
                Trader(self.game, event.x * MAP_SCALE, event.y * MAP_SCALE)

    def generate_map(self, surface):

        # this function calls the other functions

        self.generate_object_layer()

        # it calls generate_layer() in an order such that the ground is on the bottom and everything else is in the correct order

        self.generate_layer(surface, 'ground')
        self.generate_layer(surface, 'floordecor')
        self.generate_layer(surface, 'walls')
        self.generate_layer(surface, 'interactables')
        self.generate_layer(surface, 'decor')
        self.generate_layer(surface, 'alerts')

    def draw_tile(self, surface, tile, x , y):

        # on the surface passed in, draw the tile at the coordinates passed in multiplied by the size of a tile

        surface.blit(tile, (x * self.file.tilewidth, y * self.file.tileheight))

    def generate_battle_background(self):

        # this function is very similiar to the function used to generate the exploration map, with a few differences

        # a surface the size of the map on which battles take place
        image = p.Surface((1080, 600))

        # keeps track of amount of enemies spawned
        enemy_counter = 0

        # this map is tied to a menu, and that menu is tied to a 'battle' object that keeps track of a battle, so it needs to know the amount of enemies
        battle = self.menu.battle

        for x, y, tile_id, in self.file.get_layer_by_name('ground'):

            tile = self.file.get_tile_image_by_gid(tile_id)

            # grid pos is the position of a tile on the battle grid, not of a tile on the screen
            # for example, the top left tile on a battle map would have a grid_pos of [0, 0]
            # the one directly to the right would have [1, 0]
            # this is done because each character inhabits a grid position, and they need to check each tile before moving to see if any other character is taking up that tile before moving

            grid_pos = [x, y]

            x *= MAP_SCALE
            y *= MAP_SCALE

            if tile:

                tile = p.transform.scale(tile, (TILE_SIZE * MAP_SCALE, TILE_SIZE * MAP_SCALE))

                self.draw_tile(image, tile, x, y)

                # adds the tile to menus list of tiles that it can use to check for characters later
                # the grid position is passed in, as well as the tiles image, and the offset so the battle map is not at the top left of the screen

                self.menu.tiles.append(Tile(self.game, grid_pos[0], grid_pos[1], tile, offset = [386, 218]))

        for x, y, tile_id, in self.file.get_layer_by_name('obstacles'):

            tile = self.file.get_tile_image_by_gid(tile_id)

            grid_pos = [x, y]

            x *= MAP_SCALE
            y *= MAP_SCALE

            if tile:

                tile = p.transform.scale(tile, (TILE_SIZE * MAP_SCALE, TILE_SIZE * MAP_SCALE))

                # obstacles are a type of tile that cannot be traversed by characters

                self.menu.objects.append(Obstacle(self.game, grid_pos[0], grid_pos[1], tile, self.menu))

        for event in self.file.objects:

            # spawns characters at the correct location on the battle map

            if event.name == 'player_spawn':

                # the coordinates need to be divided by TILE_SIZE because on 'tiled' the events coordinates are dependent on the size of tiles, but we need the position on the grid in terms of tiles, not pixels
                self.menu.player_spawn = [event.x / TILE_SIZE, event.y / TILE_SIZE]

                self.menu.spawn_direction = event.direction

            if event.name == 'enemy_spawn':

                # when there is an event called 'enemy_spawn'
                # the dictionary called ENEMY_PARTIES is accessed
                # the key is the battle associated with battle this map is associated with
                # this returns a list of enemies
                # the 'enemy_counter' acts as the index for which enemy on this list is going to be spawned
                # the enemy is spawned at the correct coordinates

                self.menu.enemies.append(Enemy(self.game, ENEMY_PARTIES[battle][enemy_counter], (event.x / TILE_SIZE, event.y / TILE_SIZE)))

                # enemy_counter is incremented
                enemy_counter += 1

        # the image of the map is returned
        return image

    def draw_map(self):

        # creates a surface large enough to fit the map

        image = p.Surface((self.width, self.height))

        # draws to this surface
        self.generate_map(image)

        # returns the surface
        return image