from pathlib import Path

from text_extractor import TextExtractor
from layout_repairer import LayoutRepairer
from line_normalizer import LineNormalizer
from logger.logger import get_logger
from cleaners.base import BaseCleaner


class PdfIngestionProcessor:
    def __init__(self, extractor: TextExtractor, repairer: LayoutRepairer, cleaners: list[BaseCleaner], normalizer: LineNormalizer) -> None:
        self.logger = get_logger(self.__class__.__name__)
        self.extractor = extractor
        self.repairer = repairer
        self.cleaners = cleaners
        self.normalizer = normalizer
    

    def process(self, pdf_path: Path):
        self.logger.info('Reading PDF: %s', pdf_path.name)
        text = self.extractor.extract(pdf_path) 

        if not text.strip():
            self.logger.warning(
                'PDF extracted but empty content detected | file=%s',
                pdf_path.name
            )
        
        self.logger.info(
            'PDF loaded successfully | file=%s | chars=%d',
            pdf_path.name,
            len(text),
        )

        self.repairer.set_source(pdf_path.name)
        text = self.repairer.process(text)

        for cleaner in self.cleaners:
           cleaner.set_source(pdf_path.name)
           text = cleaner.run(text)

        text = self.normalizer.normalize(text)
        return text