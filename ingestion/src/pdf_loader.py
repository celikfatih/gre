from pathlib import Path
import time
from logger.logger import get_logger


logger = get_logger(__name__)


class PdfLoader:
    def __init__(self, input_dir: Path) -> None:
        self.input_dir = input_dir
    
    
    def list_items(self) -> list[Path]:
        """
        Loads all PDF files under the given path (input_dir).
        """

        start_time = time.time()

        logger.info(
            "PDF loading started | input_path=%s",
            self.input_dir,
        )

        if not self.input_dir.exists():
            logger.error("Input dir does not exist: %s", self.input_dir)
            return []
        
        pdf_files = list(self.input_dir.rglob("*.pdf"))

        logger.info(
            "PDF loading completed | total_pdfs=%d | duration=%.2fs",
            len(pdf_files),
            time.time() - start_time,
        )
        
        return pdf_files[:1]