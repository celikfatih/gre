from pathlib import Path
from typing import Any

from pdf_loader import PdfLoader
from text_writer import TextWriter
from text_extractor import TextExtractor
from layout_repairer import LayoutRepairer
# from cleaners.front_matter_cleaner import FrontMatterCleaner
from cleaners.header_footer_cleaner import HeaderFooterCleaner
from line_normalizer import LineNormalizer
from processor import PdfIngestionProcessor
from batch_runner import BatchIngestionRunner
from logger.logger import get_logger


logger = get_logger(__name__)


INPUT_DIR = Path('input/pdfs')
OUTPUT_DIR = Path('output/cleaned_texts')

loader = PdfLoader(INPUT_DIR)
writer = TextWriter(OUTPUT_DIR)

extractor = TextExtractor()
layout_repairer = LayoutRepairer()

cleaners: list[Any] = [
    # FrontMatterCleaner()
    # LineNormalizerCleaner(),
    # HeaderNormalizerCleaner(),
    HeaderFooterCleaner(),
    # PublicationMetadataCleaner()
]
normalizer = LineNormalizer()

processor = PdfIngestionProcessor(
    extractor=extractor,
    repairer=layout_repairer,
    cleaners=cleaners,
    normalizer=normalizer
)

runner = BatchIngestionRunner(
    loader=loader,
    processor=processor,
    writer=writer
)


if __name__ == '__main__':
    runner.run()