import pygame as p
from sprite import *
from settings import *
from hero import *

class Image(p.sprite.Sprite):

    def __init__(self, game):

        self.groups = game.images_group, game.all
        p.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.visible = True

    def update(self):

        self.image.blit(self.background, [0, 0])

class TextboxBackground(Image):

    def __init__(self, game):
        super().__init__(game)

        self.image = MENU_SPRITESHEETS['TEXTBOX_BACKGROUND'].copy()
        self.scale = 8
        self.image = p.transform.scale(self.image, (self.image.get_width() * self.scale, self.image.get_height() * self.scale))
        self.background = self.image
        self.pos = [0, 0]

class SkillMenuIcon(Image):

    def __init__(self, game):
        super().__init__(game)

        self.image = Sprite(MENU_SPRITESHEETS['BUFF_ICONS'].copy(), scale = 4).get_sprite(0, 320, 20, 20)
        self.background = self.image
        self.pos = [8, 8]

class SlotTextbox(Image):

    def __init__(self, game):
        super().__init__(game)

        self.image = MENU_SPRITESHEETS['SLOT_TEXTBOX'].copy()
        self.scale = 8
        self.image = p.transform.scale(self.image, (self.image.get_width() * self.scale, self.image.get_height() * self.scale))
        self.background = self.image
        self.pos = [0, 0]

class CoinIcon(Image):

    def __init__(self, game):
        super().__init__(game)

        self.image = Sprite(MENU_SPRITESHEETS['ICON_SPRITESHEET'].copy(), scale = 4).get_sprite(180, 0, 20, 20)
        self.background = self.image
        self.pos = [1460, 108]

class InventoryHealthIcon(Image):

    def __init__(self, game):
        super().__init__(game)

        self.image = Sprite(MENU_SPRITESHEETS['SMALL_ICON_SPRITESHEET'].copy(), scale = 4).get_sprite(0, 0, 9, 9)
        self.background = self.image
        self.pos = [548, 356]

class InventorySpeedIcon(Image):

    def __init__(self, game):
        super().__init__(game)

        self.image = Sprite(MENU_SPRITESHEETS['SMALL_ICON_SPRITESHEET'].copy(), scale = 4).get_sprite(27, 18, 9, 9)
        self.background = self.image
        self.pos = [548, 400]

class InventoryProtectionIcon(Image):

    def __init__(self, game):
        super().__init__(game)

        self.image = Sprite(MENU_SPRITESHEETS['SMALL_ICON_SPRITESHEET'].copy(), scale = 4).get_sprite(9, 0, 9, 9)
        self.background = self.image
        self.pos = [548, 444]

class InventoryDamageIcon(Image):

    def __init__(self, game):
        super().__init__(game)

        self.image = Sprite(MENU_SPRITESHEETS['SMALL_ICON_SPRITESHEET'].copy(), scale = 4).get_sprite(0, 18, 9, 9)
        self.background = self.image
        self.pos = [548, 488]

class InventoryAgilityIcon(Image):

    def __init__(self, game):
        super().__init__(game)

        self.image = Sprite(MENU_SPRITESHEETS['SMALL_ICON_SPRITESHEET'].copy(), scale = 4).get_sprite(18, 0, 9, 9)
        self.background = self.image
        self.pos = [672, 356]

class InventoryPrecisionIcon(Image):

    def __init__(self, game):
        super().__init__(game)

        self.image = Sprite(MENU_SPRITESHEETS['SMALL_ICON_SPRITESHEET'].copy(), scale = 4).get_sprite(27, 0, 9, 9)
        self.background = self.image
        self.pos = [672, 400]

class InventoryCritIcon(Image):

    def __init__(self, game):
        super().__init__(game)

        self.image = Sprite(MENU_SPRITESHEETS['SMALL_ICON_SPRITESHEET'].copy(), scale = 4).get_sprite(36, 0, 9, 9)
        self.background = self.image
        self.pos = [672, 444]
    
class InventoryBleedIcon(Image):

    def __init__(self, game):
        super().__init__(game)

        self.image = Sprite(MENU_SPRITESHEETS['SMALL_ICON_SPRITESHEET'].copy(), scale = 4).get_sprite(36, 9, 9, 9)
        self.background = self.image
        self.pos = [792, 356]

class InventoryVenomIcon(Image):

    def __init__(self, game):
        super().__init__(game)

        self.image = Sprite(MENU_SPRITESHEETS['SMALL_ICON_SPRITESHEET'].copy(), scale = 4).get_sprite(45, 9, 9, 9)
        self.background = self.image
        self.pos = [792, 400]

class InventoryFireIcon(Image):

    def __init__(self, game):
        super().__init__(game)

        self.image = Sprite(MENU_SPRITESHEETS['SMALL_ICON_SPRITESHEET'].copy(), scale = 4).get_sprite(54, 9, 9, 9)
        self.background = self.image
        self.pos = [792, 444]

class InventoryHealIcon(Image):

    def __init__(self, game):
        super().__init__(game)

        self.image = Sprite(MENU_SPRITESHEETS['SMALL_ICON_SPRITESHEET'].copy(), scale = 4).get_sprite(45, 0, 9, 9)
        self.background = self.image
        self.pos = [792, 488]

class InventoryDeathIcon(Image):

    def __init__(self, game):
        super().__init__(game)

        self.image = Sprite(MENU_SPRITESHEETS['SMALL_ICON_SPRITESHEET'].copy(), scale = 4).get_sprite(0, 9, 9, 9)
        self.background = self.image
        self.pos = [912, 356]

class InventoryStunIcon(Image):

    def __init__(self, game):
        super().__init__(game)

        self.image = Sprite(MENU_SPRITESHEETS['SMALL_ICON_SPRITESHEET'].copy(), scale = 4).get_sprite(9, 9, 9, 9)
        self.background = self.image
        self.pos = [912, 400]

