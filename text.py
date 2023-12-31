import pygame as p
from sprite import *
from settings import *
from image import *

# text is a type of image which uses the font loaded in main.py to draw words
# most are very simple so will not to be explained

class Text(Image):

    def __init__(self, game):
        super().__init__(game)

        self.text = ''

    def draw_text(self):

        # first the background is filled to draw over previous text

        self.image.fill(BLUE)

        x = 0
        y = 0

        # for every letter in the text

        for letter in self.text:

            # if the character is one of the characters in the list of characters that there is an image for

            if letter in self.game.letters:
                # get the image of the letter, scale it to the right size, change x by the width of this character so the next character can be drawn next to this one
                letter_image = self.game.font[letter]
                letter_image = p.transform.scale(letter_image, (FONT_WIDTH * self.scale, FONT_HEIGHT * self.scale))
                self.image.blit(letter_image, (x, y))
                x += FONT_WIDTH * self.scale

            if letter == ' ':
                x += FONT_WIDTH * self.scale

            # if a new line is started, the x is reset so characters are drawn at the start of the line again, and the y is changed so characters are drawn below the last line
            
            if letter == '\n':
                x = 0
                y += FONT_HEIGHT * self.scale

    def update(self):
        
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

class BarkText(Text):

    def __init__(self, game, text):
        super().__init__(game)

        self.text = str(text)
        self.scale = 1

        self.pos = [28, 12]

        self.width = FONT_WIDTH * self.scale * 42
        self.height = FONT_HEIGHT * self.scale * 7

        self.image = p.Surface((self.width * self.scale, self.height * self.scale))
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

        self.update()

    def draw_text(self):

        self.image.fill(BEIGE)

        x = 0
        y = 0

        for letter in self.text:

            if letter in self.game.letters:
                letter_image = self.game.font[letter]
                letter_image = p.transform.scale(letter_image, (FONT_WIDTH * self.scale, FONT_HEIGHT * self.scale))
                self.image.blit(letter_image, (x, y))
                x += FONT_WIDTH * self.scale

            if letter == ' ':
                x += FONT_WIDTH * self.scale
            
            if letter == '\n':
                x = 0
                y += FONT_HEIGHT * self.scale

        self.image = colour_swap(self.image, WHITE, BLACK)

class DamageNumber(Text):

    def __init__(self, game, text):
        super().__init__(game)

        self.text = str(text)
        self.scale = 2

        self.width = len(self.text) * FONT_WIDTH
        self.height = FONT_HEIGHT

        self.image = p.Surface((self.width * self.scale, self.height * self.scale))
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

        self.game.numbers.add(self)

        self.update()

    def draw_text(self):

        self.image.fill(FAKEBLACK)

        x = 0
        y = 0

        for letter in self.text:

            if letter in self.game.letters:
                letter_image = self.game.font[letter]
                letter_image = p.transform.scale(letter_image, (FONT_WIDTH * self.scale, FONT_HEIGHT * self.scale))
                self.image.blit(letter_image, (x, y))
                x += FONT_WIDTH * self.scale

            if letter == ' ':
                x += FONT_WIDTH * self.scale
            
            if letter == '\n':
                x = 0
                y += FONT_HEIGHT * self.scale

        if "CRIT" in self.text:

            self.image = colour_swap(self.image, WHITE, ORANGE)

        elif "MISSED" in self.text or "DODGED" in self.text:

            pass

        else:

            self.image = colour_swap(self.image, WHITE, RED)

    def update(self):
        
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

class HealNumber(Text):

    def __init__(self, game, text):
        super().__init__(game)

        self.text = str(text)
        self.scale = 2

        self.width = len(self.text) * FONT_WIDTH
        self.height = FONT_HEIGHT

        self.image = p.Surface((self.width * self.scale, self.height * self.scale))
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

        self.game.numbers.add(self)

        self.update()

    def draw_text(self):

        self.image.fill(FAKEBLACK)

        x = 0
        y = 0

        for letter in self.text:

            if letter in self.game.letters:
                letter_image = self.game.font[letter]
                letter_image = p.transform.scale(letter_image, (FONT_WIDTH * self.scale, FONT_HEIGHT * self.scale))
                self.image.blit(letter_image, (x, y))
                x += FONT_WIDTH * self.scale

            if letter == ' ':
                x += FONT_WIDTH * self.scale
            
            if letter == '\n':
                x = 0
                y += FONT_HEIGHT * self.scale

        if "CRIT" in self.text:

            self.image = colour_swap(self.image, WHITE, GREEN)

        else:

            self.image = colour_swap(self.image, WHITE, DARKGREEN)

    def update(self):
        
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

