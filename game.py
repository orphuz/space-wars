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

    def exit(self):
        turtle.mainloop()
        turtle.exitonclick()

    def update_score(self, modifier_lives, modifier_score):
        self.lives += modifier_lives
        self.score += modifier_score
        #TODO draw score
