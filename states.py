import logging

class State(object):

    _transition_table = {}

    def __init__(self, game, name):
        """ Represents a simple implementation of a state within a FSM """
        self._game = game
        self._name = name
        self.PREP_START_MSG = f"""###################################################
                                  ### Starting preperation of state <{self.name}> ###
                                  ################################################### """
        self.PREP_FIN_MSG = f"+++ Preperation of state {self.name} completed +++"

    @property
    def name(self):
        """ Return the name of the state as string """
        return self._name

    @property
    def game(self):
        """" Return the game object where the state is instatiated """
        return self._game

    def transit(self, input):
        """ Transit to next state by evaluating the user input within the transition table of the current state"""
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
        logging.debug(self.PREP_START_MSG)
        self.game.menu.clear_screen()
        self.game.spawn_all_sprites()
        self.game.hide_sprites()
        self.game.menu.welcome_screen()
        logging.debug(self.PREP_FIN_MSG)

    def execution(self):
        self.game.wait_for_input()


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
        logging.debug(self.PREP_START_MSG)
        self.game.menu.clear_screen()
        self.game.draw_field()
        self.game.draw_score()
        self.game.show_sprites()
        logging.debug(self.PREP_FIN_MSG)

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
        logging.debug(self.PREP_START_MSG)
        self.game.menu.clear_screen()
        self.game.hide_sprites()
        self.game.menu.pause_screen()
        logging.debug(self.PREP_FIN_MSG)

    def execution(self):
        self.game.wait_for_input()


class Over(State):
    """ Game over Screen """
    
    _transition_table = {
        "custom": "self.game.score.reset_highscore()",
        "confirm": "self.game.set_state(self.game.welcoming)",
        "cancel": "self.game.set_state(self.game.exiting)"    
    }

    def __init__(self, game):
        State.__init__(self, game, 'over')
        
    def preperation(self):
        logging.debug(self.PREP_START_MSG)
        self.game.menu.clear_screen()
        self.game.despawn_all_sprites()
        self.game.menu.over_screen(self.game.score.current, self.game.score.highscore)
        self.game.score.save_highscore()
        self.game.score.reset_current()
        self.game._lives = self.game.config.values['player_lives']
        logging.debug(self.PREP_FIN_MSG)

    def execution(self):
        self.game.wait_for_input()

class Exit(State):
    """ Close turtle panel and exit the game application """
    
    _transition_table = {}

    def __init__(self, game):
        State.__init__(self, game, 'exiting')
        
    def preperation(self):
        logging.debug(self.PREP_START_MSG)
        self.game.menu.clear_screen()
        logging.debug(self.PREP_FIN_MSG)

    def execution(self):
        self.game.exit()