#My SpaceWars Ganme by Kalli

import os
import random
import math
import turtle

import game
import sprites
from game_config import *

#Create game object
game = game.Game()

#Draw the border
game.draw_border()

#Create my sprites
player = sprites.Player("triangle", "white", 0, 0)
enemy = sprites.Enemy("circle", "red", -field_width/2, 0)
missile = sprites.Missile("triangle", "yellow", 2 * field_width, 2 * field_height, player)

#Keyboard Bindings
turtle.onkey(player.turn_left, "Left")
turtle.onkey(player.turn_right, "Right")
turtle.onkey(player.accelerate, "Up")
turtle.onkey(player.decelerate, "Down")
turtle.onkey(missile.fire, "space")
turtle.onkey(game.exit, "Escape")
turtle.listen()

#Main game loop
while True:
    player.move()
    enemy.move()
    missile.move()

    #Check for collistion with enemies
    if player.is_collision(enemy):
        x = random.randint(-field_width + 20, field_width - 20)
        y = random.randint(-field_height + 20, field_height - 20)
        enemy.goto(x, y)
        enemy.setheading(random.randint(0,359))
        game.update_score(-1, 0) #remove 1 live

    #Check for collistion with a missles
    if missile.is_collision(enemy):
        x = random.randint(-field_width + 20, field_width - 20)
        y = random.randint(-field_height + 20, field_height - 20)
        missile.reset()
        enemy.goto(x, y)
        game.update_score(0, 10) #add 10 to score
