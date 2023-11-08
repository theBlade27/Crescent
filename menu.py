import pygame as p
from settings import *
from image import *
from text import *
from button import *
from bar import *
from map import *

# the menu class is very important, it is how the player interacts with the game and how all information is displayed to them
# some menus are self explanatory, but more complicated ones will be explained

class Menu(p.sprite.Sprite):

    def __init__(self, game):

        self.groups = game.menus_group, game.all
        p.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.scale = 4 # how much this menus size is scaled
        self.visible = True # whether this menu is visible
        self.colour = FAKEBLACK # this menus colour

    def update(self):

        # everytime this menu updates, draw the background of this menu

        self.image.blit(self.background, [0, 0])

        # and then, on top of the background, for every image item that forms this menu, if that image is visible, draw it in the right place

        for image in self.images.values():
            if image.visible:
                self.image.blit(image.image, image.pos)

        # only update the images if the players mouse is hovering over this menu (this saves resources)

        if self.hitbox.collidepoint(self.game.mouse.pos):
            self.update_images()

    def update_images(self):

        # update every image that is in this menus list of images

        for image in self.images.values():
            image.update()

# this menu deals with displaying an animation to the player upon a skill being used, and it displays exactly how effective the skill was with numbers

class CombatAnimation(Menu):

    def __init__(self, game, attacker, targets, damage_numbers, heal_numbers, sanity_damage_numbers, sanity_heal_numbers):
        super().__init__(game)

        self.pos = [386, 218]
        self.scale = 1

        self.attacker = attacker
        self.targets = targets
        self.damage_numbers = damage_numbers
        self.heal_numbers = heal_numbers
        self.sanity_damage_numbers = sanity_damage_numbers
        self.sanity_heal_numbers = sanity_heal_numbers

        self.menus = []

        self.menucolours = []

        crit = False

        for number in damage_numbers:

            if 'CRIT' in str(number):
                crit = True

        for number in heal_numbers:

            if 'CRIT' in str(number):
                crit = True

        # if there was a crit, this menu will shake more intensely

        if crit == True:
            self.shaking = True
            self.shake_intensity = 30
        else:
            self.shaking = True
            self.shake_intensity = 15

        self.shake_offset_x = 0
        self.shake_offset_y = 0





        self.background = MENU_SPRITESHEETS['COMBAT_BACKGROUND'].copy()
        self.image = p.transform.scale(self.background, (self.background.get_width() * self.scale, self.background.get_height() * self.scale))
        self.background = self.image

        self.hitbox = p.rect.Rect(self.pos[0], self.pos[1], self.image.get_width(), self.image.get_height())

        self.height = self.image.get_height()

        self.attacker_image = self.attacker.selected_skill.combat_animation # the attackers image is the image of the skill they are currently using

        self.target_images = []

        # for every target the skill was used on (unless it was the user of the skill itself), retrieve the image of them stand it and flip it so they are facing the character using the skill

        for target in self.targets:

            if target != self.game.selected_character:

                self.target_images.append(p.transform.flip(p.transform.scale(target.combat_images[0], [target.combat_images[0].get_width() * 2, target.combat_images[0].get_height() * 2]), True, False))


        self.image.blit(self.background, [0, 0])

        starting_distance = 540 # minimum distance a character should be drawn from the left side of the screen
        ending_distance = 760 # maximum distance a character should be drawn from the left side of the screen

        total_distance = ending_distance - starting_distance

        gap = 0

        if len(self.target_images) > 0:

            gap = total_distance / len(self.target_images) # this calaculates a number so that the image of every target is evenly spaced out

        i = 0

        # for every target, draw their images, starting at the starting distance and increasing the distance by a constant number each time so the targets are evenly spaced

        for image in self.target_images:

            self.image.blit(image, [starting_distance + gap * i, self.height - image.get_height()])

            i += 1

        i = 0

        # draw the attackers image

        self.image.blit(self.attacker_image, [0, self.height - self.attacker_image.get_height()])

        # if the number of numbers in the lists of numbers for damage/health/sanity healing/sanity damage or the number of applied effects is greater than the number of targets, then this skill has done something to the attacker as well, so this needs to be conveyed
        if len(heal_numbers) > len(self.target_images) or len(damage_numbers) > len(self.target_images) or len(sanity_heal_numbers) > len(self.target_images) or len(sanity_damage_numbers) > len(self.target_images) or len(self.attacker.effect_applied_images) > 0:

            # set the y of the next image to be drawn to be right above the attackers image
            y = self.height - (self.attacker.combat_images[0].get_height() * 2)

            # then for each number list or the list of applied effects, if this lists length is greater than the length of the list of targets, draw the number or effect above the attackers head

            if len(heal_numbers) > len(self.target_images):

                number_image = HealNumber(self.game, heal_numbers[i]).image
                heal_numbers.remove(heal_numbers[i])

                y -= number_image.get_height()

                self.image.blit(number_image, [0 + (self.attacker.combat_images[0].get_width()) - (number_image.get_width() / 2), y])

            if len(sanity_heal_numbers) > len(self.target_images):

                number_image = SanityHealNumber(self.game, sanity_heal_numbers[i]).image
                sanity_heal_numbers.remove(sanity_heal_numbers[i])

                y -= number_image.get_height()

                self.image.blit(number_image, [0 + (self.attacker.combat_images[0].get_width()) - (number_image.get_width() / 2), y])

            for effect_image in attacker.effect_applied_images:

                y -= effect_image.get_height()

                self.image.blit(effect_image, [0 + (self.attacker.combat_images[0].get_width()) - (effect_image.get_width() / 2), y])

        # then for every target

        for image in self.target_images:

            # set the y value of the next image to be directly above the targets image

            y = self.height - image.get_height()

            target = self.targets[i]

            # for every type of number

            # if there is number in this list

            if len(damage_numbers) > 0:

                # change the outline colour of the character being effected by this skill to an appropiate colour

                for menu in self.game.menus.values():
                    if type(menu) == HeroPreview:
                        if menu.hero == target:
                            self.menus.append(menu)
                            self.menucolours.append(RED)
                    if type(menu) == EnemyPreview:
                        if menu.enemy == target:
                            self.menus.append(menu)
                            self.menucolours.append(RED)

                # create a text object to display this information information

                number_image = DamageNumber(self.game, damage_numbers[i]).image

                # decrease the y so the next number appears higher up on the screen and the numbers do not overlap

                y -= number_image.get_height()

                # draw the image in the correct position

                self.image.blit(number_image, [starting_distance + gap * i + (image.get_width() / 2) - (number_image.get_width() / 2), y])

            if len(heal_numbers) > 0:

                for menu in self.game.menus.values():
                    if type(menu) == HeroPreview:
                        if menu.hero == target:
                            self.menus.append(menu)
                            self.menucolours.append(GREEN)
                    if type(menu) == EnemyPreview:
                        if menu.enemy == target:
                            self.menus.append(menu)
                            self.menucolours.append(GREEN)

                number_image = HealNumber(self.game, heal_numbers[i]).image

                y -= number_image.get_height()

                self.image.blit(number_image, [starting_distance + gap * i + (image.get_width() / 2) - (number_image.get_width() / 2), y])

            if len(sanity_heal_numbers) > 0:

                for menu in self.game.menus.values():
                    if type(menu) == HeroPreview:
                        if menu.hero == target:
                            self.menus.append(menu)
                            self.menucolours.append(WHITE)
                    if type(menu) == EnemyPreview:
                        if menu.enemy == target:
                            self.menus.append(menu)
                            self.menucolours.append(WHITE)

                number_image = SanityHealNumber(self.game, sanity_heal_numbers[i]).image

                y -= number_image.get_height()

                self.image.blit(number_image, [starting_distance + gap * i + (image.get_width() / 2) - (number_image.get_width() / 2), y])

            if len(sanity_damage_numbers) > 0:

                for menu in self.game.menus.values():
                    if type(menu) == HeroPreview:
                        if menu.hero == target:
                            self.menus.append(menu)
                            self.menucolours.append(PURPLE)
                    if type(menu) == EnemyPreview:
                        if menu.enemy == target:
                            self.menus.append(menu)
                            self.menucolours.append(PURPLE)

                number_image = SanityDamageNumber(self.game, sanity_damage_numbers[i]).image

                y -= number_image.get_height()

                self.image.blit(number_image, [starting_distance + gap * i + (image.get_width() / 2) - (number_image.get_width() / 2), y])

            for effect_image in target.effect_applied_images:

                y -= effect_image.get_height()

                self.image.blit(effect_image, [starting_distance + gap * i + (image.get_width() / 2) - (effect_image.get_width() / 2), y])

            # then increase i so the next set of numbers appear more to the right so they appear above the next character

            i += 1


    def update(self):

        for i in range(len(self.menus)):
            self.menus[i].colour = self.menucolours[i]
            self.menus[i].update()

        # reset this menus position

        self.pos[0] = 386
        self.pos[1] = 218

        # if this menu is shaking

        if self.shaking:
            # change the position of this menu by a random number
            self.shake_offset_x = random.randint(-self.shake_intensity, self.shake_intensity)
            self.shake_offset_y = random.randint(-self.shake_intensity, self.shake_intensity)

            # reduce the shake intensity over time so the shaking slows down
            if self.shake_intensity > 0:
                self.shake_intensity -= 1

            for menu in self.game.menus:
                if menu == 'BATTLE':
                    self.game.menus['BATTLE'].image.fill(BLACK)

        # change by the position by shake intensity

        self.pos[0] += self.shake_offset_x
        self.pos[1] += self.shake_offset_y

    def update_images(self):

        pass

