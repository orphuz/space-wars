#My SpaceWars Ganme by Kalli

import os
import random

#import the Turtle Module for drawing
import turtle
turtle.speed(0)
turtle.bgcolor("black")
turtle.ht()
turtle.setundobuffer(1)
turtle.tracer(1)

# Main variabales
player_speed_default = 4
player_lives = 3
enemy_speed = 4
bullet_speed = 20

field_width = 580 / 2
field_height = 580 / 2


class Sprite(turtle.Turtle):
    def __init__(self, spriteshape, color, startx, starty):
        turtle.Turtle.__init__(self, shape = spriteshape)
        self.speed(0)
        self.penup()
        self.color(color)
        self.fd(0)
        self.goto(startx, starty)
        self.speed = 1

    def move(self):
        self.fd(self.speed)

        #Boundary detection
        if self.xcor() > field_width:
            self.setx(field_width)
            self.rt(60)

        if self.xcor() < -field_width:
            self.setx(-field_width)
            self.rt(60)

        if self.ycor() > field_height:
            self.sety(field_height)
            self.rt(60)

        if self.ycor() < -field_height:
            self.sety(-field_height)
            self.rt(60)

    #Collision detection
    def is_collision(self, other, hitbox):
        if (self.xcor() >= (other.xcor() - hitbox)) and \
        (self.xcor() <= (other.xcor() + hitbox)) and \
        (self.ycor() >= (other.ycor() - hitbox)) and \
        (self.ycor() <= (other.ycor() + hitbox)):
            return True
        else:
            return False

class Player(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = player_speed_default
        self.lives = player_lives

    def turn_left(self):
        self.lt(30)

    def turn_right(self):
        self.rt(30)

    def accelerate(self):
        self.speed += 1

    def decelerate(self):
        self.speed -= 1

class Enemy(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = enemy_speed
        self.lives = 1
        self.setheading(random.randint(0,360))

class Missile(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.3, stretch_len=0.4, outline=None)
        self.speed = 20
        self.status = "ready"
        self.goto(-1000, 1000) #hide missle

    def fire(self):
        if self.status == "ready":
            self.goto(player.xcor(), player.ycor())
            self.setheading(player.heading())
            self.status = "firing"


    def reset(self):
        if self.status == "firing":
            self.fd(0)
            self.goto(-1000,1000)
            self.status = "ready"

    def move(self):
        if self.status == "firing":
            #border check
            if self.xcor() < -290 or self.xcor() > 290 or \
            self.ycor() < -290 or self.ycor() > 290:
                self.reset()
            else:
                self.fd(self.speed)

class Game():
    def __init__(self):
        self.level = 1
        self.score = 0
        self.lives = 3
        self.state = "playing"
        self.pen = turtle.Turtle()
        self.draw_border()


    def draw_border(self):
        #Draw border
        self.pen.speed(0)
        self.pen.color("white")
        self.pen.pensize(3)
        self.pen.penup()
        self.pen.goto(-300, 300)
        self.pen.pendown()
        for side in range(4):
            self.pen.fd(600)
            self.pen.rt(90)
        self.pen.penup()
        self.pen.ht()

    def exit(self):
        turtle.mainloop()
        turtle.done()
        turtle.exitonclick()

    def update_score(self, modifier_lives, modifier_score):
        self.lives += modifier_lives
        self.score += modifier_score
        #TODO draw score

#Create game object
game = Game()

#Create my sprites
player = Player("triangle", "white", 0, 0)
enemy = Enemy("circle", "red", -field_width/2, 0)
missile = Missile("triangle", "yellow", 2 * field_width, 2 * field_height)

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

    #Check for collistion
    if player.is_collision(enemy, 20):
        x = random.randint(-field_width + 20, field_width - 20)
        y = random.randint(-field_height + 20, field_height - 20)
        enemy.goto(x, y)
        game.update_score(-1, 0) #remove 1 live


    if missile.is_collision(enemy, 20):
        x = random.randint(-field_width + 20, field_width - 20)
        y = random.randint(-field_height + 20, field_height - 20)
        missile.reset()
        enemy.goto(x, y)
        game.update_score(0, 10) #add 10 to score


delay = raw_input("Press enter to finish- > ")
