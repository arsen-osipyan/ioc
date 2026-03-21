import os
import copy
import time
from abc import ABC, abstractmethod
from typing import List, Any, Dict, Optional

from ..utils.parsers import Parser


class LLMAgent(ABC):
    
    def __init__(self, model_config: dict):
        self.id: str = model_config['id']
        self.name: str = model_config.get('name', self.id)
        self.provider: str = model_config.get('provider', 'Unknown')
        self.provider_model_name: str = model_config.get('provider_model_name', '')
        
        self.params: Dict[str, Any] = model_config.get('params', {})
        self.settings: Dict[str, Any] = model_config.get('settings', {})
        
        self.messages: List[Dict[str, str]] = []
        self._init_messages()
    
    def _init_messages(self) -> None:
        self.messages = []
    
    @abstractmethod
    def _generate_raw(self, prompt: str) -> Optional[str]:
        print('a')
        raise NotImplementedError()
    
    def generate(self, prompt: str, parser: Optional[Parser] = None) -> Optional[str]:
        max_retries = self.settings.get('max_retries', int(os.environ.get('MAX_RETRIES', '5')))
        # print(max_retries)
        
        for attempt in range(max_retries):
            response = self._generate_raw(prompt)
            print(response)
            
            if response is None:
                continue
            
            if parser is None:
                return response
            
            parsed_result = parser.parse(response)
            
            if parsed_result is not None:
                return response
            
        return None
    
    def reset_conversation(self) -> None:
        self._init_messages()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'model_id': self.id,
            'model_name': self.name,
            'model_provider': self.provider,
        }
    
    @abstractmethod
    def copy(self) -> 'BaseLLMAgent':
        raise NotImplementedError()