class SanityHealNumber(Text):

    def __init__(self, game, text):
        super().__init__(game)

        self.text = str(text)
        self.scale = 2

        self.width = len(self.text) * FONT_WIDTH
        self.height = FONT_HEIGHT

        self.image = p.Surface((self.width * self.scale, self.height * self.scale))
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

        self.game.numbers.add(self)

        self.update()

    def draw_text(self):

        self.image.fill(FAKEBLACK)

        x = 0
        y = 0

        for letter in self.text:

            if letter in self.game.letters:
                letter_image = self.game.font[letter]
                letter_image = p.transform.scale(letter_image, (FONT_WIDTH * self.scale, FONT_HEIGHT * self.scale))
                self.image.blit(letter_image, (x, y))
                x += FONT_WIDTH * self.scale

            if letter == ' ':
                x += FONT_WIDTH * self.scale
            
            if letter == '\n':
                x = 0
                y += FONT_HEIGHT * self.scale

    def update(self):
        
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))



class SanityDamageNumber(Text):

    def __init__(self, game, text):
        super().__init__(game)

        self.text = str(text)
        self.scale = 2

        self.width = len(self.text) * FONT_WIDTH
        self.height = FONT_HEIGHT

        self.image = p.Surface((self.width * self.scale, self.height * self.scale))
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

        self.game.numbers.add(self)

        self.update()

    def draw_text(self):

        self.image.fill(FAKEBLACK)

        x = 0
        y = 0

        for letter in self.text:

            if letter in self.game.letters:
                letter_image = self.game.font[letter]
                letter_image = p.transform.scale(letter_image, (FONT_WIDTH * self.scale, FONT_HEIGHT * self.scale))
                self.image.blit(letter_image, (x, y))
                x += FONT_WIDTH * self.scale

            if letter == ' ':
                x += FONT_WIDTH * self.scale
            
            if letter == '\n':
                x = 0
                y += FONT_HEIGHT * self.scale

        self.image = colour_swap(self.image, WHITE, PURPLE)

    def update(self):
        
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

class NPCText(Text):

    def __init__(self, game, text):
        super().__init__(game)

        self.scale = 1
        self.text = text
        self.pos = [560, 20]

        self.width = 40 * FONT_WIDTH
        self.height = 7 * FONT_HEIGHT

        self.image = p.Surface((self.width, self.height))
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

    def update(self):

        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

class TextboxText(Text):

    def __init__(self, game):
        super().__init__(game)

        self.scale = 1
        self.text = ''
        self.pos = [176, 8]

        self.width = 110 * FONT_WIDTH
        self.height = 8 * FONT_HEIGHT

        self.image = p.Surface((self.width, self.height))
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

    def update(self):

        self.text = self.game.textbox_text

        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

class CostText(Text):

    def __init__(self, game, menu):
        super().__init__(game)

        self.menu = menu
        self.scale = 4
        self.text = str(self.menu.cost)
        self.pos = [956, 544]

        self.width = 4 * FONT_WIDTH
        self.height = 1 * FONT_HEIGHT

        self.image = p.Surface((self.width, self.height))
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

    def update(self):

        self.text = str(self.menu.cost)
        
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

class MoneyText(Text):

    def __init__(self, game):
        super().__init__(game)

        self.scale = 4
        self.text = str(self.game.money)
        self.pos = [1540, 112]

        self.width = 8 * FONT_WIDTH
        self.height = 1 * FONT_HEIGHT

        self.image = p.Surface((self.width, self.height))
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

    def update(self):

        self.text = str(self.game.money)
        
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

