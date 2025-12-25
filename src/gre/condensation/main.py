import argparse
from pathlib import Path

from gre.logger.logger import get_logger
from gre.condensation.providers import LiteLLMProvider
from gre.config.llm_config import LLMConfigLoader
from gre.condensation.validators import ReviewArticleValidator
from gre.condensation.pipeline import ReviewCondensationPipeline
from gre.condensation.batch_processor import BatchCondensationProcessor


logger = get_logger(__name__)


def run(input_dir: str, output_dir: str, prompt_path: str):
    # Initialize components
    try:
        config_loader = LLMConfigLoader() # Keeps loading LLM settings from settings.yaml
        llm_config = config_loader.get_llm_config()
        
        llm_provider = LiteLLMProvider(config=llm_config)
        validator = ReviewArticleValidator()
        
        pipeline = ReviewCondensationPipeline(
            llm=llm_provider, 
            validator=validator,
            prompt_path=prompt_path
        )
        
        processor = BatchCondensationProcessor(pipeline=pipeline)
        
    except Exception as e:
        logger.critical(f'Failed to initialize pipeline components: {e}')
        return

    # Run Execution
    processor.process_directory(input_dir, output_dir)
