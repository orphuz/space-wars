import random
import math
import turtle
import logging

class Sprite(turtle.Turtle):
    def __init__(self, spriteshape, spritesize, color, startx, starty, current_config_values):
        turtle.Turtle.__init__(self, shape = spriteshape)
        self._name = 'Sprite'
        self.config_values = current_config_values
        self.screen.tracer(0)
        #self.speed(0)
        self.penup()
        self.shapesize(spritesize)
        self.radius = spritesize * 10
        self.color(color)
        self.fd(0)
        self.goto(startx, starty)
        self.speed = 1
        logging.debug("Instance of class {} created!".format(self.__class__))
    
    @property
    def xpos(self):
        """ Return x-Postion of the sprite """
        _xpos = self.xcor()
        return int(_xpos)

    @property
    def ypos(self):
        """ Return y-Postion of the sprite """
        _ypos = self.ycor()
        return int(_ypos)

    def move(self):
        """ Sprite movement per frame """
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
        """ Check for collision between self and given sprite <other> """
        if self.distance(other) <= (self.radius + other.radius):
            logging.debug('Collision of <{0}> with <{1}> detected!'.format(self._name, other._name))
            return True
        else:
            return False

    def distance(self, other):
        """ Calculate distance between self and given sprite <other> """
        _distance = math.sqrt(float(((self.xpos) - other.xpos) ** 2 + (self.ypos - other.ypos) ** 2))
        return _distance

    def random_position(self, other = None):
        """ Change sprite position to random location """
        while True:
            x = random.randint(- int(self.config_values['field_width']) // 2, self.config_values['field_width'] // 2)
            y = random.randint(- int(self.config_values['field_height']) // 2, self.config_values['field_height'] // 2)
            if other != None:
                if self.distance(other) >= (self.radius + other.radius + 30):
                    break
            else:
                break     
        self.goto(x, y)

    def random_heading(self):
        """ Change sprite heading to random angle """ 
        self.setheading(random.randint(0,359))

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
        
    def die(self):
        """ Death of enemy currently only radomly sets it to a new position """
        self.random_position()
        self.random_heading()

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
