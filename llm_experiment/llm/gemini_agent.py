import os
import copy
import time
from typing import Optional

from .llm_agent import LLMAgent
from ..utils.parsers import Parser


class GeminiAgent(LLMAgent):
    
    def __init__(self, model_config: dict):
        super().__init__(model_config)
        
        try:
            import google.generativeai as genai
            api_key = os.environ.get('GEMINI_API_KEY')
            if api_key:
                genai.configure(api_key=api_key)
                self.client = genai.GenerativeModel(self.provider_model_name)
                self.chat = None
            else:
                self.client = None
                self.chat = None
        except ImportError:
            self.client = None
            self.chat = None
            print('Warning: google-generativeai package not installed')
    
    def _init_messages(self) -> None:
        self.messages = []
        if self.client:
            # Initialize chat session with system instruction
            generation_config = self.params.copy()
            self.chat = self.client.start_chat(history=[])
    
    def _generate_raw(self, prompt: str) -> Optional[str]:
        retry_delay = self.settings.get('retry_delay', float(os.environ.get('RETRY_DELAY', '1')))

        if not self.client or not self.chat:
            return None
        
        self.messages.append({'role': 'user', 'content': prompt})

        try:
            # Add system instruction to the first user message
            if len(self.messages) == 1:
                full_prompt = 'Respond only as the character, continuing their line or filling gaps (___). No extra words.\n\n' + prompt
            else:
                full_prompt = prompt
            
            response = self.chat.send_message(
                full_prompt,
                generation_config=self.params
            )
            
            assistant_response = response.text

            print(f'response: {assistant_response}')

            self.messages.append({'role': 'assistant', 'content': assistant_response})
            
            return assistant_response
            
        except Exception as e:
            self.messages.pop()
            
            time.sleep(retry_delay)

            print(e)
            
            return None
    
    def copy(self) -> 'GeminiAgent':
        return GeminiAgent({
            'id': self.id,
            'name': self.name,
            'provider': self.provider,
            'provider_model_name': self.provider_model_name,
            'params': self.params,
            'settings': self.settings
        })