class NewGameMenu(Menu):

    def __init__(self, game):
        super().__init__(game)

        self.scale = 8

        self.pos = [0, 0]

        self.background = MENU_SPRITESHEETS['NEWGAMEBACKGROUND'].copy()
        self.image = p.transform.scale(self.background, (self.background.get_width() * self.scale, self.background.get_height() * self.scale))
        self.background = self.image

        self.hitbox = p.rect.Rect(self.pos[0], self.pos[1], self.image.get_width(), self.image.get_height())

        self.images = {
            'PLAY': PlayButton(self.game, self)
        }

class Instructions(Menu):

    def __init__(self, game):
        super().__init__(game)

        self.scale = 1

        self.pos = [352, 196]

        self.background = MENU_SPRITESHEETS['INSTRUCTIONS'].copy()
        self.image = p.transform.scale(self.background, (self.background.get_width() * self.scale, self.background.get_height() * self.scale))
        self.background = self.image

        self.hitbox = p.rect.Rect(self.pos[0], self.pos[1], self.image.get_width(), self.image.get_height())

        self.images = {
            'EXIT': ExitButtonBeige(self.game, self),
        }

        self.update_images()


class SkillInfo(Menu):

    def __init__(self, game, hero, skill):
        super().__init__(game)

        self.scale = 1

        self.hero = hero
        self.skill = skill

        self.pos = [352, 196]
        self.background = MENU_SPRITESHEETS['BACKGROUND'].copy()
        self.image = p.transform.scale(self.background, (self.background.get_width() * self.scale, self.background.get_height() * self.scale))
        self.background = self.image

        self.hitbox = p.rect.Rect(self.pos[0], self.pos[1], self.image.get_width(), self.image.get_height())

        self.images = {
            'TITLE_ICON': SkillMenuIcon(self.game),
            'TITLE': MenuTitle(self.game, 'SELECT SKILLS'),
            'EXIT': ExitButton(self.game, self),
            'SELECTED_SKILL': SelectedSkillImage(self.game, self),
            'DAMAGE_MULTIPLIER_ICON': SkillDamageIcon(self.game, self),
            'DAMAGE_MULTIPLIER_TEXT': SkillDamageMultiplier(self.game, self),
            'CRIT_ICON': SkillCritIcon(self.game, self),
            'CRIT_TEXT': SkillCritMultiplier(self.game, self),
            'PRECISION_ICON': SkillPrecisionIcon(self.game, self),
            'PRECISION_TEXT': SkillPrecisionMultiplier(self.game, self),
            'STUN_ICON': SkillStunIcon(self.game, self),
            'STUN_TEXT': SkillStunMultiplier(self.game, self),
            'DEBUFF_ICON': SkillDebuffIcon(self.game, self),
            'DEBUFF_TEXT': SkillDebuffMultiplier(self.game, self),
            'SLOT': SkillPortraitSlot(self.game),
            'PORTRAIT': SkillMenuPortrait(self.game, self),
            'ONHITEFFECT': OnHitEffectIcon(self.game, self),
            'ONUSEEFFECT': OnUseEffectIcon(self.game, self),
            'SKILLNAME': SkillName(self.game, self),
            'SKILLDESC': SkillDesc(self.game, self)
        }

        for i in range (4):
            self.images['SKILLSLOT' + str(i + 1)] = SkillInfoSlot(self.game, self, i)
            self.images['SKILL' + str(i + 1)] = SkillInfoImage(self.game, self, i)
            self.images['EFFECTS_ON_HIT' + str(i + 1)] = OnHitEnemyEffectDisplay(self.game, self, i)
            self.images['EFFECTS_ON_USE' + str(i + 1)] = OnUseEnemyEffectDisplay(self.game, self, i)

        for i in range (12):
            self.images['RANGE' + str(i + 1)] = SkillRangeIndicator(self.game, self, i)

        self.update_images()

    def update_images(self):

        if self.skill != None:

            for image in self.images.values():
                image.update()

