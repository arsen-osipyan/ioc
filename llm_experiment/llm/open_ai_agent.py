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
        self.messages = [{
                'role': 'developer',
                'content': 'Respond only as the character, continuing their line or filling gaps (___). No extra words.'
        }]
    
    def _generate_raw(self, prompt: str) -> Optional[str]:
        """Generate raw response from OpenAI API."""
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
            # Remove the user message if generation failed
            self.messages.pop()
            
            # Wait before retry
            retry_delay = int(os.environ.get('RETRY_DELAY', 1))
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