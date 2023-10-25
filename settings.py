# this file contains every constant in one place to make life easier

import pygame as p
from os import path

# lot of variable created to store folder directories so i dont have to write so much every time i need to load an image

folder = path.dirname(__file__)
data_folder = path.join(folder, 'data')
img_folder = path.join(data_folder, 'img')
UI_folder = path.join(img_folder, 'UI')
heroes_folder = path.join(img_folder, 'heroes')
enemies_folder = path.join(img_folder, 'enemies')
backgrounds_folder = path.join(UI_folder, 'backgrounds')
slots_folder = path.join(UI_folder, 'slots')
buttons_folder = path.join(UI_folder, 'buttons')
icons_folder = path.join(UI_folder, 'icons')
bars_folder = path.join(UI_folder, 'bars')
icons_folder = path.join(UI_folder, 'icons')
tiles_folder = path.join(img_folder, 'tiles')
items_folder = path.join(img_folder, 'items')

snd_folder = path.join(data_folder, 'snd')

map_folder = path.join(data_folder, 'maps')

TITLE = 'CRESCENT'
WIDTH = 1920
HEIGHT = 1080
FPS = 60


# this constant changes how quickly the camera moves to its new position
# it determines how smoothly it moves
LAG_FACTOR = 0.05

TILE_SIZE = 20
MAP_SCALE = 3
BATTLE_MAP_SCALE = 6


# RGB values for colours
BLACK = (0, 0, 0)
FAKEBLACK = (1, 1, 1)
WHITE = (255, 255, 255)
RED = (228, 59, 68)
DARKBLUE = (18, 14, 25)
BLUE = (38, 43, 68)
YELLOW = (254, 231, 97)
GREEN = (99, 199, 77)
DARKGREEN = (62, 137, 72)
BEIGE = (234, 212, 170)
ORANGE = (247, 118, 34)
PURPLE = (104, 56, 108)

MOUSE_SPRITESHEET = p.image.load(path.join(UI_folder, 'mouse.png'))


# dictionary of all the map files, so they can be easily accessed by name
MAPS = {
    'TUTORIAL': path.join(map_folder, 'tutorial.tmx'),
    'RESET': path.join(map_folder, 'reset.tmx'),
    'DESERT2': path.join(map_folder, 'level2.tmx'),
    'DESERT3': path.join(map_folder, 'level3.tmx'),
}


BUTTON_SOUND = path.join(snd_folder, 'button.wav')
HEAVY_SOUND = path.join(snd_folder, 'heavy.wav')
MEDIUM_SOUND = path.join(snd_folder, 'medium.wav')
LIGHT_SOUND = path.join(snd_folder, 'light.wav')
DEATH_SOUND = path.join(snd_folder, 'death.wav')
BLIP_SOUND = path.join(snd_folder, 'blip.wav')
MARK_SOUND = path.join(snd_folder, 'mark.wav')
BUFF_SOUND = path.join(snd_folder, 'buff.wav')
DEBUFF_SOUND = path.join(snd_folder, 'debuff.wav')
BUFF_SOUND = path.join(snd_folder, 'buff.wav')
HEAL_SOUND = path.join(snd_folder, 'heal.wav')
MISS_SOUND = path.join(snd_folder, 'miss.wav')
SANITY_SOUND = path.join(snd_folder, 'sanity.wav')
STRESS_SOUND = path.join(snd_folder, 'stress.wav')
MOVE_SOUND = path.join(snd_folder, 'move.wav')
NEXT_SOUND = path.join(snd_folder, 'next.wav')


WEAPON_VALUES = {
    'BLADE':
    [
        [7, 10, 95, 5], # damage[0], damage[1], precision, crit
        [9, 13, 105, 10],
        [12, 17, 115, 15]
    ],
    'ARCANE':
    [
        [6, 12, 95, 10],
        [8, 16, 105, 15],
        [11, 22, 115, 20]
    ]
}

ARMOUR_VALUES = {
    'BLADE':
    [
        [30, 15, 3, 5, 4, 7], # maxhealth, protection, speed, agility, healing[0], healing[1]
        [39, 25, 4, 10, 6, 10],
        [50, 35, 5, 15, 9, 14]
    ],
    'ARCANE':
    [
        [16, 0, 6, 15, 8, 10],
        [21, 5, 7, 20, 11, 14],
        [28, 10, 9, 25, 15, 20]
    ]
}

BLACKSMITH_COSTS = [1000, 2500]


