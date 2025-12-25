from ai.ai_engine import AIEngine
from ai.prompt_templates import TASK_DECOMPOSITION_PROMPT

class TaskDecomposer:
    def __init__(self, config):
        self.ai = AIEngine(config)

    def decompose(self, test_description):
        prompt = TASK_DECOMPOSITION_PROMPT.format(test_description=test_description)
        response = self.ai.query(prompt)
        steps = self._parse_steps(response)

        return steps
    
    def _parse_steps(self, ai_response):
        import json

        clean_response = ai_response.strip()
        if "```json" in clean_response:
            clean_response = clean_response.split("```json")[1].split("```")[0]

        data = json.loads(clean_response)
        return data['steps']