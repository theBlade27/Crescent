import pygame as p
from sprite import *
from settings import *
from image import *
from skill import *

class Button(Image):

    def __init__(self, game, menu):
        super().__init__(game)

        self.menu = menu

        self.spritesheet = Sprite(MENU_SPRITESHEETS['BUTTON'].copy(), scale = 4)

        self.unpressed_image = self.spritesheet.get_sprite(0, 0, 22, 27)
        self.pressed_image = self.spritesheet.get_sprite(22, 0 , 22, 27)

        self.image = self.unpressed_image.copy()

        self.sound = p.mixer.Sound(BUTTON_SOUND)

    def update(self):

        self.image.blit(self.unpressed_image, [0, 0])

        if self.hitbox.collidepoint(self.game.mouse.pos):
            self.image = colour_swap(self.image, FAKEBLACK, WHITE)

            if self.game.mouse.pressed['M1']:
                self.image = self.pressed_image.copy()
                self.image = colour_swap(self.image, FAKEBLACK, YELLOW)
                self.sound.play()

class UpgradeButton(Image):

    def __init__(self, game, menu):
        super().__init__(game)

        self.menu = menu

        self.spritesheet = Sprite(MENU_SPRITESHEETS['UPGRADE'].copy(), scale = 4)

        self.pos = [548, 528]

        self.unpressed_image = self.spritesheet.get_sprite(0, 0, 81, 26)
        self.pressed_image = self.spritesheet.get_sprite(81, 0, 81, 26)

        self.image = self.unpressed_image.copy()

        self.hitbox = p.rect.Rect(self.pos[0] + self.menu.pos[0], self.pos[1] + self.menu.pos[1], self.image.get_width(), self.image.get_height())

        self.sound = p.mixer.Sound(BUTTON_SOUND)

    def update(self):

        self.hero = self.menu.hero

        if self.hero != None and type(self.hero) == Hero:

            self.image.blit(self.unpressed_image, [0, 0])

            if self.hitbox.collidepoint(self.game.mouse.pos):
                self.image = colour_swap(self.image, FAKEBLACK, WHITE)

                if self.game.mouse.pressed['M1']:

                    if self.menu.upgrading_armour:

                        level = self.hero.armour_level

                        if level != len(BLACKSMITH_COSTS):

                            cost = BLACKSMITH_COSTS[level]

                            if self.game.money >= cost:
                                self.game.money -= cost

                                for item in self.hero.equipment:
                                    if item != None:
                                        item.remove_item(self.hero)

                                self.hero.armour_level += 1

                                self.hero.protection = ARMOUR_VALUES[self.hero.type][self.hero.armour_level][0]
                                self.hero.speed = ARMOUR_VALUES[self.hero.type][self.hero.armour_level][1]
                                self.hero.healing[0] = ARMOUR_VALUES[self.hero.type][self.hero.armour_level][2]
                                self.hero.healing[1] = ARMOUR_VALUES[self.hero.type][self.hero.armour_level][3]
                                self.hero.sanity_recovery_skills[0] = ARMOUR_VALUES[self.hero.type][self.hero.armour_level][2]
                                self.hero.sanity_recovery_skills[1] = ARMOUR_VALUES[self.hero.type][self.hero.armour_level][3]

                                self.image = self.pressed_image.copy()
                                self.image = colour_swap(self.image, FAKEBLACK, YELLOW)

                                self.menu.cost = 0
                                self.menu.upgrading_armour = False

                                for item in self.hero.equipment:
                                    if item != None:
                                        item.equip_item(self.hero)

                    if self.menu.upgrading_weapon:

                        level = self.hero.weapon_level

                        if level != len(BLACKSMITH_COSTS):

                            cost = BLACKSMITH_COSTS[level]

                            if self.game.money >= cost:
                                self.game.money -= cost

                                for item in self.hero.equipment:
                                    if item != None:
                                        item.remove_item(self.hero)

                                self.hero.weapon_level += 1

                                self.hero.damage[0] = WEAPON_VALUES[self.hero.type][self.hero.weapon_level][0]
                                self.hero.damage[1] = WEAPON_VALUES[self.hero.type][self.hero.weapon_level][1]
                                self.hero.precision = WEAPON_VALUES[self.hero.type][self.hero.weapon_level][2]
                                self.hero.crit = WEAPON_VALUES[self.hero.type][self.hero.weapon_level][3]

                                self.image = self.pressed_image.copy()
                                self.image = colour_swap(self.image, FAKEBLACK, YELLOW)

                                self.menu.cost = 0
                                self.menu.upgrading_weapon = False

                                for item in self.hero.equipment:
                                    if item != None:
                                        item.equip_item(self.hero)

                    for menu in self.game.menus.values():
                        if menu != self.menu:
                            menu.update_images()

