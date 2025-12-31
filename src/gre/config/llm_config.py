import os
import re
import yaml
from pathlib import Path
from typing import Any, Dict, Optional

from gre.logger.logger import get_logger
from graphrag.config.models.language_model_config import LanguageModelConfig
from graphrag.config.enums import AuthType, ModelType, AsyncType


class LLMConfigLoader:
    def __init__(self, settings_path: str = 'settings.yaml'):
        self.logger = get_logger(self.__class__.__name__)
        self.settings_path = Path(settings_path)
        self.config: Dict[str, Any] = self._load_config()


    def _load_config(self) -> Dict[str, Any]:
        if not self.settings_path.exists():
            self.logger.error(f'Settings file not found at {self.settings_path}')
            raise FileNotFoundError(f'Settings file not found at {self.settings_path}')

        with open(self.settings_path, 'r') as f:
            content = f.read()

        # Simple environment variable substitution
        # pattern matches ${VAR_NAME}
        pattern = re.compile(r'\$\{([^}^{]+)\}')
        
        def replace_env(match):
            var_name = match.group(1)
            return os.environ.get(var_name, match.group(0))

        content = pattern.sub(replace_env, content)
        
        try:
            return yaml.safe_load(content)
        except yaml.YAMLError as e:
            self.logger.error(f'Error parsing YAML file: {e}')
            raise


    def get_llm_config(self, model_id: str = 'default_chat_model') -> LanguageModelConfig:
        '''
        Extracts LLM configuration for a specific model ID.
        '''
        try:
            models_config = self.config.get('models', {})
            model_config = models_config.get(model_id, {})
            
            if not model_config:
                 self.logger.warning(f'No configuration found for model_id: {model_id}, using defaults/empty.')

            return LanguageModelConfig(
                model=model_config.get('model', 'gpt-4-turbo-preview'), # Fallback default
                api_key=model_config.get('api_key'),
                api_base=model_config.get('api_base'),
                api_version=model_config.get('api_version'),
                max_retries=model_config.get('max_retries', 10),
                tokens_per_minute=model_config.get('tokens_per_minute'),
                requests_per_minute=model_config.get('requests_per_minute'),
                model_provider=model_config.get('model_provider', 'openai'),
                auth_type=AuthType(model_config.get('auth_type', 'api_key')),
                async_mode=AsyncType(model_config.get('async_mode', 'threaded')),
                concurrent_requests=model_config.get('concurrent_requests', 25),
                retry_strategy=model_config.get('retry_strategy', 'exponential_backoff'),
                type=ModelType.Chat # Assuming we are loading chat models
            )
        except Exception as e:
            self.logger.error(f'Error extracting LLM config: {e}')
            raise
