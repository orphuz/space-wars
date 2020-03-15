import unittest

from helpers.event_man import Event_man

class Test_Event_man(unittest.TestCase):
    def test_add_timed_event(self):
        t_time = 12
        def t_function():
            pass
        t_event_man = Event_man()
        t_event_man.add_timed_event(t_function, t_time)
        self.assertEqual(t_event_man._timed_events[-1]["event"], t_function)
        self.assertEqual(t_event_man._timed_events[-1]["time"], t_time)


if "__main__" == __name__:
    unittest.main()