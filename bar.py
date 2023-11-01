import pygame as p
from sprite import *
from settings import *
from image import *
from hero import Hero

class RegularBar(Image):

    def __init__(self, game):
        super().__init__(game)

        self.game = game
        self.scale = 4
        self.image = MENU_SPRITESHEETS['REGULAR_BAR']
        self.image = p.transform.scale(self.image, (self.image.get_width() * self.scale, self.image.get_height() * self.scale))

        self.bar = p.surface.Surface((312, 24))
        self.bar.fill(DARKBLUE)
        self.bar_pos = [68, 16]

class SmallBar(Image):

    def __init__(self, game):
        super().__init__(game)

        self.game = game
        self.scale = 4
        self.image = MENU_SPRITESHEETS['SMALL_BAR']
        self.image = p.transform.scale(self.image, (self.image.get_width() * self.scale, self.image.get_height() * self.scale))
        self.background = self.image.copy()

        self.progress = 0

        self.bar = p.surface.Surface((216, 12))
        self.bar.fill(DARKBLUE)
        self.bar_pos = [4, 4]

class HeroSmallHealthBar(SmallBar):

    def __init__(self, game, menu):
        super().__init__(game)

        self.menu = menu

        self.image.blit(self.bar, self.bar_pos)
        self.pos = [108, 56]

    def update(self):

        self.image = self.background.copy()

        if self.menu.hero != None:
            self.hero = self.menu.hero
            self.progress = self.hero.current_health/self.hero.max_health
        self.bar_length = min(int(216 * self.progress), 216)

        self.bar = p.surface.Surface((self.bar_length, 12))
        self.bar.fill(RED)

        self.image.blit(self.bar, self.bar_pos)

class EnemySmallHealthBar(SmallBar):

    def __init__(self, game, menu):
        super().__init__(game)

        self.menu = menu

        self.image.blit(self.bar, self.bar_pos)
        self.pos = [12, 56]

    def update(self):

        self.image = self.background.copy()

        if self.menu.enemy != None:
            self.enemy = self.menu.enemy
            self.progress = self.enemy.current_health/self.enemy.max_health
        self.bar_length = min(int(216 * self.progress), 216)

        self.bar = p.surface.Surface((self.bar_length, 12))
        self.bar.fill(RED)

        self.image.blit(self.bar, self.bar_pos)

class HeroSmallSanityBar(SmallBar):

    def __init__(self, game, menu):
        super().__init__(game)

        self.menu = menu

        self.image.blit(self.bar, self.bar_pos)
        self.pos = [108, 80]

    def update(self):

        self.image = self.background.copy()

        if self.menu.hero != None:
            self.hero = self.menu.hero
            self.progress = self.hero.current_sanity/self.hero.max_sanity

        self.bar_length = min(int(216 * self.progress), 216)

        self.bar = p.surface.Surface((self.bar_length, 12))
        self.bar.fill(WHITE)

        self.image.blit(self.bar, self.bar_pos)

class HeroRegularHealthBar(RegularBar):

    def __init__(self, game):
        super().__init__(game)

        self.image.blit(self.bar, self.bar_pos)
        self.pos = [232, 60]

        self.icon = Sprite(MENU_SPRITESHEETS['SMALL_ICON_SPRITESHEET'].copy(), scale = 4).get_sprite(0, 0, 9, 9)

        self.image.blit(self.icon, (16, 12))

        self.background = self.image.copy()

    def update(self):

        self.image = self.background.copy()

        self.hero = self.game.selected_character
        self.progress = self.hero.current_health/self.hero.max_health
        self.bar_length = min(int(312 * self.progress), 312)

        self.bar = p.surface.Surface((self.bar_length, 24))
        self.bar.fill(RED)

        self.image.blit(self.bar, self.bar_pos)

class HeroRegularSanityBar(RegularBar):

    def __init__(self, game):
        super().__init__(game)

        self.image.blit(self.bar, self.bar_pos)
        self.pos = [232, 124]

        self.icon = Sprite(MENU_SPRITESHEETS['SMALL_ICON_SPRITESHEET'].copy(), scale = 4).get_sprite(63, 0, 9, 9)

        self.image.blit(self.icon, (16, 12))

        self.background = self.image.copy()

    def update(self):

        self.image = self.background.copy()

        if type(self.game.selected_character) == Hero:

            self.hero = self.game.selected_character
            self.progress = self.hero.current_sanity/self.hero.max_sanity
            self.bar_length = min(int(312 * self.progress), 312)

            self.bar = p.surface.Surface((self.bar_length, 24))
            self.bar.fill(WHITE)

            self.image.blit(self.bar, self.bar_pos)

        else:

            self.image.fill(BLUE)

