import os
import sys
import turtle
import logging
import time
import random
import pickle

from functools import partial

from sprites import Player
from sprites import Enemy
from sprites import Missile
from sprites import Powerup

import states
import game_config

class Game():
    def __init__(self, name):
        """ Main game class """
        self.name = name
        self.config_values = self.load_config()
        self._highscore = pickle.load( open( "highscore.p", "rb" ) )
        self._level = 1
        self._score = 0
        self._lives = self.config_values['player_lives']
        self.loop_delta = 1./self.config_values['game_fps'] #calculate loop time based on fixed FPS value
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
        self.enemies_max_number = 10
        self.enemies_initial_number = 3
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

    def load_config(self):
        """ Load self config from the config file """
        config = game_config.Config()
        logging.debug("self config loaded")
        return config.current_values        

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
        """ Request the initially key binded input at the currents state transition function """
        logging.debug('Player input: {}'.format(input))
        self.state.transit(input)        

    def wait_for_input(self, state):
        """ wait for input of player """
        pass
        # while self.state == state:
        #     logging.debug('self {} - Waiting for player input'.format(self.state.name))
        #     self.pen.screen.update() # includes the check for key press
        #     time.sleep(0.1) # Slow down main loop

    def calculate_next_frame(self):
        """
        Move all sprite for one iteration an check for collisions
        """
        for sprite in self.all_sprites:
            sprite.move()

            for powerup in self.powerups_tracker:
                #Check if player collects a power up
                if self.player.is_collision(powerup):
                    self.player.powerup_type = powerup.type
                    powerup.despawn()

            for enemy in self.enemies_tracker:
                #Check for player collision with enemies
                if self.player.is_collision(enemy):
                    enemy.despawn()
                    Enemy.spawn(self)
                    self.update_score(-1, 0) #remove 1 live

                for missile in self.player.missiles_shot:
                    # Check for collision with all missles shot
                    if missile.is_collision(enemy):
                        self.update_score(0, enemy.value) #add 10 to score
                        enemy.despawn()
                        missile.despawn()
                        Enemy.spawn(self)
                        if self.spawn_decision(self.enemies_spawn_prob): Enemy.spawn(self)
                        if self.spawn_decision(self.powerups_spawn_prob): Powerup.spawn(self)

    def main_loop(self):
        """ Run the main game """
        current_time = target_time = time.perf_counter()
        frame_drop_counter = 0

        while True:

            self.previous_time, current_time = current_time, time.perf_counter() #update relative timestamps

            self.state.execution()
                     
            #### sleep management to achieve constant FPS
            target_time += self.loop_delta
            sleep_time = target_time - time.perf_counter()
            if sleep_time > 0:
                time.sleep(sleep_time)
                if frame_drop_counter > 0 :
                    frame_drop_counter -= 1
                        
                self.pen.screen.update()
                
            else:
                frame_drop_counter += 1
                logging.warning(f"Dropping frame update: Execution of main loop took {abs(sleep_time):.6f}s too long - happend {frame_drop_counter} time(s)")
                if frame_drop_counter > 5:
                    logging.error("Dropped more than five frames in a row - force updating screen now")
                    self.pen.screen.update()
   
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

    def draw_screen(self, title, height, width, text_01 = "", text_02 = "", text_03 = ""):
        """ Template function to draw self screens """
        self.pen.clear()
        self.pen.penup()
        self.pen.setheading(0)
        self.pen.goto(- height / 2, width / 2)
        self.pen.pendown()
        self.pen.fd(width)
        self.pen.rt(90)
        self.pen.fd(height)
        self.pen.rt(90)
        self.pen.fd(width)
        self.pen.rt(90)
        self.pen.fd(height)
        self.pen.penup()
        self.pen.goto(0, 60)
        self.pen.pendown()
        self.pen.write(title, font=("Arial", 28, "normal"), align = 'center')
        self.pen.penup()
        if text_01 != "":
            self.pen.goto(0, -30)
            self.pen.pendown()
            self.pen.write(text_01, font=("Arial", 12, "normal"), align = 'center')
            self.pen.penup()
        if text_02 != "":
            self.pen.goto(- width / 2 + 10 , - height /2 + 30)
            self.pen.pendown()
            self.pen.write(text_02, font=("Arial", 12, "normal"), align = 'left')
            self.pen.penup()
        if text_03 != "":
            self.pen.goto(- width / 2 + 10 , - height /2 + 10)
            self.pen.pendown()
            self.pen.write(text_03, font=("Arial", 12, "normal"), align = 'left')
            self.pen.penup()
        self.pen.screen.update()
        logging.debug("<{}> screen drawn".format(title))

    def draw_field(self):
        """
        Draw border of the game field
        """
        self.pen.clear()
        self.pen.penup()
        self.pen.setheading(0)
        self.pen.goto(- int(float(self.config_values['field_width'])) / 2, int(float(self.config_values['field_height']) / 2))
        self.pen.pendown()
        self.pen.fd(self.config_values['field_width'])
        self.pen.rt(90)
        self.pen.fd(self.config_values['field_height'])
        self.pen.rt(90)
        self.pen.fd(self.config_values['field_width'])
        self.pen.rt(90)
        self.pen.fd(self.config_values['field_height'])
        self.pen.rt(90)
        self.pen.penup()
        self.pen.ht()
        logging.debug("Game field drawn")

    def draw_score(self):
        """ Disply the self score """
        self._t_score.clear()
        msg_lives = "Lives: %s" %(self._lives)
        msg_score = "Score: %s" %(self._score)
        self._t_score.penup()
        self._t_score.goto(- int(float(self.config_values['field_width']) / 2), int(float(self.config_values['field_height']) / 2 + 10))
        self._t_score.pendown()
        self._t_score.write(msg_lives, font=("Arial", 16, "normal"))
        self._t_score.penup()
        self._t_score.goto(- int(float(self.config_values['field_width']) / 2) , int(float(self.config_values['field_height']) / 2 + 30))
        self._t_score.pendown()
        self._t_score.write(msg_score, font=("Arial", 16, "normal"))
        logging.debug("Score drawn")

    def draw_welcome(self):
        """ Draw the welcome screen """
        self.draw_screen("SPACE WARS", 300, 300, "", "Press <Return> to start", "Press <ESC> to exit")
        logging.debug('Welcome screen drawn')

    def draw_pause(self):
        self.draw_screen("GAME PAUSED", 300, 300, "", "Press <Return> to continue", "Press <ESC> to go to start screen")

    def draw_over(self):
        """ Draw game over screen """
        if self._score > self._highscore: self._highscore = self._score
        #TODO: Create notification aboud a newly set highscore
        self.draw_screen("GAME OVER", 300, 300, f"Your final score: {self._score}\n\nHighscore: {self._highscore}", "Press <Return> to continue", "Press <ESC> to exit")
        pickle.dump( self._highscore, open( "highscore.p", "wb" ) )
        logging.debug('Welcome screen drawn')

    def update_score(self, modifier_lives, modifier_score):
        """ Update the game score based on the given modifiers and draw it to the canvas """
        self._lives += modifier_lives
        self._score += modifier_score
        self.draw_score()
        if self._lives <= 0:    # check for player death
            self.state.transit('player_death')

    def exit(self):
        """ Close turtle panel and exit the self application """
        self.state = self.exiting
        logging.warn("Exiting python program via turtle")
        self.pen.screen.bye
        sys.exit()

    def custom_action(self):
        logging.debug('custom aciton triggered - spawn powerup')
        Powerup.spawn(self)
