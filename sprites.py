import random
import math
import turtle
import logging

class Sprite(turtle.Turtle):

    def __init__(self, game, name, spriteshape, spritesize, color, object_tracker):
        turtle.Turtle.__init__(self)
        self.object_tracker = object_tracker
        self.game = game
        self._name = name
        self.shape(spriteshape)
        self.shapesize(spritesize)
        self.color(color)
        self.screen.tracer(0)
        self.penup()
        self.radius = spritesize * 10
        logging.debug(f"Instance of {self.__class__} created")

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
        try:
            self.object_tracker.remove(self)
        except ValueError as valerr:
            logging.error(f'{valerr} - Cannot despawn {self}  {self.__class__} as it is not a member of {self.object_tracker}')
        logging.debug(f'Instance of {self.__class__} despawned - currently:{len(self.object_tracker)} existing')

    def move(self):
        """ 
        Sprite movement per frame:
        - check for boundary collision
        - change postion and heading if necessary
        """
        self.fd(self.speed)

        #Boundary detection
        if self.xcor() + self.radius > self.game.config_values['field_width']/2:
            self.setx(self.game.config_values['field_width']/2 - self.radius)
            #Invert xIncrement
            if self.heading() <= 90:
                self.setheading(180 - self.heading())
            else:
                self.setheading(180 - self.heading())

        if self.xcor() - self.radius < -self.game.config_values['field_width']/2:
            self.setx(-self.game.config_values['field_width']/2 + self.radius)
            #Invert yxncrement
            if self.heading() <= 90:
                self.setheading(90 + self.heading())
            else:
                self.setheading(180 - self.heading())

        if self.ycor() + self.radius > self.game.config_values['field_height']/2:
            self.sety(self.game.config_values['field_height']/2 - self.radius)
            #Invert yIncrement
            if self.heading() <= 180:
                self.setheading(- self.heading())
            else:
                self.setheading(180 - self.heading())

        if self.ycor() - self.radius < -self.game.config_values['field_height']/2:
            self.sety(-self.game.config_values['field_height']/2 + self.radius)
            #Invert yIncrement
            if self.heading() > 180:
                self.setheading(- self.heading())
            else:
                self.setheading(180 - self.heading())

    def is_collision(self, other):
        """ Check for collision between self and given sprite <other> """
        if self.distance(other) <= (self.radius + other.radius):
            logging.debug(f'Collision of <{self._name}> with <{other._name}> detected!')
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
            x = random.randint(- int(self.game.config_values['field_width']) // 2, self.game.config_values['field_width'] // 2)
            y = random.randint(- int(self.game.config_values['field_height']) // 2, self.game.config_values['field_height'] // 2)
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

    _powerup_type = ''

    def __init__(self, game):
        Sprite.__init__(self, game, 'Player', 'triangle', 1, 'white', game.players_tracker)
        #self.shapesize(stretch_wid=0.3, stretch_len=0.4, outline=None)
        self.setpos(0,0)
        self.random_heading()
        self.speed = self.game.config_values['player_speed_default']
        self.lives = self.game.config_values['player_lives']
        self.missiles_shot = []
        self.max_missiles_number = 3 # Todo: make global?

    @property
    def powerup_type(self):
        return self._powerup_type

    @powerup_type.setter
    def powerup_type(self, input_powerup_type):
        if input_powerup_type != '': 
            #Start a timer
            pass
        self._powerup_type = input_powerup_type
        self.game.event_man.add_timed_event(self.remove_buff, 3)

    def apply_buff(self):
        #TODO: Implement buff mechanism (registering, stacking, etc.)
        pass

    def remove_buff(self, buff_id = None):
        #TODO: Remove buff
        logging.debug(f"POWER UP REMOVED (...not really)")

    @classmethod
    def spawn(cls, game):
        game.players_tracker.append(cls(game))
        return game.players_tracker[-1]

    def turn_left(self):
        self.lt(self.game.config_values['player_turn_rate'])

    def turn_right(self):
        self.rt(self.game.config_values['player_turn_rate'])

    def accelerate(self):
        self.speed += 1

    def decelerate(self):
        self.speed -= 1

    def fire(self):
        if self._powerup_type == '':      
            Missile.spawn(self.game, self)
        elif self._powerup_type == 'multi_shot':
            Missile.spawn(self.game, self, 10)
            Missile.spawn(self.game, self, 0)
            Missile.spawn(self.game, self, -10)


class Missile(Sprite):
    """ Missile Sprite """

    def __init__(self, game, shooter, change_heading = 0):
        Sprite.__init__(self, game, 'Missile', 'triangle', 0.5, 'yellow', shooter.missiles_shot)
        #self.shapesize(stretch_wid=0.3, stretch_len=0.4, outline=None)
        self.setpos(shooter.xpos, shooter.ypos)
        self.setheading(shooter.heading() + change_heading)
        self.speed = self.game.config_values['missile_speed']

    @classmethod
    def spawn(cls, game, shooter, change_heading = 0):
        if len(shooter.missiles_shot) < shooter.max_missiles_number:
            shooter.missiles_shot.append(Missile(game, shooter , change_heading))
            logging.debug('Missile fired - currently:{}/{} flying'.format(len(shooter.missiles_shot), shooter.max_missiles_number))
        else:
            logging.debug('All Missile already fired - currently:{}/{} flying'.format(len(shooter.missiles_shot), shooter.max_missiles_number))

    def move(self):
        ''' Check for borders and distroies missele, otherwise moves '''
        if self.xcor() < - self.game.config_values['field_width']/2 or self.xcor() > self.game.config_values['field_width']/2 or \
        self.ycor() < - self.game.config_values['field_height']/2 or self.ycor() > self.game.config_values['field_height']/2 :
            logging.debug('Missile collided with wall')
            Missile.despawn(self)
        else:
            self.fd(self.speed)

class Enemy(Sprite):
    """ Enemy sprite """

    def __init__(self, game):
        Sprite.__init__(self, game, 'Enemy', 'circle', 1, 'red', game.enemies_tracker)
        self.speed = self.game.config_values['enemy_speed']
        self.random_heading()
        self._value = 100
    
    @classmethod
    def spawn(cls, game, distance = 50):
        """ Spawns an object of type enemy """
        if len(game.enemies_tracker) < game.enemies_max_number:
            game.enemies_tracker.append(cls(game))
            game.enemies_tracker[-1].random_position(game.player, distance)
            logging.debug('Enemy spawned - currently:{}/{} existing'.format(len(game.enemies_tracker), game.enemies_max_number))
        else:
            logging.debug('Max number of enemies already existing - currently:{}/{} flying'.format(len(game.enemies_tracker), game.enemies_max_number))

    @property
    def value(self):
        return self._value


class Powerup(Sprite):
    """ Power Up sprite """

    _type = None
    _types = [
        'missile_speed',
        'multi_shot',
        'increment_missiles'
        ]

    def __init__(self, game, type):
        Sprite.__init__(self, game, 'Power Up', 'circle', 1, 'green', game.powerups_tracker)
        self.speed = 0
        if type in self._types:
            self._type = type
        else:
            logging.error('{} is not a valid type. Expected <{}>'.format(type, self._types))

    @property
    def type(self):
        return self._type

    @classmethod
    def spawn(cls, game, distance = 50):
        """ Spawns an object of type enemy """
        if len(game.powerups_tracker) < game.powerups_max_number:
            game.powerups_tracker.append(cls(game, 'multi_shot'))
            game.powerups_tracker[-1].random_position(game.player, distance)
            cls.set_despawn_timer(game)
            logging.debug(f'<Powerup>  spawned - currently:{len(game.powerups_tracker)}/{game.powerups_max_number} existing')
        else:
            logging.debug(f'Max number of <Powerups> ups already existing - currently:{len(game.powerups_tracker)}/{game.powerups_max_number}')

    @classmethod
    def set_despawn_timer(cls, game):
        lifetime = random.randint(game.config_values['powerup_min_lifetime'], game.config_values['powerup_max_lifetime'])
        game.event_man.add_timed_event(game.powerups_tracker[-1].despawn, lifetime)

