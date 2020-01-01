import random
import math
import turtle
import logging

class Sprite(turtle.Turtle):
    def __init__(self, spriteshape, spritesize, color, startx, starty, current_config_values, object_tracker):
        turtle.Turtle.__init__(self, shape = spriteshape)
        self._name = 'Sprite'
        self.config_values = current_config_values
        self._object_tracker = object_tracker
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

    def despawn(self):
        self.ht()
        self._object_tracker.remove(self)
        logging.debug("{} despawned, now left: {}".format(self._name, len(self._object_tracker)))

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
    def __init__(self, spriteshape, spritesize, color, startx, starty, current_config_values, object_tracker):
        Sprite.__init__(self, spriteshape, spritesize, color, startx, starty, current_config_values, object_tracker)
        self._name = 'Player'
        self.speed = self.config_values['player_speed_default']
        self.lives = self.config_values['player_lives']
        self.setheading(0)
        self.missiles_shot = []
        self._max_missiles_number = 5 # Todo: make global? 

    def fire(self):
        if len(self.missiles_shot) < self._max_missiles_number:
            self.missiles_shot.append(Missile("triangle", 0.5, self.xpos, self.ypos, self.config_values, self, self.missiles_shot))
            # self.missiles_shot[-1].goto(self.xpos, self.ypos)
            self.missiles_shot[-1].setheading(self.heading())
            logging.debug('Missle fired - currently {}/{} flying'.format(len(self.missiles_shot), self._max_missiles_number))
        else:
            logging.debug('All missiles already fired - currently:{}/{} flying'.format(len(self.missiles_shot), self._max_missiles_number))

    def turn_left(self):
        self.lt(self.config_values['player_turn_rate'])

    def turn_right(self):
        self.rt(self.config_values['player_turn_rate'])

    def accelerate(self):
        self.speed += 1

    def decelerate(self):
        self.speed -= 1

class Missile(Sprite):
    def __init__(self, spriteshape, spritesize, xpos, ypos, current_config_values, player, object_tracker):
        Sprite.__init__(self, spriteshape, spritesize, 'yellow', xpos, ypos, current_config_values, object_tracker)
        self._name = 'Missile'
        #self.shapesize(stretch_wid=0.3, stretch_len=0.4, outline=None)
        self.player = player
        self.speed = self.config_values['missile_speed']

    def move(self):
        #border check
        if self.xcor() < -self.config_values['field_width']/2 or self.xcor() > self.config_values['field_width']/2 or \
        self.ycor() < -self.config_values['field_height']/2 or self.ycor() > self.config_values['field_height']/2 :
            logging.debug('Missile collided with wall')
            self.despawn()
        else:
            self.fd(self.speed)

    # def fire(self):
    #     if self.status == "ready":
    #         self.goto(self.player.xcor(), self.player.ycor())
    #         self.setheading(self.player.heading())
    #         self.status = "firing"
    #         logging.debug('Missle fired')

    # def reset(self):
    #     if self.status == "firing":
    #         self.fd(0)
    #         self.goto(-1000,1000)
    #         self.status = "ready"



class Enemy(Sprite):
    def __init__(self, spriteshape, spritesize, current_config_values, object_tracker):
        Sprite.__init__(self, spriteshape, spritesize, 'red', random.randint(- current_config_values['field_width']/2, current_config_values['field_width']/2), random.randint(- current_config_values['field_height']/2, current_config_values['field_height']/2), current_config_values, object_tracker)
        self._name = 'Enemy'
        self.speed = self.config_values['enemy_speed']
        self.value = 100
        self.random_heading()

