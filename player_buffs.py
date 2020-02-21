import logging

class Buff(object):
    """
    This class represents a buff that is currently active for the player
    """
    def __init__(self, player):
        self.player = player
        self.type = None
        self.remaining_duration = 0
        self.stacks = 0
    
    def enable_effect(self, player):
        pass
    
    def disable_effect(self, player):
        pass