class InventoryDebuffIcon(Image):

    def __init__(self, game):
        super().__init__(game)

        self.image = Sprite(MENU_SPRITESHEETS['SMALL_ICON_SPRITESHEET'].copy(), scale = 4).get_sprite(18, 9, 9, 9)
        self.background = self.image
        self.pos = [912, 444]

class InventoryMobilityIcon(Image):

    def __init__(self, game):
        super().__init__(game)

        self.image = Sprite(MENU_SPRITESHEETS['SMALL_ICON_SPRITESHEET'].copy(), scale = 4).get_sprite(27, 9, 9, 9)
        self.background = self.image
        self.pos = [912, 488]

class InventoryIcon(Image):

    def __init__(self, game):
        super().__init__(game)

        self.image = Sprite(MENU_SPRITESHEETS['ICON_SPRITESHEET'].copy(), scale = 4).get_sprite(0, 0, 20, 20)
        self.background = self.image
        self.pos = [8, 8]
        
class TextboxPortrait(Image):

    def __init__(self, game):
        super().__init__(game)

        self.image = p.Surface((160, 160))
        self.image.fill(DARKBLUE)
        self.background = self.image
        self.pos = [0, 0]

    def update(self):

        self.image = self.game.textbox_portrait

class InventoryCombatImage(Image):

    def __init__(self, game, menu):
        super().__init__(game)

        self.menu = menu
        self.hero = menu.hero

        self.image = self.hero.combat_image.copy()
        self.scale = 1
        self.image = p.transform.scale(self.image, (self.image.get_width() * self.scale, self.image.get_height() * self.scale))
        self.pos = [564, 140]

    def update(self):

        self.hero = self.menu.hero
        
        self.image.fill(DARKBLUE)
        self.image.blit(self.hero.combat_image.copy(), [0, 0])

class HeroPreviewSlot(Image):

    def __init__(self, game, menu):
        super().__init__(game)

        self.menu = menu

        self.image = MENU_SPRITESHEETS['SLOT_THIN'].copy()
        self.scale = 4
        self.image = p.transform.scale(self.image, (self.image.get_width() * self.scale, self.image.get_height() * self.scale))
        self.background = self.image
        self.pos = [12, 12]

        self.hitbox = p.rect.Rect(self.pos[0] + self.menu.pos[0], self.pos[1] + self.menu.pos[1], self.image.get_width(), self.image.get_height())

    def update(self):

        self.image.blit(self.background, [0, 0])
        self.image = colour_swap(self.image, RED, FAKEBLACK)

        if self.hitbox.collidepoint(self.game.mouse.pos):

            self.image = colour_swap(self.image, FAKEBLACK, WHITE)

            if self.game.mouse.pressed['M1']:
                self.image = colour_swap(self.image, FAKEBLACK, YELLOW)
                if self.game.battle_mode == False:
                    if self.menu.hero != None:
                        self.game.camera_focus = self.menu.hero.exploration_character
                        self.game.selected_character = self.menu.hero
                        if self.game.inventory_open:
                            self.game.menus['INVENTORY'].hero = self.menu.hero
                        sound = p.mixer.Sound(BUTTON_SOUND)
                        sound.play()
                
                    for menu in self.game.menus.values():
                        if menu != self.menu:
                            menu.update_images()

        if self.menu.hero != None:
            if self.game.selected_character == self.menu.hero:

                self.image = colour_swap(self.image, FAKEBLACK, YELLOW)

class HeroInventoryPortraitSlot(Image):

    def __init__(self, game, menu, index):
        super().__init__(game)

        self.image = MENU_SPRITESHEETS['SLOT'].copy()
        self.scale = 4
        self.image = p.transform.scale(self.image, (self.image.get_width() * self.scale, self.image.get_height() * self.scale))
        self.background = self.image
        self.index = index
        self.pos = [548 + self.index * 120, 12]
        self.menu = menu

        self.hitbox = p.rect.Rect(self.pos[0] + self.menu.pos[0], self.pos[1] + self.menu.pos[1], self.image.get_width(), self.image.get_height())

    def update(self):
        
        self.image.blit(self.background, [0, 0])
        self.image = colour_swap(self.image, RED, FAKEBLACK)
        if self.hitbox.collidepoint(self.game.mouse.pos):

            self.image = colour_swap(self.image, FAKEBLACK, WHITE)
            if self.game.mouse.pressed['M1']:
                self.image = colour_swap(self.image, FAKEBLACK, YELLOW)
                if self.game.hero_party[self.index] != None:
                    self.game.menus['INVENTORY'].hero = self.game.hero_party[self.index]
                    self.game.menus['BOTTOM'].update_images()
                    sound = p.mixer.Sound(BUTTON_SOUND)
                    sound.play()

        if self.menu.hero == self.game.hero_party[self.index]:
            self.image = colour_swap(self.image, FAKEBLACK, YELLOW)

        if self.game.hero_party[self.index] == None:
            self.image.fill(BLUE)

