import logging

class State(object):

    _transition_table = {}

    def __init__(self, game, name):
        """ Represents a simple implementation of a FSM """
        self._game = game
        self._name = name
        pass

    @property
    def name(self):
        return self._name

    @property
    def game(self):
        return self._game

    def transit(self, input):
        if input in self._transition_table:
            logging.debug('Transition to {}'.format(self._transition_table[input]))
            eval(self._transition_table[input])
        else:
            logging.info('{} is not a valid option in state <{}>{}'.format(input, self.name, self.__class__))
            return self

class Welcoming(State):
    """ Welcome screen aka Intro """

    _transition_table = {
        "confirm": "self.game.set_state(self.game.running)",
        "cancel": "self.game.set_state(self.game.exiting)"    
    }

    def __init__(self, game):
        State.__init__(self, game, 'welcoming')

    def __call__(self):
        self.preperation()
       
    def preperation(self):
        self.game.spawn_all_sprites()
        self.game.hide_sprites()
        self.game.draw_welcome()
        # self.execution()

    def execution(self):
        self.game.wait_for_input(self)


class Running(State):
    """ Draw all game elements and run main game loop """
    
    _transition_table = {
        "left": "self.game.player.turn_left()",
        "right": "self.game.player.turn_right()",
        "up": "self.game.player.accelerate()",
        "down": "self.game.player.decelerate()",
        "fire": "self.game.player.fire()",
        "cancel": "self.game.set_state(self.game.paused)",
        "player_death": "self.game.set_state(self.game.over)",
        "custom": "self.game.custom_action()"
    }

    def __init__(self, game):
        State.__init__(self, game, 'running')
        
    def preperation(self):
        self.game.draw_field()
        self.game.draw_score()
        self.game.show_sprites()
        logging.debug('Preperation of state {} completed'.format(self.name))
        # self.execution()

    def execution(self):
        self.game.event_man.check_events()
        self.game.calculate_next_frame()
        self.game.draw_new_score()

class Paused(State):
    """ Paused Screen """
    
    _transition_table = {
        "confirm": "self.game.set_state(self.game.running)",
        "cancel": "self.game.set_state(self.game.over)"    
    }

    def __init__(self, game):
        State.__init__(self, game, 'paused')
        
    def preperation(self):
        self.game.hide_sprites()
        self.game.draw_pause()
        # self.execution()

    def execution(self):
        self.game.wait_for_input(self)


class Over(State):
    """ Game over Screen """
    
    _transition_table = {
        "custom": "self.game.reset_highscore()",
        "confirm": "self.game.set_state(self.game.welcoming)",
        "cancel": "self.game.set_state(self.game.exiting)"    
    }

    def __init__(self, game):
        State.__init__(self, game, 'over')
        
    def preperation(self):
        self.game.despawn_all_sprites()
        self.game.draw_over()
        self.game._score = 0
        self.game._lives = self.game.config_values['player_lives']
        # self.execution()

    def execution(self):
        self.game.wait_for_input(self)

class Exit(State):
    """ Close turtle panel and exit the game application """
    
    _transition_table = {}

    def __init__(self, game):
        State.__init__(self, game, 'exiting')
        
    def preperation(self):
        # self.execution()
        pass

    def execution(self):
        self.game.exit()