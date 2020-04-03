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
        self.render_counter = 0
        self.last_render_time = 0
        self.average_render_time = 0

    def update(self):
        """ Update timestams at the beginning of the main loop """
        self.previous_time, self.current_time = self.current_time, time.perf_counter() #update relative timestamps

    def timed_render(self, render_function):
        """ Meseaures the time of the provided render function and calculates the average time over all render iterations """
        time_before = time.perf_counter()
        render_function()
        self.render_counter = self.render_counter + 1
        self.last_render_time = time.perf_counter() - time_before
        self.average_render_time = (self.average_render_time * (self.render_counter - 1) + (self.last_render_time)) / self.render_counter
        # logging.debug(f"Average time for rendering is: {self.average_render_time}")

    def decide_to_render(self, render_function):
        """ 
        Executes timed rendering provided by the argument "render_function" if:
        - remaining time per frame including is greate than the average render time 
        - or 5 consecutive frames have already beed dropped
        and calls check if sleeping is necessary
        """
        self.target_time += self.loop_delta
        remaining_time = self.target_time - time.perf_counter()
        if remaining_time > self.average_render_time:
            if self.frame_drop_counter > 0 :
                self.frame_drop_counter = 0 
            self.timed_render(render_function)
        else:
            self.frame_drop_counter += 1
            #logging.warning(f"Dropping frame update: Execution of main loop took {abs(self.sleep_time):.6f}s too long - happend {self.frame_drop_counter} time(s)")
            if self.average_render_time != 0:
                # TODO: Understand why the if statement is necessary
                logging.warning(f"Dropping frame update: Last render time was {(((self.last_render_time / self.average_render_time)-1) * 100):.2f}% above the average. Frame drop counter increased to <{self.frame_drop_counter}>")
            if self.frame_drop_counter > 5:
                logging.error(f"Dropped <{self.frame_drop_counter}> frames in a row - force rendering (screen update) now")
                self.timed_render(render_function)
                self.frame_drop_counter = 0

        self.decide_to_sleep()        

    def decide_to_sleep(self):
        """
        Sleep for the remaining time in of loop_delta otherwise log delay
        """
        sleep_time = self.target_time - time.perf_counter()
        if sleep_time > 0:
            # logging.warning(f"Sleeping for {sleep_time:.6f}")
            time.sleep(sleep_time)
        else:
            logging.warning(f"Not sleeping because of {abs(sleep_time):.6f}s delay")