class HeroPreviewName(Text):

    def __init__(self, game, menu):
        super().__init__(game)

        self.menu = menu

        self.scale = 2
        if self.menu.hero != None:
            self.text = self.menu.hero.name
        self.pos = [108, 12]

        self.width = 10 * FONT_WIDTH
        self.height = 1 * FONT_HEIGHT

        self.image = p.Surface((self.width, self.height))
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

    def update(self):
        
        if self.menu.hero != None:
            self.text = self.menu.hero.name

        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

class EnemyPreviewName(Text):

    def __init__(self, game, menu):
        super().__init__(game)

        self.menu = menu

        self.scale = 2
        if self.menu.enemy != None:
            self.text = self.menu.enemy.name
        self.pos = [12, 12]

        self.width = 10 * FONT_WIDTH
        self.height = 1 * FONT_HEIGHT

        self.image = p.Surface((self.width, self.height))
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

    def update(self):
        
        if self.menu.enemy != None:
            self.text = self.menu.enemy.name

        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

class HeroLargeName(Text):

    def __init__(self, game):
        super().__init__(game)

        self.scale = 2
        self.text = self.game.selected_character.name
        self.pos = [232, 8]
        
        self.width = 18 * FONT_WIDTH
        self.height = 1 * FONT_HEIGHT

        self.image = p.Surface((self.width, self.height))
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

    def update(self):

        self.text = self.game.selected_character.name
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

class MenuTitle(Text):

    def __init__(self, game, text):
        super().__init__(game)

        self.scale = 4
        self.text = text
        self.pos = [88, 12]

        self.width = 16 * FONT_WIDTH
        self.height = 1 * FONT_HEIGHT

        self.image = p.Surface((self.width, self.height))
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

    def update(self):

        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

class SkillName(Text):

    def __init__(self, game, menu):
        super().__init__(game)

        self.menu = menu
        self.hero = self.menu.hero
        self.scale = 2
        self.text = self.menu.skill.name
        self.pos = [164, 268]
        self.width = 40 * FONT_WIDTH
        self.height = 1 * FONT_HEIGHT

        self.image = p.Surface((self.width, self.height))
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

    def update(self):
        
        self.hero = self.menu.hero
        if self.menu.skill != None:
            self.text = self.menu.skill.name
        
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

class SkillDesc(Text):

    def __init__(self, game, menu):
        super().__init__(game)

        self.menu = menu
        self.hero = self.menu.hero
        self.scale = 1
        self.text = self.menu.skill.desc
        self.pos = [164, 308]
        self.width = 85 * FONT_WIDTH
        self.height = 8 * FONT_HEIGHT

        self.image = p.Surface((self.width, self.height))
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

    def update(self):
        
        self.hero = self.menu.hero
        if self.menu.skill != None:
            self.text = self.menu.skill.desc
        
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

class InventoryName(Text):

    def __init__(self, game, menu):
        super().__init__(game)

        self.menu = menu
        self.hero = self.menu.hero
        self.scale = 2
        self.text = self.hero.name
        self.pos = [548, 316]
        self.width = 18 * FONT_WIDTH
        self.height = 1 * FONT_HEIGHT

        self.image = p.Surface((self.width, self.height))
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

    def update(self):
        
        self.hero = self.menu.hero
        self.text = self.hero.name
        
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

