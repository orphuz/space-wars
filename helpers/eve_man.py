import logging
import time

class Event_man():
    """
    Store and manage scheduled events. If the target time reached the related function is called and the event itself is deleted
    """

    def __init__(self):
        """ Initiate empty list of events """
        self._timed_events = []

    def add_timed_event(self, event_function, duration):
        """ Add a time based event provided as "event_function" that will be triggered after "duration" is expired """
        self._timed_events.append({"event": event_function, "trigger_time": self.get_trigger_time(duration)})
        logging.debug(f"New timed event with duration of {duration}s added: {self._timed_events[-1]['event'].__class__}.{self._timed_events[-1]['event'].__name__}")

    def get_trigger_time(self, duration):
        """ Calculate the target trigger time based on the given duration """
        trigger_time = time.time() + float(duration)
        return trigger_time

    def check_events(self):
        """ Execute stored event function if corresponting "trigger_time" is reached / exceeded """
        current_time = time.time()
        executed_events = []

        for event in self._timed_events:
            # Execute all events and register them as executed
            if event["trigger_time"] <= current_time:
                event["event"]()
                executed_events.append(event)
                logging.debug(f"Timed event triggered, scheduled time was{time.ctime(event['trigger_time'])}")

        for executed_event in executed_events:
            # Remove all executed events from the event register
            self._timed_events.remove(executed_event)

    def delete_event(self, event):
        """ Delete scheduled event provied as argument "event-object" from the register """
        if event in self._timed_events:
            self._timed_events.remove(event)
            logging.debug(f"Event {event} removed from from list of scheduled events")
        else:
            logging.error(f"Event {event} not in list of scheduled events")