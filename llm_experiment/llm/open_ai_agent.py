import os
import copy
import time
from typing import Optional

from .llm_agent import LLMAgent
from ..utils.parsers import Parser


class OpenAIAgent(LLMAgent):
    
    def __init__(self, model_config: dict):
        super().__init__(model_config)
        
        try:
            from openai import OpenAI
            api_key = os.environ.get('OPENAI_API_KEY')
            self.client = OpenAI(api_key=api_key) if api_key else None
        except ImportError:
            self.client = None
            print('Warning: openai package not installed')
    
    def _init_messages(self) -> None:
        if 'system_message' in self.settings.keys():
            self.messages = [{
                'role': 'developer',
                'content': self.settings['system_message']
            }]
        else:
            self.messages = []
    
    def _generate_raw(self, prompt: str) -> Optional[str]:
        retry_delay = self.settings.get('retry_delay', float(os.environ.get('RETRY_DELAY', '1')))

        print(self.messages)

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

            self.messages.append({'role': 'assistant', 'content': response})
            
            return response
            
        except Exception as e:
            self.messages.pop()
            
            time.sleep(retry_delay)
            
            return None
    
    def copy(self) -> 'OpenAIAgent':
        return OpenAIAgent({
            'id': self.id,
            'name': self.name,
            'provider': self.provider,
            'provider_model_name': self.provider_model_name,
            'params': self.params,
            'settings': self.settings
        })