class Loot(Menu):

    def __init__(self, game, loot_list, money):
        super().__init__(game)

        self.scale = 1

        self.pos = [352, 196]
        self.background = MENU_SPRITESHEETS['BACKGROUND'].copy()
        self.image = p.transform.scale(self.background, (self.background.get_width() * self.scale, self.background.get_height() * self.scale))
        self.background = self.image

        self.hitbox = p.rect.Rect(self.pos[0], self.pos[1], self.image.get_width(), self.image.get_height())

        self.loot_list = loot_list

        self.images = {
            'INVENTORY_ICON': InventoryIcon(self.game),
            'TITLE': MenuTitle(self.game, 'LOOT! +$' + str(money)),
            'EXIT': ExitButton(self.game, self),
        }

        for i in range (25):
            self.images['STORAGE_SLOT' + str(i + 1)] = StorageSlot(self.game, self, i)
            self.images['STORAGE_IMAGE' + str(i + 1)] = StorageImage(self.game, i)

        for i in range (len(self.loot_list)):
            self.images['LOOT_SLOT' + str(i + 1)] = LootSlot(self.game, self, i, self.loot_list)
            self.images['LOOT_IMAGE' + str(i + 1)] = LootImage(self.game, i, self.loot_list)

        self.update_images()

class Trader(Menu):

    def __init__(self, game, items, object):
        super().__init__(game)

        self.object = object

        self.scale = 1

        self.cost = 0

        self.pos = [352, 196]
        self.background = MENU_SPRITESHEETS['BACKGROUND'].copy()
        self.image = p.transform.scale(self.background, (self.background.get_width() * self.scale, self.background.get_height() * self.scale))
        self.background = self.image

        self.hitbox = p.rect.Rect(self.pos[0], self.pos[1], self.image.get_width(), self.image.get_height())

        self.selling = False

        self.images = {
            'INVENTORY_ICON': InventoryIcon(self.game),
            'TITLE': MenuTitle(self.game, 'INVENTORY'),
            'EXIT': ExitButton(self.game, self),
            'NPC_TEXTBOX': NPCTextbox(self.game),
            'NPC_TEXT': NPCText(self.game, 'FOR YOU MY FRIEND?\nHALF PRICE!'),
            'NPC_PORTRAIT_SLOT': NPCSlot(self.game),
            'NPC_PORTRAIT': NPCPortrait(self.game, 'TRADER')

        }


        for i in range(25):
            self.images['STORAGE_SLOT' + str(i + 1)] = StorageSlot(self.game, self, i)
            self.images['STORAGE_IMAGE' + str(i + 1)] = StorageImage(self.game, i)

        
        self.inventory = items

        for i in range(len(self.inventory)):
            self.images['TRADER_SLOT' + str(i + 1)] = TraderSlot(self.game, self, i)
            self.images['TRADER_IMAGE' + str(i + 1)] = TraderImage(self.game, self, i)


        self.update_images()



