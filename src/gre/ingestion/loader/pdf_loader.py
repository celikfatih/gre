from pathlib import Path
import time
from gre.logger.logger import get_logger


class PdfLoader:
    def __init__(self, input_dir: Path) -> None:
        self.input_dir = input_dir
        self.logger = get_logger(self.__class__.__name__)
    
    
    def list_items(self) -> list[Path]:
        '''
        Loads all PDF files under the given path (input_dir).
        '''

        start_time = time.time()

        self.logger.info(
            'PDF loading started | input_path=%s',
            self.input_dir,
        )

        if not self.input_dir.exists():
            logger.error('Input dir does not exist: %s', self.input_dir)
            return []
        
        pdf_files = list(self.input_dir.rglob('*.pdf'))

        self.logger.info(
            'PDF loading completed | total_pdfs=%d | duration=%.2fs',
            len(pdf_files),
            time.time() - start_time,
        )
        
        return pdf_files[:1]