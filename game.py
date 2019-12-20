import turtle
import logging


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
            1 : 'running',
            2 : 'paused'
        }
        self.config_values = config_values
        self._level = 1
        self._score = 0
        self._lives = self.config_values['player_lives']
        self._state = 'running'
        self.pen = turtle.Turtle()
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

    @property
    def state(self):
        return self._state

    def toggle_game_state(self):
        """ Toggles the game state between states <'running'> and <'paused'> """
        if self._state == 'running':
            self._state = 'paused'
            logging.info('Game paused with game.state = %s' % self.state)
        elif self._state == 'paused':
            self._state = 'running'
            logging.info('Game continued with game.state = %s' % self.state)
        else:
            logging.error('Current state <%s> is unknown' % self._state)
            raise ValueError('Current state <%s> is unknown' % self._state)


    def draw_field(self):
        """Draw border"""
        self.pen.speed(0)
        self.pen.color("white")
        self.pen.pensize(3)
        self.pen.penup()
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

    def show_score(self):
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

    def update_score(self, modifier_lives, modifier_score):
        self._lives += modifier_lives
        self._score += modifier_score
        if self._lives <= 0:    # check for player death
            self._score = 0
            self._lives = self.config_values['player_lives']
            self.toggle_game_state()
        self.show_score()

    def exit(self):
        """Exit the game on click """
        logging.warn("Exiting python program via turtle")
        turtle.mainloop()
        turtle.exitonclick()