class WeaponText(Text):

    def __init__(self, game, menu):
        super().__init__(game)

        self.menu = menu
        self.hero = self.menu.hero
        self.scale = 1
        self.text = ''
        
        if self.hero != None and type(self.hero) == Hero:
            level = self.hero.weapon_level
            if level < (len(WEAPON_VALUES[self.hero.type])) - 1:
                self.text += 'DAMAGE: {}-{} -> {}-{}'.format(
                    WEAPON_VALUES[self.hero.type][level][0], # gets the damage value for this heros level
                    WEAPON_VALUES[self.hero.type][level][1],
                    WEAPON_VALUES[self.hero.type][level + 1][0], # gets the damage value for this heros level if their level was one more
                    WEAPON_VALUES[self.hero.type][level + 1][1])
                self.text += '\nPRECISION: {} -> {}'.format(
                    WEAPON_VALUES[self.hero.type][level][2],
                    WEAPON_VALUES[self.hero.type][level + 1][2])
                self.text += '\nCRIT: {} -> {}'.format(
                    WEAPON_VALUES[self.hero.type][level][3],
                    WEAPON_VALUES[self.hero.type][level + 1][3])

        self.pos = [648, 292]
        
        self.width = 30 * FONT_WIDTH
        self.height = 6 * FONT_HEIGHT

        self.image = p.Surface((self.width, self.height))
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

    def update(self):

        self.hero = self.menu.hero
        self.text = ''
        
        if self.hero != None and type(self.hero) == Hero:
            level = self.hero.weapon_level
            if level < (len(WEAPON_VALUES[self.hero.type])) - 1:
                self.text += 'DAMAGE: {}-{} -> {}-{}'.format(
                    WEAPON_VALUES[self.hero.type][level][0],
                    WEAPON_VALUES[self.hero.type][level][1],
                    WEAPON_VALUES[self.hero.type][level + 1][0],
                    WEAPON_VALUES[self.hero.type][level + 1][1])
                self.text += '\nPRECISION: {} -> {}'.format(
                    WEAPON_VALUES[self.hero.type][level][2],
                    WEAPON_VALUES[self.hero.type][level + 1][2])
                self.text += '\nCRIT: {} -> {}'.format(
                    WEAPON_VALUES[self.hero.type][level][3],
                    WEAPON_VALUES[self.hero.type][level + 1][3])
        
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))


class ArmourText(Text):

    def __init__(self, game, menu):
        super().__init__(game)

        self.menu = menu
        self.hero = self.menu.hero
        self.scale = 1
        self.text = ''
        
        if self.hero != None and type(self.hero) == Hero:
            level = self.hero.armour_level
            if level < (len(ARMOUR_VALUES[self.hero.type])) - 1:
                self.text += '\nPROTECTION: {} -> {}'.format(
                    ARMOUR_VALUES[self.hero.type][level][0],
                    ARMOUR_VALUES[self.hero.type][level + 1][0])
                self.text += '\nSPEED: {} -> {}'.format(
                    ARMOUR_VALUES[self.hero.type][level][1],
                    ARMOUR_VALUES[self.hero.type][level + 1][1])
                self.text += '\nHEALING: {} -> {}'.format(
                    ARMOUR_VALUES[self.hero.type][level][2],
                    ARMOUR_VALUES[self.hero.type][level + 1][2])

        self.pos = [648, 408]
        
        self.width = 30 * FONT_WIDTH
        self.height = 6 * FONT_HEIGHT

        self.image = p.Surface((self.width, self.height))
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

    def update(self):

        self.hero = self.menu.hero
        self.text = ''
        
        if self.hero != None and type(self.hero) == Hero:
            level = self.hero.armour_level
            if level < (len(ARMOUR_VALUES[self.hero.type])) - 1:
                self.text += '\nPROTECTION: {} -> {}'.format(
                    ARMOUR_VALUES[self.hero.type][level][0],
                    ARMOUR_VALUES[self.hero.type][level + 1][0])
                self.text += '\nSPEED: {} -> {}'.format(
                    ARMOUR_VALUES[self.hero.type][level][1],
                    ARMOUR_VALUES[self.hero.type][level + 1][1])
                self.text += '\nHEALING: {} -> {}'.format(
                    ARMOUR_VALUES[self.hero.type][level][2],
                    ARMOUR_VALUES[self.hero.type][level + 1][2])
        
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))


class InventoryHealth(Text):

    def __init__(self, game, menu):
        super().__init__(game)

        self.menu = menu
        self.hero = self.menu.hero
        self.scale = 2
        self.text = str(int(self.hero.max_health))
        self.pos = [588, 356]
        self.width = 3 * FONT_WIDTH
        self.height = 1 * FONT_HEIGHT

        self.image = p.Surface((self.width, self.height))
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

    def update(self):

        self.hero = self.menu.hero
        self.text = str(int(self.hero.max_health))
        
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

class InventoryProtection(Text):

    def __init__(self, game, menu):
        super().__init__(game)

        self.menu = menu
        self.hero = self.menu.hero
        self.scale = 2
        self.text = str(self.hero.protection) + '%'
        self.pos = [588, 400]
        self.width = 3 * FONT_WIDTH
        self.height = 1 * FONT_HEIGHT

        self.image = p.Surface((self.width, self.height))
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

    def update(self):

        self.hero = self.menu.hero
        self.text = str(self.hero.protection) + '%'
        
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

