#My SpaceWars Game by Kalli
import os
import sys
import time
import random
import turtle
import logging

import game

# Initiate logging
LOG_FILE = "game.log"
LOG_FORMAT = "%(asctime)s\t%(module)s\t%(levelname)s\t%(message)s"
logging.basicConfig(filename = LOG_FILE,
                    level = logging.DEBUG,
                    format = LOG_FORMAT,
                    filemode = 'w')

game = game.Game("Space Wars")

while True:
    game.main_loop()