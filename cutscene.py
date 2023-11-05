import pygame as p
from sprite import *
from settings import *
from scene import *
from menu import *

class CutScene(p.sprite.Sprite):

    def __init__(self, game, category):

        # objects of this class play a cutscene to the player by creating and destroying individual scenes consecutively

        self.groups = game.cutscenes_group, game.all
        p.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.category = category

        # depending on the cutscene, different scenes are required

        if category == 'gameover':
            self.scenes = ['gameover', 'crescentscene'] # each scene in the cutscene
            self.lengths = [3, 30] # the amount of frames in each scene
            self.total_length = 2 # the amount of scenes in the cutscene

        if category == 'intro':
            self.scenes = ['logo', 'eyescene', 'heroscene', 'crescentscene']
            self.lengths = [3, 13, 16, 30]
            self.total_length = 4

        if category == 'victory':
            self.scenes = ['victory', 'thanks', 'credits', 'playtesters', 'specialthanks', 'crescentscene']
            self.lengths = [3, 3, 3, 3, 3, 3]
            self.total_length = 6

        self.scene_counter = 0

        # the first scene is created
        # for example, if 'category' is 'intro', the arguments for the scene construction would be 'self.scenes[0]' as the type, which would be 'logo', and 'self.lengths[0]' as the length, which would be 3

        self.current_scene = Scene(self.game, self.category, self.scenes[self.scene_counter], self.lengths[self.scene_counter], self)

        self.cutscene_over = False

        self.hitbox = p.rect.Rect(0, 0, 1920, 1080)

    def update(self):

        if self.hitbox.collidepoint(self.game.mouse.pos):

            # if the player clicks the screen, the cutscene ends

            if self.game.mouse.pressed['M1']:

                self.end_cutscene()

    def next_scene(self):

        # if the cutscene isnt over yet

        if self.cutscene_over == False:

            # kill the current scene

            self.current_scene.kill()

            # increment the scene counter and create a new scene

            self.scene_counter += 1

            self.current_scene = Scene(self.game, self.category, self.scenes[self.scene_counter], self.lengths[self.scene_counter], self)

            # if the next scene would be the last one, the cutscene needs to end next time 'next_scene' is called, so 'cutscene_over' is set to True

            if self.scene_counter == self.total_length - 1:
                self.cutscene_over = True

        else:

            # if the cutscene is over, end the scene

            self.end_cutscene()

    def end_cutscene(self):

        # kill the current scene

        self.current_scene.kill()

        # open up the new game menu if appropiate

        if self.category == 'intro' or self.category == 'gameover' or self.category == 'victory':
            self.game.menus['PLAY'] = NewGameMenu(self.game)

        self.kill()


