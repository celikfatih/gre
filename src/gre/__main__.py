from gre.ingestion.main import run
from gre.condensation.main import run as run_condensation
from gre.config.config import ConfigLoader
from gre.logger.logger import get_logger


def get_config():
    try:
        shared_config = ConfigLoader()
        return shared_config
    except Exception as e:
        logger.critical(f'Failed to load configuration: {e}')
        return


if __name__ == '__main__':
    config = get_config()
    run(config.get_ingestion_input_dir(), config.get_ingestion_output_dir())
    run_condensation(config.get_ingestion_output_dir(), config.get_condensation_output_dir(), config.get_condensation_prompt_path())