class HeroRegularExperienceBar(RegularBar):

    def __init__(self, game):
        super().__init__(game)

        self.image.blit(self.bar, self.bar_pos)

        self.icon = Sprite(MENU_SPRITESHEETS['SMALL_ICON_SPRITESHEET'].copy(), scale = 4).get_sprite(36, 0, 9, 9)

        self.image.blit(self.icon, (16, 12))

        self.background = self.image.copy()

    def update(self):

        self.image = self.background.copy()

        if type(self.game.selected_character) == Hero:

            self.hero = self.game.selected_character
            self.progress = self.hero.current_experience/EXPERIENCE_COSTS[self.hero.experience_level]
            self.bar_length = min(int(312 * self.progress), 312)

            self.bar = p.surface.Surface((self.bar_length, 24))
            self.bar.fill(YELLOW)

            self.image.blit(self.bar, self.bar_pos)

        else:

            self.image.fill(BLUE)

class InventoryHealthBar(RegularBar):

    def __init__(self, game, menu):
        super().__init__(game)

        self.pos = [744, 124]

        self.image.blit(self.bar, self.bar_pos)

        self.icon = Sprite(MENU_SPRITESHEETS['SMALL_ICON_SPRITESHEET'].copy(), scale = 4).get_sprite(0, 0, 9, 9)

        self.image.blit(self.icon, (16, 12))

        self.background = self.image.copy()

        self.menu = menu
        self.hero = self.menu.hero

    def update(self):

        self.image = self.background.copy()

        self.hero = self.menu.hero

        self.progress = self.hero.current_health/self.hero.max_health
        self.bar_length = min(int(312 * self.progress), 312)

        self.bar = p.surface.Surface((self.bar_length, 24))
        self.bar.fill(RED)

        self.image.blit(self.bar, self.bar_pos)



class InventorySanityBar(RegularBar):

    def __init__(self, game, menu):
        super().__init__(game)

        self.pos = [744, 188]

        self.image.blit(self.bar, self.bar_pos)

        self.icon = Sprite(MENU_SPRITESHEETS['SMALL_ICON_SPRITESHEET'].copy(), scale = 4).get_sprite(63, 0, 9, 9)

        self.image.blit(self.icon, (16, 12))

        self.background = self.image.copy()

        self.menu = menu
        self.hero = self.menu.hero

    def update(self):

        self.hero = self.menu.hero

        self.image = self.background.copy()

        if type(self.hero) == Hero:

            self.progress = self.hero.current_sanity/self.hero.max_sanity
            self.bar_length = min(int(312 * self.progress), 312)

            self.bar = p.surface.Surface((self.bar_length, 24))
            self.bar.fill(WHITE)

            self.image.blit(self.bar, self.bar_pos)

        else:

            self.image.fill(BLUE)

class InventoryExperienceBar(RegularBar):

    def __init__(self, game, menu):
        super().__init__(game)

        self.pos = [744, 252]

        self.image.blit(self.bar, self.bar_pos)

        self.icon = Sprite(MENU_SPRITESHEETS['SMALL_ICON_SPRITESHEET'].copy(), scale = 4).get_sprite(36, 0, 9, 9)

        self.image.blit(self.icon, (16, 12))

        self.background = self.image.copy()

        self.menu = menu
        self.hero = self.menu.hero


    def update(self):

        self.hero = self.menu.hero
        

        self.image = self.background.copy()

        if type(self.hero) == Hero:

            self.progress = self.hero.current_experience/EXPERIENCE_COSTS[self.hero.experience_level]
            self.bar_length = min(int(312 * self.progress), 312)

            self.bar = p.surface.Surface((self.bar_length, 24))
            self.bar.fill(YELLOW)

            self.image.blit(self.bar, self.bar_pos)

        else:

            self.image.fill(BLUE)






