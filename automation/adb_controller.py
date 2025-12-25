from time import sleep
import os
import datetime

class Adb_Controller:
    def __init__(self, config):
        self.config = config
        self.d = config.d

    def get_screen_size(self):
        width, height = self.config.d.window_size()
        return width, height
    
    def launch_bentley(self):
        self.d.launch_app("uk.co.bentley.mybentley")

    def swipe(self, x1, y1, x2, y2, duration=0.2):
        self.d.swipe(x1, y1, x2, y2, duration)
        sleep(0.3)
    
    def swipe_up(self, distance='normal', duration=0.2):
        width, height = self.get_screen_size()
        start_x = width // 2
        
        if distance == 'small':
            start_y = int(height * 0.4)
            end_y = int(height * 0.2)
        elif distance == 'extra_small':
            start_y = int(height * 0.38)
            end_y = int(height * 0.2)
        else:
            start_y = int(height * 0.8)
            end_y = int(height * 0.2)
        
        self.swipe(start_x, start_y, start_x, end_y, duration)
    
    def swipe_down(self, distance='normal', duration=0.2):
        width, height = self.get_screen_size()        
        start_x = width // 2
        
        if distance == 'small':
            start_y = int(height * 0.2)
            end_y = int(height * 0.4)
        elif distance == 'extra_small':
            start_y = int(height * 0.2)
            end_y = int(height * 0.3)
        else:
            start_y = int(height * 0.2)
            end_y = int(height * 0.8)
        
        self.swipe(start_x, start_y, start_x, end_y, duration)
    
    def swipe_left(self, duration=0.2):
        """Swipe left (move to next screen/page)"""
        width, height = self.get_screen_size()
        
        start_y = height // 2
        start_x = int(width * 0.8)
        end_x = int(width * 0.2)
        
        self.swipe(start_x, start_y, end_x, start_y, duration)
    
    def swipe_right(self, duration=0.2):
        """Swipe right (move to previous screen/page)"""
        width, height = self.get_screen_size()
        
        start_y = height // 2
        start_x = int(width * 0.2)
        end_x = int(width * 0.8)
        
        self.swipe(start_x, start_y, end_x, start_y, duration)

    def phone_setting_swipe(self, duration=0.2):
        width, height = self.get_screen_size()
        start_x = width // 2
        start_y = int(height * 0.5)
        end_y = int(height * 0.8)
        self.d.swipe(start_x, start_y, start_x, end_y, duration)

    def click(self, x, y):
        self.d.click(x, y)
        sleep(0.5)
        
    def press_home(self):
        self.d.press("home")

    def press_enter(self):
        os.system("adb shell input keyevent 66")

    def press_back(self):
        self.d.press("back")
        sleep(0.5)

    def enter_pin(self, pin: str, press_enter: bool = True):
        if not pin.isdigit():
            raise ValueError("PIN should only contain digits")
        else:
            os.system(f"adb shell input text {pin}")
        if press_enter:
            self.press_enter
        sleep(0.5)
        
    def enter_text(self, text: str, press_enter: bool = True, safe_type: bool = False):
        if safe_type:
            for char in text:
                os.system(f"adb shell input {char}")
        else:
            os.system(f"adb shell input text {text}")
        if press_enter:
            self.press_enter
        sleep(0.5)
        
    def clear_text(self, num_chars: int = 20):
        for _ in range(num_chars):
            os.system("adb shell input keyevent 67")
        sleep(0.5)

    def close_all_apps(self):
        self.d.press("recent")
        sleep(0.5)
        self.click_text("Close all", 10)
        self.launch_bentley()

    def login(self, email, password, safe_type=False):
        pass
    
    def logout(self):
        pass

    def take_screenshot(self):
        date_str = datetime.now().strftime('%H:%M:%S')
        screenshot_path = self.config.SCREENSHOT_DIR / date_str
        self.config.d.screenshot(screenshot_path)
        return screenshot_path

    def get_ui_heirarchy(self):
        xml = self.config.d.dump_heirarchy()
        return xml

    def get_available_actions(self):
        return {
            "click": {
                "description": "click at coordinates (x, y)",
                "parameters": ["x", "y"]
            },
            "swipe": {
                "description": "Swipe from (x1,y1) to (x2,y2)",
                "parameters": ["x1", "y1", "x2", "y2", "duration"]
            },
            "swipe_up": {
                "description": "Swipe up to scroll down",
                "parameters": ["distance: small/normal"]
            },
            "swipe_down": {
                "description": "Swipe down to scroll up",
                "parameters": ["distance: small/normal"]
            },
            "swipe_left": {
                "description": "Swipe left"
            },
            "swipe_right": {
                "description": "Swipe right"
            },
            "input_text": {
                "description": "Type text into focused field",
                "parameters": ["text", "press_enter"]
            },
            "clear_text": {
                "description": "Delete characters",
                "parameters": ["num_chars"]
            },
            "press_back": {
                "description": "Press back button"
            },
            "press_home": {
                "description": "Press home button"
            },
            "press_enter": {
                "description": "Press enter key"
            }
        }