class Upgrade(Menu):

    def __init__(self, game, hero):
        super().__init__(game)

        self.scale = 1

        self.cost = 0

        self.hero = hero

        self.pos = [352, 196]
        self.background = MENU_SPRITESHEETS['BACKGROUND'].copy()
        self.image = p.transform.scale(self.background, (self.background.get_width() * self.scale, self.background.get_height() * self.scale))
        self.background = self.image

        self.hitbox = p.rect.Rect(self.pos[0], self.pos[1], self.image.get_width(), self.image.get_height())

        self.upgrading_armour = False
        self.upgrading_weapon = False

        self.images = {
            'INVENTORY_ICON': InventoryIcon(self.game),
            'TITLE': MenuTitle(self.game, 'INVENTORY'),
            'EXIT': ExitButton(self.game, self),
            'ARMOUR': ArmourUpgradeButton(self.game, self),
            'WEAPON': WeaponUpgradeButton(self.game, self),
            'UPGRADE': UpgradeButton(self.game, self),
            'WEAPON_TEXT': WeaponText(self.game, self),
            'ARMOUR_TEXT': ArmourText(self.game, self),
            'COST_ICON': CostIcon(self.game),
            'COST_TEXT': CostText(self.game, self),
            'NPC_TEXTBOX': NPCTextbox(self.game),
            'NPC_TEXT': NPCText(self.game, 'NEED AN UPGRADE?'),
            'NPC_PORTRAIT_SLOT': NPCSlot(self.game),
            'NPC_PORTRAIT': NPCPortrait(self.game, 'BLACKSMITH')

        }

        for i in range (4):
            self.images['HEROSLOT' + str(i + 1)] = HeroUpgradePortraitSlot(self.game, self, i)
            self.images['PORTRAIT' + str(i + 1)] = HeroUpgradePortrait(self.game, i)

        for i in range (25):
            self.images['STORAGE_SLOT' + str(i + 1)] = StorageSlot(self.game, self, i)
            self.images['STORAGE_IMAGE' + str(i + 1)] = StorageImage(self.game, i)


        self.update_images()

