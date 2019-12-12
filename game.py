import turtle

from game_config import *

# Define the GUI
turtle.speed(0)
turtle.bgcolor("black")
turtle.ht()
turtle.setundobuffer(1)
turtle.tracer(1)

# Main Game Class
class Game():
    def __init__(self):
        self.level = 1
        self.score = 0
        self.lives = 3
        self.state = "playing"
        self.pen = turtle.Turtle()

    def draw_border(self):
        #Draw border
        self.pen.speed(0)
        self.pen.color("white")
        self.pen.pensize(3)
        self.pen.penup()
        self.pen.goto(- field_width/2, field_height/2)
        self.pen.pendown()
        self.pen.fd(field_width) # this will not work for
        self.pen.rt(90)
        self.pen.fd(field_height) # this will not work for
        self.pen.rt(90)
        self.pen.fd(field_width) # this will not work for
        self.pen.rt(90)
        self.pen.fd(field_height) # this will not work for
        self.pen.rt(90)
        self.pen.penup()
        self.pen.ht()
        self.pen.penup() # only done once as startpoint for the repeated "pen.undo()" in show:score

    def exit(self):
        turtle.mainloop()
        turtle.exitonclick()

    def erase_score(self):
        """Erase score by placing a filled rectangle """
        turtle.setpos(- field_width/2, field_height/2)
        turtle.color(turtle.bgcolor())
        turtle.begin_fill()
        turtle.fd(field_width)
        turtle.setheading(90)
        turtle.fd(60)
        turtle.setheading(180)
        turtle.fd(field_width)
        turtle.setheading(270)
        turtle.fd(60)
        turtle.setheading(0)
        turtle.fd(field_width)
        turtle.end_fill()


    def show_score(self):
        """ Disply the game score """
        self.erase_score()
        msg_lives = "Lives: %s" %(self.lives)
        msg_score = "Score: %s" %(self.score)
        self.pen.goto(- field_width/2, field_height/2 + 10)
        self.pen.write(msg_lives, font=("Arial", 16, "normal"))
        self.pen.goto(- field_width/2, field_height/2 + 30)
        self.pen.write(msg_score, font=("Arial", 16, "normal"))

    def update_score(self, modifier_lives, modifier_score):
        self.lives += modifier_lives
        self.score += modifier_score
        #TODO draw score
