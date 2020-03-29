import configparser
import logging

class Config():
    def __init__(self):
        ''' Manage the game configuration with an external config file '''
        self._config_file = "data/config.ini"
        self._DEFAULTVALUES = {
            'game_fps' : 60,
            'field_width' : 600,
            'field_height' : 600,
            'sprite_radius_default': 15,
            'player_lives': 3,
            'player_speed_default': 2.5,
            'player_turn_rate': 24,
            'enemy_speed': 2.5,
            'enemy_max_number': 3,
            'missile_speed': 10,
            'powerup_max_number' : 2, 
            'powerup_min_lifetime': 2,
            'powerup_max_lifetime': 5
        }
        self.config = configparser.ConfigParser()
        
        self.values = self.current_values

    @property
    def current_values(self):
        """ Read current values from the .ini file and parse them into the correct type """
        self._read_file()
        parsed_values = self._parse_values()
        return parsed_values
    
    def _read_file(self):
        ''' Read the .ini file '''
        try:
            self.config.read(self._config_file)
        except IOError as ioerr:
            logging.error(f"{ioerr} - Reading config from <{self._config_file}> falied")
        if self.config == []:
            self.config = self._DEFAULTVALUES
            logging.warning('Falling back to default values')

    def _parse_values(self):
        """ Parse the config data into it's correct type and return them as dictionary """
        try:
            parsed_values = {
                'game_fps' : self.config.getfloat('Current','game_fps'),
                'field_width' : self.config.getint('Current','field_width'),
                'field_height' : self.config.getint('Current','field_height'),
                'sprite_radius_default': self.config.getint('Current','sprite_radius_default'),
                'player_lives': self.config.getint('Current','player_lives'),
                'player_speed_default': self.config.getfloat('Current','player_speed_default'),
                'player_turn_rate': self.config.getint('Current','player_turn_rate'),
                'enemy_max_no': self.config.getint('Current','enemy_max_no'),
                'enemy_speed': self.config.getfloat('Current','enemy_speed'),
                'missile_speed':self.config.getint('Current','missile_speed'),
                'powerup_min_lifetime':self.config.getint('Current','powerup_min_lifetime'),
                'powerup_max_lifetime':self.config.getint('Current','powerup_max_lifetime')
            }
            logging.debug("Config values from section <[current]> loaded")
        except configparser.NoSectionError as err:
            logging.error("NoSectionError: {0}".format(err))
            logging.warn("Section [Current] missing - Falling back to <_DEFAULTVALUES>")
            self.reset_to_default()
            parsed_values = self._DEFAULTVALUES
        return parsed_values

    @current_values.setter
    def current_values(self, value_key, value):
        """ Change a values in the current config base on key: value pair provided as args """
        if value_key not in list(self.config.values):
            logging.warn('%s is not a valid config value' % value_key)
            raise ValueError('%s is not a valid config value' % value_key)
        else:
            with open(self._config_file, 'w') as configfile:
                self.config[value_key] = value

    def write_file(self):
        ''' Write the standard config file '''
        try:
            with open(self._config_file, 'w') as configfile:
                self.config.write(configfile)
        except IOError as ioerr:
            logging.error(f"{ioerr} - Writng config to <{self._config_file}> falied")

    def reset_to_default(self):
        ''' Write hard coded default vaules to the config file '''
        self.config['Current'] = self._DEFAULTVALUES
        self.write_file()
        logging.warn('_DEFAULTVALUES set and written to file {}'.format(self._config_file))
