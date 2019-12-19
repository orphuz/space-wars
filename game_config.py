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
        self.config = self.ReadConfigFile()

    def WriteConfigFile(self):
        ''' Write the standard config file '''
        self.config['DEFAULT'] = {'game_fps': '60' ,
                              'field_width': '600',
                              'field_height': '600',
                              'modifier_lives': '1',
                              'modifier_score': '100',
                              'sprite_radius_default': '15',
                              'player_lives': '3',
                              'player_speed_default': '2.5',
                              'player_turn_rate': '24',
                              'enemy_speed ': '2.5',
                              'enemy_max_no': '3',
                              'missile_speed': '10'}
        self.config['Current'] = {
            'game_fps': game_fps,
            'field_width': field_width,
            'field_height': field_height,
            'modifier_lives': modifier_lives,
            'modifier_score': modifier_score,
            'sprite_radius_default': sprite_radius_default,
            'player_lives': player_lives,
            'player_speed_default': player_speed_default,
            'player_turn_rate': player_turn_rate,
            'enemy_speed': enemy_speed,
            'enemy_max_no': enemy_max_no,
            'missile_speed': missile_speed
        }
        with open(self.config_file, 'w') as configfile:
           self.config.write(configfile)

    def ReadConfigFile(self):
        ''' Read the config file '''
        self.config.read(self.config_file)
        return self.config

    def get(self, section, name):
        return self.config.get(section, name)
