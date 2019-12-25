import os
import sys
import turtle
import logging
import time
import random

import sprites
import states
import game_config

class Game():
    def __init__(self, name):
        """ Main self class """
        self.name = name
        self.config_values = self.load_config()
        self._level = 1
        self._score = 0
        self._lives = self.config_values['player_lives']
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
            "cancel": "self.welcome()"
        })
        self.over = states.State("over", {
            "confirm": "self.run()",
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

        self.create_sprites()
        self.bind_keys()
        self.welcome()
 
    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state_request):
        if state_request not in STATES:
            logging.error('Requested state <%s> is unknown' % state_request)
            raise ValueError('Requested state <%s> is unknown' % state_request)
        self._state = state_request
        #print('Set self.state = {}'.format(self.state.name))
        logging.debug('Set self.state = {}'.format(self.state.name))

    def load_config(self):
        """ Load self config from the config file """
        config = game_config.Config()
        logging.debug("self config loaded")
        return config.current_values

    def create_sprites(self):
        """ Create sprites for player, missile and enemies """
        self.player = sprites.Player("triangle", 1, "white", 0, 0, self.config_values)
        self.missile = sprites.Missile("triangle", 0.5, self.config_values, self.player) #Missle does always exist but is rendered offscreen when not used
        self.enemies = list()
        for i in range(self.config_values['enemy_max_no']):
            self.enemies.append(sprites.Enemy("circle", 1, self.config_values)) 

    def bind_keys(self):
        # Assign Keyboard Bindings
        self.pen.screen.onkey(self.player.turn_left, "Left")
        self.pen.screen.onkey(self.player.turn_right, "Right")
        self.pen.screen.onkey(self.player.accelerate, "Up")
        self.pen.screen.onkey(self.player.decelerate, "Down")
        self.pen.screen.onkey(self.missile.fire, "space")
        self.pen.screen.onkey(self.confirm, "Return")
        self.pen.screen.onkey(self.cancel, "Escape")
        self.pen.screen.listen()
        logging.debug("Key bindings successfully assigned ")

    def wait_for_input(self):
        while self.state == self.welcoming or self.state == self.paused or self.state == self.over:
            logging.debug('self {} - Waiting for player input'.format(self.state.name))
            self.pen.screen.update() # includes the check for key press
            time.sleep(0.1) # Slow down main loop

    def confirm(self):
        eval(self.state.transit("confirm"))

    def cancel(self):
        eval(self.state.transit("cancel"))

    def welcome(self):
        """ Welcome screen aka Intro """
        self.draw_welcome()
        self.state = self.welcoming

    def run(self):
        """ Draw all self elements and run the self """
        self.draw_field()
        self.draw_score()
        self.state = self.running
        
    def pause(self):
        self.draw_pause()
        self.state = self.paused
    
    def dead(self):
        self.state = self.over
        self.draw_over(self._score)
        self._score = 0
        self._lives = self.config_values['player_lives']

    def exit(self):
        """ Close turtle panel and exit the self application """
        self.state = self.exiting
        logging.warn("Exiting python program via turtle")
        self.pen.screen.bye
        sys.exit()

    def hide_sprites(self):
        self.player.ht()
        for enemy in self.enemies:
            enemy.ht()
        self.missile.ht()

    def show_sprites(self):
        self.player.st()
        for enemy in self.enemies:
            enemy.st()
        self.missile.st()

    def draw_screen(self, title, height, width, text_01 = "", text_02 = "", text_03 = ""):
        """ Template function to draw self screens """
        self.hide_sprites()
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
        self.show_sprites()
        self.pen.clear()
        self.pen.penup()
        self.pen.setheading(0)
        self.pen.goto(- self.config_values['field_width']/2, self.config_values['field_height']/2)
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
        self._t_score.goto(- self.config_values['field_width']/2, self.config_values['field_height']/2 + 10)
        self._t_score.pendown()
        self._t_score.write(msg_lives, font=("Arial", 16, "normal"))
        self._t_score.penup()
        self._t_score.goto(- self.config_values['field_width']/2, self.config_values['field_height']/2 + 30)
        self._t_score.pendown()
        self._t_score.write(msg_score, font=("Arial", 16, "normal"))
        logging.debug("Score drawn")

    def draw_welcome(self):
        """ Draw the welcome screen """
        self.draw_screen("SPACE WARS", 300, 300, "", "Press <Return> to start", "Press <ESC> to exit")

    def draw_pause(self):
        self.draw_screen("GAME PAUSED", 300, 300, "", "Press <Return> to continue", "Press <ESC> to go to start screen")

    def draw_over(self, final_score):
        """ Draw game over screen """
        self.draw_screen("GAME OVER", 300, 300, "Your final score: {}".format(self._score), "Press <Return> to continue", "Press <ESC> to exit")

    def update_score(self, modifier_lives, modifier_score):
        """ Update the game score based on the given modifiers and draw it to the canvas """
        self._lives += modifier_lives
        self._score += modifier_score
        if self._lives <= 0:    # check for player death
            eval(self.state.transit("player_death"))
        self.draw_score()