class PlayButton(Image):

    def __init__(self, game, menu):
        super().__init__(game)

        self.menu = menu

        self.spritesheet = Sprite(MENU_SPRITESHEETS['PLAYBUTTON'].copy(), scale = 8)

        self.pos = [53 * 8, 98 * 8]

        self.unpressed_image = self.spritesheet.get_sprite(0, 0, 130, 50)
        self.pressed_image = self.spritesheet.get_sprite(0, 50 , 130, 50)

        self.image = self.unpressed_image.copy()

        self.hitbox = p.rect.Rect(self.pos[0] + self.menu.pos[0], self.pos[1] + self.menu.pos[1], self.image.get_width(), self.image.get_height())

        self.sound = p.mixer.Sound(BUTTON_SOUND)

    def update(self):

        self.image.blit(self.unpressed_image, [0, 0])

        if self.hitbox.collidepoint(self.game.mouse.pos):
            self.image = self.pressed_image.copy()

            if self.game.mouse.pressed['M1']:
                self.game.menus['PLAY'].kill()
                self.game.reset_game()
                self.kill()
                self.sound.play()

class MapButton(Button):

    def __init__(self, game, menu):
        super().__init__(game, menu)

        self.icon = Sprite(MENU_SPRITESHEETS['ICON_SPRITESHEET'].copy(), scale = 4).get_sprite(20, 0, 20, 20)

        self.unpressed_image.blit(self.icon, (4, 8))
        self.pressed_image.blit(self.icon, (4, 12))

        self.pos = [1460, 0]
        self.hitbox = p.rect.Rect(self.pos[0] + self.menu.pos[0], self.pos[1] + self.menu.pos[1], self.image.get_width(), self.image.get_height())


class CampButton(Button):

    def __init__(self, game, menu):
        super().__init__(game, menu)

        self.icon = Sprite(MENU_SPRITESHEETS['ICON_SPRITESHEET'].copy(), scale = 4).get_sprite(60, 0, 20, 20)

        self.unpressed_image.blit(self.icon, (4, 8))
        self.pressed_image.blit(self.icon, (4, 12))

        self.pos = [1552, 0]
        self.hitbox = p.rect.Rect(self.pos[0] + self.menu.pos[0], self.pos[1] + self.menu.pos[1], self.image.get_width(), self.image.get_height())

class InventoryButton(Button):

    def __init__(self, game, menu):
        super().__init__(game, menu)

        self.icon = Sprite(MENU_SPRITESHEETS['ICON_SPRITESHEET'].copy(), scale = 4).get_sprite(0, 0, 20, 20)

        self.unpressed_image.blit(self.icon, (4, 8))
        self.pressed_image.blit(self.icon, (4, 12))

        self.pos = [1644, 0]
        self.hitbox = p.rect.Rect(self.pos[0] + self.menu.pos[0], self.pos[1] + self.menu.pos[1], self.image.get_width(), self.image.get_height())

    def update(self):
        super().update()
    
        if self.hitbox.collidepoint(self.game.mouse.pos):
            if self.game.mouse.pressed['M1']:
                self.game.open_menu('INVENTORY')

class RepositionButton(Button):

    def __init__(self, game, menu):
        super().__init__(game, menu)

        self.icon = Sprite(MENU_SPRITESHEETS['ICON_SPRITESHEET'].copy(), scale = 4).get_sprite(40, 0, 20, 20)

        self.unpressed_image.blit(self.icon, (4, 8))
        self.pressed_image.blit(self.icon, (4, 12))

        self.pos = [1736, 0]
        self.hitbox = p.rect.Rect(self.pos[0] + self.menu.pos[0], self.pos[1] + self.menu.pos[1], self.image.get_width(), self.image.get_height())

class SettingsButton(Button):

    def __init__(self, game, menu):
        super().__init__(game, menu)

        self.icon = Sprite(MENU_SPRITESHEETS['ICON_SPRITESHEET'].copy(), scale = 4).get_sprite(80, 0, 20, 20)

        self.unpressed_image.blit(self.icon, (4, 8))
        self.pressed_image.blit(self.icon, (4, 12))

        self.pos = [1828, 0]
        self.hitbox = p.rect.Rect(self.pos[0] + self.menu.pos[0], self.pos[1] + self.menu.pos[1], self.image.get_width(), self.image.get_height())

