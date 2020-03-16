import unittest

from helpers.eve_man import Event_man

import time

class Test_Event_man(unittest.TestCase):

    def setUp(self):
        """ Intitate an instance of class 'Event_man' before every test execution"""
        self.t_event_man = Event_man()

    def tearDown(self):
        """ Delete the instance of class 'Event_man' after  every test execution"""
        del self.t_event_man

    def test_add_timed_event(self):
        t_duration = 12
        def t_function():
            pass
        self.t_event_man.add_timed_event(t_function, t_duration)
        self.assertEqual(self.t_event_man._timed_events[-1]["event"], t_function)
        self.assertAlmostEqual(self.t_event_man._timed_events[-1]["trigger_time"], self.t_event_man.get_trigger_time(t_duration), places = 4,)

    def test_get_trigger_time(self):
        t_duration = 12
        t_tirgger_time = t_duration + time.time()
        self.assertAlmostEqual(t_tirgger_time, self.t_event_man.get_trigger_time(t_duration))
    
    def test_get_trigger_time_with_invalid_type(self):
        t_wrong_type_duration = 'thisIsnotANumberButAString'
        with self.assertRaises(TypeError):
            self.t_event_man.get_trigger_time(t_wrong_type_duration)
    
    def test_get_trigger_time_with_invalid_value_nagative(self):
        t_negative_duration = -12
        with self.assertRaises(ValueError):
            self.t_event_man.get_trigger_time(t_negative_duration)

    def test_get_trigger_time_with_invalid_value_zero(self):
        t_zero_duration = 0
        with self.assertRaises(ValueError):
            self.t_event_man.get_trigger_time(t_zero_duration)

if "__main__" == __name__:
    unittest.main()