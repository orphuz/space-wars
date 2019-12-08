import random
import math

import turtle
from game_config import *

class Sprite(turtle.Turtle):
    def __init__(self, spriteshape, spritesize, color, startx, starty):
        turtle.Turtle.__init__(self, shape = spriteshape)
        self.speed(0)
        self.penup()
        self.shapesize(spritesize)
        self.radius = spritesize * 10
        self.color(color)
        self.fd(0)
        self.goto(startx, starty)
        self.speed = 1

    def move(self):
        self.fd(self.speed)

        #Boundary detection
        if self.xcor() + self.radius > field_width/2:
            self.setx(field_width/2 - self.radius)
            #Invert xIncrement
            if self.heading() <= 90:
                self.setheading(180 - self.heading())
            else:
                self.setheading(180 - self.heading())

        if self.xcor() - self.radius < -field_width/2:
            self.setx(-field_width/2 + self.radius)
            #Invert yxncrement
            if self.heading() <= 90:
                self.setheading(90 + self.heading())
            else:
                self.setheading(180 - self.heading())

        if self.ycor() + self.radius > field_height/2:
            self.sety(field_height/2 - self.radius)
            #Invert yIncrement
            if self.heading() <= 180:
                self.setheading(- self.heading())
            else:
                self.setheading(180 - self.heading())

        if self.ycor() - self.radius < -field_height/2:
            self.sety(-field_height/2 + self.radius)
            #Invert yIncrement
            if self.heading() > 180:
                self.setheading(- self.heading())
            else:
                self.setheading(180 - self.heading())

    def is_collision(self, other):
        if (self.xcor() + self.radius >= (other.xcor() - other.radius)) and \
        (self.xcor() - self.radius <= (other.xcor() + other.radius)) and \
        (self.ycor() + self.radius >= (other.ycor() - other.radius)) and \
        (self.ycor() - self.radius <= (other.ycor() + other.radius)):
            return True
        else:
            return False

class Player(Sprite):
    def __init__(self, spriteshape, spritesize, color, startx, starty):
        Sprite.__init__(self, spriteshape, spritesize, color, startx, starty)
        self.speed = player_speed_default
        self.lives = player_lives
        self.setheading(0)

    def turn_left(self):
        self.lt(player_turn_rate)

    def turn_right(self):
        self.rt(player_turn_rate)

    def accelerate(self):
        self.speed += 1

    def decelerate(self):
        self.speed -= 1

class Enemy(Sprite):
    def __init__(self, spriteshape, spritesize, color, startx, starty):
        Sprite.__init__(self, spriteshape, spritesize, color, startx, starty)
        self.speed = enemy_speed
        self.lives = 1
        self.setheading(random.randint(0,360))

class Missile(Sprite):
    def __init__(self, spriteshape, spritesize, color, startx, starty, player):
        Sprite.__init__(self, spriteshape, spritesize, color, startx, starty)
        #self.shapesize(stretch_wid=0.3, stretch_len=0.4, outline=None)
        self.player = player
        self.speed = missile_speed
        self.status = "ready"
        self.goto(-1000, 1000) #hide missle

    def fire(self):
        if self.status == "ready":
            self.goto(self.player.xcor(), self.player.ycor())
            self.setheading(self.player.heading())
            self.status = "firing"

    def reset(self):
        if self.status == "firing":
            self.fd(0)
            self.goto(-1000,1000)
            self.status = "ready"

    def move(self):
        if self.status == "firing":
            #border check
            if self.xcor() < -field_width/2 or self.xcor() > field_width/2 or \
            self.ycor() < -field_height/2 or self.ycor() > field_height/2 :
                self.reset()
            else:
                self.fd(self.speed)
