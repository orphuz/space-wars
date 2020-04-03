import os
import sys
import turtle
import logging
import time
import random

from functools import partial

from sprites import Player
from sprites import Enemy
from sprites import Missile
from sprites import Powerup

from helpers.config import Config
from helpers.menu import Menu
from helpers.fps import Fps_manager
from helpers.event import Event_man
from helpers.score import Score

import states

class Game():
    def __init__(self, name):
        """ Main game class """
        self.event_man = Event_man()
        self.config = Config()
        # self.config.values = self.config.current_values
        self.menu = Menu()
        self._highscorefile = "data/highscore.pickle"
        self.score = Score(self._highscorefile)
        self._level = 1
        self._lives = self.config.values['player_lives']

        self._user_input = None

        self.pen = turtle.Turtle(visible = False)
        self.pen.screen.tracer(0)
        self.pen.color('white')
        self.pen.screen.bgcolor("black")
        self.pen.speed(0)

        self._t_score = turtle.Turtle(visible = False)
        self._t_score.color('white')
        self._t_score.penup()

        self.players_tracker = []
        self.player = None

        self.enemies_tracker = []
        self.enemies_initial_number = 3
        self.enemies_max_number = 10
        self.enemies_spawn_prob = 0.5

        self.powerups_tracker = []
        self.powerups_max_number = 2
        self.powerups_spawn_prob = 0.5

        self.welcoming = states.Welcoming(self)
        self.running = states.Running(self)   
        self.paused = states.Paused(self)
        self.over = states.Over(self)
        self.exiting = states.Exit(self)
       
        self.STATES = (
            self.welcoming, 
            self.running,
            self.paused,
            self.over,
            self.exiting
        )

        self.state = self.welcoming

        self.bind_keys()

        self.set_state(self.state)

    @property
    def all_sprites(self):
        all_sprite_objects = self.players_tracker + self.enemies_tracker + self.powerups_tracker
        for this_player in self.players_tracker:
            all_sprite_objects += this_player.missiles_shot
        return all_sprite_objects
 
    def set_state(self, state_request):
        """ Check validity of game state and set it """
        if state_request not in self.STATES:
            logging.error('Requested state <%s> is unknown' % state_request)
            raise ValueError('Requested state <%s> is unknown' % state_request)
        self.state = state_request
        logging.debug('Set game.state = {}'.format(self.state.name))
        self.state.preperation()   

    def bind_keys(self):
        """ Assign Keyboard Bindings """
        input_custom = partial(self.player_input, 'custom')
        self.pen.screen.onkey(input_custom, "c")
        input_left = partial(self.player_input, 'left')
        self.pen.screen.onkey(input_left, "Left")
        input_right = partial(self.player_input, 'right')
        self.pen.screen.onkey(input_right, "Right")
        input_up = partial(self.player_input, 'up')
        self.pen.screen.onkey(input_up, "Up")
        input_down = partial(self.player_input, 'down')
        self.pen.screen.onkey(input_down, "Down")
        input_fire = partial(self.player_input, 'fire')
        self.pen.screen.onkey(input_fire, "space")
        input_return = partial(self.player_input, "confirm")
        self.pen.screen.onkey(input_return, "Return")
        input_esc = partial(self.player_input, "cancel")
        self.pen.screen.onkey(input_esc, "Escape")
        self.pen.screen.listen()
        logging.debug("Key bindings successfully assigned ")

    def player_input(self, input):
        """ Store the player input in a class variable so it can be processed later """
        # TODO: Ensure that multiple inputs can be handled and none is lost
        logging.debug('Player input: {}'.format(input))
        self._user_input = input

    def process_input(self):
        """ If _user_input is not None processes it by triggering the state transition, otherwise does nothing """
        if self._user_input != None:
            current_input = self._user_input
            self._user_input = None
            self.state.transit(current_input)

    def wait_for_input(self):
        """ wait for input of player by essentially doing nothing """
        pass

    def calculate_next_frame(self):
        """
        Move all sprite for one iteration an check for collisions
        """
        sprites = self.all_sprites
        for sprite in sprites:
            sprite.move()

        powerups = self.powerups_tracker
        for powerup in powerups:
            #Check if player collects a power up
            if self.player.is_collision(powerup):
                self.player.apply_buff(powerup)
                powerup.despawn()
        
        enemies = self.enemies_tracker
        for enemy in enemies:
            #Check for player collision with enemies
            if self.player.is_collision(enemy):
                enemy.despawn()
                Enemy.spawn(self)
                self.update_lives(-1) #remove 1 live

            missiles  = self.player.missiles_shot
            for missile in missiles:
                # Check for collision with all missles shot
                if missile.is_collision(enemy):
                    self.score.update_current(enemy.value) #add 10 to score
                    enemy.despawn()
                    missile.despawn()
                    Enemy.spawn(self)
                    if self.spawn_decision(self.enemies_spawn_prob): Enemy.spawn(self)
                    if self.spawn_decision(self.powerups_spawn_prob): Powerup.spawn(self)

            new_powerups = self.powerups_tracker 
            for powerup in new_powerups:
                #Check if player collects a power up
                if powerup.is_collision(enemy):
                    powerup.despawn()

    def main_loop(self, testmode = False):
        """ Run the main game """
        if 'render_manager' not in locals():  render_manager = Fps_manager(self.config.values['game_fps'], 5) # Condition for testing purpose
        
        while True:

            render_manager.update()

            self.process_input() # process user unput
            self.state.execution() # update frame

            render_manager.decide_to_render(self.pen.screen.update) #render frame (if frame time is not yet exceeded)

            if testmode: return      
   
    def spawn_decision(self, probability = 0.5):
        """
        Returns a random true or false decision weighted by provied argument "probability"
        """
        random.seed()
        decision = False
        if random.randint(1, 101) > probability * 100:
            decision = True
        return decision

    def spawn_all_sprites(self):
        """
        Create all sprites (player and enemy) based on their initial number
        """
        self.player = Player.spawn(self) 
        for _ in range(self.enemies_initial_number):
            Enemy.spawn(self)
        logging.debug('All enemies spawned')

    def despawn_all_sprites(self):
        """ Hides and removes all sprites in the game """
        self.hide_sprites()

        for sprite in self.all_sprites:
            sprite.despawn()
        self.players_tracker.clear()
        self.enemies_tracker.clear()
        self.player.missiles_shot.clear()
        logging.debug('All sprites despawned')

    def hide_sprites(self):
        """ Hides all spirtes in the game """
        for sprite in self.all_sprites:
            sprite.ht()
        logging.debug('All sprites hidden')

    def show_sprites(self):
        """ Displays all spirtes in the game """
        for sprite in self.all_sprites:
            sprite.st()
        logging.debug('All sprites made visible')

    def draw_field(self):
        """
        Draw border of the game field
        """
        self.pen.clear()
        self.pen.penup()
        self.pen.setheading(0)
        self.pen.goto(- int(float(self.config.values['field_width'])) / 2, int(float(self.config.values['field_height']) / 2))
        self.pen.pendown()
        self.pen.fd(self.config.values['field_width'])
        self.pen.rt(90)
        self.pen.fd(self.config.values['field_height'])
        self.pen.rt(90)
        self.pen.fd(self.config.values['field_width'])
        self.pen.rt(90)
        self.pen.fd(self.config.values['field_height'])
        self.pen.rt(90)
        self.pen.penup()
        self.pen.ht()
        logging.debug("Game field drawn")

    def draw_score(self):
        """ Display the score """
        self._t_score.clear()
        msg_lives = f"Lives: {self._lives}"
        msg_score = f"Score: {self.score.current}"
        msg_highscore = f"High Score: {self.score.highscore}"
        self._t_score.penup()
        self._t_score.goto(- int(float(self.config.values['field_width']) / 2), int(float(self.config.values['field_height']) / 2 + 10))
        self._t_score.pendown()
        self._t_score.write(msg_lives, font=("Arial", 16, "normal"))
        self._t_score.penup()
        self._t_score.goto(- int(float(self.config.values['field_width']) / 2) , int(float(self.config.values['field_height']) / 2 + 30))
        self._t_score.pendown()
        self._t_score.write(msg_score, font=("Arial", 16, "normal"))
        self._t_score.penup()
        self._t_score.goto( int(float(self.config.values['field_width']) / 2 - 165), int(float(self.config.values['field_height']) / 2 + 10))
        self._t_score.pendown()
        self._t_score.write(msg_highscore, font=("Arial", 16, "normal"))
        logging.debug("Score drawn")

    def draw_new_score(self):
        """ Draws a new score if the new_score flag is set to True and resets the flag """
        if self.score.is_new == True:
            self.draw_score()
            self.score.be_old()

    def update_lives(self, modifier_lives):
        self._lives += modifier_lives
        if self._lives <= 0:    # check for player death
                self.state.transit('player_death')

    def reset_high_score(self):
        self.score.reset_highscore()
        self.state.preperation()  

    def exit(self):
        """ Close turtle panel and exit the self application """
        self.state = self.exiting
        logging.warn("Exiting python program via turtle")
        self.pen.screen.bye
        raise SystemExit
        #sys.exit()

    def custom_action(self):
        """ Custom action trigger vie key press - currently "c" """
        logging.debug('custom aciton triggered - spawn powerup')
        Powerup.spawn(self)