class HeroInventorySkillSlot(Image):

    def __init__(self, game, menu, index):
        super().__init__(game)

        self.image = MENU_SPRITESHEETS['SLOT'].copy()
        self.scale = 4
        self.image = p.transform.scale(self.image, (self.image.get_width() * self.scale, self.image.get_height() * self.scale))
        self.background = self.image
        self.index = index
        self.pos = [552 + self.index * 120, 528]
        self.menu = menu

        self.hero = self.menu.hero

        self.hitbox = p.rect.Rect(self.pos[0] + self.menu.pos[0], self.pos[1] + self.menu.pos[1], self.image.get_width(), self.image.get_height())

    def update(self):

        self.hero = self.menu.hero

        self.image = self.background.copy()

        if type(self.hero) == Hero:
        
            self.image.blit(self.background, [0, 0])
            self.image = colour_swap(self.image, RED, FAKEBLACK)
            if self.hitbox.collidepoint(self.game.mouse.pos):

                self.image = colour_swap(self.image, FAKEBLACK, WHITE)
                if self.game.mouse.pressed['M1']:
                    self.hero.selected_skill = self.hero.skills[self.index]
                    sound = p.mixer.Sound(BUTTON_SOUND)
                    sound.play()
                    self.game.menus['BOTTOM'].update_images()

                if self.game.mouse.pressed['M2']:
                    self.hero.selected_skill = self.hero.skills[self.index]
                    sound = p.mixer.Sound(BUTTON_SOUND)
                    sound.play()
                    self.game.menus['BOTTOM'].update_images()
                    self.game.close_menu('INVENTORY')
                    self.game.open_menu('SELECT_SKILLS', self.hero)

            if self.hero.selected_skill == self.hero.skills[self.index]:
                self.image = colour_swap(self.image, FAKEBLACK, YELLOW)

            if self.game.selected_character == None:
                self.image.fill(BLUE)

        else:
            self.image.fill(BLUE)

class HeroInventorySkillImage(Image):

    def __init__(self, game, menu, index):
        super().__init__(game)

        self.menu = menu
        self.hero = self.menu.hero

        self.index = index
        if type(self.hero) == Hero:
            self.image = p.transform.scale(self.hero.skills[self.index].image.copy(), [80, 80])
        else:
            self.image = p.Surface((80, 80))
            self.image.fill(BLUE)
        self.pos = [564 + self.index * 120, 540]

    def update(self):

        self.hero = self.menu.hero

        if type(self.hero) == Hero:
            self.image.fill(DARKBLUE)
            self.image = p.transform.scale(self.hero.skills[self.index].image.copy(), [80, 80])

        else:

            self.image.fill(BLUE)

class HeroLargeSlot(Image):

    def __init__(self, game):
        super().__init__(game)

        self.image = MENU_SPRITESHEETS['SLOT_THICK'].copy()
        self.scale = 8
        self.image = p.transform.scale(self.image, (self.image.get_width() * self.scale, self.image.get_height() * self.scale))
        self.background = self.image
        self.pos = [4, 8]

    def update(self):
        
        self.image = self.background.copy()

class HugeSlot(Image):

    def __init__(self, game):
        super().__init__(game)

        self.image = MENU_SPRITESHEETS['SLOT_LARGE'].copy()
        self.scale = 4
        self.image = p.transform.scale(self.image, (self.image.get_width() * self.scale, self.image.get_height() * self.scale))
        self.background = self.image
        self.pos = [548, 124]

    def update(self):
        
        self.image = self.background.copy()  
    
class HeroPreviewPortrait(Image):

    def __init__(self, game, menu):
        super().__init__(game)

        self.menu = menu
        if self.menu.hero != None:
            self.image = self.menu.hero.portrait.copy()
        else:
            self.image = p.Surface((80, 80))
            self.image.fill((DARKBLUE))
        self.pos = [16, 16]

    def update(self):

        self.image.fill(DARKBLUE)
        if self.menu.hero != None:
            self.image.blit(self.menu.hero.portrait.copy(), [0, 0])

class HeroInventoryPortrait(Image):

    def __init__(self, game, index):
        super().__init__(game)

        self.index = index
        if self.game.hero_party[self.index] != None:
            self.image = self.game.hero_party[self.index].portrait.copy()
        else:
            self.image = p.Surface((40, 40))
            self.image.fill(BLUE)
        self.pos = [560 + self.index * 120, 24]

    def update(self):

        if self.game.hero_party[self.index] != None:
            self.image.fill(DARKBLUE)
            self.image.blit(self.game.hero_party[self.index].portrait, [0, 0])

class HeroLargePortrait(Image):

    def __init__(self, game):
        super().__init__(game)

        self.image = self.game.selected_character.large_portrait.copy()
        self.pos = [36, 40]

    def update(self):

        self.image.fill(DARKBLUE)
        self.image.blit(self.game.selected_character.large_portrait.copy(), [0, 0])

class SkillMenuPortrait(Image):

    def __init__(self, game, menu):
        super().__init__(game)

        self.menu = menu
        self.hero = self.menu.hero

        self.image = self.hero.portrait.copy()
        self.pos = [1048, 540]

    def update(self):

        self.image.fill(DARKBLUE)
        self.image.blit(self.hero.portrait.copy(), [0, 0])

class SkillPortraitSlot(Image):

    def __init__(self, game):
        super().__init__(game)

        self.image = MENU_SPRITESHEETS['SLOT'].copy()
        self.scale = 4
        self.image = p.transform.scale(self.image, (self.image.get_width() * self.scale, self.image.get_height() * self.scale))
        self.background = self.image
        self.pos = [1036, 528]

    def update(self):
        
        self.image = self.background.copy()

class SkillRangeIndicator(Image):
    
    def __init__(self, game, menu, index):
        super().__init__(game)

        self.menu = menu
        self.hero = self.menu.hero

        self.index = index

        self.scale = 4

        self.out_of_range_image = MENU_SPRITESHEETS['REPOSITION_SMALL'].copy()
        self.out_of_range_image = p.transform.scale(self.out_of_range_image, (self.out_of_range_image.get_width() * self.scale, self.out_of_range_image.get_height() * self.scale))

        self.damage_icon = Sprite(MENU_SPRITESHEETS['SMALL_ICON_SPRITESHEET'].copy(), scale = 4).get_sprite(0, 18, 9, 9)
        self.heal_icon = Sprite(MENU_SPRITESHEETS['SMALL_ICON_SPRITESHEET'].copy(), scale = 4).get_sprite(45, 0, 9, 9)

        self.image = self.out_of_range_image.copy()

        self.pos = [964 - index * 72, 564]

    def update(self):

        self.hero = self.menu.hero
        skill = self.hero.selected_skill

        self.image.blit(self.out_of_range_image, [0, 0])

        if skill.heals == False:

            if self.index >= skill.range[0] and self.index < skill.range[1]:

                self.image.blit(self.damage_icon, [16, 16])

        if skill.heals:

            if self.index >= skill.range[0] and self.index < skill.range[1]:

                self.image.blit(self.heal_icon, [16, 16])

