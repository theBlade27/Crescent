import pygame as p
from settings import *
from sprite import *
from camera import *
from map import *
vec = p.math.Vector2

class TileObject(p.sprite.Sprite):

    def __init__(self, game, image, x, y, interactable = False, collidable = False):

        self.groups = game.tile_objects
        p.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = image
        self.background = self.image.copy()

        self.pos = [x, y]
        self.grid_pos = [self.pos[0] / (MAP_SCALE * TILE_SIZE), self.pos[1] / (MAP_SCALE * TILE_SIZE)]
        self.hitbox = p.Rect(x, y, 20 * MAP_SCALE, 20 * MAP_SCALE)
        
        self.interactable = interactable
        self.collidable = collidable
        self.movable = False

        if self.collidable:
            self.collision_hitbox = CollisionHitbox(self.game, self.pos[0], self.pos[1])

        if self.interactable:
            self.game.interactable_objects.add(self)
            
class Interaction(p.sprite.Sprite):

    def __init__(self, game, x, y, description):

        self.groups = game.interactable_objects
        p.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        
        self.pos = [x, y]
        self.hitbox = p.Rect(x, y, 20 * MAP_SCALE, 20 * MAP_SCALE)

        self.description = description

    def update(self):

        accessible = True

        character_location = self.game.camera_focus.pos
        distance_to_target = character_location - vec((self.pos[0] + 30), (self.pos[1] + 30))

        if distance_to_target.length() > INTERACT_RADIUS:
            accessible = False
             
        if self.hitbox.collidepoint(self.game.camera.apply_mouse()):
            self.game.mouse.image = self.game.mouse.images[2]
            if accessible == True:

                self.game.textbox_text = self.description
                self.game.menus['TOP'].images['TEXT'].update()
                self.game.textbox_portrait = Sprite(PORTRAITS, scale = 8).get_sprite(20, 0, 20, 20)
                self.game.menus['TOP'].images['PORTRAIT'].update()

class BattleInteraction(Interaction):

    def __init__(self, game, x, y, description, type):
        super().__init__(game, x, y, description)

        self.description += '\nSTART BATTLE? (Y)'
        self.type = type

    def update(self):
    
        accessible = True

        character_location = self.game.camera_focus.pos
        distance_to_target = character_location - vec((self.pos[0] + 30), (self.pos[1] + 30))

        if distance_to_target.length() > INTERACT_RADIUS:
            accessible = False
             
        if self.hitbox.collidepoint(self.game.camera.apply_mouse()):
            self.game.mouse.image = self.game.mouse.images[2]
            if accessible == True:

                self.game.textbox_text = self.description
                self.game.menus['TOP'].images['TEXT'].update()
                self.game.textbox_portrait = Sprite(PORTRAITS, scale = 8).get_sprite(0, 0, 20, 20)
                self.game.menus['TOP'].images['PORTRAIT'].update()

                pressed_keys = p.key.get_pressed()

                if pressed_keys[p.K_y]:
                    self.game.start_battle(self.type)
                    sound = p.mixer.Sound(BLIP_SOUND)
                    sound.play()


        
class CollisionHitbox(p.sprite.Sprite):

    def __init__(self, game, x, y):

        self.groups = game.collision_hitboxes
        p.sprite.Sprite.__init__(self, self.groups)

        self.pos = [x, y]

        self.collidable = True

        self.hitbox = p.Rect(x, y, 20 * MAP_SCALE, 20 * MAP_SCALE)

class DoorTile(TileObject):

    def __init__(self, game, image, x, y):
        super().__init__(game, image, x, y, True, True)

        self.closed = True

        self.closed_image = Sprite(TILESET, scale = MAP_SCALE).get_sprite(160, 220, 20, 20)
        self.open_image = Sprite(TILESET, scale = MAP_SCALE).get_sprite(180, 220, 20, 20)

    def update(self):

        accessible = True
        for character in self.game.hero_party:
            if character != None:
                if character.exploration_character.hitbox.colliderect(self.hitbox):
                    accessible = False

        character_location = self.game.camera_focus.pos
        distance_to_target = character_location - vec((self.pos[0] + 30), (self.pos[1] + 30))

        if distance_to_target.length() > INTERACT_RADIUS:
            accessible = False
             
        if self.hitbox.collidepoint(self.game.camera.apply_mouse()):
            if self.game.mouse.pressed['M1']:

                if accessible == True:
                    self.closed = not self.closed
                    sound = p.mixer.Sound(BLIP_SOUND)
                    sound.play()

        if self.closed:

            self.image = self.closed_image
            self.collision_hitbox.collidable = True

        else:

            self.image = self.open_image
            self.collision_hitbox.collidable = False