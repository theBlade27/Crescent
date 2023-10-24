import pygame as p
from sprite import *
from settings import *

class Scene(p.sprite.Sprite):

    def __init__(self, game, category, type, length, cutscene):

        self.groups = game.scenes_group, game.all
        p.sprite.Sprite.__init__(self, self.groups)

        self.game = game

        if type == 'heroscene' or type == 'gameover':
            self.up = True
        else:
            self.up = False

        if type == 'crescentscene':
            self.static = True
        else:
            self.static = False

        if self.up == False:

            self.pos = [0, 0]

        else:

            self.pos = [0, -2160]

        folder = path.dirname(__file__)
        data_folder = path.join(folder, 'data')
        img_folder = path.join(data_folder, 'img')
        cutscenes_folder = path.join(img_folder, 'cutscenes')

        self.folder = path.join(cutscenes_folder, category)

        self.length = length

        self.images = []

        self.vel = 0
        
        if self.static == False:

            for x in range(length):
                self.images.append(p.transform.scale(p.image.load(path.join(self.folder, (type + str(x + 1) + '.png'))), [1920, 3240]))

        else:

            for x in range(length):
                self.images.append(p.transform.scale(p.image.load(path.join(self.folder, (type + str(x + 1) + '.png'))), [1920, 1080]))

        self.current_frame = 0
        self.last_update = 0

        self.image = self.images[self.current_frame]

        if type == 'logo':

            self.lengths = [2000, 2000, 2000]

        if type == 'eyescene':

            self.lengths = [3000, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 3000, 100, 100]

        if type == 'starscene':

            self.lengths = [3000, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100]

        if type == 'facescene':

            self.lengths = [3000, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100]

        if type == 'heroscene':

            self.lengths = [300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300]

        if type == 'crescentscene':

            self.lengths = [3000, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 100, 100, 100]

        if type == 'gameover':

            self.lengths = [3000, 3000, 3000, 100]

        self.animation_complete = False
        self.movement_complete = False

        self.cutscene = cutscene

    def update(self):

        if self.movement_complete == True:

            self.cutscene.next_scene()

        if self.animation_complete == False:

            self.play_animations()


        else:

            if self.static == False:

                if self.movement_complete == False:

                    if self.up == False:

                        self.vel += 5

                        self.pos[1] -= self.vel

                    else:

                        self.vel += 5

                        self.pos[1] += self.vel

        if self.static == False:

            if self.up == False:

                if self.pos[1] < -2160:

                    self.pos[1] = -2160
                    self.movement_complete = True

            else:

                if self.pos[1] > 0:

                    self.pos[1] = 0
                    self.movement_complete = True


        
    def play_animations(self):

        now = p.time.get_ticks()

        if now - self.last_update > self.lengths[self.current_frame]:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.image = self.images[self.current_frame]

        if self.current_frame == (self.length - 1):
            self.animation_complete = True
            if self.static:
                self.cutscene.next_scene()

        