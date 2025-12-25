import pdfplumber
from pathlib import Path
from gre.logger.logger import get_logger


class TextExtractor:
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)
    

    def extract(self, pdf_path: Path) -> str:
        '''
        Low-level PDF text extraction.
        '''
        pages: list[str] = []

        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text(
                    x_tolerance = 2,
                    y_tolerance = 2
                )
                if text:
                    pages.append(f'=== PAGE {i+1} ===\n{text}')
        
        return '\n'.join(pages)