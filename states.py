import logging

class State():
    def __init__(self, name, transition_table):
        """ Represents a simple implementation of a FSM """
        self._name = name
        self._transition_table = transition_table

    def transit(self, input):
        if input in self._transition_table:
            logging.debug('Transition to {}'.format(self._transition_table[input]))
            return (self._transition_table[input])
        else:
            logging.warn('{} is not a valid option in state <{}>'.format(input, self.name))
            return self

    @property
    def name(self):
        return self._name