class InventorySpeed(Text):

    def __init__(self, game, menu):
        super().__init__(game)

        self.menu = menu
        self.hero = self.menu.hero
        self.scale = 2
        self.text = str(self.hero.speed)
        self.pos = [588, 444]
        self.width = 3 * FONT_WIDTH
        self.height = 1 * FONT_HEIGHT

        self.image = p.Surface((self.width, self.height))
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

    def update(self):

        self.hero = self.menu.hero
        self.text = str(self.hero.speed)
        
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

class InventoryDamage(Text):

    def __init__(self, game, menu):
        super().__init__(game)

        self.menu = menu
        self.hero = self.menu.hero
        self.scale = 2
        self.text = str(int(self.hero.damage[0])) + '-' + str(int(self.hero.damage[1]))
        self.pos = [588, 488]
        self.width = 9 * FONT_WIDTH
        self.height = 1 * FONT_HEIGHT

        self.image = p.Surface((self.width, self.height))
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

    def update(self):

        self.hero = self.menu.hero

        self.text = str(int(self.hero.damage[0])) + '-' + str(int(self.hero.damage[1]))
        
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

class SkillDamageMultiplier(Text):

    def __init__(self, game, menu):
        super().__init__(game)

        self.menu = menu
        self.hero = self.menu.hero
        self.skill = self.menu.skill
        self.scale = 2
        self.text = 'X' + str(self.skill.multiplier)
        self.pos = [48, 384]
        self.width = 9 * FONT_WIDTH
        self.height = 1 * FONT_HEIGHT

        self.image = p.Surface((self.width, self.height))
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

    def update(self):
        
        self.hero = self.menu.hero
        self.skill = self.menu.skill

        self.image.fill(BLUE)

        if self.skill != None:

            self.text = 'X' + str(self.skill.multiplier)

        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))



class SkillCritMultiplier(Text):

    def __init__(self, game, menu):
        super().__init__(game)

        self.menu = menu
        self.hero = self.menu.hero
        self.skill = self.menu.skill
        self.scale = 2
        if self.skill.bonus_crit < 0:
            self.text = '-' + str(self.skill.bonus_crit)
        if self.skill.bonus_crit > 0:
            self.text = '+' + str(self.skill.bonus_crit)
        if self.skill.bonus_crit == 0:
            self.text = '+0'
        self.pos = [48, 424]
        self.width = 9 * FONT_WIDTH
        self.height = 1 * FONT_HEIGHT

        self.image = p.Surface((self.width, self.height))
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

    def update(self):
        
        self.hero = self.menu.hero
        self.skill = self.menu.skill

        self.image.fill(BLUE)

        if self.skill != None:

            if self.skill.bonus_crit < 0:
                self.text = '-' + str(self.skill.bonus_crit)
            if self.skill.bonus_crit > 0:
                self.text = '+' + str(self.skill.bonus_crit)
            if self.skill.bonus_crit == 0:
                self.text = '+0'

        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

class SkillPrecisionMultiplier(Text):

    def __init__(self, game, menu):
        super().__init__(game)

        self.menu = menu
        self.hero = self.menu.hero
        self.skill = self.menu.skill
        self.scale = 2
        if self.skill.bonus_precision < 0:
            self.text = '-' + str(self.skill.bonus_precision)
        if self.skill.bonus_precision > 0:
            self.text = '+' + str(self.skill.bonus_precision)
        if self.skill.bonus_precision == 0:
            self.text = '+0'
        self.pos = [48, 464]
        self.width = 9 * FONT_WIDTH
        self.height = 1 * FONT_HEIGHT

        self.image = p.Surface((self.width, self.height))
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

    def update(self):
        
        self.hero = self.menu.hero
        self.skill = self.menu.skill

        self.image.fill(BLUE)

        if self.skill != None:

            if self.skill.bonus_precision < 0:
                self.text = '-' + str(self.skill.bonus_precision)
            if self.skill.bonus_precision > 0:
                self.text = '+' + str(self.skill.bonus_precision)
            if self.skill.bonus_precision == 0:
                self.text = '+0'

        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

    
