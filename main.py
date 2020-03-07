#My SpaceWars Game by Kalli
import logging

import game

# Initiate logging
LOG_FILE = "game.log"
LOG_FORMAT = "%(asctime)s\t%(module)s\t%(levelname)s\t%(message)s"
logging.basicConfig(filename = LOG_FILE,
                    level = logging.DEBUG,
                    format = LOG_FORMAT,
                    filemode = 'w')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

game = game.Game("Space Wars")

game.main_loop()