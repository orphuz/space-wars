import turtle


# Define the GUI
turtle.speed(0)
turtle.bgcolor("black")
turtle.ht()
turtle.setundobuffer(1)
turtle.tracer(0)

# Main Game Class
class Game():
    def __init__(self, config_values):
        self.config_values = config_values
        self.level = 1
        self.score = 0
        self.lives = self.config_values['player_lives']
        self.state = "playing"
        self.pen = turtle.Turtle()
        self.t_lives = turtle.Turtle()
        self.t_lives.color("white")
        self.t_lives.tracer(0)
        self.t_lives.ht()
        self.t_lives.speed(0)
        self.t_lives.penup()
        self.t_score = turtle.Turtle()
        self.t_score.color("white")
        self.t_score.tracer(0)
        self.t_score.ht()
        self.t_score.speed(0)
        self.t_score.penup()


    def draw_border(self):
        """Draw border"""
        self.pen.speed(0)
        self.pen.color("white")
        self.pen.pensize(3)
        self.pen.penup()
        self.pen.goto(- self.config_values['field_width']/2, self.config_values['field_height']/2)
        self.pen.pendown()
        self.pen.fd(self.config_values['field_width']) # this will not work for
        self.pen.rt(90)
        self.pen.fd(self.config_values['field_height']) # this will not work for
        self.pen.rt(90)
        self.pen.fd(self.config_values['field_width']) # this will not work for
        self.pen.rt(90)
        self.pen.fd(self.config_values['field_height']) # this will not work for
        self.pen.rt(90)
        self.pen.penup()
        self.pen.ht()

    def exit(self):
        """Exit the game on click """
        turtle.mainloop()
        turtle.exitonclick()

    def show_score(self):
        """ Disply the game score """
        self.t_lives.undo()
        self.t_score.undo()
        msg_lives = "Lives: %s" %(self.lives)
        msg_score = "Score: %s" %(self.score)
        self.t_lives.penup()
        self.t_lives.goto(- self.config_values['field_width']/2, self.config_values['field_height']/2 + 10)
        self.t_lives.pendown()
        self.t_lives.write(msg_lives, font=("Arial", 16, "normal"))
        self.t_score.penup()
        self.t_score.goto(- self.config_values['field_width']/2, self.config_values['field_height']/2 + 30)
        self.t_score.pendown()
        self.t_score.write(msg_score, font=("Arial", 16, "normal"))

    def update_score(self, modifier_lives, modifier_score):
        self.lives += modifier_lives
        self.score += modifier_score
        self.show_score()
