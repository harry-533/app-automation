import json
from pathlib import Path
from ai.ai_engine import AIEngine

class PathManager:
    def __init__(self, config):
        self.config = config
        self.ai = AIEngine(config)
        self.paths_file = config.PATHS_FILE
        self.paths = self._load_paths()

    def find_matching_path(self, test_description):
        for path in self.paths:
            similarity = self.ai.compare_similarity(
                test_description,
                path['test_description']
            )

            if similarity > self.config.PATH_SIMILARITY_THRESHOLD:
                return path
        
        return None

    def save_path(self, test_description, steps, success):
        existing = self.find_matching_path(test_description)
        if existing:
            existing['attempts'] += 1
            if success:
                existing['successes'] += 1
            existing['success_rate'] = existing['successes'] / existing['attempts']
        else:
            new_path = {
                'test_description': test_description,
                'steps': steps,
                'attempt': 1,
                'successes': 1 if success else 0,
                'success_rate': 1.0 if success else 0.0
            }
            self.paths.append(new_path)
        
        self._save_paths()

    def _load_paths(self):
        if self.paths_file.exists():
            with open(self.paths_file) as f:
                return json.load(f)
        return []
    
    def _save_paths(self):
        with open(self.paths_file, 'w') as f:
            json.dump(self.paths, f, indent=2)