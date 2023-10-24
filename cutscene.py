import pygame as p
from sprite import *
from settings import *
from scene import *
from menu import *

class CutScene(p.sprite.Sprite):

    def __init__(self, game, category):

        self.groups = game.cutscenes_group, game.all
        p.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.category = category

        if category == 'gameover':
            self.scenes = ['gameover', 'crescentscene']
            self.lengths = [4, 30]
            self.total_length = 2

        if category == 'intro':
            self.scenes = ['logo', 'eyescene', 'starscene', 'facescene', 'heroscene', 'crescentscene']
            self.lengths = [3, 13, 48, 20, 32, 30]
            self.total_length = 6

        self.scene_counter = 0

        self.current_scene = Scene(self.game, self.category, self.scenes[self.scene_counter], self.lengths[self.scene_counter], self)

        self.cutscene_over = False

        self.hitbox = p.rect.Rect(0, 0, 1920, 1080)

    def update(self):

        if self.hitbox.collidepoint(self.game.mouse.pos):

            if self.game.mouse.pressed['M1']:

                self.end_cutscene()

    def next_scene(self):

        if self.cutscene_over == False:

            self.current_scene.kill()

            self.scene_counter += 1

            self.current_scene = Scene(self.game, self.category, self.scenes[self.scene_counter], self.lengths[self.scene_counter], self)

            if self.scene_counter == self.total_length - 1:
                self.cutscene_over = True

        else:

            self.end_cutscene()

    def end_cutscene(self):

        self.current_scene.kill()

        if self.category == 'intro' or self.category == 'gameover':
            self.game.menus['PLAY'] = NewGameMenu(self.game)

        self.kill()


