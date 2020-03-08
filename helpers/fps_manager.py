import logging
import time

class Fps_manager():
    """
    Ensures constant FPS by deciding if the next render shall take place
    Usage:  1. Initiate classe object befor the beginning of the main loop
            2. Call class method "update()" at the beginning for the main loop
            3. Render frame if class method "decide to render()" retruns "True", otherwise drop it
    """
    def __init__(self, fps_value, max_frame_drops = 5):
        """ Initiate timer values und frame_drop_counter """
        self.loop_delta = 1./fps_value
        self.current_time = self.target_time = time.perf_counter()
        self.frame_drop_counter = 0
        self.max_frame_drops = max_frame_drops

    def update(self):
        """ Update timestams at the beginning of the main loop """
        self.previous_time, self.current_time = self.current_time, time.perf_counter() #update relative timestamps

    def decide_to_render(self):
        """ Returns true if time frame of main loop is not yet exceeded
            or 5 consecutive frames have already beed dropped """
        self.target_time += self.loop_delta
        self.sleep_time = self.target_time - time.perf_counter()
        if self.sleep_time > 0:
            if self.frame_drop_counter > 0 :
                self.frame_drop_counter -= 1
            time.sleep(self.sleep_time)      
            return True
        else:
            self.frame_drop_counter += 1
            logging.warning(f"Dropping frame update: Execution of main loop took {abs(self.sleep_time):.6f}s too long - happend {self.frame_drop_counter} time(s)")
            if self.frame_drop_counter > 5:
                logging.error("Dropped more than five frames in a row - force rendering (screen update) now")
                return True
            return False