# dictionary of all the battle map files, so they can be easily accessed by name
BATTLE_MAPS = {
    'TUTORIAL': path.join(map_folder, 'tutorial_battle.tmx'),
    'GHOSTBLADE': path.join(map_folder, 'ghostblade.tmx'),
    'L2B1': path.join(map_folder, 'level2_battle1.tmx'),
    'L2B2': path.join(map_folder, 'level2_battle2.tmx'),
    'L3B1': path.join(map_folder, 'level3_battle1.tmx'),
    'L3B2': path.join(map_folder, 'level3_battle2.tmx'),
    'L3B3': path.join(map_folder, 'level3_battle3.tmx'),
}

# dictionary of all the different encounters the player may face, so they can be easily accessed by name
ENEMY_PARTIES = {
    'GHOSTBLADE': ['GHOSTBLADE'],
    'TUTORIAL': ['BANDIT1'],
    'L2B1': ['BANDIT2', 'BANDIT1'],
    'L2B2': ['BANDIT3'],
    'L3B1': ['BANDIT4', 'BANDIT3', 'BANDIT1'],
    'L3B2': ['BANDIT2', 'BANDIT3', 'BANDIT4'],
    'L3B3': ['BANDIT2', 'BANDIT1', 'BANDIT4', 'BANDIT3']
}

# dictionary of all different loot tables, so they can be easily accessed by name
# each entry is a list of lists

LOOT_TABLE = {

    'GHOSTBLADE': [
        [], # common items
        ['CHERISHED_LETTER'], # rare items
        [], # very rare items
        [0, 0] # minimum and maximum amount of gold
    ],

    'BARREL': [
        ['BANDAGE', 'TORCH'],
        ['FOOD'],
        [],
        [0, 1]
    ],

    'DESERT': [
        ['BANDAGE', 'TORCH'],
        ['FOOD'],
        ['CRESCENT_COIN', 'GLISTENING_JAMBIYA', 'CURSED_COIN'],
        [3, 7]
    ],

    'TUTORIALCHEST': [
        ['BANDAGE', 'FOOD'],
        ['HOLY_BOOK'],
        [],
        [5, 5]
    ],

    'CHEST': [
        ['BANDAGE', 'TORCH', 'FOOD', 'FOOD2'],
        ['CRESCENT_COIN', 'GLISTENING_JAMBIYA', 'CURSED_COIN'],
        ['LUCKY_RING', 'FORSAKEN_COIN'],
        [5, 10]
    ],

    'L2CHEST': [
        ['FOOD', 'FOOD2'],
        ['SAPPHIRE_EARRINGS', 'MAGIC_LAMP'],
        ['LUCKY_RING', 'FORSAKEN_COIN'],
        [0, 0]
    ],

    'CRATE': [
        ['FOOD'],
        ['FOOD2'],
        ['FOOD3'],
        [0, 1]
    ]

}

LOOT_TABLE['TUTORIAL'] = LOOT_TABLE['DESERT']
LOOT_TABLE['L2B1'] = LOOT_TABLE['DESERT']
LOOT_TABLE['L2B2'] = LOOT_TABLE['DESERT']
LOOT_TABLE['L3B1'] = LOOT_TABLE['DESERT']
LOOT_TABLE['L3B2'] = LOOT_TABLE['DESERT']
LOOT_TABLE['L3B3'] = LOOT_TABLE['DESERT']

TILESET = p.image.load(path.join(tiles_folder, 'tileset.png'))

PORTRAITS = p.image.load(path.join(UI_folder, 'npc_portraits.png'))

MOVEMENTINDICATOR = p.image.load(path.join(UI_folder, 'movement_indicator.png'))
MOVEMENTINDICATOR = p.transform.scale(MOVEMENTINDICATOR, (60, 60))
MOVEMENTINDICATOR.set_alpha(100)

CONFIRMATION = p.image.load(path.join(UI_folder, 'confirmation.png'))
CONFIRMATION = p.transform.scale(CONFIRMATION, (60, 60))

CROSS = p.image.load(path.join(UI_folder, 'cross.png'))
CROSS = p.transform.scale(CROSS, (60, 60))

ATTACKINDICATOR = p.image.load(path.join(UI_folder, 'attack_indicator.png'))
ATTACKINDICATOR = p.transform.scale(ATTACKINDICATOR, (60, 60))
ATTACKINDICATOR.set_alpha(100)