class ExitButton(Button):

    def __init__(self, game, menu):
        super().__init__(game, menu)

        self.icon = Sprite(MENU_SPRITESHEETS['ICON_SPRITESHEET'].copy(), scale = 4).get_sprite(160, 0, 20, 20)

        self.unpressed_image.blit(self.icon, (4, 8))
        self.pressed_image.blit(self.icon, (4, 12))

        self.pos = [1052, 12]
        self.hitbox = p.rect.Rect(self.pos[0] + self.menu.pos[0], self.pos[1] + self.menu.pos[1], self.image.get_width(), self.image.get_height())

    def update(self):
        super().update()
    
        if self.hitbox.collidepoint(self.game.mouse.pos):
            if self.game.mouse.pressed['M1']:
                self.game.close_menu('INVENTORY')
                self.game.close_menu('SELECT_SKILLS')
                self.game.close_menu('UPGRADE')
                if type(self.game.selected_character) == Hero:
                    self.game.selected_character.selected_skill == None
                self.menu.kill()


class WeaponUpgradeButton(Button):

    def __init__(self, game, menu):
        super().__init__(game, menu)

        self.hero = self.menu.hero

        if self.hero != None:

            self.level = self.hero.weapon_level

            self.icon = Sprite(MENU_SPRITESHEETS['ICON_SPRITESHEET'].copy(), scale = 4).get_sprite(0 + self.level * 20, 20, 20, 20)

        else:

            self.icon = p.Surface((80, 80))

        self.spritesheet = Sprite(MENU_SPRITESHEETS['BUTTON'].copy(), scale = 4)

        self.unpressed_image = self.spritesheet.get_sprite(0, 0, 22, 27)
        self.pressed_image = self.spritesheet.get_sprite(22, 0 , 22, 27)

        self.unpressed_image.blit(self.icon, (4, 8))
        self.pressed_image.blit(self.icon, (4, 12))

        self.image = self.unpressed_image.copy()

        self.pos = [556, 292]
        self.hitbox = p.rect.Rect(self.pos[0] + self.menu.pos[0], self.pos[1] + self.menu.pos[1], self.image.get_width(), self.image.get_height())

    def update(self):
        
        self.hero = self.menu.hero
        if type(self.hero) == Hero and self.hero != None:
            self.level = self.hero.weapon_level
            self.icon = Sprite(MENU_SPRITESHEETS['ICON_SPRITESHEET'].copy(), scale = 4).get_sprite(0 + self.level * 20, 20, 20, 20)

            self.unpressed_image = self.spritesheet.get_sprite(0, 0, 22, 27)
            self.pressed_image = self.spritesheet.get_sprite(22, 0 , 22, 27)

            self.unpressed_image.blit(self.icon, (4, 8))
            self.pressed_image.blit(self.icon, (4, 12))

            self.image = self.unpressed_image.copy()

            if self.hitbox.collidepoint(self.game.mouse.pos):
                self.image = colour_swap(self.image, FAKEBLACK, WHITE)

                if self.game.mouse.pressed['M1']:
                    if self.menu.upgrading_weapon:
                        self.menu.upgrading_weapon = False
                        self.menu.cost = 0
                    else:
                        self.menu.upgrading_weapon = True
                        self.menu.upgrading_armour = False

                        level = self.hero.weapon_level
                        if level == len(BLACKSMITH_COSTS):
                            self.menu.cost = 'MAX'
                        else:
                            cost = BLACKSMITH_COSTS[level]
                            self.menu.cost = cost

            if self.menu.upgrading_weapon == True:
                self.image = self.pressed_image.copy()
                self.image = colour_swap(self.image, FAKEBLACK, YELLOW)

