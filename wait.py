import pygame as p
from settings import *
from sprite import *
from effect import *

class Timer(p.sprite.Sprite):

    def __init__(self, game, time):
        self.groups = game.timers, game.all
        p.sprite.Sprite.__init__(self, self.groups)

        now = p.time.get_ticks()
        self.target_time = now + time
        self.game = game

    def update(self):

        now = p.time.get_ticks()

        if now >= self.target_time:
            self.kill()

class CalculateSkillTimer(Timer):

    def __init__(self, game, character, change_in_health):
        super().__init__(game, 1000)

        self.character = character
        self.change_in_health = change_in_health

    def update(self):

        self.game.textbox_text = 'IT IS {}\'S TURN'.format(self.character.name)
        if self.change_in_health != 0:
            self.game.textbox_text += '\n{} TOOK {} DAMAGE'.format(self.character.name, self.change_in_health)
        self.game.menus['TOP'].update_images()
        self.game.textbox_portrait = Sprite(PORTRAITS, scale = 8).get_sprite(0, 0, 20, 20)
        self.game.menus['TOP'].images['PORTRAIT'].update()
        
        now = p.time.get_ticks()

        if now >= self.target_time:
            if self.character in self.game.battle.all_characters:
                self.character.calculate_skill()
            else:
                self.game.selected_character = self.game.battle.all_characters[(self.game.battle.turn_order_counter - 1) % len(self.game.battle.all_characters)]
                self.game.battle.start_next_character_turn()
            self.kill()

class PlayerTurnTimer(Timer):

    def __init__(self, game, character, change_in_health):
        super().__init__(game, 1000)

        self.character = character
        self.change_in_health = change_in_health

    def update(self):

        self.game.textbox_text = 'IT IS {}\'S TURN'.format(self.character.name)
        if self.change_in_health != 0:
            self.game.textbox_text += '\n{} TOOK {} DAMAGE'.format(self.character.name, self.change_in_health)

        if self.character not in self.game.battle.all_characters:
            self.game.textbox_text += '\n{} MET THEIR END.'.format(self.character.name)

        self.game.menus['TOP'].update_images()
        self.game.textbox_portrait = Sprite(PORTRAITS, scale = 8).get_sprite(0, 0, 20, 20)
        self.game.menus['TOP'].images['PORTRAIT'].update()
        
        now = p.time.get_ticks()

        if now >= self.target_time:
            if self.character not in self.game.battle.all_characters:
                self.game.selected_character = self.game.battle.all_characters[(self.game.battle.turn_order_counter - 1) % len(self.game.battle.all_characters)]
                self.game.battle.start_next_character_turn()
            self.kill()

class EnemyIsMovingTimer(Timer):

    def __init__(self, game, character):
        super().__init__(game, 1000)

        self.character = character

    def update(self):

        self.game.textbox_text = '{} IS MOVING'.format(self.character.name)
        self.game.menus['TOP'].update_images()
        self.game.textbox_portrait = Sprite(PORTRAITS, scale = 8).get_sprite(0, 0, 20, 20)
        self.game.menus['TOP'].images['PORTRAIT'].update()
        
        now = p.time.get_ticks()

        if now >= self.target_time:
            self.character.move_tile()
            self.kill()

class EnemyIsAttackingTimer(Timer):

    def __init__(self, game, character):
        super().__init__(game, 1000)

        self.character = character

    def update(self):

        self.game.textbox_text = '{} IS USING {}'.format(self.character.name, self.character.selected_skill.name)
        self.game.menus['TOP'].update_images()
        self.game.textbox_portrait = Sprite(PORTRAITS, scale = 8).get_sprite(0, 0, 20, 20)
        self.game.menus['TOP'].images['PORTRAIT'].update()
        
        now = p.time.get_ticks()

        if now >= self.target_time:
            self.character.use_selected_skill()
            self.kill()

class NextTurnTimer(Timer):

    def __init__(self, game, character):
        super().__init__(game, 1000)

        self.character = character

    def update(self):
        
        now = p.time.get_ticks()

        if now >= self.target_time:
            self.game.battle.start_next_character_turn()
            self.kill()

class ShowSkillEffectivenessTimer(Timer):

    def __init__(self, game, character, text):
        super().__init__(game, 2000)

        self.text = text
        self.character = character

    def update(self):

        self.game.textbox_text = self.text
        self.game.menus['TOP'].update_images()
        self.game.textbox_portrait = Sprite(PORTRAITS, scale = 8).get_sprite(0, 0, 20, 20)
        self.game.menus['TOP'].images['PORTRAIT'].update()


        now = p.time.get_ticks()

        if now >= self.target_time:
            self.game.battle.start_next_character_turn()
            self.game.menus['COMBAT_ANIMATIONS'].kill()
            self.game.numbers.empty()
            self.kill()

class StunnedTimer(Timer):

    def __init__(self, game, character):
        super().__init__(game, 2000)

        self.character = character

    def update(self):

        self.game.textbox_text = '{} IS STUNNED'.format(self.character.name)
        self.game.menus['TOP'].update_images()
        self.game.textbox_portrait = Sprite(PORTRAITS, scale = 8).get_sprite(0, 0, 20, 20)
        self.game.menus['TOP'].images['PORTRAIT'].update()

        now = p.time.get_ticks()

        if now >= self.target_time:
            if self.character in self.game.battle.all_characters:
                for effect in self.character.effects:
                    if isinstance(effect, Stun):
                        effect.remove_effect()
                self.character.effects.append(StunResist(self.game, self.character))
                self.game.battle.start_next_character_turn()
            else:
                self.game.selected_character = self.game.battle.all_characters[(self.game.battle.turn_order_counter + 1) % len(self.game.battle.all_characters)]
                self.game.battle.start_next_character_turn()
            self.kill()

class BarkTimer(Timer):

    def __init__(self, game, character, text):
        super().__init__(game, 3000)

        self.character = character
        self.text = text
        self.character.barking = True
        self.game.open_menu('BARK', character, text = text)
        self.menu = self.game.menus['BARK']

    def update(self):

        now = p.time.get_ticks()

        if now >= self.target_time:
            self.character.barking = False
            self.menu.kill()
            self.kill()