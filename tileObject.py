import pygame as p
from settings import *
from sprite import *
from camera import *
from item import *
from hero import *
vec = p.math.Vector2

class TileObject(p.sprite.Sprite):

    # objects of this class are what the player interacts with when they move around the map

    def __init__(self, game, image, x, y, interactable = False, collidable = False):

        self.groups = game.tile_objects, game.all
        p.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = image
        self.background = self.image.copy()

        
        self.pos = [x, y]
        self.hitbox = p.Rect(x, y, 20 * MAP_SCALE, 20 * MAP_SCALE)
        
        self.interactable = interactable # whether this tile does anything when clicked on
        self.collidable = collidable # whether the player can collide with this tile

        if self.collidable:
            # if this tile is collidable, create a collision hitbox at this position
            self.collision_hitbox = CollisionHitbox(self.game, self.pos[0], self.pos[1])
            
class Interaction(p.sprite.Sprite):

    def __init__(self, game, x, y, description):

        self.groups = game.interactable_objects, game.all
        p.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        
        self.pos = [x, y]
        self.hitbox = p.Rect(x, y, 20 * MAP_SCALE, 20 * MAP_SCALE)

        self.description = description # description that shows up when the mouse hovers over this tile
        self.alert_visible = True # alerts appear above this tile if this is True

    def update(self):

        accessible = True

        # the distance between the player controlled character and the position of this object is calculated

        character_location = self.game.camera_focus.pos
        distance_to_target = character_location - vec((self.pos[0] + 30), (self.pos[1] + 30))

        # if this distance is greater than INTERACT_RADIUS, the object is not accessible

        if distance_to_target.length() > INTERACT_RADIUS:
            accessible = False

        # if the mouse is hovering over this object
             
        if self.hitbox.collidepoint(self.game.camera.apply_mouse()):

            # change the mouse image to a magnifying glass
            self.game.mouse.image = self.game.mouse.images[2]

            # if this object is accessible
            if accessible == True:

                # display the description of this object at the top of the screen
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
        self.proximity = proximity # some battles start as soon as you go near them, while others need to by interacted with directly

    def update(self):

        # if the battle associated with this object hasnt been beaten yet

        if self.beaten == False:

            # the alert above this object needs to appear on the map

            self.alert_visible = True
    
            accessible = True

            character_location = self.game.camera_focus.pos
            distance_to_target = character_location - vec((self.pos[0] + 30), (self.pos[1] + 30))

            if distance_to_target.length() > INTERACT_RADIUS:
                accessible = False

            if self.proximity:

                # if the distance is less than BATTLE_RADIUS
                if distance_to_target.length() < BATTLE_RADIUS:
                    # start a battle
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

                    pressed_keys = p.key.get_pressed()

                    # when the player presses e on their keyboard
                    if pressed_keys[p.K_e]:
                        self.game.start_battle(self.type)
                        self.game.last_interacted = self
                        sound = p.mixer.Sound(BLIP_SOUND)
                        sound.play()

        elif self.beaten == True:

            # once the battle is beaten, the alert no longer needs to be visible

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

                    pressed_keys = p.key.get_pressed()
                    if pressed_keys[p.K_e]:

                        for i in range(len(self.game.hero_party)):

                            # add a hero to the players party in the first empty slot

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

        # if the stage has been cleared

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

                        pressed_keys = p.key.get_pressed()
                        if pressed_keys[p.K_e]:

                            # go to the next level

                            self.game.next_level(MAPS[self.type])

        # if the stage has not been cleared yet

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

                    pressed_keys = p.key.get_pressed()
                    if pressed_keys[p.K_e]:

                        self.game.next_level(MAPS[self.type])

        


        

class Loot(Interaction):

    def __init__(self, game, x, y, description, type):
        super().__init__(game, x, y, description)

        self.description += '\nLOOT?'
        self.type = type
        self.looted = False
        self.alert_visible = True
        self.inventory = []

        # generate some loot for this object that will show up to the player once they interact with this object

        self.inventory, self.money = self.game.generate_loot(self.type)

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

                    pressed_keys = p.key.get_pressed()
                    if pressed_keys[p.K_e]:

                        # open the loot menu with the loot generated earlier as an argument

                        self.game.open_menu('LOOT', loot_list = self.inventory, money = self.money)

                        # increase the players money
                        self.game.money += self.money
                        self.looted = True
                        sound = p.mixer.Sound(BLIP_SOUND)
                        sound.play()

                        for menu in self.game.menus.values():
                            menu.update_images()

        else:

            self.alert_visible = False


class Blacksmith(Interaction):

    def __init__(self, game, x, y):
        super().__init__(game, x, y, 'IT\'S A BLACKSMITH!')

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
                if pressed_keys[p.K_e]:

                    # bring up the upgrade menu
                    self.game.open_menu('UPGRADE')
                    sound = p.mixer.Sound(BLIP_SOUND)
                    sound.play()

                    for menu in self.game.menus.values():
                        menu.update_images()

class Trader(Interaction):

    def __init__(self, game, x, y):
        super().__init__(game, x, y, 'IT\'S A TRADER!')

        # generate some items for the trader to sell
        # the trader has more items than other loot pools, so the amount needed of each rarity of item is passed in as arguments
        self.inventory, money = self.game.generate_loot('TRADER', [2, 4], [1, 3], [1, 2])

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
                if pressed_keys[p.K_e]:

                    # bring up the trader menu with the generated loot as an argument
                    self.game.open_menu('TRADER', items = self.inventory, object = self)
                    sound = p.mixer.Sound(BLIP_SOUND)
                    sound.play()

                    for menu in self.game.menus.values():
                        menu.update_images()
        
        
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

        # finds the object that this needs to keep track of by finding an object directly below this one

        for object in self.game.interactable_objects:

            if [object.pos[0], object.pos[1]] == [self.pos[0], self.pos[1] + 60]:

                self.object = object

    def update(self):

        # if the object directly below this one has 'alert_visible' to True, appear normally

        if self.object.alert_visible == True:

            self.image = self.regular_image

        # otherwise, appear invisible

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
                # if a character is currently inside the doors hitbox, it cannot be closed
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

        # changes the image of the tile based on whether the door is closed or not

        if self.closed:

            self.image = self.closed_image
            self.collision_hitbox.collidable = True

        else:

            self.image = self.open_image
            self.collision_hitbox.collidable = False