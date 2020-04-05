import logging

from functools import partial


class Buffs():
    def __init__(self, target, powerup_types):
        self.target = target
        self.stack = []
        self.powerup_types = powerup_types

        self.target.missle_speed = self.target.game.config.values['missile_speed']
        self.counter_icrementmissiles = 0      
        self.counter_multishot = 0

        self.target.max_missiles_number =  (self.counter_multishot + 1) * (self.counter_icrementmissiles + 1)

    def apply(self, buff):
        #TODO: Implement buff mechanism based on power up collectible provided as argugment <buff> (registering, stacking, etc.)
        if buff.type in self.powerup_types:
            self.stack.append(buff)
            logging.debug(f"Buff <{buff.type}> added")
            if buff.duration > 0:
                self.target.game.event_man.add_timed_event(partial(self.remove, buff), buff.duration, description = f"Remove debuff effect <{buff.type}>")
        else:
            logging.error(f"Unknown buff type <{buff.type}>")
        self.update_effects()

    def remove(self, buff = None):
        #TODO: Remove buff
        if buff == None:
            raise ValueError(f"object to remove must be an istance of class <Powerup>")
        self.stack.remove(buff)
        self.update_effects()
        logging.debug(f"Buff <{buff.type}> removed")

    def update_effects(self):
        """ Counts and stores the number of active buffs of each type """
        self.reset_counters()
        buffs = self.stack
        for buff in buffs:
            if buff.type == self.powerup_types[0]: self.counter_missilespeed += 1
            if buff.type == self.powerup_types[1]: self.counter_multishot += 1
            if buff.type == self.powerup_types[2]: self.counter_icrementmissiles += 1

        self.target.max_missiles_number = self.burst_size * self.max_bursts
        self.target.missle_speed = self.target.game.config.values['missile_speed'] * (self.counter_missilespeed * 0.5 + 1)

    def reset_counters(self):
        """ Resets the number of active buffs of each type to <0> """
        self.counter_missilespeed = 0
        self.counter_multishot = 0
        self.counter_icrementmissiles = 0

    @property
    def burst_size(self):
        return ((self.counter_multishot + 1) * 2) + -1
    
    @property
    def max_bursts(self):
        return self.counter_icrementmissiles + 1   
