import pygame as p
from sprite import *
from settings import *
vec = p.math.Vector2

class ExplorationCharacter(p.sprite.Sprite):

    # objects of this class each correspond to one of the heros in the players party
    # they deal with moving around the map and colliding with objects

    def __init__(self, game, type, pos, hero):

        self.groups = game.exploration_characters
        p.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        # this variable determines the type of hero, for example the player starts with 'THE BLADE', the knight characters, so 'BLADE' would be passed in as the parameter
        self.type = type

        # the image is loaded from the character spritesheet dictionary with the characters name as the key, and then scaled to be the same scale as the map
        self.spritesheet = Sprite(CHARACTER_SPRITESHEETS[self.type], MAP_SCALE)
        self.hero = hero

        # these booleans are used to keep track of whether the character is moving and whether they need to face left or right
        self.running = False
        self.flipped = False

        # these keep track of what frame the animation is on when the last time the image was changed
        self.last_update = 0
        self.current_frame = 0

        # these three variables deal with movement, and will be explained further in the movement functions
        self.pos = vec(pos[0], pos[1])
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        # each character is a slightly different size so their positions in their spritesheet is slightly different

        if self.type == 'BLADE':
            
            # animations for when the character is standing still
            self.idleanimations = [
                self.spritesheet.get_sprite(5, 3, 10, 17),
                self.spritesheet.get_sprite(25, 3, 10, 17)
            ]

            # animations for when the character is moving
            self.runanimations = [
                self.spritesheet.get_sprite(5, 3, 10, 17),
                self.spritesheet.get_sprite(45, 3, 10, 17),
                self.spritesheet.get_sprite(5, 3, 10, 17),
                self.spritesheet.get_sprite(65, 3, 10, 17)
            ]

        if self.type == 'ARCANE':
            
            self.idleanimations = [
                self.spritesheet.get_sprite(5, 2, 13, 18),
                self.spritesheet.get_sprite(25, 2, 13, 18)
            ]

            self.runanimations = [
                self.spritesheet.get_sprite(5, 2, 13, 18),
                self.spritesheet.get_sprite(45, 2, 13, 18),
                self.spritesheet.get_sprite(5, 2, 13, 18),
                self.spritesheet.get_sprite(65, 2, 13, 18)
            ]

        if self.type == 'BREACH':
            
            self.idleanimations = [
                self.spritesheet.get_sprite(4, 3, 10, 17),
                self.spritesheet.get_sprite(24, 3, 10, 17)
            ]

            self.runanimations = [
                self.spritesheet.get_sprite(4, 3, 10, 17),
                self.spritesheet.get_sprite(44, 3, 10, 17),
                self.spritesheet.get_sprite(4, 3, 10, 17),
                self.spritesheet.get_sprite(64, 3, 10, 17)
            ]

        if self.type == 'FORTRESS':

            self.idleanimations = [
                self.spritesheet.get_sprite(3, 1, 14, 19),
                self.spritesheet.get_sprite(23, 1, 14, 19)
            ]

            self.runanimations = [
                self.spritesheet.get_sprite(3, 1, 14, 19),
                self.spritesheet.get_sprite(43, 1, 14, 19),
                self.spritesheet.get_sprite(3, 1, 14, 19),
                self.spritesheet.get_sprite(63, 1, 14, 19)
            ]

        self.image = self.idleanimations[0]
        self.rect = self.image.get_rect()
        self.rect.center = (pos[0], pos[1])
        self.hitbox = self.rect

    def update(self):

        self.running = True

        self.calculate_acceleration()
        self.calculate_velocity()
        self.calculate_position()

        # after velocity has been calculated, if the character has no velocity, they are not 'running', so the idle animation will play
        if self.vel.x == 0 and self.vel.y == 0:
            self.running = False

        self.play_animations()

    def calculate_acceleration(self):

        # makes sure that 'self.pos' is a vector, as it needs to be a vector for comparisons to work
        self.pos = vec(self.pos[0], self.pos[1])

        # acceleration is set to 0 for every character
        self.acc = vec(0, 0)

        # self.game.camera_focus is always the character the player is controlling
        if self.game.camera_focus == self:

            # when WASD are pressed, only the player controlled character gains acceleration in the corresponding direction

            pressed_keys = p.key.get_pressed()
            if pressed_keys[p.K_s]:
                self.acc.y = ACCELERATION
            if pressed_keys[p.K_w]:
                self.acc.y = -ACCELERATION
            if pressed_keys[p.K_d]:
                self.acc.x = ACCELERATION
            if pressed_keys[p.K_a]:
                self.acc.x = -ACCELERATION

            # this increments the games ticks whenever the player presses WASD
            # this makes sure effects such as hunger and bleeding progress

            if self.acc.length() > 0:
                self.game.ticks += 1
                self.game.tick_check()

        else:

            if self.game.battle_mode == False:

                if self.game.camera_focus != self:

                    # this section of code only applies to non player controlled characters

                    # the location of the player controlled character is set to a variable
                    target_location = self.game.selected_character.exploration_character.pos

                    # the distance vector between this character and the player controlled character is found by subtracting the position vector of this character from the position vector of the player controlled character
                    distance_to_target = target_location - self.pos

                    # if the length of this vector is greater than the FOLLOW_DISTANCE, the character needs to move closer
                    if distance_to_target.length() > FOLLOW_DISTANCE:
                        # so the rotation needed is calculated from the distance vector
                        rotation = distance_to_target.angle_to(vec(1, 0))
                        # the acceleration is set to a vector that has been rotated to point towards the player controlled character
                        self.acc = vec(1, 0).rotate(-rotation)
                        # and finally the acceleration is scaled to the correct magnitude
                        self.acc.scale_to_length(ACCELERATION)

                    for hero in self.game.hero_party:

                        # this section of code makes non player controlled characters repel each other so they dont clump up

                        if hero != None:
                            # this if statement makes sure the character doesnt repel themselves
                            if hero.exploration_character != self:
                                # the distance vector between this character and the other character is found by subtracting the position vector of the other character from the position vector of this character
                                distance_from_hero = self.pos - hero.exploration_character.pos
                                # if the length of this distance is greater than 0 and smaller than the repulsion radius
                                if 0 < distance_from_hero.length() < REPULSION_RADIUS:
                                    # the acceleration is set to a vector which is the same as the distance, but unlike the following player code it is in the other direction
                                    self.acc += distance_from_hero.normalize()
                                    # this if statement prevents crashes as [0, 0] cannot be scaled
                                    if self.acc != [0, 0]:
                                        # scales the acceleration to the correct magnitude
                                        self.acc.scale_to_length(ACCELERATION)

        # the velocity multiplied by the FRICTION is added to the acceleration
        # this makes it so they slow down to a stop smoothly after WASD stops being pressed
        self.acc += self.vel * FRICTION

    def calculate_velocity(self):

        # the velocity is changed by the acceleration
        # when acceleration is positive, (the player is pressing a key) the velocity is increased
        # when acceleration is negative, (the player has stopped pressing keys), the velocity is decreased

        self.vel += self.acc

        # this reduces velocity to 0 if it is below a certain number, so the player comes to a full stop instead of slowing down forever
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        if abs(self.vel.y) < 0.1:
            self.vel.y = 0

        # sets 'self.flipped' to True or False based on whether the x velocity is positive or negative
        if self.vel.x > 0:
            self.flipped = False
        elif self.vel.x < 0:
            self.flipped = True

    def calculate_position(self):

        # the rects (a rectangle that is the same as the players hitbox) position, is set to the players position
        # finally, the position of the character is changed by the velocity, plus the acceleration multiplied by 0.5
        self.rect.center = self.pos
        self.pos += self.vel + 0.5 * self.acc

        # the reason that collisions has to be checked seperately for the x direction and then the y direction is that if both are done simultaneously, unexpected behaviour happens and sometimes the characters clips around corners

        # the hitboxs x position is set to the players x position
        self.hitbox.centerx = self.pos.x
        # hitbox is checked for collisions in the x axis
        self.checkgroupcollisions(self, self.game.collision_hitboxes, 'x')

        # same but for y axis
        self.hitbox.centery = self.pos.y
        self.checkgroupcollisions(self, self.game.collision_hitboxes, 'y')

        # the rect is set to the same position as the hitbox
        self.rect.center = self.hitbox.center

    def play_animations(self):

        now = p.time.get_ticks()

        if self.running:
            # if 100 milliseconds have passed since the last update
            if now - self.last_update > 100:
                # set the time of the last update to now
                self.last_update = now
                # change the current frame to the next one in list of frames
                # the remainder is found to allow the current frame to be reset to 0 when the last item in the list has been reached
                self.current_frame = (self.current_frame + 1) % len(self.runanimations)
                # the image is the flipped based on whether 'self.flipped' is true or false
                self.image = p.transform.flip(self.runanimations[self.current_frame], self.flipped, False)
        
        else:
            if now - self.last_update > 1000:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.idleanimations)
                self.image = p.transform.flip(self.idleanimations[self.current_frame], self.flipped, False)

    def checkcollision(self, object1, object2):

        # returns whether object1s hitbox has collided with object2s hitbox

        return object1.hitbox.colliderect(object2.hitbox)
    
    def checkgroupcollisions(self, object, group, axis):

        # collisions is a list of all the sprites that the object has collided with
        # the argument 'object' is the object that is going to be checked for collisions
        # the argument 'group' is the group that the object will check each item for collision with
        # the argument False means that the object is not killed if there is a collision
        # the final argument is the function used to check each individual collision
        collisions = p.sprite.spritecollide(object, group, False, self.checkcollision)

        if group == self.game.collision_hitboxes:

            if axis == 'x':
                if collisions:

                    # if the first tile in the list is a collidable object

                    if collisions[0].collidable:

                        # if the tiles hitboxs center is further right than the objects (the players) hitboxs center

                        if collisions[0].hitbox.centerx > object.hitbox.centerx:
                            # the objects position is set to the hitboxs left minus the the objects hitboxs width
                            # this results in the objects hitboxs left side touching the tiles hitboxs right side
                            object.pos.x = int(collisions[0].hitbox.left - object.hitbox.width/2)

                        # the same but for the other direction
                        if collisions[0].hitbox.centerx < object.hitbox.centerx:
                            object.pos.x = int(collisions[0].hitbox.right + object.hitbox.width/2)

                        # whenever there is a collision, velocity is set to 0 so the object doesnt move
                        object.vel.x = 0
                        # the position of the objects hitbox is set the objects new position
                        object.hitbox.centerx = object.pos.x

            # same but for y
            if axis == 'y':
                if collisions:

                    if collisions[0].collidable:

                        if collisions[0].hitbox.centery > object.hitbox.centery:
                            object.pos.y = int(collisions[0].hitbox.top - object.hitbox.height/2)

                        if collisions[0].hitbox.centery < object.hitbox.centery:
                            object.pos.y = int(collisions[0].hitbox.bottom + object.hitbox.height/2)

                        object.vel.y = 0
                        object.hitbox.centery = object.pos.y




