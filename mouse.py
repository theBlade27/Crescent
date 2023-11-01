import pygame as p
from sprite import *
from settings import *

class Mouse(p.sprite.Sprite):

    # the object of this class deals with storing the players mouse position, making it change images bsaed on the players actions, and storing which buttons are being pressed

    def __init__(self, game):

        self.groups = game.mouse_group, game.all
        p.sprite.Sprite.__init__(self, self.groups)
        
        self.game = game

        # makes the computers default mosue invisible so it doesnt appear on top of the games pixel art mouse
        p.mouse.set_visible(False)

        # gets the mouses current position
        self.pos = p.mouse.get_pos()

        self.spritesheet = Sprite(MOUSE_SPRITESHEET, scale = 3)


        self.images = [
            self.spritesheet.get_sprite(0, 0, 16, 16), # image of hand
            self.spritesheet.get_sprite(16, 0, 16, 16), # image of hand with finger down, used when the player is clicking
            self.spritesheet.get_sprite(32, 0, 16, 16) # image of a magnifying glass, used when the player hovers their mouse over an interactable
        ]

        self.image = self.images[0]

        # dictionary of pressed keys
        self.pressed = {
            'M1': False,
            'M2': False
        }

        # stores whether the mouse is currently clicking so the mouse doesnt constantly click when the player holds the button down
        self.is_clicking = False

    def update(self):

        # updates the position of this object to be the same as the players mouse position
        self.pos = p.mouse.get_pos()
        
        self.pressed = {
            'M1': False,
            'M2': False
        }

        # gets a list of the mouse buttons, where clicked ones are equal to True
        clicked_buttons = p.mouse.get_pressed()

        # clicked_buttons[0] is M1 and clicked_buttons[1] is M2
        if clicked_buttons[0] or clicked_buttons[2]:

            # if the mouse isnt already clicking
            if not self.is_clicking:
                # set 'is_clicking' to True
                self.is_clicking = True

                # update the dictionary to store whether a button is being clicked
                if clicked_buttons[0]:
                    self.pressed['M1'] = True
                if clicked_buttons[2]:
                    self.pressed['M2'] = True

        else:
            # otherwise set 'is_clicking' to False
            self.is_clicking = False

        # change the images based on whether a button is being pressed or not
        if self.is_clicking:
            self.image = self.images[1]
        else:
            self.image = self.images[0]

    


