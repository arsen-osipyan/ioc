import os
import copy
import time
from typing import Optional

from .llm_agent import LLMAgent
from ..utils.parsers import Parser


class YandexGPTAgent(LLMAgent):
    
    def __init__(self, model_config: dict):
        super().__init__(model_config)
        
        try:
            import requests
            self.api_key = os.environ.get('YANDEXGPT_API_KEY')
            self.folder_id = os.environ.get('YANDEXGPT_FOLDER_ID')
            self.api_url = os.environ.get('YANDEXGPT_API_URL', 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion')
            self.requests = requests
            self.client = True if self.api_key and self.folder_id else None
        except ImportError:
            self.client = None
            self.requests = None
            print('Warning: requests package not installed')
    
    def _init_messages(self) -> None:
        self.messages = [{
                'role': 'system',
                'text': 'Respond only as the character, continuing their line or filling gaps (___). No extra words.'
        }]
    
    def _generate_raw(self, prompt: str) -> Optional[str]:
        retry_delay = self.settings.get('retry_delay', float(os.environ.get('RETRY_DELAY', '1')))

        if not self.client:
            return None
        
        self.messages.append({'role': 'user', 'text': prompt})

        try:
            headers = {
                'Authorization': f'Api-Key {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'modelUri': f'gpt://{self.folder_id}/{self.provider_model_name}',
                'completionOptions': self.params,
                'messages': self.messages
            }
            
            response = self.requests.post(
                self.api_url,
                headers=headers,
                json=data
            )
            
            response.raise_for_status()
            result = response.json()
            
            assistant_response = result['result']['alternatives'][0]['message']['text']

            print(f'response: {assistant_response}')

            self.messages.append({'role': 'assistant', 'text': assistant_response})
            
            return assistant_response
            
        except Exception as e:
            self.messages.pop()
            
            time.sleep(retry_delay)

            print(e)
            
            return None
    
    def copy(self) -> 'YandexGPTAgent':
        return YandexGPTAgent({
            'id': self.id,
            'name': self.name,
            'provider': self.provider,
            'provider_model_name': self.provider_model_name,
            'params': self.params,
            'settings': self.settings
        })
