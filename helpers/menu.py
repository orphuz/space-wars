import logging
import turtle

class Menu(object):
    def __init__(self, game):
        self.screen_width = 300
        self.screen_height = 300
        self.game = game
        self.pen = turtle.Turtle(visible = False)
        self.pen.screen.tracer(0)
        self.pen.color('white')
        self.pen.screen.bgcolor("black")
        self.pen.speed(0)

    def _menu_screen(self, title, height, width, text_01 = "", text_02 = "", text_03 = ""):
        """ Template function to draw screens """
        self.pen.clear()
        self.pen.penup()
        self.pen.setheading(0)
        self.pen.goto(- height / 2, width / 2)
        self.pen.pendown()
        self.pen.fd(width)
        self.pen.rt(90)
        self.pen.fd(height)
        self.pen.rt(90)
        self.pen.fd(width)
        self.pen.rt(90)
        self.pen.fd(height)
        self.pen.penup()
        self.pen.goto(0, 60)
        self.pen.pendown()
        self.pen.write(title, font=("Arial", 28, "normal"), align = 'center')
        self.pen.penup()
        if text_01 != "":
            self.pen.goto(0, -30)
            self.pen.pendown()
            self.pen.write(text_01, font=("Arial", 12, "normal"), align = 'center')
            self.pen.penup()
        if text_02 != "":
            self.pen.goto(- width / 2 + 10 , - height /2 + 30)
            self.pen.pendown()
            self.pen.write(text_02, font=("Arial", 12, "normal"), align = 'left')
            self.pen.penup()
        if text_03 != "":
            self.pen.goto(- width / 2 + 10 , - height /2 + 10)
            self.pen.pendown()
            self.pen.write(text_03, font=("Arial", 12, "normal"), align = 'left')
            self.pen.penup()
        self.pen.screen.update()
        logging.debug("<{}> screen drawn".format(title))

    def welcome_screen(self):
        """ Draw the welcome screen """
        self._menu_screen("SPACE WARS", self.screen_height, self.screen_width, "", "Press <Return> to start", "Press <ESC> to exit")
        logging.debug('Welcome screen drawn')

    def pause_screen(self):
        """ Draw the pause screen """
        self._menu_screen("GAME PAUSED", self.screen_height, self.screen_width, "", "Press <Return> to continue", "Press <ESC> to go to start screen")

    def over_screen(self, score, highscore):
        """ Draw game over screen """
        #TODO: Create notification about a newly set highscore, e.g. by comparing to currently pickled high score (=last high score)
        self._menu_screen("GAME OVER", self.screen_height, self.screen_width, f"Your final score: {score}\n\nHighscore: {highscore}", "Press <Return> to continue", "Press <ESC> to exit")
        logging.debug('Welcome screen drawn')

    def clear_screen(self):
        self.pen.clear()
        logging.debug('Menu screen cleared')