class Inventory(Menu):

    def __init__(self, game, hero):
        super().__init__(game)

        self.scale = 1

        self.hero = hero

        self.pos = [352, 196]
        self.background = MENU_SPRITESHEETS['BACKGROUND'].copy()
        self.image = p.transform.scale(self.background, (self.background.get_width() * self.scale, self.background.get_height() * self.scale))
        self.background = self.image

        self.hitbox = p.rect.Rect(self.pos[0], self.pos[1], self.image.get_width(), self.image.get_height())

        self.images = {
            'INVENTORY_ICON': InventoryIcon(self.game),
            'TITLE': MenuTitle(self.game, 'INVENTORY'),
            'EXIT': ExitButton(self.game, self),
            'SLOT': HugeSlot(self.game),
            'COMBAT_IMAGE': InventoryCombatImage(self.game, self),
            'HEALTH_BAR': InventoryHealthBar(self.game, self),
            'SANITY_BAR': InventorySanityBar(self.game, self),
            'EXPERIENCE_BAR': InventoryExperienceBar(self.game, self),
            'NAME': InventoryName(self.game, self),
            'HEALTH': InventoryHealth(self.game, self),
            'HEALTH_ICON': InventoryHealthIcon(self.game),
            'PROTECTION': InventoryProtection(self.game, self),
            'PROTECTION_ICON': InventoryProtectionIcon(self.game),
            'SPEED': InventorySpeed(self.game, self),
            'SPEED_ICON': InventorySpeedIcon(self.game),
            'DAMAGE': InventoryDamage(self.game, self),
            'DAMAGE_ICON': InventoryDamageIcon(self.game),
            'AGILITY': InventoryAgility(self.game, self),
            'AGILITY_ICON': InventoryAgilityIcon(self.game),
            'PRECISION': InventoryPrecision(self.game, self),
            'PRECISION_ICON': InventoryPrecisionIcon(self.game),
            'CRIT': InventoryCrit(self.game, self),
            'CRIT_ICON': InventoryCritIcon(self.game),
            'BLEED': InventoryBleed(self.game, self),
            'BLEED_ICON': InventoryBleedIcon(self.game),
            'VENOM': InventoryVenom(self.game, self),
            'VENOM_ICON': InventoryVenomIcon(self.game),
            'FIRE': InventoryFire(self.game, self),
            'FIRE_ICON': InventoryFireIcon(self.game),
            'HEAL': InventoryHeal(self.game, self),
            'HEAL_ICON': InventoryHealIcon(self.game),
            'DEATH': InventoryDeath(self.game, self),
            'DEATH_ICON': InventoryDeathIcon(self.game),
            'STUN': InventoryStun(self.game, self),
            'STUN_ICON': InventoryStunIcon(self.game),
            'DEBUFF': InventoryDebuff(self.game, self),
            'DEBUFF_ICON': InventoryDebuffIcon(self.game),
            'MOBILITY': InventoryMobility(self.game, self),
            'MOBILITY_ICON': InventoryMobilityIcon(self.game),
            'WEAPON': InventoryWeaponLevel(self.game, self),
            'ARMOUR': InventoryArmourLevel(self.game, self)
        }

        for i in range (4):
            self.images['HEROSLOT' + str(i + 1)] = HeroInventoryPortraitSlot(self.game, self, i)
            self.images['PORTRAIT' + str(i + 1)] = HeroInventoryPortrait(self.game, i)
            self.images['SKILLSLOT' + str(i + 1)] = HeroInventorySkillSlot(self.game, self, i)
            self.images['SKILL' + str(i + 1)] = HeroInventorySkillImage(self.game, self, i)

        for i in range(3):
            self.images['EQUIPMENT' + str(i + 1)] = EquipmentSlot(self.game, self, i)
            self.images['EQUIPMENT_IMAGE' + str(i + 1)] = EquipmentImage(self.game, self, i)

        for i in range (25):
            self.images['STORAGE_SLOT' + str(i + 1)] = StorageSlot(self.game, self, i)
            self.images['STORAGE_IMAGE' + str(i + 1)] = StorageImage(self.game, i)
         
        self.update_images()

