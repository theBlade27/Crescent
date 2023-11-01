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

        self.game.close_menu('INVENTORY')
        self.game.close_menu('SELECT_SKILLS')

    def update(self):

        self.game.textbox_text = 'IT IS {}\'S TURN'.format(self.character.name)
        if self.change_in_health != 0:
            self.game.textbox_text += '\n{} TOOK {} DAMAGE'.format(self.character.name, int(self.change_in_health))
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

        self.game.close_menu('INVENTORY')
        self.game.close_menu('SELECT_SKILLS')

    def update(self):

        self.game.textbox_text = 'IT IS {}\'S TURN'.format(self.character.name)
        if self.change_in_health != 0:
            self.game.textbox_text += '\n{} TOOK {} DAMAGE'.format(self.character.name, int(self.change_in_health))

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
            if self.character.meltingdown:
                self.character.meltdown()
            if self.character.givingup:
                self.character.giveup()
            self.kill()

class EnemyIsMovingTimer(Timer):

    def __init__(self, game, character):
        super().__init__(game, 1000)

        self.character = character

        self.game.close_menu('INVENTORY')
        self.game.close_menu('SELECT_SKILLS')

    def update(self):

        self.game.textbox_text = '{} IS MOVING'.format(self.character.name)
        self.game.menus['TOP'].update_images()
        self.game.textbox_portrait = Sprite(PORTRAITS, scale = 8).get_sprite(0, 0, 20, 20)
        self.game.menus['TOP'].images['PORTRAIT'].update()
        
        now = p.time.get_ticks()

        if now >= self.target_time:
            self.character.move_tile()
            self.kill()
            
class HeroIsMovingTimer(Timer):

    def __init__(self, game, character):
        super().__init__(game, 2000)

        self.character = character

        self.game.close_menu('INVENTORY')
        self.game.close_menu('SELECT_SKILLS')

    def update(self):

        self.game.textbox_text = '{} IS HAVING A MOMENT...'.format(self.character.name)
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

        self.game.close_menu('INVENTORY')
        self.game.close_menu('SELECT_SKILLS')

    def update(self):

        self.game.textbox_text = '{} IS USING {}'.format(self.character.name, self.character.selected_skill.name)
        self.game.menus['TOP'].update_images()
        self.game.textbox_portrait = Sprite(PORTRAITS, scale = 8).get_sprite(0, 0, 20, 20)
        self.game.menus['TOP'].images['PORTRAIT'].update()
        
        now = p.time.get_ticks()

        if now >= self.target_time:
            
            self.character.use_selected_skill()
            self.kill()

class HeroIsAttackingTimer(Timer):

    def __init__(self, game, character):
        super().__init__(game, 2000)

        self.character = character

        self.game.close_menu('INVENTORY')
        self.game.close_menu('SELECT_SKILLS')

    def update(self):

        self.game.textbox_text = '{} IS LASHING OUT!'.format(self.character.name, self.character.selected_skill.name)
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

        self.game.close_menu('INVENTORY')
        self.game.close_menu('SELECT_SKILLS')

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

        self.game.close_menu('INVENTORY')
        self.game.close_menu('SELECT_SKILLS')

    def update(self):

        self.game.textbox_text = self.text
        self.game.menus['TOP'].update_images()
        self.game.textbox_portrait = Sprite(PORTRAITS, scale = 8).get_sprite(0, 0, 20, 20)
        self.game.menus['TOP'].images['PORTRAIT'].update()


        now = p.time.get_ticks()

        if now >= self.target_time:
            self.game.battle.start_next_character_turn()
            if 'COMBAT_ANIMATIONS' in self.game.menus:
                self.game.menus['COMBAT_ANIMATIONS'].kill()
            for menu in self.game.menus.values():
                menu.colour = FAKEBLACK
                menu.update()
            self.game.numbers.empty()
            self.kill()

class StunnedTimer(Timer):

    def __init__(self, game, character):
        super().__init__(game, 2000)

        self.character = character

        self.game.close_menu('INVENTORY')
        self.game.close_menu('SELECT_SKILLS')

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

        if self.character.meltingdown:
            for menu in list(self.game.menus):
                if menu == 'HERO1' or menu == 'HERO2' or menu == 'HERO3' or menu == 'HERO4':
                    self.game.menus[menu].colour = PURPLE
                    self.game.menus[menu].update()

        if self.character.givingup:
            for menu in list(self.game.menus):
                if menu == 'HERO1' or menu == 'HERO2' or menu == 'HERO3' or menu == 'HERO4':
                    if self.game.menus[menu].hero == self.character:
                        self.game.menus[menu].colour = PURPLE
                        self.game.menus[menu].update()

        now = p.time.get_ticks()

        if now >= self.target_time:
            if self.character.meltingdown:
                self.character.meltingdown = False
                for menu in self.game.menus.values():
                    menu.update_images()
            if self.character.givingup:
                self.character.givingup = False
                NextTurnTimer(self.game, self.character)
                for menu in self.game.menus.values():
                    menu.update_images()
            self.character.barking = False
            self.menu.kill()
            self.kill()