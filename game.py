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

import states
import game_config

class Game():
    def __init__(self, name):
        """ Main game class """
        self.name = name
        self.config_values = self.load_config()
        # self.enemies = []
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
        logging.debug("Instance of class {} created!".format(self.__class__))

        self.welcoming = states.State("welcoming", {
            "confirm": "self.run()",
            "cancel": "self.exit()"
        })
        self.running = states.State("running", {
            "cancel": "self.pause()",
            "player_death": "self.dead()"
        })
        self.paused = states.State("paused", {
            "confirm": "self.run()",
            "cancel": "self.dead()"
        })
        self.over = states.State("over", {
            "confirm": "self.welcome()",
            "cancel": "self.exit()"
        })
        self.exiting = states.State("exiting", {"cancel": "self.exit()"}) # Hack
        
        global STATES
        STATES = (
            self.welcoming, 
            self.running,
            self.paused,
            self.over,
            self.exiting
        )

        self.player = Player(self)
        self.bind_keys()
        self.state = self.welcoming
        self.mainloop()
 
    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state_request):
        """ Check validity of game state and set it """
        if state_request not in STATES:
            logging.error('Requested state <%s> is unknown' % state_request)
            raise ValueError('Requested state <%s> is unknown' % state_request)
        self._state = state_request
        #print('Set self.state = {}'.format(self.state.name))
        logging.debug('Set self.state = {}'.format(self.state.name))

    def mainloop(self):
        """ Main loop to check game state and trigger actions """
        while self.state != self.exiting:

            if self.state == self.welcoming:
                self.welcome()
            
            if self.state == self.paused:
                self.pause()

            if self.state == self.over:
                self.dead()

            if self.state == self.exit:
                self.exit()

            self.pen.screen.update() # includes the check for key press
            
            time.sleep(0.1) # Slow down main loop

    def load_config(self):
        """ Load self config from the config file """
        config = game_config.Config()
        logging.debug("self config loaded")
        return config.current_values        

    def bind_keys(self):
        """ Assign Keyboard Bindings """
        self.pen.screen.onkey(partial(self.player_ctrl, self.player.turn_left), "Left")
        self.pen.screen.onkey(partial(self.player_ctrl, self.player.turn_right), "Right")
        self.pen.screen.onkey(partial(self.player_ctrl, self.player.accelerate), "Up")
        self.pen.screen.onkey(partial(self.player_ctrl, self.player.decelerate), "Down")
        self.pen.screen.onkey(partial(self.player_ctrl, self.player.fire), "space")
        self.pen.screen.onkey(self.confirm, "Return")
        self.pen.screen.onkey(self.cancel, "Escape")
        self.pen.screen.listen()
        logging.debug("Key bindings successfully assigned ")

    def wait_for_input(self):
        """ wait for input of player """
        while self.state == self.welcoming or self.state == self.paused or self.state == self.over:
            logging.debug('self {} - Waiting for player input'.format(self.state.name))
            self.pen.screen.update() # includes the check for key press
            time.sleep(0.1) # Slow down main loop

    def player_ctrl(self, fun):
        """ Executes game controls only when the game is in state <running> """
        if self.state == self.running:
            fun()
        else:
            logging.debug("Player controls are only available when game is running (current state: {})".format(self.state.name))

    def confirm(self):
        """ Player input to confirm """
        exec_function = self.state.transit("confirm")
        eval(exec_function)

    def cancel(self):
        """ Player input to cancel """
        eval(self.state.transit("cancel"))

    def death(self):
        """ Game input player dies """
        eval(self.state.transit("player_death"))

    def welcome(self):
        """ Welcome screen aka Intro """
        Enemy.instances.clear()
        for _ in range(self.config_values['enemy_max_no']):
            Enemy.spawn(self)
        self.hide_sprites()
        self.draw_welcome()
        self.state = self.welcoming
        while self.state == self.welcoming:
            self.wait_for_input()

    def run(self):
        """ Draws all game elements and runs the game """
        self.show_sprites()
        self.draw_field()
        self.draw_score()
        self.state = self.running

        current_time = target_time = time.perf_counter()

        while self.state == self.running:
                #logging.debug("Start of self loop with self.state = %s" % self.state)
                self.previous_time, current_time = current_time, time.perf_counter() #update relative timestamps
                # time_delta = current_time - previous_time

                self.pen.screen.update()

                self.player.move()

                for enemy in Enemy.instances:
                    enemy.move()

                for missile in Missile.instances:
                    missile.move()

                for enemy in Enemy.instances:
                    #Check for collision with enemies
                    if self.player.is_collision(enemy):
                        enemy.despawn()
                        Enemy.spawn(self)
                        self.update_score(-1, 0) #remove 1 live

                    for missile in Missile.instances:
                        # Check for collision with all missles shot
                        if missile.is_collision(enemy):
                            enemy.despawn()
                            missile.despawn()
                            Enemy.spawn(self)
                            Enemy.spawn(self)
                            self.update_score(0, enemy.value) #add 10 to score                 
            
                #### sleep management to achieve constant FPS
                target_time += self.loop_delta
                sleep_time = target_time - time.perf_counter()
                if sleep_time > 0:
                    # logging.debug("Sleeping for: {}".format(sleep_time))
                    time.sleep(sleep_time)
                else:
                    print("Execution of main loop took too long: {}".format(sleep_time))
                    logging.warning("Execution of main loop took too long: {}".format(sleep_time))
        
    def pause(self):
        self.hide_sprites()
        self.draw_pause()
        self.state = self.paused
        while self.state == self.paused:
            self.wait_for_input()
    
    def dead(self):
        self.state = self.over
        self.hide_sprites()
        for enemy in Enemy.instances:
            enemy.despawn()
        for enemy in Missile.instances:
            enemy.despawn()
        logging.debug('Deleted all enemies, now left: {}'.format(len(Enemy.instances)))
        self.player.missiles_shot.clear()
        logging.debug('Deleted all players, now left: {}'.format(len(self.player.missiles_shot)))

        self.draw_over()
        self._score = 0
        self._lives = self.config_values['player_lives']

        while self.state == self.paused:
            self.wait_for_input()

    def exit(self):
        """ Close turtle panel and exit the self application """
        self.state = self.exiting
        logging.warn("Exiting python program via turtle")
        self.pen.screen.bye
        sys.exit()

    def hide_sprites(self):
        self.player.ht()
        for enemy in Enemy.instances:
            enemy.ht()
        for missile in Missile.instances:
            missile.ht()

    def show_sprites(self):
        self.player.st()
        for enemy in Enemy.instances:
            enemy.st()
        for missile in Missile.instances:
            missile.st()

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
        """ Draw border of the game field """
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

    def draw_pause(self):
        self.draw_screen("GAME PAUSED", 300, 300, "", "Press <Return> to continue", "Press <ESC> to go to start screen")

    def draw_over(self):
        """ Draw game over screen """
        self.draw_screen("GAME OVER", 300, 300, "Your final score: {}".format(self._score), "Press <Return> to continue", "Press <ESC> to exit")

    def update_score(self, modifier_lives, modifier_score):
        """ Update the game score based on the given modifiers and draw it to the canvas """
        self._lives += modifier_lives
        self._score += modifier_score
        self.draw_score()
        if self._lives <= 0:    # check for player death
            self.death()