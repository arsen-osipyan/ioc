import os
import copy
import asyncio
from typing import List, Any, Dict, Optional

from openai import AsyncOpenAI

from .utils.parsers import Parser


class Model:
    
    def __init__(self, model_config: dict, client: AsyncOpenAI = None):
        self.id: str = model_config['id']
        self.name: str = model_config.get('name', self.id)
        self.provider: str = model_config.get('provider', 'Unknown')
        self.openrouter_model_name: str = model_config.get('openrouter_model_name', '')
        
        self.params: Dict[str, Any] = model_config.get('params', {})
        self.settings: Dict[str, Any] = model_config.get('settings', {})
        
        self.messages: List[Dict[str, str]] = []
        self._init_messages()
        
        self.client = AsyncOpenAI(
            base_url=os.environ.get('OPENROUTER_URL'),
            api_key=os.environ.get('OPENROUTER_API_KEY'),
        ) if client is None else client
    
    def _init_messages(self) -> None:
        if 'system_message' in self.settings.keys():
            self.messages = [{
                'role': 'system',
                'content': self.settings['system_message']
            }]
        else:
            self.messages = []
    
    async def _generate_raw(self, prompt: str) -> Optional[str]:
        retry_delay = self.settings.get('retry_delay', float(os.environ.get('RETRY_DELAY', '1')))

        if not self.client:
            return None
        
        self.messages.append({'role': 'user', 'content': prompt})

        try:
            completion = await self.client.chat.completions.create(
                model=self.openrouter_model_name,
                messages=self.messages,
                **self.params
            )
            
            response = completion.choices[0].message.content

            self.messages.append({'role': 'assistant', 'content': response})
            
            return response
            
        except Exception as e:
            self.messages.pop()
            print(f'Error in Model._generate_raw(): {e}')
            await asyncio.sleep(retry_delay)
            return None
    
    async def generate(self, prompt: str, parser: Optional[Parser] = None) -> Optional[str]:
        max_retries = self.settings.get('max_retries', int(os.environ.get('MAX_RETRIES', '5')))
        
        for attempt in range(max_retries):
            response = await self._generate_raw(prompt)
            
            if response is None:
                continue
            
            if parser is None:
                return response
            
            parsed_result = parser.parse(response)
            
            if parsed_result is not None:
                # print(f'<prompt>{prompt}</prompt>\n<response>{response}</response>\n<parsed_result>{str(parsed_result)}</parsed_result>\n\n')
                return parsed_result
            
        print(f'Response invalid after {max_retries} attempts. Last response: "{response}".')

        return None
    
    def reset_conversation(self) -> None:
        self._init_messages()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'model_id': self.id
        }
    
    def copy(self) -> 'Model':
        return Model({
            'id': self.id,
            'name': self.name,
            'provider': self.provider,
            'openrouter_model_name': self.openrouter_model_name,
            'params': self.params,
            'settings': self.settings
        }, client=self.client)
