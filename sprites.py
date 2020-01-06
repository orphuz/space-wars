import random
import math
import turtle
import logging

class Sprite(turtle.Turtle):

    instances = []
    max_number = 3

    def __init__(self, game, name, spriteshape, spritesize, color):
        turtle.Turtle.__init__(self)
        self.game = game
        self._name = name
        self.shape(spriteshape)
        self.shapesize(spritesize)
        self.color(color)
        self.config_values = game.config_values
        self.screen.tracer(0)
        self.penup()
        self.radius = spritesize * 10
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

    @property
    def name(self):
        """ Return y-Postion of the sprite """
        return self._name

    def despawn(self):
        self.ht()
        self.instances.remove(self)

    def move(self):
        """ 
        Sprite movement per frame:
        - check for boundary collision
        - change postion and heading if necessary
        """
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

    def random_position(self, other = None, distance = 30):
        """ Change sprite position to random location """
        while True:
            x = random.randint(- int(self.config_values['field_width']) // 2, self.config_values['field_width'] // 2)
            y = random.randint(- int(self.config_values['field_height']) // 2, self.config_values['field_height'] // 2)
            self.goto(x, y)
            if other != None:
                if self.distance(other) >= (self.radius + other.radius + distance):
                    break
                else:
                    logging.debug('<{}> withtin range of {} - retrying with half distance'.format(other, distance))
                    distance = distance // 2
            else:
                break

    def random_heading(self):
        """ Change sprite heading to random angle """ 
        self.setheading(random.randint(0,359))

class Player(Sprite):
    """ Player Sprite """
    def __init__(self, game):
        Sprite.__init__(self, game, 'Player', 'triangle', 1, 'white')
        #self.shapesize(stretch_wid=0.3, stretch_len=0.4, outline=None)
        self.setpos(0,0)
        self.random_heading()
        self.speed = self.config_values['player_speed_default']
        self.lives = self.config_values['player_lives']

        # self.missiles_shot = []
        # self.max_missiles_number = 5 # Todo: make global? 

    def turn_left(self):
        self.lt(self.config_values['player_turn_rate'])

    def turn_right(self):
        self.rt(self.config_values['player_turn_rate'])

    def accelerate(self):
        self.speed += 1

    def decelerate(self):
        self.speed -= 1

    def fire(self):       
        Missile.spawn(self.game, self)


class Missile(Sprite):
    """ Missile Sprite """

    instances = []
    max_number = 2

    def __init__(self, game, player):
        Sprite.__init__(self, game, 'Missile', 'triangle', 0.5, 'yellow')
        #self.shapesize(stretch_wid=0.3, stretch_len=0.4, outline=None)
        self.setpos(player.xpos, player.ypos)
        self.setheading(player.heading())
        self.speed = self.config_values['missile_speed']

    @classmethod
    def spawn(cls, game, player):
        if len(cls.instances) < cls.max_number:
            cls.instances.append(cls(game, player))
            logging.debug('Missile fired - currently:{}/{} flying'.format(len(cls.instances), cls.max_number))
        else:
            logging.debug('All Missile already fired - currently:{}/{} flying'.format(len(cls.instances), cls.max_number))

    def move(self):
        ''' Check for borders and distroies missele, otherwise moves '''
        if self.xcor() < - self.config_values['field_width']/2 or self.xcor() > self.config_values['field_width']/2 or \
        self.ycor() < - self.config_values['field_height']/2 or self.ycor() > self.config_values['field_height']/2 :
            logging.debug('Missile collided with wall')
            Missile.despawn(self)
        else:
            self.fd(self.speed)

class Enemy(Sprite):
    """ Enemy sprite """
    instance = []
    max_number = 30

    def __init__(self, game):
        Sprite.__init__(self, game, 'Enemy', 'circle', 1, 'red')
        self.speed = self.config_values['enemy_speed']
        self.random_heading()
        self._value = 100
    
    @classmethod
    def spawn(cls, game, distance = 200):
        """ Spawns an object of type enemy """
        if len(cls.instances) < cls.max_number:
            cls.instances.append(cls(game))
            cls.instances[-1].random_position(game.player, distance)
            logging.debug('Enemy spawned - currently:{}/{} existing'.format(len(cls.instances), cls.max_number))
        else:
            logging.debug('All Missile already fired - currently:{}/{} flying'.format(len(cls.instances), cls.max_number))

    @property
    def value(self):
        return self._value