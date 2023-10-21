import pygame as p
from sprite import *
from settings import *
vec = p.math.Vector2

class ExplorationCharacter(p.sprite.Sprite):

    def __init__(self, game, type, pos, hero):

        self.groups = game.exploration_characters
        p.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.type = type
        self.spritesheet = Sprite(CHARACTER_SPRITESHEETS[self.type], MAP_SCALE)
        self.hero = hero

        self.running = False
        self.flipped = False

        self.last_update = 0
        self.current_frame = 0

        self.pos = vec(pos[0], pos[1])
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        if self.type == 'BLADE':
            
            self.idleanimations = [
                self.spritesheet.get_sprite(5, 3, 10, 17),
                self.spritesheet.get_sprite(25, 3, 10, 17)
            ]

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

        if self.vel.x == 0 and self.vel.y == 0:
            self.running = False

        self.play_animations()

    def calculate_acceleration(self):

        self.pos = vec(self.pos[0], self.pos[1])

        self.acc = vec(0, 0)

        if self.game.camera_focus == self:

            pressed_keys = p.key.get_pressed()
            if pressed_keys[p.K_s]:
                self.acc.y = ACCELERATION
            if pressed_keys[p.K_w]:
                self.acc.y = -ACCELERATION
            if pressed_keys[p.K_d]:
                self.acc.x = ACCELERATION
            if pressed_keys[p.K_a]:
                self.acc.x = -ACCELERATION

            if self.acc.length() > 0:
                self.game.ticks += 1
                self.game.tick_check()

        else:

            if self.game.battle_mode == False:

                if self.game.camera_focus != self:

                    target_location = self.game.selected_character.exploration_character.pos
                    distance_to_target = target_location - self.pos

                    if distance_to_target.length() > FOLLOW_DISTANCE:
                        rotation = distance_to_target.angle_to(vec(1, 0))
                        self.acc = vec(1, 0).rotate(-rotation)
                        self.acc.scale_to_length(ACCELERATION)

                    for hero in self.game.hero_party:

                        if hero != None:

                            if hero.exploration_character != self:
                                distance_from_hero = self.pos - hero.exploration_character.pos
                                if 0 < distance_from_hero.length() < REPULSION_RADIUS:
                                    self.acc += distance_from_hero.normalize()
                                    if self.acc != [0, 0]:
                                        self.acc.scale_to_length(ACCELERATION)

        self.acc += self.vel * FRICTION

    def calculate_velocity(self):

        self.vel += self.acc

        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        if abs(self.vel.y) < 0.1:
            self.vel.y = 0

        if self.vel.x > 0:
            self.flipped = False
        elif self.vel.x < 0:
            self.flipped = True

    def calculate_position(self):

        self.rect.center = self.pos
        self.pos += self.vel + 0.5 * self.acc

        self.hitbox.centerx = self.pos.x
        self.checkgroupcollisions(self, self.game.collision_hitboxes, 'x')

        self.hitbox.centery = self.pos.y
        self.checkgroupcollisions(self, self.game.collision_hitboxes, 'y')

        self.rect.center = self.hitbox.center

    def play_animations(self):

        now = p.time.get_ticks()

        if self.running:
            if now - self.last_update > 100:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.runanimations)
                self.image = p.transform.flip(self.runanimations[self.current_frame], self.flipped, False)
        
        else:
            if now - self.last_update > 1000:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.idleanimations)
                self.image = p.transform.flip(self.idleanimations[self.current_frame], self.flipped, False)

    def checkcollision(self, object1, object2):

        return object1.hitbox.colliderect(object2.hitbox)
    
    def checkgroupcollisions(self, object, group, axis):

        collisions = p.sprite.spritecollide(object, group, False, self.checkcollision)

        if group == self.game.collision_hitboxes:

            if axis == 'x':
                if collisions:

                    if collisions[0].collidable:

                        if collisions[0].hitbox.centerx > object.hitbox.centerx:
                            object.pos.x = int(collisions[0].hitbox.left - object.hitbox.width/2)

                        if collisions[0].hitbox.centerx < object.hitbox.centerx:
                            object.pos.x = int(collisions[0].hitbox.right + object.hitbox.width/2)

                        object.vel.x = 0
                        object.hitbox.centerx = object.pos.x

            if axis == 'y':
                if collisions:

                    if collisions[0].collidable:

                        if collisions[0].hitbox.centery > object.hitbox.centery:
                            object.pos.y = int(collisions[0].hitbox.top - object.hitbox.height/2)

                        if collisions[0].hitbox.centery < object.hitbox.centery:
                            object.pos.y = int(collisions[0].hitbox.bottom + object.hitbox.height/2)

                        object.vel.y = 0
                        object.hitbox.centery = object.pos.y