class SkillStunMultiplier(Text):

    def __init__(self, game, menu):
        super().__init__(game)

        self.menu = menu
        self.hero = self.menu.hero
        self.skill = self.menu.skill
        self.scale = 2
        if 'STUNNING' in self.skill.effects_on_hit:
            if self.skill.bonus_stun < 0:
                self.text = '-' + str(self.skill.bonus_stun)
            if self.skill.bonus_stun > 0:
                self.text = '+' + str(self.skill.bonus_stun)
            if self.skill.bonus_stun == 0:
                self.text = '+0'
        self.pos = [48, 504]
        self.width = 9 * FONT_WIDTH
        self.height = 1 * FONT_HEIGHT

        self.image = p.Surface((self.width, self.height))
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

    def update(self):
        
        self.hero = self.menu.hero
        self.skill = self.menu.skill

        self.image.fill(BLUE)

        if self.skill != None:

            if 'STUNNING' in self.skill.effects_on_hit:

                if self.skill.bonus_stun < 0:
                    self.text = '-' + str(self.skill.bonus_stun)
                if self.skill.bonus_stun > 0:
                    self.text = '+' + str(self.skill.bonus_stun)
                if self.skill.bonus_stun == 0:
                    self.text = '+0'

            else:

                self.text = ''

        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

class SkillDebuffMultiplier(Text):

    def __init__(self, game, menu):
        super().__init__(game)

        self.menu = menu
        self.hero = self.menu.hero
        self.skill = self.menu.skill
        self.scale = 2
        if self.skill.debuffing:
            if self.skill.bonus_debuff < 0:
                self.text = '-' + str(self.skill.bonus_debuff)
            if self.skill.bonus_debuff > 0:
                self.text = '+' + str(self.skill.bonus_debuff)
            if self.skill.bonus_debuff == 0:
                self.text = '+0'
        self.pos = [48, 544]
        self.width = 9 * FONT_WIDTH
        self.height = 1 * FONT_HEIGHT

        self.image = p.Surface((self.width, self.height))
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

    def update(self):
        
        self.hero = self.menu.hero
        self.skill = self.menu.skill

        self.image.fill(BLUE)

        if self.skill != None:

            if self.skill.debuffing:

                if self.skill.bonus_debuff < 0:
                    self.text = '-' + str(self.skill.bonus_debuff)
                if self.skill.bonus_debuff > 0:
                    self.text = '+' + str(self.skill.bonus_debuff)
                if self.skill.bonus_debuff == 0:
                    self.text = '+0'

            else:

                self.text = ''

        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))



class InventoryAgility(Text):

    def __init__(self, game, menu):
        super().__init__(game)

        self.menu = menu
        self.hero = self.menu.hero
        self.scale = 2
        self.text = str(self.hero.agility) + '%'
        self.pos = [712, 356]
        self.width = 3 * FONT_WIDTH
        self.height = 1 * FONT_HEIGHT

        self.image = p.Surface((self.width, self.height))
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

    def update(self):

        self.hero = self.menu.hero
        self.text = str(self.hero.agility) + '%'
        
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

class InventoryPrecision(Text):

    def __init__(self, game, menu):
        super().__init__(game)

        self.menu = menu
        self.hero = self.menu.hero
        self.scale = 2
        self.text = str(self.hero.precision) + '%'
        self.pos = [712, 400]
        self.width = 3 * FONT_WIDTH
        self.height = 1 * FONT_HEIGHT

        self.image = p.Surface((self.width, self.height))
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

    def update(self):

        self.hero = self.menu.hero
        self.text = str(self.hero.precision) + '%'
        
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

class InventoryCrit(Text):

    def __init__(self, game, menu):
        super().__init__(game)

        self.menu = menu
        self.hero = self.menu.hero
        self.scale = 2
        self.text = str(self.hero.crit) + '%'
        self.pos = [712, 444]
        self.width = 3 * FONT_WIDTH
        self.height = 1 * FONT_HEIGHT

        self.image = p.Surface((self.width, self.height))
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

    def update(self):

        self.hero = self.menu.hero
        self.text = str(self.hero.crit) + '%'
        
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