class TopMenu(Menu):

    def __init__(self, game):
        super().__init__(game)

        self.pos = [0, 0]
        self.background = MENU_SPRITESHEETS['TOP'].copy()
        self.image = p.transform.scale(self.background, (self.background.get_width() * self.scale, self.background.get_height() * self.scale))
        self.background = self.image

        self.hitbox = p.rect.Rect(self.pos[0], self.pos[1], self.image.get_width(), self.image.get_height())

        self.images = {
            'TEXTBOX_BACKGROUND': TextboxBackground(self.game),
            'SLOT': SlotTextbox(self.game),
            'PORTRAIT': TextboxPortrait(self.game),
            #'MAP': MapButton(self.game, self),
            #'CAMP': CampButton(self.game, self),
            'INVENTORY': InventoryButton(self.game, self),
            #'REPOSITION': RepositionButton(self.game, self),
            #'SETTINGS': SettingsButton(self.game, self),
            'HELP': HelpButton(self.game, self),
            'COIN_ICON': CoinIcon(self.game),
            'TEXT': TextboxText(self.game),
            'MONEY_TEXT': MoneyText(self.game)
        }


class BottomMenu(Menu):

    def __init__(self, game):
        super().__init__(game)

        self.pos = [0, 844]
        self.hero = self.game.hero_party[0]
        self.background = MENU_SPRITESHEETS['BOTTOM'].copy()
        self.image = p.transform.scale(self.background, (self.background.get_width() * self.scale, self.background.get_height() * self.scale))
        self.background = self.image.copy()

        self.hitbox = p.rect.Rect(self.pos[0], self.pos[1], self.image.get_width(), self.image.get_height())

        self.images = {
            'SLOT': HeroLargeSlot(self.game),
            'PORTRAIT': HeroLargePortrait(self.game),
            'NAME': HeroLargeName(self.game),
            'HEALTH': HeroRegularHealthBar(self.game),
            'EFFECT1': HeroBottomMenuBuff(self.game, self, 0),
            'EFFECT2': HeroBottomMenuBuff(self.game, self, 1),
            'EFFECT3': HeroBottomMenuBuff(self.game, self, 2),
            'EFFECT4': HeroBottomMenuBuff(self.game, self, 3),
            'EFFECT5': HeroBottomMenuBuff(self.game, self, 4),
            'EFFECT6': HeroBottomMenuBuff(self.game, self, 5),
            'EFFECT7': HeroBottomMenuBuff(self.game, self, 6),
            'EFFECT8': HeroBottomMenuBuff(self.game, self, 7),
            'SANITY': HeroRegularSanityBar(self.game),
            'SKILL1': SkillButton(self.game, self, 0),
            'SKILL2': SkillButton(self.game, self, 1),
            'SKILL3': SkillButton(self.game, self, 2),
            'SKILL4': SkillButton(self.game, self, 3),
            'MOVE': SkillButton(self.game, self, 4),
            'SKIP': SkillButton(self.game, self, 5),
            #'RETREAT': SkillButton(self.game, self, 6),
        }

    def update(self):

        self.image.blit(self.background, [0, 0])

        for image in self.images.values():
            if image.visible:
                self.image.blit(image.image, image.pos)

        if self.hitbox.collidepoint(self.game.mouse.pos):
            self.update_images()
        
    def update_images(self):
        
        for image in self.images.values():
            image.update()

# this menu is incredibly important, it is where all battles take place

