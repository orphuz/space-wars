import turtle
import logging

import states

# Define the GUI
turtle.speed(0)
turtle.bgcolor("black")
turtle.ht()
turtle.setundobuffer(1)
turtle.tracer(0)

# Main Game Class
class Game():
    def __init__(self, config_values):
        self._STATES = {
            1 : 'welcome',
            2 : 'running',
            3 : 'paused',
            4 : 'over',
            5 : 'exit'
        }

        self.config_values = config_values
        self._level = 1
        self._score = 0
        self._lives = self.config_values['player_lives']
        #self._state = 'paused'
        self.pen = turtle.Turtle()
        self.pen.speed(0)
        self.pen.clear()
        self.pen.color("white")
        self.pen.pensize(3)
        self._t_lives = turtle.Turtle()
        self._t_lives.color("white")
        self._t_lives.tracer(0)
        self._t_lives.ht()
        self._t_lives.speed(0)
        self._t_lives.penup()
        self._t_score = turtle.Turtle()
        self._t_score.color("white")
        self._t_score.tracer(0)
        self._t_score.ht()
        self._t_score.speed(0)
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

        self.state = self.welcoming


    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state_request):
        if state_request not in _STATES:
            logging.error('Requested state <%s> is unknown' % state_request)
            raise ValueError('Requested state <%s> is unknown' % state_request)
        self._state = state_request
        logging.debug('Set game.state = %s' % self.state)

    # def toggle_game_state(self):
    #     """ Toggles the game state between states <'running'> and <'paused'> """
    #     if self.state == 'running':
    #         self.pause()
    #     elif self.state == 'paused' or self.state == 'over':
    #         self.run()


    def confirm(self):
        eval(self.state.transit("confirm"))

    def cancel(self):
        eval(self.state.transit("cancel"))

    def welcome(self):
        """ Welcome screen aka Intro """
        self.draw_welcome()
        self.state = self.welcoming

    def run(self):
        """ Draw all game elements and start the game """
        self.draw_field()
        self.draw_score()
        self.state = self.running
        logging.debug('Game running')

    def pause(self):
        self.draw_pause()
        self.state = self.paused

    def dead(self):
        self.state = self.over
        self.draw_over(self._score)
        self._score = 0
        self._lives = self.config_values['player_lives']

    def exit(self):
        """Exit the game on click """
        self.state = self.exiting

    def draw_welcome(self):
        """ Draw the welcome screen """
        self.pen.clear()
        self.pen.penup()
        self.pen.setheading(0)
        self.pen.goto(- self.config_values['field_width']/4, self.config_values['field_height']/4)
        self.pen.pendown()
        self.pen.fd(self.config_values['field_width'] / 2)
        self.pen.rt(90)
        self.pen.fd(self.config_values['field_height'] / 2)
        self.pen.rt(90)
        self.pen.fd(self.config_values['field_width'] / 2)
        self.pen.rt(90)
        self.pen.fd(self.config_values['field_height'] / 2)
        self.pen.penup()
        self.pen.goto(0, 0)
        self.pen.pendown()
        self.pen.write('WELCOME TO: Space Wars', font=("Arial", 28, "normal"), align = 'center')
        self.pen.penup()
        self.pen.goto(0, -10)
        self.pen.pendown()
        msg_score = "Press <ENTER> to start"
        self.pen.write(msg_score, font=("Arial", 12, "normal"), align = 'center')
        self.pen.penup()
        self.pen.ht()
        logging.debug("Welcome screen drawn")

    def draw_field(self):
        """Draw border"""
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
        """ Disply the game score """
        self._t_lives.undo()
        self._t_score.undo()
        msg_lives = "Lives: %s" %(self._lives)
        msg_score = "Score: %s" %(self._score)
        self._t_lives.penup()
        self._t_lives.goto(- self.config_values['field_width']/2, self.config_values['field_height']/2 + 10)
        self._t_lives.pendown()
        self._t_lives.write(msg_lives, font=("Arial", 16, "normal"))
        self._t_score.penup()
        self._t_score.goto(- self.config_values['field_width']/2, self.config_values['field_height']/2 + 30)
        self._t_score.pendown()
        self._t_score.write(msg_score, font=("Arial", 16, "normal"))
        logging.debug("Score drawn")

    def draw_pause(self):
        self.pen.clear()
        self.pen.penup()
        self.pen.setheading(0)
        self.pen.goto(- self.config_values['field_width']/4, self.config_values['field_height']/4)
        self.pen.pendown()
        self.pen.fd(self.config_values['field_width'] / 2)
        self.pen.rt(90)
        self.pen.fd(self.config_values['field_height'] / 2)
        self.pen.rt(90)
        self.pen.fd(self.config_values['field_width'] / 2)
        self.pen.rt(90)
        self.pen.fd(self.config_values['field_height'] / 2)
        self.pen.penup()
        self.pen.goto(0, 0)
        self.pen.pendown()
        self.pen.write('GAME PAUSED', font=("Arial", 28, "normal"), align = 'center')
        self.pen.penup()
        self.pen.ht()
        logging.debug("Pause screen drawn")

    def draw_over(self, final_score):
        self.pen.clear()
        self.pen.penup()
        self.pen.setheading(0)
        self.pen.goto(- self.config_values['field_width']/4, self.config_values['field_height']/4)
        self.pen.pendown()
        self.pen.fd(self.config_values['field_width'] / 2)
        self.pen.rt(90)
        self.pen.fd(self.config_values['field_height'] / 2)
        self.pen.rt(90)
        self.pen.fd(self.config_values['field_width'] / 2)
        self.pen.rt(90)
        self.pen.fd(self.config_values['field_height'] / 2)
        self.pen.penup()
        self.pen.goto(0, 30)
        self.pen.pendown()
        self.pen.write('GAME OVER', font=("Arial", 28, "normal"), align = 'center')
        self.pen.penup()
        self.pen.goto(0, -10)
        self.pen.pendown()
        msg_score = "Your final score: %s" %(self._score)
        self.pen.write(msg_score, font=("Arial", 12, "normal"), align = 'center')
        self.pen.penup()
        self.pen.ht()
        logging.debug("Game Over screen drawn")

    def update_score(self, modifier_lives, modifier_score):
        self._lives += modifier_lives
        self._score += modifier_score
        if self._lives <= 0:    # check for player death
            eval(self.state.transit("player_death"))
        self.draw_score()