class OnHitEffectIcon(Image):

    def __init__(self, game, menu):
        super().__init__(game)

        self.scale = 4

        self.icon = Sprite(MENU_SPRITESHEETS['SMALL_ICON_SPRITESHEET'].copy(), scale = 4).get_sprite(0, 18, 9, 9)

        self.image = p.Surface((36, 36))
        self.image.fill(BLUE)

        self.pos = [192, 468]

    def update(self):

        self.image.blit(self.icon, [0, 0])

class OnUseEffectIcon(Image):

    def __init__(self, game, menu):
        super().__init__(game)

        self.scale = 4

        self.icon = Sprite(MENU_SPRITESHEETS['SMALL_ICON_SPRITESHEET'].copy(), scale = 4).get_sprite(45, 0, 9, 9)

        self.image = p.Surface((36, 36))
        self.image.fill(BLUE)

        self.pos = [612, 468]

    def update(self):

        self.image.blit(self.icon, [0, 0])

class OnUseEnemyEffectDisplay(Image):
    
    def __init__(self, game, menu, index):
        super().__init__(game)

        self.menu = menu
        self.hero = self.menu.hero

        self.index = index

        self.scale = 4

        self.image = p.Surface((80, 80))
        self.image.fill(BLUE)

        self.pos = [660 + index * 96, 476]

    def update(self):

        self.hero = self.menu.hero
        skill = self.hero.selected_skill

        self.image.fill(BLUE)

        if skill != None:

            if self.index < len(skill.effects_on_user):

                if skill.effects_on_user[self.index] == 'BURNING':

                    self.image.blit(p.transform.scale(Burning(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_user[self.index] == 'BURNING2':

                    self.image.blit(p.transform.scale(Burning2(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_user[self.index] == 'BURNING3':

                    self.image.blit(p.transform.scale(Burning3(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_user[self.index] == 'BLEEDING':

                    self.image.blit(p.transform.scale(Bleeding(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_user[self.index] == 'BLEEDING2':

                    self.image.blit(p.transform.scale(Bleeding2(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_user[self.index] == 'BLEEDING3':

                    self.image.blit(p.transform.scale(Bleeding3(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_user[self.index] == 'STUNNING':

                    self.image.blit(p.transform.scale(Stun(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_user[self.index] == 'MARKING':

                    self.image.blit(p.transform.scale(Mark(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_user[self.index] == 'WEAKNESS':

                    self.image.blit(p.transform.scale(Weakness(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_user[self.index] == 'WEAKNESS2':

                    self.image.blit(p.transform.scale(Weakness2(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_user[self.index] == 'WEAKNESS3':

                    self.image.blit(p.transform.scale(Weakness3(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_user[self.index] == 'STRENGTH':

                    self.image.blit(p.transform.scale(Strength(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_user[self.index] == 'STRENGTH2':

                    self.image.blit(p.transform.scale(Strength2(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_user[self.index] == 'STRENGTH3':

                    self.image.blit(p.transform.scale(Strength3(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_user[self.index] == 'DODGE':

                    self.image.blit(p.transform.scale(Dodge(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_user[self.index] == 'DODGE2':

                    self.image.blit(p.transform.scale(Dodge2(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_user[self.index] == 'DODGE3':

                    self.image.blit(p.transform.scale(Dodge3(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_user[self.index] == 'ANTIDODGE':

                    self.image.blit(p.transform.scale(AntiDodge(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_user[self.index] == 'ANTIDODGE2':

                    self.image.blit(p.transform.scale(AntiDodge2(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_user[self.index] == 'ANTIDODGE3':

                    self.image.blit(p.transform.scale(AntiDodge3(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_user[self.index] == 'BLINDNESS':

                    self.image.blit(p.transform.scale(Blindness(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_user[self.index] == 'BLINDNESS2':

                    self.image.blit(p.transform.scale(Blindness2(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_user[self.index] == 'BLINDNESS3':

                    self.image.blit(p.transform.scale(Blindness3(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_user[self.index] == 'PRECISION':

                    self.image.blit(p.transform.scale(Precision(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_user[self.index] == 'PRECISION2':

                    self.image.blit(p.transform.scale(Precision2(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_user[self.index] == 'PRECISION3':

                    self.image.blit(p.transform.scale(Precision3(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_user[self.index] == 'SPEED':

                    self.image.blit(p.transform.scale(Speed(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_user[self.index] == 'SPEED2':

                    self.image.blit(p.transform.scale(Speed2(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_user[self.index] == 'SPEED3':

                    self.image.blit(p.transform.scale(Speed3(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_user[self.index] == 'PROTECTION':

                    self.image.blit(p.transform.scale(Protection(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_user[self.index] == 'PROTECTION2':

                    self.image.blit(p.transform.scale(Protection2(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_user[self.index] == 'PROTECTION3':

                    self.image.blit(p.transform.scale(Protection3(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_user[self.index] == 'BROKEN':

                    self.image.blit(p.transform.scale(BrokenArmour(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_user[self.index] == 'BROKEN2':

                    self.image.blit(p.transform.scale(BrokenArmour2(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_user[self.index] == 'BROKEN3':

                    self.image.blit(p.transform.scale(BrokenArmour3(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_user[self.index] == 'SLOWNESS':

                    self.image.blit(p.transform.scale(Slowness(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_user[self.index] == 'SLOWNESS2':

                    self.image.blit(p.transform.scale(Slowness2(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_user[self.index] == 'SLOWNESS3':

                    self.image.blit(p.transform.scale(Slowness3(self.game, None).image, [80, 80]), [0, 0])

                

            

class OnHitEnemyEffectDisplay(Image):
    
    def __init__(self, game, menu, index):
        super().__init__(game)

        self.menu = menu
        self.hero = self.menu.hero

        self.index = index

        self.scale = 4

        self.image = p.Surface((80, 80))
        self.image.fill(BLUE)

        self.pos = [240 + index * 96, 476]

    def update(self):

        self.hero = self.menu.hero
        skill = self.hero.selected_skill

        self.image.fill(BLUE)

        if skill != None:

            if self.index < len(skill.effects_on_hit):

                if skill.effects_on_hit[self.index] == 'BURNING':

                    self.image.blit(p.transform.scale(Burning(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_hit[self.index] == 'BURNING2':

                    self.image.blit(p.transform.scale(Burning2(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_hit[self.index] == 'BURNING3':

                    self.image.blit(p.transform.scale(Burning3(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_hit[self.index] == 'BLEEDING':

                    self.image.blit(p.transform.scale(Bleeding(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_hit[self.index] == 'BLEEDING2':

                    self.image.blit(p.transform.scale(Bleeding2(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_hit[self.index] == 'BLEEDING3':

                    self.image.blit(p.transform.scale(Bleeding3(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_hit[self.index] == 'STUNNING':

                    self.image.blit(p.transform.scale(Stun(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_hit[self.index] == 'MARKING':

                    self.image.blit(p.transform.scale(Mark(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_hit[self.index] == 'WEAKNESS':

                    self.image.blit(p.transform.scale(Weakness(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_hit[self.index] == 'WEAKNESS2':

                    self.image.blit(p.transform.scale(Weakness2(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_hit[self.index] == 'WEAKNESS3':

                    self.image.blit(p.transform.scale(Weakness3(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_hit[self.index] == 'STRENGTH':

                    self.image.blit(p.transform.scale(Strength(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_hit[self.index] == 'STRENGTH2':

                    self.image.blit(p.transform.scale(Strength2(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_hit[self.index] == 'STRENGTH3':

                    self.image.blit(p.transform.scale(Strength3(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_hit[self.index] == 'DODGE':

                    self.image.blit(p.transform.scale(Dodge(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_hit[self.index] == 'DODGE2':

                    self.image.blit(p.transform.scale(Dodge2(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_hit[self.index] == 'DODGE3':

                    self.image.blit(p.transform.scale(Dodge3(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_hit[self.index] == 'ANTIDODGE':

                    self.image.blit(p.transform.scale(AntiDodge(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_hit[self.index] == 'ANTIDODGE2':

                    self.image.blit(p.transform.scale(AntiDodge2(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_hit[self.index] == 'ANTIDODGE3':

                    self.image.blit(p.transform.scale(AntiDodge3(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_hit[self.index] == 'BLINDING':

                    self.image.blit(p.transform.scale(Blindness(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_hit[self.index] == 'BLINDING2':

                    self.image.blit(p.transform.scale(Blindness2(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_hit[self.index] == 'BLINDING3':

                    self.image.blit(p.transform.scale(Blindness3(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_hit[self.index] == 'CRIT':

                    self.image.blit(p.transform.scale(Crit(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_hit[self.index] == 'CRIT2':

                    self.image.blit(p.transform.scale(Crit2(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_hit[self.index] == 'CRIT3':

                    self.image.blit(p.transform.scale(Crit3(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_hit[self.index] == 'PRECISION':

                    self.image.blit(p.transform.scale(Precision(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_hit[self.index] == 'PRECISION2':

                    self.image.blit(p.transform.scale(Precision2(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_hit[self.index] == 'PRECISION3':

                    self.image.blit(p.transform.scale(Precision3(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_hit[self.index] == 'SPEED':

                    self.image.blit(p.transform.scale(Speed(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_hit[self.index] == 'SPEED2':

                    self.image.blit(p.transform.scale(Speed2(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_hit[self.index] == 'SPEED3':

                    self.image.blit(p.transform.scale(Speed3(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_hit[self.index] == 'PROTECTION':

                    self.image.blit(p.transform.scale(Protection(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_hit[self.index] == 'PROTECTION2':

                    self.image.blit(p.transform.scale(Protection2(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_hit[self.index] == 'PROTECTION3':

                    self.image.blit(p.transform.scale(Protection3(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_hit[self.index] == 'BROKEN':

                    self.image.blit(p.transform.scale(BrokenArmour(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_hit[self.index] == 'BROKEN2':

                    self.image.blit(p.transform.scale(BrokenArmour2(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_hit[self.index] == 'BROKEN3':

                    self.image.blit(p.transform.scale(BrokenArmour3(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_hit[self.index] == 'SLOWNESS':

                    self.image.blit(p.transform.scale(Slowness(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_hit[self.index] == 'SLOWNESS2':

                    self.image.blit(p.transform.scale(Slowness2(self.game, None).image, [80, 80]), [0, 0])

                elif skill.effects_on_hit[self.index] == 'SLOWNESS3':

                    self.image.blit(p.transform.scale(Slowness3(self.game, None).image, [80, 80]), [0, 0])






class HeroPreviewBuff(Image):

    def __init__(self, game, menu, index):
        super().__init__(game)

        self.menu = menu
        self.index = index

        self.image = p.Surface((40, 40))
        self.image.fill(BLUE)

        if self.menu.hero != None:
            if len(self.menu.hero.effects) > self.index:
                self.image.fill(BLUE)
                self.image.blit(self.menu.hero.effects[self.index].image.copy(), [0, 0])

        self.pos = [12 + 40 * self.index, 104]

    def update(self):

        self.image.fill(BLUE)
        if self.menu.hero != None:
            if len(self.menu.hero.effects) > self.index:
                self.image.fill(BLUE)
                self.image.blit(self.menu.hero.effects[self.index].image.copy(), [0, 0])
            else:
                self.image.fill(BLUE)

class EnemyPreviewBuff(Image):

    def __init__(self, game, menu, index):
        super().__init__(game)

        self.menu = menu
        self.index = index

        self.image = p.Surface((40, 40))
        self.image.fill(BLUE)

        if self.menu.enemy != None:
            if len(self.menu.enemy.effects) > self.index:
                self.image.fill(BLUE)
                self.image.blit(self.menu.enemy.effects[self.index].image.copy(), [0, 0])

        if self.index < 4:
            self.pos = [240 + 40 * self.index, 12]
        else:
            self.pos = [240 + 40 * (self.index - 4), 52]

    def update(self):
        
        if self.menu.enemy != None:
            if len(self.menu.enemy.effects) > self.index:
                self.image.fill(BLUE)
                self.image.blit(self.menu.enemy.effects[self.index].image.copy(), [0, 0])
            else:
                self.image.fill(BLUE)

class HeroBottomMenuBuff(Image):

    def __init__(self, game, menu, index):
        super().__init__(game)

        self.menu = menu
        self.index = index
        self.image = MENU_SPRITESHEETS['SLOT_THIN'].copy()
        self.scale = 2
        self.image = p.transform.scale(self.image, (self.image.get_width() * self.scale, self.image.get_height() * self.scale))

        self.background = self.image.copy()

        if self.menu.hero != None:
            if len(self.game.selected_character.effects) > self.index:
                self.icon = self.game.selected_character.effects[self.index].image.copy()
                self.image.blit(self.icon, (2, 2))

        self.pos = [232 + 48 * self.index, 188]

    def update(self):

        self.image = self.background.copy()

        if len(self.game.selected_character.effects) > self.index:
            self.icon = self.game.selected_character.effects[self.index].image.copy()
            self.image.blit(self.icon, (2, 2))
        else:
            self.image.fill(BLUE)

class EquipmentSlot(Image):

    def __init__(self, game, menu, index):
        super().__init__(game)

        self.menu = menu
        self.index = index
        self.image = MENU_SPRITESHEETS['SLOT'].copy()
        self.scale = 4
        self.image = p.transform.scale(self.image, (self.image.get_width() * self.scale, self.image.get_height() * self.scale))
        self.background = self.image
        self.selecting = False

        self.pos = [1036, 316 + self.index * 108]

        self.hitbox = p.rect.Rect(self.pos[0] + self.menu.pos[0], self.pos[1] + self.menu.pos[1], self.image.get_width(), self.image.get_height())

    def update(self):

        self.hero = self.menu.hero

        self.image = self.background.copy()

        if type(self.hero) == Hero:
        
            self.image.blit(self.background, [0, 0])
            self.image = colour_swap(self.image, RED, FAKEBLACK)
            if self.hitbox.collidepoint(self.game.mouse.pos):

                self.image = colour_swap(self.image, FAKEBLACK, WHITE)
                if self.game.mouse.pressed['M1']:
                    if self.selecting == False:
                        self.game.selecting_equipment = True
                        self.game.menus['INVENTORY'].images['EQUIPMENT1'].selecting = False
                        self.game.menus['INVENTORY'].images['EQUIPMENT2'].selecting = False
                        self.game.menus['INVENTORY'].images['EQUIPMENT3'].selecting = False
                        self.selecting = True
                        self.game.selected_item = None
                    else:
                        self.game.selecting_equipment = False
                        self.selecting = False


            if self.selecting:
                self.image = colour_swap(self.image, FAKEBLACK, YELLOW)

        else:
            self.image.fill(BLUE)


class StorageSlot(Image):

    def __init__(self, game, menu, index):
        super().__init__(game)

        self.menu = menu
        self.index = index
        self.image = MENU_SPRITESHEETS['SLOT'].copy()
        self.scale = 4
        self.image = p.transform.scale(self.image, (self.image.get_width() * self.scale, self.image.get_height() * self.scale))
        self.background = self.image

        column = self.index % 5
        row = self.index // 5

        self.pos = [8 + column * 108, 96 + row * 108]

        self.hitbox = p.rect.Rect(self.pos[0] + self.menu.pos[0], self.pos[1] + self.menu.pos[1], self.image.get_width(), self.image.get_height())

    def update(self):
        
        self.image.blit(self.background, [0, 0])
        self.image = colour_swap(self.image, RED, FAKEBLACK)

        pressed_keys = p.key.get_pressed()

        self.game.deleting = False

        if pressed_keys[p.K_LSHIFT]:
            self.game.deleting = True

        if self.hitbox.collidepoint(self.game.mouse.pos):

            self.image = colour_swap(self.image, FAKEBLACK, WHITE)

            if self.game.inventory[self.index] != None:
                self.game.textbox_text = self.game.inventory[self.index].desc

            if self.game.mouse.pressed['M1']:

                if self.game.deleting:
                    self.game.inventory[self.index] = None
                    sound = p.mixer.Sound(BUTTON_SOUND)
                    sound.play()

                elif self.game.selecting_equipment == False:
                    if self.game.selected_item == None:
                        self.game.selected_item = self.game.inventory[self.index]
                        sound = p.mixer.Sound(BUTTON_SOUND)
                        sound.play()
                    elif self.game.selected_item == self.game.inventory[self.index]:
                        self.game.selected_item = None
                        sound = p.mixer.Sound(BUTTON_SOUND)
                        sound.play()
                
                    else:

                        temp = self.game.selected_item
                        if self.game.selected_item in self.game.inventory:
                            pos_of_item = self.game.inventory.index(self.game.selected_item)
                            self.game.inventory[pos_of_item] = self.game.inventory[self.index]
                            self.game.inventory[self.index] = temp
                            self.game.selected_item = None
                            sound = p.mixer.Sound(BUTTON_SOUND)
                            sound.play()

                else:
                    for i in range(3):
                        if self.game.inventory[self.index] != None:
                            if self.game.inventory[self.index].equipable:
                                if self.game.inventory[self.index].character == self.menu.hero.type or self.game.inventory[self.index].character == 'ANY':
                                    if self.menu.images['EQUIPMENT' + str(i + 1)].selecting == True:
                                        temp = self.menu.hero.equipment[i]
                                        if self.menu.hero.equipment[i] != None:
                                            self.menu.hero.equipment[i].remove_item(self.menu.hero)
                                        self.menu.hero.equipment[i] = self.game.inventory[self.index]
                                        self.menu.hero.equipment[i].equip_item(self.menu.hero)
                                        self.game.inventory[self.index] = temp
                                        self.menu.images['EQUIPMENT' + str(i + 1)].selecting = False
                                        self.game.selecting_equipment = False
                                        sound = p.mixer.Sound(BUTTON_SOUND)
                                        sound.play()
                        else:
                            if self.menu.images['EQUIPMENT' + str(i + 1)].selecting == True:
                                temp = self.menu.hero.equipment[i]
                                if self.menu.hero.equipment[i] != None:
                                    self.menu.hero.equipment[i].remove_item(self.menu.hero)
                                self.menu.hero.equipment[i] = self.game.inventory[self.index]
                                self.game.inventory[self.index] = temp
                                self.menu.images['EQUIPMENT' + str(i + 1)].selecting = False
                                self.game.selecting_equipment = False
                                sound = p.mixer.Sound(BUTTON_SOUND)
                                sound.play()
                            

            if self.game.mouse.pressed['M2']:

                self.game.selected_item = self.game.inventory[self.index]
                if self.game.selected_item != None:
                    self.game.selected_item.use(self.index)
                sound = p.mixer.Sound(BUTTON_SOUND)
                sound.play()


        if self.game.deleting:
            if self.game.inventory[self.index] != None:
                self.image = colour_swap(self.image, FAKEBLACK, RED)
        elif self.game.selected_item == self.game.inventory[self.index]:
            if self.game.inventory[self.index] != None:
                self.image = colour_swap(self.image, FAKEBLACK, YELLOW)

class StorageImage(Image):

    def __init__(self, game, index):
        super().__init__(game)

        self.index = index

        if self.game.inventory[self.index] != None:

            self.image = self.game.inventory[self.index].image.copy()

        else:

            self.image = p.Surface((80, 80))
            self.image.fill(DARKBLUE)

        column = self.index % 5
        row = self.index // 5

        self.pos = [20 + column * 108, 108 + row * 108]

    def update(self):
        
        self.image.fill(DARKBLUE)

        if self.game.inventory[self.index] != None:

            self.image = self.game.inventory[self.index].image.copy()

class EquipmentImage(Image):

    def __init__(self, game, menu, index):
        super().__init__(game)

        self.index = index
        self.menu = menu
        self.hero = self.menu.hero

        if type(self.hero) == Hero:

            if self.hero.equipment[self.index] != None:

                self.image = self.hero.equipment[self.index].image.copy()

            else:

                self.image = p.Surface((80, 80))
                self.image.fill(DARKBLUE)

        else:

            self.image = p.Surface((80, 80))
            self.image.fill(DARKBLUE)

        self.pos = [1048, 328 + self.index * 108]

    def update(self):
        
        self.image.fill(DARKBLUE)

        self.hero = self.menu.hero

        if type(self.hero) == Hero:


            if self.hero.equipment[self.index] != None:

                self.image = self.hero.equipment[self.index].image.copy()

        else:

            self.image.fill(BLUE)


class LootSlot(Image):

    def __init__(self, game, menu, index, loot_list):
        super().__init__(game)

        self.menu = menu
        self.index = index
        self.image = MENU_SPRITESHEETS['SLOT'].copy()
        self.scale = 4
        self.image = p.transform.scale(self.image, (self.image.get_width() * self.scale, self.image.get_height() * self.scale))
        self.background = self.image
        self.loot_list = loot_list

        column = self.index % 4
        row = self.index // 4

        self.pos = [712 + column * 108, 124 + row * 108]

        self.hitbox = p.rect.Rect(self.pos[0] + self.menu.pos[0], self.pos[1] + self.menu.pos[1], self.image.get_width(), self.image.get_height())

    def update(self):
        
        self.image.blit(self.background, [0, 0])
        self.image = colour_swap(self.image, RED, FAKEBLACK)
        if self.hitbox.collidepoint(self.game.mouse.pos):

            if self.loot_list[self.index] != None:

                self.game.textbox_text = self.loot_list[self.index].desc

            self.image = colour_swap(self.image, FAKEBLACK, WHITE)
            if self.game.mouse.pressed['M1']:
                self.game.selected_item = self.loot_list[self.index]
                if self.game.selected_item != None:
                    slotfound, slot = self.game.check_inventory_full()
                    if slotfound == True:
                        self.game.inventory[slot] = self.game.selected_item
                        self.loot_list[self.index] = None
                        self.game.selected_item = None
                    sound = p.mixer.Sound(BUTTON_SOUND)
                    sound.play()

class LootImage(Image):

    def __init__(self, game, index, loot_list):
        super().__init__(game)

        self.index = index
        self.loot_list = loot_list

        if self.loot_list[self.index] != None:

            self.image = self.loot_list[self.index].image.copy()

        else:

            self.image = p.Surface((80, 80))
            self.image.fill(DARKBLUE)

        column = self.index % 4
        row = self.index // 4

        self.pos = [724 + column * 108, 136 + row * 108]

    def update(self):
        
        self.image.fill(DARKBLUE)

        if self.loot_list[self.index] != None:

            self.image = self.loot_list[self.index].image.copy()


class SkillDamageIcon(Image):

    def __init__(self, game, menu):
        super().__init__(game)

        self.damage_icon = Sprite(MENU_SPRITESHEETS['SMALL_ICON_SPRITESHEET'].copy(), scale = 4).get_sprite(0, 18, 9, 9)
        self.heal_icon = Sprite(MENU_SPRITESHEETS['SMALL_ICON_SPRITESHEET'].copy(), scale = 4).get_sprite(45, 0, 9, 9)

        self.image = self.damage_icon.copy()

        self.pos = [8, 384]
        self.menu = menu

    def update(self):

        self.image.fill(BLUE)

        if self.menu.hero.selected_skill != None:

            if self.menu.hero.selected_skill.heals == False:

                self.image.blit(self.damage_icon, [0, 0])

            else:

                self.image.blit(self.heal_icon, [0, 0])

class SkillCritIcon(Image):

    def __init__(self, game, menu):
        super().__init__(game)

        self.icon = Sprite(MENU_SPRITESHEETS['SMALL_ICON_SPRITESHEET'].copy(), scale = 4).get_sprite(36, 0, 9, 9)

        self.image = self.icon.copy()

        self.pos = [8, 424]
        self.menu = menu

    def update(self):

        self.image.fill(BLUE)

        self.image.blit(self.icon, [0, 0])

    

class SkillPrecisionIcon(Image):

    def __init__(self, game, menu):
        super().__init__(game)

        self.icon = Sprite(MENU_SPRITESHEETS['SMALL_ICON_SPRITESHEET'].copy(), scale = 4).get_sprite(27, 0, 9, 9)

        self.image = self.icon.copy()

        self.pos = [8, 464]
        self.menu = menu

    def update(self):

        self.image.fill(BLUE)

        self.image.blit(self.icon, [0, 0])

class SkillStunIcon(Image):

    def __init__(self, game, menu):
        super().__init__(game)

        self.icon = Sprite(MENU_SPRITESHEETS['SMALL_ICON_SPRITESHEET'].copy(), scale = 4).get_sprite(9, 9, 9, 9)

        self.image = self.icon.copy()

        self.pos = [8, 464]
        self.menu = menu

    def update(self):

        self.image.fill(BLUE)

        if self.menu.hero.selected_skill != None:

            if 'STUNNING' in self.menu.hero.selected_skill.effects_on_hit:

                self.image.blit(self.icon, [0, 0])

class SkillDebuffIcon(Image):

    def __init__(self, game, menu):
        super().__init__(game)

        self.icon = Sprite(MENU_SPRITESHEETS['SMALL_ICON_SPRITESHEET'].copy(), scale = 4).get_sprite(18, 9, 9, 9)

        self.image = self.icon.copy()

        self.pos = [8, 504]
        self.menu = menu

    def update(self):

        self.image.fill(BLUE)

        if self.menu.hero.selected_skill != None:

            if self.menu.hero.selected_skill.debuffing:

                self.image.blit(self.icon, [0, 0])

class SkillInfoImage(Image):

    def __init__(self, game, menu, index):
        super().__init__(game)

        self.menu = menu
        self.hero = self.menu.hero

        self.index = index
        if type(self.hero) == Hero:
            self.image = p.transform.scale(self.hero.skills[self.index].image.copy(), [80, 80])
        else:
            self.image = p.Surface((80, 80))
            self.image.fill(BLUE)
        self.pos = [24 + self.index * 120, 140]

    def update(self):

        self.hero = self.menu.hero

        if type(self.hero) == Hero:
            self.image.fill(DARKBLUE)
            self.image = p.transform.scale(self.hero.skills[self.index].image.copy(), [80, 80])

class SelectedSkillImage(Image):

    def __init__(self, game, menu):
        super().__init__(game)

        self.menu = menu
        self.hero = self.menu.hero
        self.skill = self.hero.selected_skill

        self.background = MENU_SPRITESHEETS['SLOT_THICK'].copy()
        self.scale = 4
        self.background = p.transform.scale(self.background, (self.background.get_width() * self.scale, self.background.get_height() * self.scale))

        self.icon = p.transform.scale(self.skill.image.copy(), [80, 80])

        self.pos = [8, 268]

    def update(self):

        self.hero = self.menu.hero 
        self.skill = self.hero.selected_skill
        if self.skill != None:
            self.icon = p.transform.scale(self.skill.image.copy(), [80, 80])

        self.image = self.background.copy()
        self.image.blit(self.icon, [16, 16])

class SkillInfoSlot(Image):

    def __init__(self, game, menu, index):
        super().__init__(game)

        self.image = MENU_SPRITESHEETS['SLOT_THICK'].copy()
        self.scale = 4
        self.image = p.transform.scale(self.image, (self.image.get_width() * self.scale, self.image.get_height() * self.scale))
        self.background = self.image
        self.index = index
        self.pos = [8 + self.index * 120, 124]
        self.menu = menu

        self.hero = self.menu.hero

        self.hitbox = p.rect.Rect(self.pos[0] + self.menu.pos[0], self.pos[1] + self.menu.pos[1], self.image.get_width(), self.image.get_height())

    def update(self):

        self.hero = self.menu.hero

        self.image = self.background.copy()

        if type(self.hero) == Hero:
        
            self.image.blit(self.background, [0, 0])
            self.image = colour_swap(self.image, RED, FAKEBLACK)
            if self.hitbox.collidepoint(self.game.mouse.pos):

                self.image = colour_swap(self.image, FAKEBLACK, WHITE)
                if self.game.mouse.pressed['M1']:
                    self.hero.selected_skill = self.hero.skills[self.index]
                    sound = p.mixer.Sound(BUTTON_SOUND)
                    sound.play()
                    self.game.menus['BOTTOM'].update_images()

            if self.hero.selected_skill == self.hero.skills[self.index]:
                self.image = colour_swap(self.image, FAKEBLACK, YELLOW)