class BattleMenu(Menu):

    def __init__(self, game, battle):
        super().__init__(game)

        self.pos = [386, 218]

        self.images = {

        }

        self.tiles = [

        ]

        self.objects = [

        ]

        self.heroes = [

        ]

        self.enemies = [

        ]

        self.characters = [

        ]

        self.player_spawn = [0, 0]
        self.spawn_direction = None

        self.cross = False

        self.battle = battle
        self.map = Map(self.game, BATTLE_MAPS[self.battle], self) # when this object is created, the spawn location and enemys needed are also retrieved

        # generates this maps background

        self.background = self.map.generate_battle_background()

        # make this menus image its background

        self.image = self.background

        # adds every hero to this menus list of heroes and the list of all characters, as well as putting them in the right place

        for hero in self.game.hero_party:
            if hero != None:
                self.heroes.append(hero)

        self.spawn_heroes()

        for hero in self.heroes:
            self.characters.append(hero)

        # then add every enemy to the list of all characters, set their grid positions and give them an index
        index = 1

        for enemy in self.enemies:
            self.characters.append(enemy)
            enemy.grid_pos = [enemy.grid_pos[0], enemy.grid_pos[1]]
            enemy.index = index
            index += 1

        # create a preview menu for each enemy

        for i in range(len(self.enemies)):
            self.game.menus['ENEMY' + str(i + 1)] = EnemyPreview(self.game, i, self.enemies[i])

        self.hitbox = p.rect.Rect(self.pos[0], self.pos[1], self.image.get_width(), self.image.get_height())

    def spawn_heroes(self):

        # depending on the direction heroes are spawned in, every hero is spawned at the player spawn location on the map, with their position slightly changed by their starting position, so frontliners start closer to the enemies
        # the hero is also flipped depending on whether they spawn facing left or right
        for hero in self.heroes:

            if self.spawn_direction == 'right':

                hero.grid_pos = [self.player_spawn[0] + hero.starting_grid_pos[0], self.player_spawn[1] + hero.starting_grid_pos[1]]
                hero.flipped = False

            if self.spawn_direction == 'left':

                hero.grid_pos = [self.player_spawn[0] - hero.starting_grid_pos[0], self.player_spawn[1] + hero.starting_grid_pos[1]]
                hero.flipped = True

            if self.spawn_direction == 'up':

                hero.grid_pos = [self.player_spawn[0] - hero.starting_grid_pos[1], self.player_spawn[1] - hero.starting_grid_pos[0]]

            if self.spawn_direction == 'down':

                hero.grid_pos = [self.player_spawn[0] + hero.starting_grid_pos[1], self.player_spawn[1] + hero.starting_grid_pos[0]]

    def check_obstructed(self):

        # makes every tile with a character on it obstructed

        for character in self.characters:
            for tile in self.tiles:
                if tile.grid_pos == character.grid_pos:
                    tile.obstructed = True

    def check_hero(self):

        # makes every tile with a hero know it has a hero on it

        for hero in self.heroes:
            for tile in self.tiles:
                if tile.grid_pos == hero.grid_pos:
                    tile.has_hero = True

    def check_enemy(self):

        # makes every tile with an enemy know it has an enemy on it

        for enemy in self.enemies:
            for tile in self.tiles:
                if tile.grid_pos == enemy.grid_pos:
                    tile.has_enemy = True

    def update(self):

        # first, the maps background is drawn

        self.image.blit(self.background, [0, 0])

        # then, every tile is updated so it knows whether it can be moved to or attacked

        self.check_obstructed()
        self.check_hero()
        self.check_enemy()

        # for every tile, if it is being targeted, draw the confirmation marker on top of it

        for tile in self.tiles:
            self.image.blit(tile.image, (tile.grid_pos[0] * TILE_SIZE * MAP_SCALE, tile.grid_pos[1] * TILE_SIZE * MAP_SCALE))
            if tile.being_targeted:
                tile.image.blit(CONFIRMATION, (0, 0))

        # then, draw every object and character in the right place

        for object in self.objects:
            self.image.blit(object.image, (object.grid_pos[0] * TILE_SIZE * MAP_SCALE, object.grid_pos[1] * TILE_SIZE * MAP_SCALE))

        for character in self.characters:
            self.image.blit(character.image, (character.grid_pos[0] * TILE_SIZE * MAP_SCALE, character.grid_pos[1] * TILE_SIZE * MAP_SCALE))

        self.draw_indicator()

    def draw_indicator(self):

        # if the tile cannot be targeted (it has an obstacle, or the player is using a skill on an invalid target), it will have a cross drawn on top of it

        if self.cross:
            tile = self.game.selected_tile
            self.image.blit(CROSS, (tile.grid_pos[0] * TILE_SIZE * MAP_SCALE, tile.grid_pos[1] * TILE_SIZE * MAP_SCALE))

