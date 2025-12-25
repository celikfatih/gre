import logging
from pathlib import Path


_initialized = False


def get_logger(name: str) -> logging.Logger:
    global _initialized

    if not _initialized:
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            handlers=[
                logging.FileHandler(log_dir / 'preprocessing.log'),
                logging.StreamHandler()
            ]
        )

        _initialized = True
    
    return logging.getLogger(name)