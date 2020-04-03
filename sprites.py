import random
import math
import turtle
import logging

from functools import partial

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
        self.linked_events = []
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
            for event_id in self.linked_events:
                if event_id in self.game.event_man.event_ids: self.game.event_man.delete_event_by_id(event_id)
            self.object_tracker.remove(self)
            logging.debug(f'Instance of {self.__class__} despawned - currently:{len(self.object_tracker)} existing')
            #del self
        except ValueError as valerr:
            logging.error(f'{valerr} - Cannot despawn {self} as it is not a member of {self.object_tracker}')

    def move(self):
        """ 
        Sprite movement per frame:
        - move sprite in <heading> direction by amount of <speed>
        - check for boundary collision
        - change postion and heading if necessary
        """
        self.fd(self.speed)
        
        if self.collision_with_boundary():
            self.reaction_to_boundary_collision()

    def collision_with_boundary(self):
        """ Check for collision of the sprite with a boundary defined by field_width and field_height """
        if self.xcor() < - self.game.config.values['field_width']/2 or self.xcor() > self.game.config.values['field_width']/2 or \
        self.ycor() < - self.game.config.values['field_height']/2 or self.ycor() > self.game.config.values['field_height']/2 :
            logging.debug(f'Collision of <{self._name}> with <boundary> detected!')
            return True
        else:
            False
    
    def reaction_to_boundary_collision(self):
        """ Set default reaction of sprites to bounce off the boundary """
        self.bounce_off_boundary()

    def bounce_off_boundary(self):
        """ Calculate new postion and heading of the sprite when bouncing off a boundary """
        if self.xcor() + self.radius > self.game.config.values['field_width']/2:
            self.setx(self.game.config.values['field_width']/2 - self.radius)
            #Invert xIncrement
            if self.heading() <= 90:
                self.setheading(180 - self.heading())
            else:
                self.setheading(180 - self.heading())

        if self.xcor() - self.radius < -self.game.config.values['field_width']/2:
            self.setx(-self.game.config.values['field_width']/2 + self.radius)
            #Invert yxncrement
            if self.heading() <= 90:
                self.setheading(90 + self.heading())
            else:
                self.setheading(180 - self.heading())

        if self.ycor() + self.radius > self.game.config.values['field_height']/2:
            self.sety(self.game.config.values['field_height']/2 - self.radius)
            #Invert yIncrement
            if self.heading() <= 180:
                self.setheading(- self.heading())
            else:
                self.setheading(180 - self.heading())

        if self.ycor() - self.radius < -self.game.config.values['field_height']/2:
            self.sety(-self.game.config.values['field_height']/2 + self.radius)
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
            x = random.randint(- int(self.game.config.values['field_width']) // 2, self.game.config.values['field_width'] // 2)
            y = random.randint(- int(self.game.config.values['field_height']) // 2, self.game.config.values['field_height'] // 2)
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
        self.speed = self.game.config.values['player_speed_default']
        self.lives = self.game.config.values['player_lives']
        self.missiles_shot = []
        self.max_missiles_number = 3 # Todo: make global?
        
        self.buffs = []

        self.counter_multishot = 0

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

    def apply_buff(self, buff):
        #TODO: Implement buff mechanism (registering, stacking, etc.)
        if buff.type in Powerup._types:
            self.buffs.append(buff)
            logging.debug(f"Buff <{buff.type}> added")
            if buff.duration > 0:
                self.game.event_man.add_timed_event(partial(self.remove_buff, buff), buff.duration, description = f"Remove debuff effect <{buff.type}>")
        else:
            logging.error(f"Unknown buff type <{buff.type}>")
        self.update_buff_effect()

    def remove_buff(self, buff = None):
        #TODO: Remove buff
        if buff == None:
            raise ValueError(f"object to remove must be an istance of class <Powerup>")
        self.buffs.remove(buff)
        self.update_buff_effect()
        logging.debug(f"Buff <{buff.type}> removed")

    def update_buff_effect(self):
        """ Counts and stores the number of active buffs of each type """
        self.reset_counter()
        buffs = self.buffs
        for buff in buffs:
            if buff.type == Powerup._types[0]: self.counter_missilespeed += 1
            if buff.type == Powerup._types[1]: self.counter_multishot += 1
            if buff.type == Powerup._types[2]: self.counter_icrementmissiles += 1

    def reset_counter(self):
        """ Resets the number of active buffs of each type to <0> """
        self.counter_missilespeed = 0
        self.counter_multishot = 0
        self.counter_icrementmissiles = 0          

    @classmethod
    def spawn(cls, game):
        game.players_tracker.append(cls(game))
        return game.players_tracker[-1]

    def turn_left(self):
        self.lt(self.game.config.values['player_turn_rate'])

    def turn_right(self):
        self.rt(self.game.config.values['player_turn_rate'])

    def accelerate(self):
        self.speed += 1

    def decelerate(self):
        self.speed -= 1

    def fire(self):
        """ Fire missles modified by current active buffs """
        if self.counter_multishot > 0:
            Missile.spawn(self.game, self, 10)
            Missile.spawn(self.game, self, 0)
            Missile.spawn(self.game, self, -10)
        else:      
            Missile.spawn(self.game, self)


class Missile(Sprite):
    """ Missile Sprite """

    def __init__(self, game, shooter, change_heading = 0):
        Sprite.__init__(self, game, 'Missile', 'triangle', 0.5, 'yellow', shooter.missiles_shot)
        #self.shapesize(stretch_wid=0.3, stretch_len=0.4, outline=None)
        self.setpos(shooter.xpos, shooter.ypos)
        self.setheading(shooter.heading() + change_heading)
        self.speed = self.game.config.values['missile_speed']

    @classmethod
    def spawn(cls, game, shooter, change_heading = 0):
        """ Spawn a missile on the position of the player with head based in the players direction """
        if len(shooter.missiles_shot) < shooter.max_missiles_number:
            shooter.missiles_shot.append(Missile(game, shooter , change_heading))
            logging.debug('Missile fired - currently:{}/{} flying'.format(len(shooter.missiles_shot), shooter.max_missiles_number))
        else:
            logging.debug('All Missile already fired - currently:{}/{} flying'.format(len(shooter.missiles_shot), shooter.max_missiles_number))

    def reaction_to_boundary_collision(self):
        """ Set the reaction on boundary collision to <despawn()>, default is bouncing_off_boundary """
        Missile.despawn(self)

class Enemy(Sprite):
    """ Enemy sprite """

    def __init__(self, game):
        Sprite.__init__(self, game, 'Enemy', 'circle', 1, 'red', game.enemies_tracker)
        self.speed = self.game.config.values['enemy_speed']
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

    def __init__(self, game, type, duration = 3):
        Sprite.__init__(self, game, 'Power Up', 'circle', 1, 'green', game.powerups_tracker)
        self.speed = 0
        if type in self._types:
            self._type = type
            self.duration = duration
        else:
            logging.error('{} is not a valid type. Expected <{}>'.format(type, self._types))

    @property
    def type(self):
        return self._type

    @classmethod
    def spawn(cls, game, distance = 50):
        """ Spawns an object of type enemy """
        if len(game.powerups_tracker) < game.powerups_max_number:          
            new_powerup = cls(game, 'multi_shot')
            game.powerups_tracker.append(new_powerup)
            new_powerup.random_position(game.player, distance)
            new_powerup.set_despawn_timer()
            logging.debug(f'<Powerup>  spawned - currently:{len(game.powerups_tracker)}/{game.powerups_max_number} existing')
        else:
            logging.debug(f'Max number of <Powerups> ups already existing - currently:{len(game.powerups_tracker)}/{game.powerups_max_number}')

    def set_despawn_timer(self):
        """ Set despawn time a event in eve_man and store the events id in the sprites list of linked events """
        lifetime = random.randint(self.game.config.values['powerup_min_lifetime'], self.game.config.values['powerup_max_lifetime'])
        despawn_event_id = self.game.event_man.add_timed_event(self.despawn, lifetime, description = "Despawn power up after its lifetime is expired")
        self.linked_events.append(despawn_event_id)
