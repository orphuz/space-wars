import unittest

from game import Game


class Test_Game_States(unittest.TestCase):
    """ 
    Check all possible game states and transitons based on user input
    """

    def setUp(self):
        """
        Inistanciate an instance of the game and 
        start running the main loop in test mode (only one iteration)
        before every test execution
        """
        self.game = Game("Test Space Wars")
        self.game.main_loop(testmode = True)

    def tearDown(self):
        """ Delete the game instance after every test execution"""
        self.game.set_state(self.game.exiting)

    def test_01_start_in_welcoming(self):
        """ Check if game starts up in to state <welconing> """
        self.assertEqual(self.game.state, self.game.welcoming)

    def test_02_transition_welcoming_to_running(self):
        """ Check game state transition from <welconing> to <running> on user input <confirm> """
        self.test_01_start_in_welcoming()
        self.game.player_input("confirm")
        self.game.main_loop(testmode = True)
        self.assertEqual(self.game.state, self.game.running)
    
    def test_03_transition_running_to_pause(self):
        """ Check game state transition from <running> to <paused> on user input <cancel> """
        self.test_02_transition_welcoming_to_running()
        self.game.player_input("cancel")
        self.game.main_loop(testmode = True)
        self.assertEqual(self.game.state, self.game.paused)

    def test_04_transition_paused_to_running(self):
        """ Check game state transition from <paused> to <running> on user input <confirm> """
        self.test_03_transition_running_to_pause()
        self.game.player_input("confirm")
        self.game.main_loop(testmode = True)
        self.assertEqual(self.game.state, self.game.running)

    def test_05_transition_paused_to_over(self):
        """ Check game state transition from <paused> to <over> on user input <cancel> """
        self.test_03_transition_running_to_pause()
        self.game.player_input("cancel")
        self.game.main_loop(testmode = True)
        self.assertEqual(self.game.state, self.game.over)
    
    def test_06_transition_over_to_welcoming(self):
        """ Check game state transition from <over> to <welcoming> on user input <confirm> """
        self.test_05_transition_paused_to_over()
        self.game.player_input("confirm")
        self.game.main_loop(testmode = True)
        self.assertEqual(self.game.state, self.game.welcoming)

    def test_07_transition_over_to_reset_score(self):
        """ Check game state transition from <over> to <over> while reseting the high score on user input <custom> """
        self.test_05_transition_paused_to_over()
        self.game.player_input("custom")
        self.game.main_loop(testmode = True)
        self.assertEqual(self.game.state, self.game.over)
        self.assertEqual(self.game.score.highscore, 0)

    def test_08_menu_transition_to_exiting(self):
        """ Check that game is exited after state transition from <over> to <exiting> on user input <cancel> """
        self.test_05_transition_paused_to_over()
        self.game.player_input("cancel")      
        with self.assertRaises(SystemExit):
            self.game.main_loop(testmode = True)
        