class ArmourUpgradeButton(Button):

    def __init__(self, game, menu):
        super().__init__(game, menu)

        self.hero = self.menu.hero

        if self.hero != None:

            self.level = self.hero.armour_level
            self.icon = Sprite(MENU_SPRITESHEETS['ICON_SPRITESHEET'].copy(), scale = 4).get_sprite(60 + self.level * 20, 20, 20, 20)

        else:

            self.icon = p.Surface((80, 80))

        self.spritesheet = Sprite(MENU_SPRITESHEETS['BUTTON'].copy(), scale = 4)

        self.unpressed_image = self.spritesheet.get_sprite(0, 0, 22, 27)
        self.pressed_image = self.spritesheet.get_sprite(22, 0 , 22, 27)

        self.unpressed_image.blit(self.icon, (4, 8))
        self.pressed_image.blit(self.icon, (4, 12))

        self.image = self.unpressed_image.copy()

        self.pos = [556, 408]
        self.hitbox = p.rect.Rect(self.pos[0] + self.menu.pos[0], self.pos[1] + self.menu.pos[1], self.image.get_width(), self.image.get_height())

    def update(self):
        
        self.hero = self.menu.hero

        if type(self.hero) == Hero and self.hero != None:
            self.level = self.hero.armour_level
            self.icon = Sprite(MENU_SPRITESHEETS['ICON_SPRITESHEET'].copy(), scale = 4).get_sprite(60 + self.level * 20, 20, 20, 20)

            self.unpressed_image = self.spritesheet.get_sprite(0, 0, 22, 27)
            self.pressed_image = self.spritesheet.get_sprite(22, 0 , 22, 27)

            self.unpressed_image.blit(self.icon, (4, 8))
            self.pressed_image.blit(self.icon, (4, 12))

            self.image = self.unpressed_image.copy()

            

            if self.hitbox.collidepoint(self.game.mouse.pos):
                self.image = colour_swap(self.image, FAKEBLACK, WHITE)

                if self.game.mouse.pressed['M1']:
                    if self.menu.upgrading_armour:
                        self.menu.upgrading_armour = False
                        self.menu.cost = 0
                    else:
                        self.menu.upgrading_armour = True
                        self.menu.upgrading_weapon = False

                        level = self.hero.armour_level
                        if level == len(BLACKSMITH_COSTS):
                            self.menu.cost = 'MAX'
                        else:
                            cost = BLACKSMITH_COSTS[level]
                            self.menu.cost = cost

            if self.menu.upgrading_armour == True:
                self.image = self.pressed_image.copy()
                self.image = colour_swap(self.image, FAKEBLACK, YELLOW)

class SkillButton(Button):

    def __init__(self, game, menu, index):
        super().__init__(game, menu)

        self.hero = self.game.selected_character
        self.index = index
        self.skill = self.hero.skills[self.index]
        self.icon = self.skill.image

        self.spritesheet = Sprite(MENU_SPRITESHEETS['BUTTON'].copy(), scale = 8)

        self.unpressed_image = self.spritesheet.get_sprite(0, 0, 22, 27)
        self.pressed_image = self.spritesheet.get_sprite(22, 0 , 22, 27)

        self.unpressed_image.blit(self.icon, (8, 16))
        self.pressed_image.blit(self.icon, (8, 24))

        self.image = self.unpressed_image.copy()

        self.pos = [632 + index * 184, 12]
        self.hitbox = p.rect.Rect(self.pos[0] + self.menu.pos[0], self.pos[1] + self.menu.pos[1], self.image.get_width(), self.image.get_height())

    def update(self):

        self.visible = True

        if self.game.battle_mode == False:
            self.visible = False

        if type(self.game.selected_character) == Hero:

            self.hero = self.game.selected_character
            self.skill = self.hero.skills[self.index]
            self.icon = self.skill.image

            if self.index == 4 and self.game.selected_character.has_moved:
                self.visible = False

            if self.index == 5 and self.game.selected_character.has_used_skill:
                self.visible = False

            if self.game.selected_character.stunned or self.game.actingout:
                self.visible = False

            self.unpressed_image = self.spritesheet.get_sprite(0, 0, 22, 27)
            self.pressed_image = self.spritesheet.get_sprite(22, 0 , 22, 27)

            self.unpressed_image.blit(self.icon, (8, 16))
            self.pressed_image.blit(self.icon, (8, 24))

            self.image = self.unpressed_image.copy()

            if self.hitbox.collidepoint(self.game.mouse.pos):
                self.image = colour_swap(self.image, FAKEBLACK, WHITE)

                if self.game.mouse.pressed['M1']:
                    if self.game.battle_mode:
                        self.image = self.pressed_image.copy()
                        self.image = colour_swap(self.image, FAKEBLACK, YELLOW)
                        if self.game.selected_character.stunned == False:
                            self.hero.selected_skill = self.skill
                        for tile in self.game.menus['BATTLE'].tiles:
                            tile.being_targeted = False
                        if (not(self.index == 4 and self.game.selected_character.has_moved)) and (not(self.index == 5 and self.game.selected_character.has_used_skill)) and not self.game.selected_character.stunned and not self.game.actingout:
                            self.sound.play()

                if self.game.mouse.pressed['M2']:

                    if self.game.battle_mode:
                        self.image = self.pressed_image.copy()
                        self.image = colour_swap(self.image, FAKEBLACK, YELLOW)
                        if (self.index >= 0 and self.index <= 3) and not self.game.selected_character.stunned and not self.game.actingout:
                            self.hero.selected_skill = self.skill
                            sound = p.mixer.Sound(BUTTON_SOUND)
                            sound.play()
                            self.game.open_menu('SELECT_SKILLS', self.hero)



            if self.hero.selected_skill == self.skill:
                self.image = self.pressed_image.copy()
                self.image = colour_swap(self.image, FAKEBLACK, YELLOW)

        else:

            self.image.fill(BLUE)



