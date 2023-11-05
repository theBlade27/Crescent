import pygame as p
from settings import *
from sprite import *
from effect import *

class Timer(p.sprite.Sprite):

    # timers are used to make things not happen instantly
    # for example, we dont want the enemies to act instantly, or combat animation to end instantly
    # most timers are basically the same, so not every single one is commented on

    def __init__(self, game, time):
        self.groups = game.timers, game.all
        p.sprite.Sprite.__init__(self, self.groups)

        now = p.time.get_ticks()

        # the time after which the timer needs to run its code is passed as an argument, and the target time is calculated
        self.target_time = now + time
        self.game = game

    def update(self):

        now = p.time.get_ticks()

        # if the current time is greater than the target time, the timer runs the necessary code and then kills itself

        if now >= self.target_time:
            self.kill()

class CalculateSkillTimer(Timer):

    def __init__(self, game, character, change_in_health):
        super().__init__(game, 1000)

        self.character = character
        self.change_in_health = change_in_health

        self.game.close_menu()

    def update(self):

        # display whose turn it is and how much damage they have taken from debuffs

        self.game.textbox_text = 'IT IS {}\'S TURN'.format(self.character.name)
        if self.change_in_health != 0:
            self.game.textbox_text += '\n{} TOOK {} DAMAGE'.format(self.character.name, int(self.change_in_health))
        self.game.menus['TOP'].update_images()
        self.game.textbox_portrait = Sprite(PORTRAITS, scale = 8).get_sprite(0, 0, 20, 20)
        self.game.menus['TOP'].images['PORTRAIT'].update()
        
        now = p.time.get_ticks()

        if now >= self.target_time:
            # if the character isnt dead, calculate what skill they need to use
            if self.character in self.game.battle.all_characters:
                self.character.calculate_skill()

            # otherwise, start the next characters turn
            else:
                self.game.selected_character = self.game.battle.all_characters[(self.game.battle.turn_order_counter - 1) % len(self.game.battle.all_characters)]
                self.game.battle.start_next_character_turn()
            self.kill()

class PlayerTurnTimer(Timer):

    def __init__(self, game, character, change_in_health):
        super().__init__(game, 1000)

        self.character = character
        self.change_in_health = change_in_health

        self.game.close_menu()

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
            # if the character is dead, start the next characters turn
            if self.character not in self.game.battle.all_characters:
                self.game.selected_character = self.game.battle.all_characters[(self.game.battle.turn_order_counter - 1) % len(self.game.battle.all_characters)]
                self.game.battle.start_next_character_turn()
            # if the character is melting down, run the 'meltdown' function
            if self.character.meltingdown:
                self.character.meltdown()
                # if the character is giving up, run the 'giveup' function
            if self.character.givingup:
                self.character.giveup()
            self.kill()

class EnemyIsMovingTimer(Timer):

    def __init__(self, game, character):
        super().__init__(game, 1000)

        self.character = character

        self.game.close_menu()

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

        self.game.close_menu()

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

        self.game.close_menu()

    def update(self):

        # display the skill the enemy is going to use

        self.game.textbox_text = '{} IS USING {}'.format(self.character.name, self.character.selected_skill.name)
        self.game.menus['TOP'].update_images()
        self.game.textbox_portrait = Sprite(PORTRAITS, scale = 8).get_sprite(0, 0, 20, 20)
        self.game.menus['TOP'].images['PORTRAIT'].update()
        
        now = p.time.get_ticks()

        if now >= self.target_time:

            # the enemy uses the skill they have selected
            
            self.character.use_selected_skill()
            self.kill()

class HeroIsAttackingTimer(Timer):

    def __init__(self, game, character):
        super().__init__(game, 2000)

        self.character = character

        self.game.close_menu()

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

        self.game.close_menu()

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

        self.game.close_menu()

    def update(self):

        self.game.textbox_text = self.text
        self.game.menus['TOP'].update_images()
        self.game.textbox_portrait = Sprite(PORTRAITS, scale = 8).get_sprite(0, 0, 20, 20)
        self.game.menus['TOP'].images['PORTRAIT'].update()


        now = p.time.get_ticks()

        if now >= self.target_time:

            # start the next turn
            self.game.battle.start_next_character_turn()

            # close the menu which is showing the combat animations
            if 'COMBAT_ANIMATIONS' in self.game.menus:
                self.game.menus['COMBAT_ANIMATIONS'].kill()

            # reset the colours of all menu borders to black (some of them change colour when a character takes damage or is healed)
            for menu in self.game.menus.values():
                menu.colour = FAKEBLACK
                menu.update()

            # kill all damage numbers that were being displayed
            self.game.numbers.empty()
            self.kill()

class StunnedTimer(Timer):

    def __init__(self, game, character):
        super().__init__(game, 2000)

        self.character = character

        self.game.close_menu()

    def update(self):

        self.game.textbox_text = '{} IS STUNNED'.format(self.character.name)
        self.game.menus['TOP'].update_images()
        self.game.textbox_portrait = Sprite(PORTRAITS, scale = 8).get_sprite(0, 0, 20, 20)
        self.game.menus['TOP'].images['PORTRAIT'].update()

        now = p.time.get_ticks()

        if now >= self.target_time:
            if self.character in self.game.battle.all_characters:
                # remove the stun effect and give the stun resistance effect
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

        # if the hero is melting down or giving up, make the menu border purple to indicate to the player the heros sanity needs to be dealt with

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
                # skip to the next characters turn
                NextTurnTimer(self.game, self.character)
                for menu in self.game.menus.values():
                    menu.update_images()
            self.character.barking = False
            self.menu.kill()
            self.kill()