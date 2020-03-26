import unittest

from math import sin, cos, radians

from game import Game


class Test_01_Game_State_Transitions(unittest.TestCase):
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
        del self.game

    def test_01_start_in_welcoming(self):
        """ Check if game starts up in to state <welconing> """
        self.assertEqual(self.game.state, self.game.welcoming)

    def test_02_transition_from_welcoming_to_running(self):
        """ Check game state transition from <welconing> to <running> on user input <confirm> """
        self.test_01_start_in_welcoming()
        self.game.player_input("confirm")
        self.game.main_loop(testmode = True)
        self.assertEqual(self.game.state, self.game.running)
    
    def test_03_transition_from_running_to_pause(self):
        """ Check game state transition from <running> to <paused> on user input <cancel> """
        self.test_02_transition_from_welcoming_to_running()
        self.game.player_input("cancel")
        self.game.main_loop(testmode = True)
        self.assertEqual(self.game.state, self.game.paused)

    def test_04_transition_from_paused_to_running(self):
        """ Check game state transition from <paused> to <running> on user input <confirm> """
        self.test_03_transition_from_running_to_pause()
        self.game.player_input("confirm")
        self.game.main_loop(testmode = True)
        self.assertEqual(self.game.state, self.game.running)

    def test_05_transition_from_paused_to_over(self):
        """ Check game state transition from <paused> to <over> on user input <cancel> """
        self.test_03_transition_from_running_to_pause()
        self.game.player_input("cancel")
        self.game.main_loop(testmode = True)
        self.assertEqual(self.game.state, self.game.over)
    
    def test_06_transition_from_over_to_welcoming(self):
        """ Check game state transition from <over> to <welcoming> on user input <confirm> """
        self.test_05_transition_from_paused_to_over()
        self.game.player_input("confirm")
        self.game.main_loop(testmode = True)
        self.assertEqual(self.game.state, self.game.welcoming)

    def test_07_transition_from_over_to_reset_score(self):
        """ Check game state transition from <over> to <over> while reseting the high score on user input <custom> """
        self.test_05_transition_from_paused_to_over()
        self.game.player_input("custom")
        self.game.main_loop(testmode = True)
        self.assertEqual(self.game.state, self.game.over)
        self.assertEqual(self.game.score.highscore, 0)

    def test_08_transition_from_over_to_exiting(self):
        """ Check that game is exited after state transition from <over> to <exiting> on user input <cancel> """
        self.test_05_transition_from_paused_to_over()
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
        del self.game

    def test_01_player_turn_left(self):
        """ Check if player sprite heading direction is changed corretly on input <turn_left> """
        previous_direction = self.game.player.heading()
        self.game.player_input("left")
        self.game.main_loop(testmode = True)
        new_direction = previous_direction + self.game.config_values["player_turn_rate"]
        if new_direction >= 360: new_direction -= 360
        self.assertEqual(self.game.player.heading(), new_direction )

    def test_02_player_turn_right(self):
        """ Check if player sprite heading direction is changed corretly on input <turn_right>  """
        previous_direction = self.game.player.heading()
        self.game.player_input("right")
        self.game.main_loop(testmode = True)
        new_direction = previous_direction - self.game.config_values["player_turn_rate"]
        if new_direction < 0: new_direction += 360
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
        Check if custom action is triggered correctly on user input <custom>
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

