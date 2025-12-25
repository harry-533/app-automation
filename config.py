import os
from pathlib import Path
from datetime import datetime
import uiautomator2 as u2

class Config:
    def __init__(self, ai_mode='free'):
        self.PROJECT_ROOT = Path(__file__).parent
        self.OUTPUT_DIR = self.PROJECT_ROOT / 'output'
        self.KNOWLEDGE_DIR = self.PROJECT_ROOT / 'knowledge'

        date_str = datetime.now().strftime('%Y-%m-%d')
        self.SCREENSHOTS_DIR = self.OUTPUT_DIR / 'screenshots' / date_str
        self.REPORTS_DIR = self.OUTPUT_DIR / 'reports' / date_str
        self.LOGS_DIR = self.OUTPUT_DIR / 'logs' / date_str

        for dir_path in [self.SCREENSHOTS_DIR, self.REPORTS_DIR, self.LOGS_DIR, self.KNOWLEDGE_DIR]:
            dir_path.mkdir(parents=True, exist_ok=True)

        self.AI_MODE = ai_mode
        self.ANTRHOPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')
        self.FREE_MODEL = "llama3.2-vision"
        self.PAID_MODEL = "claude-sonnet-4-20250514"

        self.ADB_PATH = "adb"

        self.STEP_DELAY = 1.0
        self.MAX_RETRIES_PER_STEP = 3
        self.SCREENSHOT_EVERY_STEP = True
        self.AI_VERIFICATION_CONFIDENCE_THRESHOLD = 0.7

        self.ENABLE_PATH_LEARNING = True
        self.PATH_SIMILARITY_THRESHOLD = 0.8
        self.PATHS_FILE = self.KNOWLEDGE_DIR / 'paths.json'
        self.FUNCTION_STATS_FILE = self.KNOWLEDGE_DIR / 'function_success_rates.json'

        self.d = u2.connect()