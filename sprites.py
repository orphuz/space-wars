import random
import math
import turtle
import logging

class Sprite(turtle.Turtle):
    def __init__(self, spriteshape, spritesize, color, startx, starty, current_config_values):
        turtle.Turtle.__init__(self, shape = spriteshape)
        self._name = 'Sprite'
        self.config_values = current_config_values
        self.speed(0)
        self.penup()
        self.tracer(0)
        self.shapesize(spritesize)
        self.radius = spritesize * 10
        self.color(color)
        self.fd(0)
        self.goto(startx, starty)
        self.speed = 1
        logging.debug("Instance of class {} created!".format(self.__class__))

    def move(self):
        self.fd(self.speed)

        #Boundary detection
        if self.xcor() + self.radius > self.config_values['field_width']/2:
            self.setx(self.config_values['field_width']/2 - self.radius)
            #Invert xIncrement
            if self.heading() <= 90:
                self.setheading(180 - self.heading())
            else:
                self.setheading(180 - self.heading())

        if self.xcor() - self.radius < -self.config_values['field_width']/2:
            self.setx(-self.config_values['field_width']/2 + self.radius)
            #Invert yxncrement
            if self.heading() <= 90:
                self.setheading(90 + self.heading())
            else:
                self.setheading(180 - self.heading())

        if self.ycor() + self.radius > self.config_values['field_height']/2:
            self.sety(self.config_values['field_height']/2 - self.radius)
            #Invert yIncrement
            if self.heading() <= 180:
                self.setheading(- self.heading())
            else:
                self.setheading(180 - self.heading())

        if self.ycor() - self.radius < -self.config_values['field_height']/2:
            self.sety(-self.config_values['field_height']/2 + self.radius)
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
            logging.debug('Collision of <{0}> with <{1}> detected!'.format(self._name, other._name))
            return True
        else:
            return False

class Player(Sprite):
    def __init__(self, spriteshape, spritesize, color, startx, starty, current_config_values):
        Sprite.__init__(self, spriteshape, spritesize, color, startx, starty, current_config_values)
        self._name = 'Player'
        self.speed = self.config_values['player_speed_default']
        self.lives = self.config_values['player_lives']
        self.setheading(0)

    def turn_left(self):
        self.lt(self.config_values['player_turn_rate'])

    def turn_right(self):
        self.rt(self.config_values['player_turn_rate'])

    def accelerate(self):
        self.speed += 1

    def decelerate(self):
        self.speed -= 1

class Enemy(Sprite):
    def __init__(self, spriteshape, spritesize, current_config_values):
        Sprite.__init__(self, spriteshape, spritesize, 'red', random.randint(- current_config_values['field_width']/2, current_config_values['field_width']/2), random.randint(- current_config_values['field_height']/2, current_config_values['field_height']/2), current_config_values)
        self._name = 'Enemy'
        self.speed = self.config_values['enemy_speed']
        self.value = 100
        self.setheading(random.randint(0,360))

class Missile(Sprite):
    def __init__(self, spriteshape, spritesize, current_config_values, player):
        Sprite.__init__(self, spriteshape, spritesize, 'yellow', -1000, -1000, current_config_values)
        self._name = 'Missile'
        #self.shapesize(stretch_wid=0.3, stretch_len=0.4, outline=None)
        self.player = player
        self.speed = self.config_values['missile_speed']
        self.status = "ready"

    def fire(self):
        if self.status == "ready":
            self.goto(self.player.xcor(), self.player.ycor())
            self.setheading(self.player.heading())
            self.status = "firing"
            logging.debug('Missle fired')

    def reset(self):
        if self.status == "firing":
            self.fd(0)
            self.goto(-1000,1000)
            self.status = "ready"

    def move(self):
        if self.status == "firing":
            #border check
            if self.xcor() < -self.config_values['field_width']/2 or self.xcor() > self.config_values['field_width']/2 or \
            self.ycor() < -self.config_values['field_height']/2 or self.ycor() > self.config_values['field_height']/2 :
                logging.debug('Missile collided with wall')
                self.reset()
            else:
                self.fd(self.speed)