HEALINDICATOR = p.image.load(path.join(UI_folder, 'heal_indicator.png'))
HEALINDICATOR = p.transform.scale(HEALINDICATOR, (60, 60))
HEALINDICATOR.set_alpha(100)


CHARACTER_SPRITESHEETS = {
    'BLADE': p.image.load(path.join(heroes_folder, 'blade.png')),
    'ARCANE': p.image.load(path.join(heroes_folder, 'arcane.png')),
    'FORTRESS': p.image.load(path.join(heroes_folder, 'fortress.png')),
    'BREACH': p.image.load(path.join(heroes_folder, 'breach.png')),
    'BANDIT1': p.image.load(path.join(enemies_folder, 'bandit1.png')),
    'BANDIT2': p.image.load(path.join(enemies_folder, 'bandit2.png')),
    'BANDIT3': p.image.load(path.join(enemies_folder, 'bandit3.png')),
    'GHOSTBLADE': p.image.load(path.join(enemies_folder, 'ghostblade.png')),
    'BANDIT4': p.image.load(path.join(enemies_folder, 'bandit4.png'))
}

MENU_SPRITESHEETS = {
    'TOP': p.image.load(path.join(backgrounds_folder, 'background_top.png')),
    'TEXTBOX_BACKGROUND': p.image.load(path.join(backgrounds_folder, 'background_textbox.png')),
    'SLOT_TEXTBOX': p.image.load(path.join(slots_folder, 'slot_textbox.png')),
    'BUTTON': p.image.load(path.join(buttons_folder, 'button.png')),
    'ICON_SPRITESHEET': p.image.load(path.join(icons_folder, 'menu_icons.png')),
    'HERO_PREVIEW': p.image.load(path.join(backgrounds_folder, 'background_hero_preview.png')),
    'ENEMY_PREVIEW': p.image.load(path.join(backgrounds_folder, 'background_enemy_preview.png')),
    'SLOT_THIN': p.image.load(path.join(slots_folder, 'slot_thin.png')),
    'SMALL_BAR': p.image.load(path.join(bars_folder, 'bar_small.png')),
    'BUFF_ICONS': p.image.load(path.join(icons_folder, 'buff_icons.png')),
    'BOTTOM': p.image.load(path.join(backgrounds_folder, 'background_bottom.png')),
    'SLOT_THICK': p.image.load(path.join(slots_folder, 'slot_thick.png')),
    'REGULAR_BAR': p.image.load(path.join(bars_folder, 'bar.png')),
    'SMALL_ICON_SPRITESHEET': p.image.load(path.join(icons_folder, 'small_icons.png')),
    'BACKGROUND': p.image.load(path.join(backgrounds_folder, 'background.png')),
    'SLOT': p.image.load(path.join(slots_folder, 'slot.png')),
    'SLOT_LARGE': p.image.load(path.join(slots_folder, 'slot_large.png')),
    'ITEMS': p.image.load(path.join(items_folder, 'items.png')),
    'COMBAT_BACKGROUND': p.image.load(path.join(backgrounds_folder, 'combat_background.png')),
    'REPOSITION_SMALL': p.image.load(path.join(slots_folder, 'slot_reposition_small.png')),
    'BARK': p.image.load(path.join(backgrounds_folder, 'background_bark.png')),
    'NEWGAMEBACKGROUND': p.image.load(path.join(backgrounds_folder, 'newgamebackground.png')),
    'PLAYBUTTON': p.image.load(path.join(buttons_folder, 'play.png')),
    'UPGRADE': p.image.load(path.join(buttons_folder, 'upgrade_button.png')),
    'NPC_TEXTBOX': p.image.load(path.join(UI_folder, 'NPCtext.png'))
}

FONT = p.image.load(path.join(UI_folder, 'font.png'))
FONT_WIDTH = 11
FONT_HEIGHT = 18

# this number determines how much a characters acceleration increases by when WASD is pressed
ACCELERATION = 1

# this number determines how fast a character slows down
FRICTION = -0.2

# this number determines the minimum distance a character has to be start moving towards the player controlled character
FOLLOW_DISTANCE = 100

# this number determines the maximum distance a character has to be from another in order to be repulsed
REPULSION_RADIUS = 60

# this number determines the maximum distance the player controlled character can be and still interact with a tile on the map
INTERACT_RADIUS = 100

# this number determines the maximum distance the player controlled character can be from an enemy to start a battle
BATTLE_RADIUS = 200
