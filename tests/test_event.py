import unittest

from helpers.event import Event_man, Event

import time

class Test_01_Event_man(unittest.TestCase):

    def setUp(self):
        """ Intitate an instance of class 'Event_man' before every test execution"""
        self.t_event_man = Event_man()
        def t_function(self):
            print('this is a test function')
        self.t_function = t_function
        self.creation_time = time.time()
        self.t_duration = 12
        #self.t_event = Event(self.t_function, self.t_duration)

    def tearDown(self):
        """ Delete the instance of class 'Event_man' after  every test execution"""
        del self.t_event_man

    def test_01_add_timed_event(self):
        t_duration = 12
        def t_function():
            pass  
        self.t_event_man.add_timed_event(t_function, t_duration)
        trigger_time = time.time() + float(t_duration)
        self.assertEqual(self.t_event_man._timed_events[-1].function, t_function)
        self.assertAlmostEqual(self.t_event_man._timed_events[-1].trigger_time, trigger_time, places = 2)

    def test_02_delete_event(self):
        """ Check if event object provided as agrument is deleted """
        self.t_event_man.add_timed_event(self.t_function, self.t_duration)
        event_to_delete = self.t_event_man._timed_events[-1]
        self.t_event_man.delete_event(event_to_delete)
        current_event_ids = []
        for event in self.t_event_man._timed_events:
            current_event_ids.append(event.id)
        self.assertNotIn(event_to_delete.id, current_event_ids)

    def test_03_delete_event_by_id(self):
        """ Check if event object provided by ID is deleted """    
        id_of_event_to_delete = self.t_event_man.add_timed_event(self.t_function, self.t_duration)
        self.t_event_man.delete_event_by_id(id_of_event_to_delete)
        current_event_ids = []
        for event in self.t_event_man._timed_events:
            current_event_ids.append(event.id)
        self.assertNotIn(id_of_event_to_delete, current_event_ids)

class Test_02_Event(unittest.TestCase):

    def setUp(self):
        """ Intitate an instance of class 'Event_man' before every test execution"""
        def t_function(self):
            print('this is a test function')
        self.t_function = t_function
        self.creation_time = time.time()
        self.t_duration = 12
        self.t_event = Event(self.t_function, self.t_duration)

    def tearDown(self):
        """ Delete the instance of class <Event> after every test execution"""
        del self.t_event

    def test_01_get_trigger_time(self):
        """ Check if trigger time for event is calculated correctly based on duration provided """
        t_tirgger_time = self.t_duration + time.time()
        self.assertAlmostEqual(t_tirgger_time, self.t_event.get_trigger_time(self.t_duration), places = 2)

    def test_02_get_trigger_time_with_invalid_type(self):
        """ Check if invalid type <str> for argument duration rasies a <TypeError> """
        t_wrong_type_duration = 'thisIsnotANumberButAString'
        with self.assertRaises(TypeError):
            self.t_event.get_trigger_time(t_wrong_type_duration)
    
    def test_03_get_trigger_time_with_invalid_value_nagative(self):
        """ Check if negative value for argument duration rasies a <ValueError> """
        t_negative_duration = -12
        with self.assertRaises(ValueError):
            self.t_event.get_trigger_time(t_negative_duration)

    def test_04_get_trigger_time_with_invalid_value_zero(self):
        """ Check if a duration of <0> rasies a <ValueError> """
        t_zero_duration = 0
        with self.assertRaises(ValueError):
            self.t_event.get_trigger_time(t_zero_duration)

if "__main__" == __name__:
    unittest.main()