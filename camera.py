import pygame as p
from settings import *

class Camera(p.sprite.Sprite):

    def __init__(self, game, width, height):
        self.groups = game.all
        p.sprite.Sprite.__init__(self, self.groups)

        self.game = game   
        self.width = width
        self.height = height
        self.x = -self.game.camera_focus.hitbox.centerx + int(WIDTH/2)
        self.y = -self.game.camera_focus.hitbox.centery + int(HEIGHT/2)
        
        self.camera = p.Rect(0, 0, width, height)

    def apply(self, object):

        return object.hitbox.move(self.camera.topleft)
    
    def apply_hitbox(self, hitbox):

        return hitbox.move(self.camera.topleft)

    def apply_mouse(self):

        mouse_x, mouse_y = p.mouse.get_pos()

        adjusted_x = mouse_x - self.camera.left
        adjusted_y = mouse_y - self.camera.top

        return adjusted_x, adjusted_y
    
    def update(self):

        desired_x = -self.game.camera_focus.hitbox.centerx + int(WIDTH/2)
        desired_y = -self.game.camera_focus.hitbox.centery + int(HEIGHT/2)

        self.x += LAG_FACTOR * (desired_x - self.x)
        self.y += LAG_FACTOR * (desired_y - self.y)

        self.camera = p.Rect(int(self.x), int(self.y), self.width, self.height)