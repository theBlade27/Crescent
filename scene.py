import pygame as p
from sprite import *
from settings import *

class Scene(p.sprite.Sprite):

    def __init__(self, game, category, type, length, cutscene):

        self.groups = game.scenes_group, game.all
        p.sprite.Sprite.__init__(self, self.groups)

        self.game = game

        # some scenes shift up, while others shift down
        # it is decided here

        if type == 'heroscene' or type == 'gameover' or type == 'victory' or type == 'thanks' or type == 'credits' or type == 'playtesters' or type == 'specialthanks':
            self.up = True
        else:
            self.up = False

        # some scenes dont move at all

        if type == 'crescentscene':
            self.static = True
        else:
            self.static = False

        # if a scene needs to shift downwards, its top left corner starts at to the top left of the screen

        if self.up == False:

            self.pos = [0, 0]

        # otherwise, the top left corner of the scene starts higher up to give it space to move downwards and make it look like the cutscene is shifting upwards

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

        # if the scene is static, the image of it only has to be one screen tall as the cutscene doesnt shift up or down
        
        if self.static == False:

            for x in range(length):
                self.images.append(p.transform.scale(p.image.load(path.join(self.folder, (type + str(x + 1) + '.png'))), [1920, 3240]))

        # otherwise, the image is three screens tall

        else:

            for x in range(length):
                self.images.append(p.transform.scale(p.image.load(path.join(self.folder, (type + str(x + 1) + '.png'))), [1920, 1080]))

        self.current_frame = 0
        self.last_update = 0 # used to keep track of last update so the scene knows when to switch to the next scene

        self.image = self.images[self.current_frame]

        # each frame in the scene has a different amount of time it lasts
        # each number on the list is the length of a frame in milliseconds

        if type == 'logo':

            self.lengths = [2000, 2000, 2000]

        if type == 'eyescene':

            self.lengths = [2000, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 2000, 2000, 2000]

        if type == 'heroscene':

            self.lengths = [200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200]

        if type == 'crescentscene':

            self.lengths = [3000, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 2000, 2000, 2000]

        if type == 'gameover':

            self.lengths = [4000, 4000, 4000]

        if type == 'victory':

            self.lengths = [4000, 4000, 4000]

        if type == 'thanks':

            self.lengths = [4000, 4000, 4000]

        if type == 'credits':

            self.lengths = [4000, 4000, 4000]

        if type == 'playtesters':

            self.lengths = [4000, 4000, 4000]

        if type == 'specialthanks':

            self.lengths = [4000, 4000, 4000]

        self.animation_complete = False
        self.movement_complete = False

        self.cutscene = cutscene

    def update(self):

        # when the scene has finished moving, the cutscene this scene belongs to deals with playing the next scene

        if self.movement_complete == True:

            self.cutscene.next_scene()

        # if the animation hsa not finished, continue playing the animation

        if self.animation_complete == False:

            self.play_animations()


        else:

            if self.static == False:

                # if the scene hasnt finished shifted

                if self.movement_complete == False:

                    # if the scene is one that needs to shift downwards

                    if self.up == False:

                        self.vel += 5

                        # the scene goes up, creating the illusion of the cutscene shifting downwards

                        self.pos[1] -= self.vel

                    # otherwise

                    else:

                        self.vel += 5

                        # the scene goes down, creating the illusion of the cutscene shifting upwards

                        self.pos[1] += self.vel

        if self.static == False:

            # if the scene is one that needs to shift downwards

            if self.up == False:

                # if the scene has moved two screen upwards, movement is complete

                if self.pos[1] < -2160:

                    self.pos[1] = -2160
                    self.movement_complete = True

            # otherwise

            else:

                # if the scene has moved two screen downwards, movement is complete

                if self.pos[1] > 0:

                    self.pos[1] = 0
                    self.movement_complete = True


        
    def play_animations(self):

        now = p.time.get_ticks()

        # pretty much the same code as the code used for animating the movement of a character

        if now - self.last_update > self.lengths[self.current_frame]:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.image = self.images[self.current_frame]

        if self.current_frame == (self.length - 1):
            # if this scene is the last one, the animation is complete
            self.animation_complete = True
            if self.static:
                self.cutscene.next_scene()

        