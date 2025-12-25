"""
automation/adb_controller.py
----------------------------
PURPOSE: Low-level ADB commands
Functions: tap(), swipe(), input_text(), get_screen_size()
"""
from time import sleep

class Adb_Controller:
    def __init__(self, config):
        self.config = config

    def get_screen_size(self):
        width, height = self.config.d.window_size()
        return width, height

    def swipe_up(self, duration=0.2):
        width, height = self.get_screen_size()
        start_x = width // 2
        start_y = int(height * 0.8)
        end_y = int(height * 0.2)
        self.config.d.swipe(start_x, start_y, start_x, end_y, duration)

    def small_swipe_up(self, duration=0.05):
        width, height = self.get_screen_size()
        start_x = width // 2
        start_y = int(height * 0.4)
        end_y = int(height * 0.2)
        self.config.d.swipe(start_x, start_y, start_x, end_y, duration)
    
    def extra_small_swipe_up(self, duration=0.05):
        width, height = self.get_screen_size()
        start_x = width // 2
        start_y = int(height * 0.38)
        end_y = int(height * 0.2)
        self.config.d.swipe(start_x, start_y, start_x, end_y, duration)

    def swipe_down(self, duration=0.2):
        width, height = self.get_screen_size()
        start_x = width // 2
        start_y = int(height * 0.2)
        end_y = int(height * 0.8)
        self.config.d.swipe(start_x, start_y, start_x, end_y, duration)

    def small_swipe_down(self, duration=0.05):
        width, height = self.get_screen_size()
        start_x = width // 2
        start_y = int(height * 0.2)
        end_y = int(height * 0.4)
        self.config.d.swipe(start_x, start_y, start_x, end_y, duration)

    def extra_small_swipe_down(self, duration=0.05):
        width, height = self.get_screen_size()
        start_x = width // 2
        start_y = int(height * 0.2)
        end_y = int(height * 0.3)
        self.config.d.swipe(start_x, start_y, start_x, end_y, duration)

    def click(self, x, y):
        self.config.d.click(x, y)
        sleep(0.5)
    
    def click_text(self, text):
        if self.config.d(text=text).exists:
            self.d(text=text).click()
            sleep(0.5)
            return True
        else:
            return False