import logging
import time

class Event_man():
    """
    Lorem Ipsum
    """

    def __init__(self):
        """ Initiate timer values und frame_drop_counter """
        self._timed_events = []

    def add_timed_event(self, event_function, trigger_time):
        """ Add a time based event provided as "event_function" that will be trigger when "event_time is reached """
        self._timed_events.append({"event": event_function, "time": trigger_time})
        logging.warning(f"New timed event added: {self._timed_events[-1]}")