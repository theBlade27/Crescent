import pygame as p
from sprite import *
from settings import *

class Mouse(p.sprite.Sprite):

    def __init__(self, game):

        self.groups = game.mouse_group, game.all
        p.sprite.Sprite.__init__(self, self.groups)
        
        self.game = game

        p.mouse.set_visible(False)
        self.pos = p.mouse.get_pos()

        self.spritesheet = Sprite(MOUSE_SPRITESHEET, scale = 3)

        self.images = [
            self.spritesheet.get_sprite(0, 0, 16, 16),
            self.spritesheet.get_sprite(16, 0, 16, 16),
            self.spritesheet.get_sprite(32, 0, 16, 16)
        ]

        self.image = self.images[0]

        self.pressed = {
            'M1': False,
            'M2': False
        }

        self.is_clicking = False

    def update(self):

        self.pos = p.mouse.get_pos()
        
        self.pressed = {
            'M1': False,
            'M2': False
        }

        clicked_buttons = p.mouse.get_pressed()

        if clicked_buttons[0] or clicked_buttons[2]:

            if not self.is_clicking:
                self.is_clicking = True

                if clicked_buttons[0]:
                    self.pressed['M1'] = True
                if clicked_buttons[2]:
                    self.pressed['M2'] = True

        else:
            self.is_clicking = False

        if self.pressed['M1'] or self.pressed['M2']:
            self.image = self.images[1]
        else:
            self.image = self.images[0]

    


