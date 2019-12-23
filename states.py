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

# class StateWelcome(SuperState):
#     def __init__(self):
#         """ Game State: Welcome screen """
#         self._transition_table = {
#             "start": "StateRunning",
#             "exit": "StateExit"
#         }
#
# class StateRunning(SuperState):
#     def __init__(self):
#         """ Game State: Game is running """
#         self._transition_table = {
#             "pause": "StatePause",
#             "over": "StateOver"
#         }
#
# class StatePause(SuperState):
#     def __init__(self):
#         """ Game State: Game Over """
#         self._transition_table = {
#             "menu": "StateWelcome",
#             "continue": "StateRunning",
#             "exit": "StateExit"
#         }
#
# class StateOver(SuperState):
#     def __init__(self):
#         """ Game State: Game Over """
#         self._transition_table = {
#             "menu": "StateWelcome",
#             "restart": "StateRunning",
#             "exit": "StateExit"
#         }
#
# class StateExit(SuperState):
#     def __init__(self):
#         """ Game State: Exiting the game """
#         self._transition_table = {}
