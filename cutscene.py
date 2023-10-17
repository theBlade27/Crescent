import pygame as p
from sprite import *
from settings import *
from scene import *

class CutScene(p.sprite.Sprite):

    def __init__(self, game, category):

        self.groups = game.cutscenes_group, game.all
        p.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.category = category

        if category == 'intro':
            self.scenes = ['eyescene', 'starscene']
            self.lengths = [13, 48]
            self.total_length = 2

        self.scene_counter = 0

        self.current_scene = Scene(self.game, self.category, self.scenes[self.scene_counter], self.lengths[self.scene_counter], self)

        self.cutscene_over = False

    def next_scene(self):

        if self.cutscene_over == False:

            self.current_scene.kill()

            self.scene_counter += 1

            self.current_scene = Scene(self.game, self.category, self.scenes[self.scene_counter], self.lengths[self.scene_counter], self)

            if self.scene_counter == self.total_length - 1:
                self.cutscene_over = True

        else:

            self.current_scene.kill()

            self.kill()