class Test_03_Game_Sprite_Collisions(unittest.TestCase):
    """ 
    Check all possible reactions to collisions of sprites while the game is running
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
        del self.game

    def test_01_collision_of_player_with_enemy_lose_life(self):
        """
        Check if a life is lost when the <player> collides with an <enemy> sprite
        """
        previous_lives = self.game._lives = 2
        self.game.enemies_tracker[-1].setpos(self.game.player.xpos, self.game.player.ypos)
        self.game.main_loop(testmode = True)
        self.assertEqual(self.game._lives, previous_lives - 1)
    
    def test_02_collision_of_player_with_enemy_despawn_enemy(self):
        """
        Check if the <enemy> is despawend when the <player> collides with the <enemy> sprite
        """
        colliding_enemy_id = id(self.game.enemies_tracker[-1])
        self.game.enemies_tracker[-1].setpos(self.game.player.xpos, self.game.player.ypos)
        self.game.main_loop(testmode = True)
        current_enemy_ids = []
        for enemy in self.game.enemies_tracker:
            current_enemy_ids.append(id(enemy))
        self.assertNotIn(colliding_enemy_id, current_enemy_ids)
    
    def test_03_collision_of_player_with_powerup_despawn_powerup(self):
        """
        Check if the <powerup> is despawend when the <player> collides with it's sprite
        """
        from sprites import Powerup
        Powerup.spawn(self.game)
        colliding_powerup_id = id(self.game.powerups_tracker[-1])
        self.game.powerups_tracker[-1].setpos(self.game.player.xpos, self.game.player.ypos)
        self.game.main_loop(testmode = True)
        current_powerup_ids = []
        for powerup in self.game.enemies_tracker:
            current_powerup_ids.append(id(powerup))
        self.assertNotIn(colliding_powerup_id, current_powerup_ids)
    
    def test_04_collision_of_bullet_with_enemy_despawn_enemy(self):
        """
        Check if the <enemy> is despawend when the <missile> collides with it's sprite
        """
        self.game.player_input("fire")
        self.game.main_loop(testmode = True)
        colliding_enemy = self.game.enemies_tracker[-1]
        colliding_missile = self.game.player.missiles_shot[-1]
        colliding_enemy.setpos(colliding_missile.xpos, colliding_missile.ypos)
        self.game.main_loop(testmode = True)
        current_enemy_ids = []
        for enemy in self.game.enemies_tracker:
            current_enemy_ids.append(id(enemy))
        self.assertNotIn(id(colliding_enemy), current_enemy_ids)
    
    def test_05_collision_of_bullet_with_enemy_despawn_bullet(self):
        """
        Check if the <enemy> is despawend when the <missile> collides with it's sprite
        """
        self.game.player_input("fire")
        self.game.main_loop(testmode = True)
        colliding_enemy = self.game.enemies_tracker[-1]
        colliding_missile = self.game.player.missiles_shot[-1]
        colliding_enemy.setpos(colliding_missile.xpos, colliding_missile.ypos)
        self.game.main_loop(testmode = True)
        current_missiles_ids = []
        for missile in self.game.player.missiles_shot:
            current_missiles_ids.append(id(missile))
        self.assertNotIn(id(colliding_missile), current_missiles_ids)


class Test_04_Game_Boundary_Collisions(unittest.TestCase):
    """ 
    Check all possible reactions to collisions of boundaries while the game is running
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
        del self.game


    def check_bounce_on_right_boundary(self, sprite):
        """ 
        Check correct bouncing on <right> boundary:
        - on collision the sprite's heading direction is inverted in the <x> component
        """
        sprite.setheading(30)
        old_heading = sprite.heading()
        old_x_comp = cos(radians(old_heading))
        old_y_comp = sin(radians(old_heading))
        sprite.setpos(self.game.config_values['field_width'] /2, 0)
        self.game.main_loop(testmode = True)
        x_comp = cos(radians(sprite.heading()))
        y_comp = sin(radians(sprite.heading()))
        self.assertAlmostEqual(x_comp, - old_x_comp )
        self.assertAlmostEqual(y_comp, old_y_comp)

    def check_bounce_on_left_boundary(self, sprite):
        """ 
        Check correct bouncing on <left> boundary:
        - on collision the sprite's heading direction is inverted in the <x> component
        """
        sprite.setheading(130)
        old_heading = sprite.heading()
        old_x_comp = cos(radians(old_heading))
        old_y_comp = sin(radians(old_heading))
        sprite.setpos(self.game.config_values['field_width'] / -2, 0)
        self.game.main_loop(testmode = True)
        x_comp = cos(radians(sprite.heading()))
        y_comp = sin(radians(sprite.heading()))
        self.assertAlmostEqual(x_comp, - old_x_comp )
        self.assertAlmostEqual(y_comp, old_y_comp)

    def check_bounce_on_top_boundary(self, sprite):
        """ 
        Check correct bouncing on<top> boundary:
        -  on collision the sprite's heading direction is inverted in the <y> component
        """
        sprite.setheading(30)
        old_heading = sprite.heading()
        old_x_comp = cos(radians(old_heading))
        old_y_comp = sin(radians(old_heading))
        sprite.setpos(0 , self.game.config_values['field_height'] / 2)
        self.game.main_loop(testmode = True)
        x_comp = cos(radians(sprite.heading()))
        y_comp = sin(radians(sprite.heading()))
        self.assertAlmostEqual(x_comp, old_x_comp )
        self.assertAlmostEqual(y_comp, - old_y_comp)
    
    def check_bounce_on_bottom_boundary(self, sprite):
        """ 
        Check correct bouncing on <bottom> boundary:
        - on collision the sprite's heading direction is inverted in the <y> component
        """
        sprite.setheading(330)
        old_heading = sprite.heading()
        old_x_comp = cos(radians(old_heading))
        old_y_comp = sin(radians(old_heading))
        sprite.setpos(0 , self.game.config_values['field_height'] / -2)
        self.game.main_loop(testmode = True)
        x_comp = cos(radians(sprite.heading()))
        y_comp = sin(radians(sprite.heading()))
        self.assertAlmostEqual(x_comp, old_x_comp )
        self.assertAlmostEqual(y_comp, - old_y_comp)

    def test_01_collision_of_player_with_all_borders(self):
        """
        Check if <player> sprite bounces off all four boundaries correctly
        """
        sprite = self.game.player
        self.check_bounce_on_left_boundary(sprite)
        self.check_bounce_on_right_boundary(sprite)
        self.check_bounce_on_top_boundary(sprite)
        self.check_bounce_on_bottom_boundary(sprite)
    
    def test_02_collision_of_enemy_with_all_borders(self):
        sprite = self.game.enemies_tracker[-1]
        self.check_bounce_on_left_boundary(sprite)
        self.check_bounce_on_right_boundary(sprite)
        self.check_bounce_on_top_boundary(sprite)
        self.check_bounce_on_bottom_boundary(sprite)
        """
        Check if <enemy> sprite bounces off all four boundaries correctly
        """

    def test_03_collision_of_missile_with_all_borders(self):
        """
        Check if <missile> sprite despawn on collision with a boundary
        """
        from time import sleep
        self.game.player_input("fire")
        self.game.main_loop(testmode = True)
        colliding_missile_id = id(self.game.player.missiles_shot[-1])
        self.game.player.missiles_shot[-1].setpos(self.game.config_values['field_width'] / 2 + 10, 0)
        self.game.player.missiles_shot[-1].speed = 0
        self.game.main_loop(testmode = True)
        current_missiles_ids = []
        for missile in self.game.player.missiles_shot:
            current_missiles_ids.append(id(missile))
        self.assertNotIn(colliding_missile_id, current_missiles_ids)