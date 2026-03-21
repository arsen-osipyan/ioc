from .llm_agent import LLMAgent
from .open_ai_agent import OpenAIAgent
from .deepseek_agent import DeepSeekAgent
from .yandexgpt_agent import YandexGPTAgent
from .grok_agent import GrokAgent
from .gemini_agent import GeminiAgent


def create_llm_agent(model_config: dict) -> LLMAgent:
    provider = model_config.get('provider', '').lower()
    
    if provider == 'openai':
        return OpenAIAgent(model_config)
    elif provider == 'deepseek':
        return DeepSeekAgent(model_config)
    elif provider == 'yandexgpt':
        return YandexGPTAgent(model_config)
    elif provider == 'grok':
        return GrokAgent(model_config)
    elif provider == 'gemini':
        return GeminiAgent(model_config)
    else:
        raise ValueError(f'Unsupported provider: {provider}.')


__all__ = [
    'LLMAgent',
    'OpenAIAgent',
    'DeepSeekAgent',
    'YandexGPTAgent',
    'GrokAgent',
    'GeminiAgent',
    'create_llm_agent'
]
