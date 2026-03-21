import os
import copy
import time
from typing import Optional

from .llm_agent import LLMAgent
from ..utils.parsers import Parser


class DeepSeekAgent(LLMAgent):
    
    def __init__(self, model_config: dict):
        super().__init__(model_config)
        
        try:
            from openai import OpenAI
            api_key = os.environ.get('DEEPSEEK_API_KEY')
            base_url = os.environ.get('DEEPSEEK_BASE_URL', 'https://api.deepseek.com')
            self.client = OpenAI(api_key=api_key, base_url=base_url) if api_key else None
        except ImportError:
            self.client = None
            print('Warning: openai package not installed')
    
    def _init_messages(self) -> None:
        self.messages = [{
                'role': 'system',
                'content': 'Respond only as the character, continuing their line or filling gaps (___). No extra words.'
        }]
    
    def _generate_raw(self, prompt: str) -> Optional[str]:
        retry_delay = self.settings.get('retry_delay', float(os.environ.get('RETRY_DELAY', '1')))

        if not self.client:
            return None
        
        self.messages.append({'role': 'user', 'content': prompt})

        try:
            completion = self.client.chat.completions.create(
                model=self.provider_model_name,
                messages=self.messages,
                **self.params
            )
            
            response = completion.choices[0].message.content

            print(f'response: {response}')

            self.messages.append({'role': 'assistant', 'content': response})
            
            return response
            
        except Exception as e:
            self.messages.pop()
            
            time.sleep(retry_delay)

            print(e)
            
            return None
    
    def copy(self) -> 'DeepSeekAgent':
        return DeepSeekAgent({
            'id': self.id,
            'name': self.name,
            'provider': self.provider,
            'provider_model_name': self.provider_model_name,
            'params': self.params,
            'settings': self.settings
        })
