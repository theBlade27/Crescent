import pygame as p
from sprite import *
from settings import *

class Scene(p.sprite.Sprite):

    def __init__(self, game, category, type, length, cutscene):

        self.groups = game.scenes_group, game.all
        p.sprite.Sprite.__init__(self, self.groups)

        self.game = game

        self.pos = [0, 0]

        folder = path.dirname(__file__)
        data_folder = path.join(folder, 'data')
        img_folder = path.join(data_folder, 'img')
        cutscenes_folder = path.join(img_folder, 'cutscenes')

        self.folder = path.join(cutscenes_folder, category)

        self.length = length

        self.images = []

        self.vel = 0

        for x in range(length):
            self.images.append(p.transform.scale(p.image.load(path.join(self.folder, (type + str(x + 1) + '.png'))), [1920, 3240]))

        self.current_frame = 0
        self.last_update = 0

        self.image = self.images[self.current_frame]

        if type == 'eyescene':

            self.lengths = [3000, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 3000, 100, 100]

        if type == 'starscene':

            self.lengths = [3000, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100]

        self.animation_complete = False
        self.movement_complete = False

        self.cutscene = cutscene

    def update(self):

        if self.movement_complete == True:

            self.cutscene.next_scene()

        if self.animation_complete == False:

            self.play_animations()

        else:

            if self.movement_complete == False:

                self.vel += 5

                self.pos[1] -= self.vel

        if self.pos[1] < -2160:

            self.pos[1] = -2160
            self.movement_complete = True


        
    def play_animations(self):

        now = p.time.get_ticks()

        if now - self.last_update > self.lengths[self.current_frame]:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.image = self.images[self.current_frame]

        if self.current_frame == (self.length - 1):
            self.animation_complete = True

        