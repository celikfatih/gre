from abc import ABC, abstractmethod
from logger.logger import get_logger
from typing import Any


class BaseCleaner(ABC):
    def __init__(self) -> None:
        self.logger = get_logger(self.__class__.__name__)
        self.source_id: str | None = None
    

    def run(self, text: str) -> str:
        if not text:
            self.log_warning('Cleaner received empty input')
            return text
        
        input_len = len(text)
        self.log_info(
            'Cleaner started | input chars=%d',
            input_len
        )

        output = self.clean(text)

        output_len = len(output or '')
        removed_ratio = 1 - (output_len / max(input_len, 1))

        if not output.strip():
            self.log_error(
                'Cleaner produced empty output | removed_ratio=%.2f',
                removed_ratio
            )
        else:
            self.log_info(
                'Cleaner completed | output_chars=%d | removed_ratio=%.2f',
                output_len, 
                removed_ratio
            )
        
        return output
    

    def set_source(self, source_id: str) -> None:
        self.source_id = source_id


    @abstractmethod
    def clean(self, text: str) -> str:
        pass


    def log_info(self, msg: str, *args: Any) -> None:
        if self.source_id:
            self.logger.info(f"file={self.source_id} | {msg}", *args)
        else:
            self.logger.info(msg, *args)


    def log_warning(self, msg: str, *args: Any) -> None:
        if self.source_id:
            self.logger.warning(f"file={self.source_id} | {msg}", *args)
        else:
            self.logger.warning(msg, *args)
    

    def log_error(self, msg: str, *args: Any) -> None:
        if self.source_id:
            self.logger.error(f"file={self.source_id} | {msg}", *args)
        else:
            self.logger.error(msg, *args)