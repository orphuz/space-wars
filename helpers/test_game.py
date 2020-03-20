import unittest

from game import Game


class Test_01_Game_States(unittest.TestCase):
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


class Test_02_Game_Inputs(unittest.TestCase):
    """ 
    Check all possible reactions to user input while the game is running
    """

    def setUp(self):
        """
        Inistanciate an instance of the game,
        start running the main loop in test mode (only one iteration) and
        transit to game state <running>
        before every test execution
        """
        self.game = Game("Test Space Wars")
        self.game.main_loop(testmode = True)
        self.game.player_input("confirm")
        self.game.main_loop(testmode = True)

    def tearDown(self):
        """ Delete the game instance after every test execution"""
        self.game.set_state(self.game.exiting)

    def test_01_player_turn_left(self):
        """ Check if player sprite heading direction is changed corretly on input <turn_left> """
        previous_direction = self.game.player.heading()
        self.game.player_input("left")
        self.game.main_loop(testmode = True)
        new_direction = previous_direction + self.game.config_values["player_turn_rate"]
        self.assertEqual(self.game.player.heading(), new_direction )

    def test_02_player_turn_right(self):
        """ Check if player sprite heading direction is changed corretly on input <turn_right>  """
        previous_direction = self.game.player.heading()
        self.game.player_input("right")
        self.game.main_loop(testmode = True)
        new_direction = previous_direction - self.game.config_values["player_turn_rate"]
        self.assertEqual(self.game.player.heading(), new_direction )

    def test_03_player_accelerate(self):
        """ Check if player speed is accelerated on input <up>  """
        previous_speed = self.game.player.speed
        self.game.player_input("up")
        self.game.main_loop(testmode = True)
        expected_new_speed = previous_speed + 1
        self.assertEqual(self.game.player.speed, expected_new_speed)

    def test_04_player_decelerate(self):
        """ Check if player speed is decelerated on input <down>  """
        previous_speed = self.game.player.speed
        self.game.player_input("down")
        self.game.main_loop(testmode = True)
        expected_new_speed = previous_speed - 1
        self.assertEqual(self.game.player.speed, expected_new_speed)
    
    def test_05_player_fire(self):
        """
        Check if a missile is corrctly fired on input <fire> by ensuring:
        - Number of active missiles is increased by 1
        - New object of type "Missile" is spawned
        - Missile shot has same direciton as player
        """
        from sprites import Missile
        previous_number_of_missiles = len(self.game.player.missiles_shot)
        self.game.player_input("fire")
        self.game.main_loop(testmode = True)
        current_number_of_missiles = len(self.game.player.missiles_shot)
        self.assertEqual(current_number_of_missiles, previous_number_of_missiles + 1)
        self.assertIsInstance(self.game.player.missiles_shot[-1], Missile) 
        self.assertEqual(self.game.player.missiles_shot[-1].heading(), self.game.player.heading())
    
    def test_06_custom_action(self):
        """
        Check if custom action is triggered correctly on user input <custop>
        Current custom action: Randomly spawn a power up
        - Number of active powerups is increased by 1
        - New object of type <Power-up> is spawned
        """
        from sprites import Powerup
        previous_number_of_powerups = len(self.game.powerups_tracker)
        self.game.player_input("custom")
        self.game.main_loop(testmode = True)
        current_number_of_powerups = len(self.game.powerups_tracker)
        self.assertEqual(current_number_of_powerups, previous_number_of_powerups + 1)
        self.assertIsInstance(self.game.powerups_tracker[-1], Powerup)          