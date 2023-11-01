import pygame as p
from settings import *

class Camera(p.sprite.Sprite):

    # the camera is in charge of making the screen follow the character the player is controlling

    def __init__(self, game, width, height):
        self.groups = game.camera_group, game.all
        p.sprite.Sprite.__init__(self, self.groups)

        self.game = game   

        # the cameras width and height is passed in, it is the same as the width and height of the entire screen
        self.width = width
        self.height = height

        # the cameras left side is set to be half a screens width away from the centre of the character
        self.x = -self.game.camera_focus.hitbox.centerx + int(WIDTH/2)
        # the cameras top side is set to be half a screens height away from the centre of the character
        self.y = -self.game.camera_focus.hitbox.centery + int(HEIGHT/2)
        # this makes the character the centre of the screen
        

        # a camera rect is made, and is moved around whenever the camera updates
        self.camera = p.Rect(0, 0, width, height)

    def apply(self, object):

        # returns the position of an object after the position of the camera is accounted for

        return object.hitbox.move(self.camera.topleft)
    
    def apply_hitbox(self, hitbox):

        # returns the position of an hitbox after the position of the camera is accounted for

        return hitbox.move(self.camera.topleft)

    def apply_mouse(self):

        # for menus, the position of the mouse is easy to get, because they are both UI elements and there positions are not affected by player movement
        # however, getting the position of the mouse in relation to a map object so you can interact with them is a bit more complicated

        # the position of the mouse is stored

        mouse_x, mouse_y = p.mouse.get_pos()

        # the cameras position is subtracted from the mouses position

        adjusted_x = mouse_x - self.camera.left
        adjusted_y = mouse_y - self.camera.top

        # the position of the mouse after the position of the camera has been accounted for is returned

        return adjusted_x, adjusted_y
    
    def update(self):

        # this piece of code is what makes the camera move towards the player controlled character

        # just like in the initialisation of the camera class, this makes the character the centre of the screen
        desired_x = -self.game.camera_focus.hitbox.centerx + int(WIDTH/2)
        desired_y = -self.game.camera_focus.hitbox.centery + int(HEIGHT/2)

        # however, i did not want the camera to instantly snap on to the players position
        # so the position is only changed by the difference between the desired position and the current position, multiplied by the LAG_FACTOR, a decimal number smaller than 1
        self.x += LAG_FACTOR * (desired_x - self.x)
        self.y += LAG_FACTOR * (desired_y - self.y)

        # finally, the camera rect is set to a rect with the new position

        self.camera = p.Rect(int(self.x), int(self.y), self.width, self.height)