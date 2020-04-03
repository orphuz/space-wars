import logging
import pickle

class Score():
    def __init__(self, highscorefile):
        self._highscorefile = highscorefile
        self._score = 0
        self._highscore = self.load_highscore()
        self._new_score = False
        
        
    def load_highscore(self):
        """ Try to load a high score value from a pickel. If it fails, sets high score to 0 """
        highscore = 0
        try:
            highscore = pickle.load( open( self._highscorefile, "rb" ) )
            logging.debug(f"High score of <{highscore}> sucessfully loaded ")
        except IOError as ioerr:
            logging.warn(f"{ioerr} - No pickled high score found, creating new with integer value 0")
            pickle.dump(int(0), open(self._highscorefile, "wb" ) )
        finally:
            return highscore

    @property
    def current(self):
        return self._score

    @property
    def highscore(self):
        return self._highscore

    @property
    def is_new(self):
        return self._new_score

    def be_new(self):
        self._new_score = True

    def be_old(self):
        self._new_score = False

    def update_current(self, modifier):
        """ Update the game score based on the given modifier """
        self._new_score = True      
        self._score += modifier
        if self._highscore < self._score: self._highscore = self._score

    def reset_current(self):
        """ Reset the current score to 0 """
        self._score = 0

    def save_highscore(self):
        """ Save high score to pickle file """
        pickle.dump( self._highscore, open( self._highscorefile, "wb" ) )
        logging.debug(f"Highscore <{self._highscore}> saved pesistently in file <{self._highscorefile}>")
 
    def reset_highscore(self):
        """ Reset high score value to 0 and refresh screen """
        self._highscore = 0
        self.save_highscore()  