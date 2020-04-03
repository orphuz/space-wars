import logging
import time
import types
import functools

class Event_man():
    """
    Store and manage scheduled events. If the target time reached the related function is called and the event itself is deleted
    """

    def __init__(self):
        """ Initiate empty list of events """
        self._timed_events = []

    @property
    def events(self):
        return self._timed_events

    @property
    def event_ids(self):
        event_ids = []
        for event in self.events:
            event_ids.append(event.id)
        return event_ids

    def add_timed_event(self, event_function, duration, description = None):
        """ Create an object of type Event based on provided args and add it to the list of timed events """
        new_event = Event(event_function, duration, description)
        self._timed_events.append(new_event)
        logging.debug(f"New timed event with <{new_event.id}> for trigger time <{new_event.trigger_time}> added")
        return new_event.id

    def check_events(self):
        """ Execute stored event function if corresponting "trigger_time" is reached / exceeded """
        current_time = time.time()

        events = self._timed_events
        for event in events:
            # Execute and delete all due events
            if event.trigger_time <= current_time:
                event.execute()
                logging.debug(f"Timed event triggered, scheduled time was{time.ctime(event.trigger_time)}")
                if event in self._timed_events: self.delete_event(event)

    def delete_event(self, event):
        """ Delete scheduled event provied as argument "event" from the list of timed events """
        events = self._timed_events
        if event in events:
            self._timed_events.remove(event)
            logging.debug(f"Event {event.id} removed from from list of scheduled events")
        else:
            logging.error(f"Event {event.id} not in list of scheduled events")

    def delete_event_by_id(self, event_id):
        """ Delete scheduled event with provided id from the list of timed events """
        event_ids = self.event_ids
        if event_id in event_ids:
            events = self._timed_events
            for event in events:
                if event.id == event_id:
                    self._timed_events.remove(event)
                    logging.debug(f"Event <{event.id}> removed from from list of scheduled events")
        else:
            logging.error(f"Event <{event.id}> not in list of scheduled events")


class Event():
    """
    Event class to hold seperate data for each event
    """

    def __init__(self, function, duration, description = None):
        """ Store all relevant data including the function to execute after proper type checking """
        if isinstance(function, types.MethodType) or isinstance(function, types.FunctionType) or isinstance(function, functools.partial):
            self.function = function
        else:
            raise TypeError(f'Provided argument for <function> must be a of type method or function but is <{type(function)}')

        if isinstance(duration, int):
            self.duration = duration
            self.trigger_time = self.get_trigger_time(duration)
        else:
            raise TypeError('Provided argument for <function> must be a of type function')

        self.description = None
        if description != None:
            if isinstance(description, str):
                self.description = description
            else:
                raise TypeError('Provided argument for <description> must be a string')

        self.id = id(self)

        if description != None:
            logging.debug(f"Event {self.id} created: {self.description}")
        else:
            logging.debug(f"Event {self.id} created")

    def get_trigger_time(self, duration):
            """ Calculate the target trigger time based on the given duration """
            try:
                if duration > 0:
                    trigger_time = time.time() + float(duration)
                    return trigger_time
                else:
                    raise ValueError(f"Argument 'duration' must be a number greater 0")
            except TypeError as tyerr:
                raise TypeError(f"{tyerr} - Arugment 'duration' must be a number")

    def execute(self):
        logging.debug(f"Executing event <{self.id}> - Description: '{self.description}'")
        self.function()
