import configparser

## Default Game preferences
game_fps = 60

field_width = 600 # max 900
field_height = 600 # max 700

modifier_lives = 1
modifier_score = 100

# Sprite Properties
sprite_radius_default = 15

# Player Properties
player_lives = 3
player_speed_default = 2.5
player_turn_rate = 24

# Enemy Properties
enemy_speed = 2.5
enemy_max_no = 7

# Missile Properties
missile_speed = 10


class Config():
    def __init__(self):
        self.config_file = "config.ini"
        self.config = configparser.ConfigParser()
        self.read_file()
        self.current_values()
        self._DEFAULTVALUES = {
            'game_fps' : 60,
            'field_width' : 600,
            'field_height' : 600,
            'sprite_radius_default': 15,
            'player_lives': 3,
            'player_speed_default': 2.5,
            'player_turn_rate': 24,
            'enemy_speed': 2.5,
            'enemy_max_no': 3,
            'missile_speed':10
        }

    def read_file(self):
        ''' Read the config file '''
        self.config.read(self.config_file)


    def current_values(self):
        Current = {
            'game_fps' : self.config.getfloat('Current','game_fps'),
            'field_width' : self.config.getint('Current','field_width'),
            'field_height' : self.config.getint('Current','field_height'),
            'sprite_radius_default': self.config.getint('Current','sprite_radius_default'),
            'player_lives': self.config.getint('Current','player_lives'),
            'player_speed_default': self.config.getfloat('Current','player_speed_default'),
            'player_turn_rate': self.config.getint('Current','player_turn_rate'),
            'enemy_max_no': self.config.getint('Current','enemy_max_no'),
            'enemy_speed': self.config.getfloat('Current','enemy_speed'),
            'missile_speed':self.config.getint('Current','missile_speed')
        }
        return Current

    def write_file(self):
        ''' Write the standard config file '''
        self.config['Current'] = self.current_values()
        with open(self.config_file, 'w') as configfile:
           self.config.write(configfile)
