#My SpaceWars Ganme by Kalli

import os
import random
import math
import turtle
import time

import game
import sprites
import game_config

config = game_config.Config()
current_config_values = config.current_values()
print(current_config_values)


#Create game object
game = game.Game(current_config_values)

#Draw the border
game.draw_border()

#Draw the game score
game.show_score()

#Create the player sprite
player = sprites.Player("triangle", 1, "white", 0, 0, current_config_values)

#Create the enemy sprites
enemies = list()
for i in range(current_config_values['enemy_max_no']):
    enemies.append(sprites.Enemy("circle", 1, current_config_values))

missile = sprites.Missile("triangle", 0.5, current_config_values, player) #Missle does always exist but is rendered offscreen when not used

#Keyboard Bindings
turtle.onkey(player.turn_left, "Left")
turtle.onkey(player.turn_right, "Right")
turtle.onkey(player.accelerate, "Up")
turtle.onkey(player.decelerate, "Down")
turtle.onkey(missile.fire, "space")
turtle.onkey(game.exit, "Escape")
turtle.listen()


loop_delta = 1./current_config_values['game_fps'] #calculate loop time based on fixed FPS value
current_time = target_time = time.clock() #set initial values for the timer loop

#Main game loop
while True:
    #### loop frequency evaluation
    previous_time, current_time = current_time, time.clock() #update relative timestamps
    time_delta = current_time - previous_time
    #print 'loop frequency: %s' % (1. / time_delta) #todo LOG THIS

    turtle.update()
    player.move()
    for enemy in enemies:
        enemy.move()

        #Check for collistion with enemies
        if player.is_collision(enemy):
            x = random.randint(-current_config_values['field_width']/2, current_config_values['field_width']/2)
            y = random.randint(-current_config_values['field_height']/2, current_config_values['field_height']/2)
            enemy.goto(x, y)
            enemy.setheading(random.randint(0,359))
            game.update_score(-1, 0) #remove 1 live

        #Check for collistion with a missles
        if missile.is_collision(enemy):
            x = random.randint(-current_config_values['field_width']/2, current_config_values['field_width']/2)
            y = random.randint(-current_config_values['field_height']/2, current_config_values['field_height']/2)
            missile.reset()
            enemy.goto(x, y)
            game.update_score(0, enemy.value) #add 10 to score

    missile.move()

    #### sleep management to achieve constant FPS
    target_time += loop_delta
    sleep_time = target_time - time.clock()
    if sleep_time > 0:
        time.sleep(sleep_time)
        #print(time_delta)
    else:
        print 'took too long' #TODO Raise error instead of printig this messeage