class InventoryBleed(Text):

    def __init__(self, game, menu):
        super().__init__(game)

        self.menu = menu
        self.hero = self.menu.hero
        self.scale = 2
        self.text = str(self.hero.bleed) + '%'
        self.pos = [832, 356]
        self.width = 3 * FONT_WIDTH
        self.height = 1 * FONT_HEIGHT

        self.image = p.Surface((self.width, self.height))
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

    def update(self):

        self.hero = self.menu.hero
        self.text = str(self.hero.bleed) + '%'
        
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

class InventoryVenom(Text):

    def __init__(self, game, menu):
        super().__init__(game)

        self.menu = menu
        self.hero = self.menu.hero
        self.scale = 2
        self.text = str(self.hero.venom) + '%'
        self.pos = [832, 400]
        self.width = 3 * FONT_WIDTH
        self.height = 1 * FONT_HEIGHT

        self.image = p.Surface((self.width, self.height))
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

    def update(self):

        self.hero = self.menu.hero
        self.text = str(self.hero.venom) + '%'
        
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

class InventoryFire(Text):

    def __init__(self, game, menu):
        super().__init__(game)

        self.menu = menu
        self.hero = self.menu.hero
        self.scale = 2
        self.text = str(self.hero.fire) + '%'
        self.pos = [832, 444]
        self.width = 3 * FONT_WIDTH
        self.height = 1 * FONT_HEIGHT

        self.image = p.Surface((self.width, self.height))
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

    def update(self):

        self.hero = self.menu.hero
        self.text = str(self.hero.fire) + '%'
        
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

class InventoryHeal(Text):

    def __init__(self, game, menu):
        super().__init__(game)

        self.menu = menu
        self.hero = self.menu.hero
        self.scale = 2
        self.text = str(int(self.hero.healing[0]))
        self.pos = [832, 488]
        self.width = 3 * FONT_WIDTH
        self.height = 1 * FONT_HEIGHT

        self.image = p.Surface((self.width, self.height))
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

    def update(self):

        self.hero = self.menu.hero
        self.text = str(int(self.hero.healing[0]))
        
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

class InventoryDeath(Text):

    def __init__(self, game, menu):
        super().__init__(game)

        self.menu = menu
        self.hero = self.menu.hero
        self.scale = 2
        self.text = str(self.hero.death) + '%'
        self.pos = [952, 356]
        self.width = 3 * FONT_WIDTH
        self.height = 1 * FONT_HEIGHT

        self.image = p.Surface((self.width, self.height))
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

    def update(self):

        self.hero = self.menu.hero
        self.text = str(self.hero.death) + '%'
        
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

class InventoryStun(Text):

    def __init__(self, game, menu):
        super().__init__(game)

        self.menu = menu
        self.hero = self.menu.hero
        self.scale = 2
        self.text = str(self.hero.stun) + '%'
        self.pos = [952, 400]
        self.width = 3 * FONT_WIDTH
        self.height = 1 * FONT_HEIGHT

        self.image = p.Surface((self.width, self.height))
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

    def update(self):

        self.hero = self.menu.hero
        self.text = str(self.hero.stun) + '%'
        
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

class InventoryDebuff(Text):

    def __init__(self, game, menu):
        super().__init__(game)

        self.menu = menu
        self.hero = self.menu.hero
        self.scale = 2
        self.text = str(self.hero.debuff) + '%'
        self.pos = [952, 444]
        self.width = 3 * FONT_WIDTH
        self.height = 1 * FONT_HEIGHT

        self.image = p.Surface((self.width, self.height))
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

    def update(self):

        self.hero = self.menu.hero
        self.text = str(self.hero.debuff) + '%'
        
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

class InventoryMobility(Text):

    def __init__(self, game, menu):
        super().__init__(game)

        self.menu = menu
        self.hero = self.menu.hero
        self.scale = 2
        self.text = str(self.hero.mobility)
        self.pos = [952, 488]
        self.width = 3 * FONT_WIDTH
        self.height = 1 * FONT_HEIGHT

        self.image = p.Surface((self.width, self.height))
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

    def update(self):

        self.hero = self.menu.hero
        self.text = str(self.hero.mobility)
        
        self.draw_text()
        self.image = p.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))