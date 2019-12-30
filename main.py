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
   
while game.state != game.exiting:
    loop_delta = 1./game.config_values['game_fps'] #calculate loop time based on fixed FPS value
    current_time = target_time = time.perf_counter()

    while game.state == game.running:
        #logging.debug("Start of self loop with game.state = %s" % game.state)
        previous_time, current_time = current_time, time.perf_counter() #update relative timestamps
        time_delta = current_time - previous_time

        game.pen.screen.update()

        game.player.move()

        for enemy in game.enemies:
            enemy.move()

        for missile in game.player.missiles_shot:
            missile.move()

        for enemy in game.enemies:
            #Check for collision with enemies
            if game.player.is_collision(enemy):
                enemy.despawn()
                game.spawn_enemy()
                game.update_score(-1, 0) #remove 1 live

            for missile in game.player.missiles_shot:
                # Check for collision with all missles shot
                if missile.is_collision(enemy):
                    enemy.despawn()
                    missile.despawn()
                    game.spawn_enemy()
                    game.spawn_enemy()
                    game.update_score(0, enemy.value) #add 10 to score
                            
    
        #### sleep management to achieve constant FPS
        target_time += loop_delta
        sleep_time = target_time - time.perf_counter()
        if sleep_time > 0:
            # logging.debug("Sleeping for: {}".format(sleep_time))
            time.sleep(sleep_time)
        else:
            print("Execution of main loop took too long: {}".format(sleep_time))
            logging.warning("Execution of main loop took too long: {}".format(sleep_time))

    while game.state == game.welcoming or game.state == game.paused or game.state == game.over:
        game.wait_for_input()

    if game.state == "exit":
        game.exit()

    game.pen.screen.update() # includes the check for key press
    
    time.sleep(0.1) # Slow down main loop