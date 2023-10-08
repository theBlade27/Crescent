import pygame as p
import pytmx
from settings import *
from hero import *
from tileObject import *
from tiles import *
from enemy import *

class Map:

    def __init__(self, game, filename, menu = None):

        self.game = game
        self.file = pytmx.load_pygame(filename)
        self.width = self.file.width * TILE_SIZE * MAP_SCALE
        self.height = self.file.height * TILE_SIZE * MAP_SCALE
        self.hitbox = p.Rect(0, 0, self.width, self.height)
        self.menu = menu
    
    def generate_layer(self, surface, layer):

        for x, y, tile_id, in self.file.get_layer_by_name(layer):

            tile = self.file.get_tile_image_by_gid(tile_id)

            x *= MAP_SCALE
            y *= MAP_SCALE

            if tile:

                tile = p.transform.scale(tile, (TILE_SIZE * MAP_SCALE, TILE_SIZE * MAP_SCALE))

                properties = self.file.get_tile_properties_by_gid(tile_id)

                if layer == 'walls':
                    TileObject(self.game, tile, x * TILE_SIZE, y * TILE_SIZE, collidable = properties['collidable'])

                elif layer == 'interactables':
                    if properties['type'] == 'door':
                        DoorTile(self.game, tile, x * TILE_SIZE, y * TILE_SIZE)
                    else:
                        TileObject(self.game, tile, x * TILE_SIZE, y * TILE_SIZE, True, collidable = properties['collidable'])

                elif layer == 'decor':
                    TileObject(self.game, tile, x * TILE_SIZE, y * TILE_SIZE)

                elif layer == 'alerts':
                    TileObject(self.game, tile, x * TILE_SIZE, y * TILE_SIZE)

                else:
                    self.draw_tile(surface, tile, x, y)

    def generate_object_layer(self):
        
        for event in self.file.objects:

            if event.name == 'spawn':
                self.game.spawn_location = (event.x * MAP_SCALE, event.y * MAP_SCALE)

            if event.name == 'interaction':
                Interaction(self.game, event.x * MAP_SCALE, event.y * MAP_SCALE, event.description)

            if event.name == 'battle':
                BattleInteraction(self.game, event.x * MAP_SCALE, event.y * MAP_SCALE, event.description, event.encounter)

            if event.name == 'loot':
                Loot(self.game, event.x * MAP_SCALE, event.y * MAP_SCALE, event.description, event.loot)

    def generate_map(self, surface):

        self.generate_layer(surface, 'ground')
        self.generate_layer(surface, 'floordecor')
        self.generate_layer(surface, 'walls')
        self.generate_layer(surface, 'interactables')
        self.generate_layer(surface, 'decor')
        self.generate_layer(surface, 'alerts')

        self.generate_object_layer()

    def draw_tile(self, surface, tile, x , y):

        surface.blit(tile, (x * self.file.tilewidth, y * self.file.tileheight))

    def generate_battle_background(self):

        image = p.Surface((1080, 600))

        enemy_counter = 0
        battle = self.menu.battle

        for x, y, tile_id, in self.file.get_layer_by_name('ground'):

            tile = self.file.get_tile_image_by_gid(tile_id)

            grid_pos = [x, y]

            x *= MAP_SCALE
            y *= MAP_SCALE

            if tile:

                tile = p.transform.scale(tile, (TILE_SIZE * MAP_SCALE, TILE_SIZE * MAP_SCALE))

                self.draw_tile(image, tile, x, y)

                self.menu.tiles.append(Tile(self.game, grid_pos[0], grid_pos[1], tile, offset = [386, 218]))

        for x, y, tile_id, in self.file.get_layer_by_name('obstacles'):

            tile = self.file.get_tile_image_by_gid(tile_id)

            grid_pos = [x, y]

            x *= MAP_SCALE
            y *= MAP_SCALE

            if tile:

                tile = p.transform.scale(tile, (TILE_SIZE * MAP_SCALE, TILE_SIZE * MAP_SCALE))

                self.menu.objects.append(Obstacle(self.game, grid_pos[0], grid_pos[1], tile, self.menu))

        for event in self.file.objects:

            if event.name == 'player_spawn':

                self.menu.player_spawn = [event.x / TILE_SIZE, event.y / TILE_SIZE]
                self.menu.spawn_direction = event.direction

            if event.name == 'enemy_spawn':

                self.menu.enemies.append(Enemy(self.game, ENEMY_PARTIES[battle][enemy_counter], (event.x / TILE_SIZE, event.y / TILE_SIZE)))
                enemy_counter += 1

        return image

    def draw_map(self):

        image = p.Surface((self.width, self.height))
        self.generate_map(image)
        return image