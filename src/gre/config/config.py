import yaml
from pathlib import Path
from typing import Any, Dict, Optional
from gre.logger.logger import get_logger


class ConfigLoader:
    def __init__(self, config_path: Optional[str] = None):
        self.logger = get_logger(self.__class__.__name__)
        if config_path:
             self.config_path = Path(config_path)
        else:
            # Default to config.yaml in the same directory as this file
            self.config_path = Path(__file__).cwd() / 'preprocessing.yaml'
            self.logger.info(f'Using config file at {self.config_path}')
            
        self.config: Dict[str, Any] = self._load_config()


    def _load_config(self) -> Dict[str, Any]:
        if not self.config_path.exists():
            self.logger.warning(f'Config file not found at {self.config_path}. Using empty config.')
            return {}

        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            self.logger.error(f'Error parsing YAML file: {e}')
            raise


    def get_ingestion_input_dir(self, default: str = 'input/pdfs') -> str:
        return self.config.get('ingestion', {}).get('input_dir', default)


    def get_ingestion_output_dir(self, default: str = 'output/cleaned_texts') -> str:
        return self.config.get('ingestion', {}).get('output_dir', default)
        

    def get_condensation_output_dir(self, default: str = 'output/condensed_texts') -> str:
        return self.config.get('condensation', {}).get('output_dir', default)


    def get_condensation_prompt_path(self, default: str = 'prompts/review_condense.txt') -> str:
        return self.config.get('condensation', {}).get('prompt_path', default)