class EnemyPreview(Menu):

    def __init__(self, game, index, enemy):
        super().__init__(game)

        self.pos = [1504, 196 + 108 * index]
        self.enemy = enemy
        self.background = MENU_SPRITESHEETS['ENEMY_PREVIEW'].copy()
        self.image = p.transform.scale(self.background, (self.background.get_width() * self.scale, self.background.get_height() * self.scale))
        self.background = self.image

        self.hitbox = p.rect.Rect(self.pos[0], self.pos[1], self.image.get_width(), self.image.get_height())

        self.images = {
            'NAME': EnemyPreviewName(self.game, self),
            'HEALTH': EnemySmallHealthBar(self.game, self),
            'EFFECT1': EnemyPreviewBuff(self.game, self, 0),
            'EFFECT2': EnemyPreviewBuff(self.game, self, 1),
            'EFFECT3': EnemyPreviewBuff(self.game, self, 2),
            'EFFECT4': EnemyPreviewBuff(self.game, self, 3),
            'EFFECT5': EnemyPreviewBuff(self.game, self, 4),
            'EFFECT6': EnemyPreviewBuff(self.game, self, 5),
            'EFFECT7': EnemyPreviewBuff(self.game, self, 6),
            'EFFECT8': EnemyPreviewBuff(self.game, self, 7)
        }

        self.update_images()

    def update(self):
        
        background = colour_swap(self.background.copy(), FAKEBLACK, self.colour)

        self.image = background

        for image in self.images.values():
            if image.visible:
                self.image.blit(image.image, image.pos)

        if self.hitbox.collidepoint(self.game.mouse.pos):
            self.update_images()

        if self.enemy == None:
            self.visible = False
        else:
            self.visible = True

            if self.game.clear_view:
                self.visible = False
            else:
                self.visible = True

        if self.hitbox.collidepoint(self.game.mouse.pos):
            if self.game.mouse.pressed['M2']:
                self.game.open_menu('INVENTORY', self.enemy)

                self.game.play_sound_effect(BUTTON_SOUND)

class Bark(Menu):

    def __init__(self, game, hero, text):
        super().__init__(game)

        self.game.barks.add(self)

        self.background = MENU_SPRITESHEETS['BARK'].copy()
        self.image = p.transform.scale(self.background, (self.background.get_width() * self.scale, self.background.get_height() * self.scale))
        self.background = self.image

        if hero in self.game.hero_party:
            self.index = self.game.hero_party.index(hero)
            self.pos = [352, 200 + 160 * self.index]

            self.hitbox = p.rect.Rect(self.pos[0], self.pos[1], self.image.get_width(), self.image.get_height())

            self.images = {
                'TEXT': BarkText(self.game, text)
            }
        else:
            self.images = {

            }
            self.visible = False
            self.game.barks.remove(self)
            self.game.menus_group.remove(self)
            self.game.all.remove(self)
            self.kill()

class HeroPreview(Menu):

    def __init__(self, game, index):
        super().__init__(game)

        self.index = index

        self.pos = [4, 200 + 160 * index]
        self.hero = self.game.hero_party[index]
        self.background = MENU_SPRITESHEETS['HERO_PREVIEW'].copy()
        self.image = p.transform.scale(self.background, (self.background.get_width() * self.scale, self.background.get_height() * self.scale))
        self.background = self.image

        self.hitbox = p.rect.Rect(self.pos[0], self.pos[1], self.image.get_width(), self.image.get_height())

        self.images = {
            'SLOT': HeroPreviewSlot(self.game, self),
            'PORTRAIT': HeroPreviewPortrait(self.game, self),
            'NAME': HeroPreviewName(self.game, self),
            'HEALTH': HeroSmallHealthBar(self.game, self),
            'SANITY': HeroSmallSanityBar(self.game, self),
            'EFFECT1': HeroPreviewBuff(self.game, self, 0),
            'EFFECT2': HeroPreviewBuff(self.game, self, 1),
            'EFFECT3': HeroPreviewBuff(self.game, self, 2),
            'EFFECT4': HeroPreviewBuff(self.game, self, 3),
            'EFFECT5': HeroPreviewBuff(self.game, self, 4),
            'EFFECT6': HeroPreviewBuff(self.game, self, 5),
            'EFFECT7': HeroPreviewBuff(self.game, self, 6),
            'EFFECT8': HeroPreviewBuff(self.game, self, 7)
        }

    def update(self):

        background = colour_swap(self.background.copy(), FAKEBLACK, self.colour)

        self.image = background

        for image in self.images.values():
            if image.visible:
                self.image.blit(image.image, image.pos)

        if self.hitbox.collidepoint(self.game.mouse.pos):
            self.update_images()

        self.hero = self.game.hero_party[self.index]

        if self.hero == None:
            self.visible = False
        else:
            self.visible = True

            if self.game.clear_view:
                self.visible = False
            else:
                self.visible = True

        if self.visible:

            if self.hitbox.collidepoint(self.game.mouse.pos):
                if self.game.mouse.pressed['M2']:
                    self.game.open_menu('INVENTORY', self.hero)
                    self.game.menus['INVENTORY'].hero = self.hero
                    self.game.menus['INVENTORY'].update_images()

                    self.game.play_sound_effect(BUTTON_SOUND)





        







