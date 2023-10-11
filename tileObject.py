import pygame as p
from settings import *
from sprite import *
from camera import *
from item import *
from hero import *
vec = p.math.Vector2

class TileObject(p.sprite.Sprite):

    def __init__(self, game, image, x, y, interactable = False, collidable = False):

        self.groups = game.tile_objects, game.all
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
            
class Interaction(p.sprite.Sprite):

    def __init__(self, game, x, y, description):

        self.groups = game.interactable_objects, game.all
        p.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        
        self.pos = [x, y]
        self.hitbox = p.Rect(x, y, 20 * MAP_SCALE, 20 * MAP_SCALE)

        self.description = description
        self.alert_visible = True

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

    def __init__(self, game, x, y, description, type, proximity):
        super().__init__(game, x, y, description)

        self.description += '\nSTART BATTLE?'
        self.type = type
        self.beaten = False
        self.alert_visible = True
        self.proximity = proximity

    def update(self):

        if self.beaten == False:

            self.alert_visible = True
    
            accessible = True

            character_location = self.game.camera_focus.pos
            distance_to_target = character_location - vec((self.pos[0] + 30), (self.pos[1] + 30))

            if distance_to_target.length() > INTERACT_RADIUS:
                accessible = False

            if self.proximity:
                if distance_to_target.length() < BATTLE_RADIUS:
                    self.game.start_battle(self.type)
                    self.game.last_interacted = self
                    sound = p.mixer.Sound(BLIP_SOUND)
                    sound.play()

                
            if self.hitbox.collidepoint(self.game.camera.apply_mouse()):
                self.game.mouse.image = self.game.mouse.images[2]
                if accessible == True:

                    self.game.textbox_text = self.description
                    self.game.menus['TOP'].images['TEXT'].update()
                    self.game.textbox_portrait = Sprite(PORTRAITS, scale = 8).get_sprite(0, 0, 20, 20)
                    self.game.menus['TOP'].images['PORTRAIT'].update()

                    if self.game.mouse.pressed['M1']:
                        self.game.start_battle(self.type)
                        self.game.last_interacted = self
                        sound = p.mixer.Sound(BLIP_SOUND)
                        sound.play()

        elif self.beaten == True:

            self.alert_visible = False

class GetNewCharacter(Interaction):

    def __init__(self, game, x, y, character, description):
        super().__init__(game, x, y, description)

        self.description += '\nADD A NEW CHARACTER TO YOUR PARTY?'

        self.character = character

        self.interacted = False
        self.alert_visible = True


    def update(self):
        
        
        if self.interacted == False:

            self.alert_visible = True

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

                    if self.game.mouse.pressed['M1']:

                        for i in range(len(self.game.hero_party)):

                            if self.game.hero_party[i] == None:

                                self.game.hero_party[i] = Hero(self.game, self.character, self.pos)
                                self.game.menus['HERO' + str(i + 1)].update()
                                self.game.menus['HERO' + str(i + 1)].update_images()
                                
                                self.interacted = True
                                self.alert_visible = False

                                break

    

class Level(Interaction):

    def __init__(self, game, x, y, description, type, stageclear):
        super().__init__(game, x, y, description)

        self.description += '\nNEXT STAGE?'
        self.type = type
        self.alert_visible = False
        self.stageclear = stageclear

    def update(self):

        if self.stageclear == True:

            if self.game.stageclear:

                self.alert_visible = True
            
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

                        if self.game.mouse.pressed['M1']:

                            self.game.next_level(MAPS[self.type])

        else:

            self.alert_visible = True
            
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

                    if self.game.mouse.pressed['M1']:

                        self.game.next_level(MAPS[self.type])

        


        

class Loot(Interaction):

    def __init__(self, game, x, y, description, type):
        super().__init__(game, x, y, description)

        self.description += '\nLOOT?'
        self.type = type
        self.looted = False
        self.alert_visible = True
        self.inventory = []

        self.generate_loot()

    def generate_loot(self):

        self.loot_list = []
        self.inventory = []

        number_of_common = random.randint(1, 2)
        number_of_rare = random.randint(1, 1)
        number_of_very_rare = random.randint(0, 1)

        if self.type == 'TUTORIALCHEST':

            self.inventory = [Bandage(self.game)]

        elif self.type == 'L2CHEST':

            self.inventory = [Bandage(self.game)]

        else:

            for i in range(number_of_common):
                self.loot_list.append(random.choice(LOOT_TABLE[self.type][0]))

            for i in range(number_of_rare):
                self.loot_list.append(random.choice(LOOT_TABLE[self.type][1]))

            for i in range(number_of_very_rare):
                self.loot_list.append(random.choice(LOOT_TABLE[self.type][2]))

            for item in self.loot_list:

                if item == 'BANDAGE':

                    self.inventory.append(Bandage(self.game))

                if item == 'TORCH':

                    self.inventory.append(Torch(self.game))

    def update(self):

        if self.looted == False:

            self.alert_visible = True
    
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

                    if self.game.mouse.pressed['M1']:
                        self.game.open_menu('LOOT', loot_list = self.inventory)
                        self.looted = True
                        sound = p.mixer.Sound(BLIP_SOUND)
                        sound.play()

        else:

            self.alert_visible = False
        
class CollisionHitbox(p.sprite.Sprite):

    def __init__(self, game, x, y):

        self.groups = game.collision_hitboxes, game.all
        p.sprite.Sprite.__init__(self, self.groups)

        self.pos = [x, y]

        self.collidable = True

        self.hitbox = p.Rect(x, y, 20 * MAP_SCALE, 20 * MAP_SCALE)

class AlertTile(TileObject):

    def __init__(self, game, image, x, y):
        super().__init__(game, image, x, y)

        self.regular_image = image.copy()
        self.invisible = Sprite(TILESET, scale = MAP_SCALE).get_sprite(0, 160, 20, 20)
        self.image = self.regular_image.copy()

        for object in self.game.interactable_objects:

            if [object.pos[0], object.pos[1]] == [self.pos[0], self.pos[1] + 60]:

                self.object = object

    def update(self):

        if self.object.alert_visible == True:

            self.image = self.regular_image

        elif self.object.alert_visible == False:

            self.image = self.invisible

class CharacterTile(TileObject):

    def __init__(self, game, image, x, y):
        super().__init__(game, image, x, y)

        self.regular_image = image.copy()
        self.invisible = Sprite(TILESET, scale = MAP_SCALE).get_sprite(0, 160, 20, 20)
        self.image = self.regular_image.copy()

        for object in self.game.interactable_objects:

            if [object.pos[0], object.pos[1]] == [self.pos[0], self.pos[1]]:

                self.object = object

    def update(self):

        if self.object.interacted == False:

            self.image = self.regular_image

        elif self.object.interacted == True:

            self.image = self.invisible

        



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