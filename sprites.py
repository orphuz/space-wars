import random
import math
import turtle
import logging

class Sprite(turtle.Turtle):

    instances = []
    max_number = 3

    def __init__(self, spriteshape, spritesize, color, startx, starty, current_config_values):
        turtle.Turtle.__init__(self, shape = spriteshape)
        self._name = 'Sprite'
        self.config_values = current_config_values
        self.screen.tracer(0)
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

    @property
    def name(self):
        """ Return y-Postion of the sprite """
        return self._name

    @classmethod
    def despawn(cls, this_sprite):
        this_sprite.ht()
        cls.instances.remove(this_sprite)

    # def despawn(self):
    #     self.ht()
    #     self._object_tracker.remove(self)
    #     logging.debug("{} despawned, now left: {}".format(self._name, len(self._object_tracker)))

    def move(self):
        """ Sprite movement per frame checks for boundary collision and chances postion and heading if necessary """
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
            if other != None:
                if self.distance(other) >= (self.radius + other.radius + distance):
                    break
                else:
                    logging.debug('<{}> withtin range of {} - retrying with half distance'.format(other, distance))
                    distance = distance // 2
            else:
                break     
        self.goto(x, y)

    def random_heading(self):
        """ Change sprite heading to random angle """ 
        self.setheading(random.randint(0,359))

class Player(Sprite):
    """ Player Sprite """
    def __init__(self, spriteshape, spritesize, color, startx, starty, current_config_values):
        Sprite.__init__(self, spriteshape, spritesize, color, startx, starty, current_config_values)
        self._name = 'Player'
        self.speed = self.config_values['player_speed_default']
        self.lives = self.config_values['player_lives']
        self.setheading(0)
        self.missiles_shot = []
        self._max_missiles_number = 5 # Todo: make global? 

    def turn_left(self):
        self.lt(self.config_values['player_turn_rate'])

    def turn_right(self):
        self.rt(self.config_values['player_turn_rate'])

    def accelerate(self):
        self.speed += 1

    def decelerate(self):
        self.speed -= 1

    def fire(self):       
        Missile.spawn(self)
        #logging.debug('Missle fired - currently {}/{} flying'.format(len(self.missiles_shot), self._max_missiles_number))
        

class Missile(Sprite):
    """ Missile Sprite """

    instances = []
    max_number = 2

    def __init__(self, spriteshape, spritesize, xpos, ypos, current_config_values, player):
        Sprite.__init__(self, spriteshape, spritesize, 'yellow', xpos, ypos, current_config_values)
        #self.shapesize(stretch_wid=0.3, stretch_len=0.4, outline=None)
        self.player = player
        self.speed = self.config_values['missile_speed']
        self.setheading(player.heading())

    @classmethod
    def spawn(cls, player):
        if len(cls.instances) < cls.max_number:
            cls.instances.append(cls("triangle", 0.5, player.xpos, player.ypos, player.config_values, player))
            logging.debug('Missile fired - currently:{}/{} flying'.format(len(cls.instances), cls.max_number))
        else:
            logging.debug('All Missile already fired - currently:{}/{} flying'.format(len(cls.instances), cls.max_number))

    def move(self):
        ''' Check for borders and distroies missele, otherwise moves '''
        if self.xcor() < -self.config_values['field_width']/2 or self.xcor() > self.config_values['field_width']/2 or \
        self.ycor() < -self.config_values['field_height']/2 or self.ycor() > self.config_values['field_height']/2 :
            logging.debug('Missile collided with wall')
            Missile.despawn(self)
        else:
            self.fd(self.speed)

class Enemy(Sprite):
    """ Enemy sprite """
    instance = []
    max_number = 30

    def __init__(self, spriteshape, spritesize, current_config_values):
        Sprite.__init__(self, spriteshape, spritesize, 'red', random.randint(- current_config_values['field_width']/2, current_config_values['field_width']/2), random.randint(- current_config_values['field_height']/2, current_config_values['field_height']/2), current_config_values)
        self._name = 'Enemy'
        self.speed = self.config_values['enemy_speed']
        self.value = 100
        self.random_heading()
    
    @classmethod
    #     self.enemies.append(sprites.Enemy("circle", 1, self.config_values, self.enemies))
    #     self.enemies[-1].st()
    #     if  random_pos == True:
    #         self.enemies[-1].random_position(self.player, distance)
    #     logging.debug("Enemy spawned, now: {}".format(len(self.enemies)))
    def spawn(cls, player, distance = 200):
        """ Spawns an object of type enemy """
        if len(cls.instances) < cls.max_number:
            cls.instances.append(cls("circle", 1, player.config_values))
            cls.instances[-1].random_position(player, distance)
            logging.debug('Enemy spawned - currently:{}/{} existing'.format(len(cls.instances), cls.max_number))
        else:
            logging.debug('All Missile already fired - currently:{}/{} flying'.format(len(cls.instances), cls.max_number))

