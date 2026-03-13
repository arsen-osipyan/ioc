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
        """Generate raw response without parsing or retry logic."""
        raise NotImplementedError()
    
    def generate(self, prompt: str, parser: Optional[Parser] = None) -> Optional[str]:
        """
        Generate response with optional parsing and retry logic.
        
        If parser is provided, will retry generation until:
        - A valid parsed response is obtained, or
        - Maximum retry limit is reached
        
        Args:
            prompt: The prompt to generate from
            parser: Optional parser to validate the response
            
        Returns:
            Generated response string, or None if all retries failed
        """
        max_retries = self.settings.get('max_retries', 5)
        
        for attempt in range(max_retries):
            response = self._generate_raw(prompt)
            
            if response is None:
                continue
            
            # If no parser provided, return response immediately
            if parser is None:
                return response
            
            # Try to parse the response
            parsed_result = parser.parse(response)
            
            # If parsing succeeded (not None), return the original response
            if parsed_result is not None:
                return response
            
            # If parsing failed and we have more retries, continue
            # The conversation history is already updated in _generate_raw
        
        # All retries exhausted
        return None
    
    def reset_conversation(self) -> None:
        self._init_messages()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'model_name': self.name,
            'model_provider': self.provider,
        }
    
    @abstractmethod
    def copy(self) -> 'BaseLLMAgent':
        raise NotImplementedError()
