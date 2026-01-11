import os
import copy
from typing import List, Any, Dict

from openai import OpenAI


class LLMAgent:

    def __init__(self, model_config: dict):
        self.id = model_config['id']
        self.name = model_config.get('name')
        self.provider = model_config.get('provider')
        self.provider_model_name = model_config.get('provider_model_name')

        self.params: Dict[str, Any] = model_config.get('params', dict())
        self.settings: Dict[str, Any] = model_config.get('settings', dict())
        
        self.client: OpenAI = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
        
        self.messages: List[Dict[str, str]] = [
            {'role': 'developer', 'content': 'Respond only as the character, continuing their line or filling gaps (___). No extra words.'}
        ]
    
    def generate(self, prompt: str) -> str:
        self.messages.append({'role': 'user', 'content': prompt})

        n_retries = self.settings.get('n_retries', 1)
        retry_delay = self.settings.get('retry_delay', 0.0)
        
        attempt = 1
        while attempt <= n_retries:
            try:
                completion = self.client.chat.completions.create(
                    model=self.provider_model_name,
                    messages=self.messages,
                    **self.params
                )

                self.messages.append({'role': 'assistant', 'content': completion.choices[0].message.content})
                
                return completion.choices[0].message.content
            except Exception:
                self.messages.pop()
            
            attempt += 1

            if retry_delay > 0.0:
                time.sleep(retry_delay)

        return None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'model_id': self.id,
            'model_name': self.name,
            'model_provider': self.provider,
            # 'model_provider_model_name': self.provider_model_name
        }
    
    def copy(self):
        return copy.copy(self)
    
    def __copy__(self):
        new_instance = self.__class__({
            'id': self.id,
            'name': self.name,
            'provider': self.provider,
            'provider_model_name': self.provider_model_name,
            'params': self.params,
            'settings': self.settings
        })
        return new_instance
    
    def __str__(self):
        return f'{self.name} ({self.provider})'
