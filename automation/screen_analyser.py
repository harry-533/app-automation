"""
automation/screen_analyser.py
-----------------------------
PURPOSE: Capture screenshots and UI hierarchy
Functions: take_screenshot(), get_ui_hierarchy()
"""
import datetime

class ScreenAnalyser:
    def __init__(self, config):
        self.config = config

    def take_screenshot(self):
        date_str = datetime.now().strftime('%H:%M:%S')
        screenshot_path = self.config.SCREENSHOT_DIR / date_str
        self.config.d.screenshot(screenshot_path)
        return screenshot_path

    def get_ui_heirarchy(self):
        xml = self.config.d.dump_heirarchy()
        return xml