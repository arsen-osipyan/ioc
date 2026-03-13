from .llm_agent import LLMAgent
from .open_ai_agent import OpenAIAgent


def create_agent(model_config: dict) -> LLMAgent:
    provider = model_config.get('provider', '').lower()
    
    if provider == 'openai':
        return OpenAIAgent(model_config)
    else:
        raise ValueError(f'Unsupported provider: {provider}.')


__all__ = ['LLMAgent', 'OpenAIAgent', 'create_agent']
