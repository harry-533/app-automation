import base64
import json

class AIEngine:
    def __init__(self, config):
        self.config = config
        self.mode = config.AI_MODE

        if self.mode == 'free':
            self._init_free_mode()
        else:
            self._init_paid_mode()

    def _init_free_mode(self):
        import ollama
        self.client = ollama
        self.model = self.config.FREE_MODEL

    def _init_paid_mode(self):
        import anthropic
        self.client = anthropic.Anthropic(
            api_key = self.config.ANTHROPIC_API_KEY
        )
        self.model = self.config.PAID_MODEL
    
    def query(self, prompt, image=None):
        if self.mode == 'free':
            return self._query_ollama(prompt, image)
        else:
            return self._query_claude(prompt, image)
        
    def _query_ollama(self, prompt, image):
        messages = [{'role': 'user', 'content': prompt}]

        if image:
            img_base64 = base64.b64encode(image).decode()
            messages[0]['images'] = [img_base64]

        response = self.client.chat(model=self.model, messages=messages)
        return response['message']['content']
    
    def _query_claude(self, prompt, image):
        content = []

        if image:
            img_base64 = base64.b64encode(image).decode()
            content.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/png",
                    "data": img_base64
                }
            })
        
        content.append({"type": "test", "text": prompt})

        message = self.client.messages.create(
            model=self.model,
            max_tokens = 1024,
            messages=[{"role": "user", "content": content}]
        )

        return message.content[0].text
    
    def decide_next_action(self, goal, current_screen, ui_heirarchy, actions_so_far):
        from ai.prompt_templates import NEXT_ACTION_PROMPT

        prompt = NEXT_ACTION_PROMPT.format(
            goal=goal,
            ui_heirarchy=ui_heirarchy,
            actions_so_far=actions_so_far
        )

        response = self.query(prompt, image=current_screen)
        return json.loads(self._clean_json(response))
    
    def compare_similarity(self, text1, text2):
        from ai.prompt_templates import SIMILARITY_PROMPT

        prompt = SIMILARITY_PROMPT.format(text1=text1, text2=text2)
        response = self.query(prompt)

        data = json.loads(self._clean_json(response))
        return data['similarity']

    def _clean_json(self, text):
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
        return text.strip()