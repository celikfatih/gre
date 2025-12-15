from pdf_loader import PdfLoader
from text_writer import TextWriter
from processor import PdfIngestionProcessor
from logger.logger import get_logger


logger = get_logger(__name__)


class BatchIngestionRunner:
    def __init__(self, loader: PdfLoader, processor: PdfIngestionProcessor, writer: TextWriter) -> None:
        self.loader = loader
        self.processor = processor
        self.writer = writer
    

    def run(self):
        logger.info('Ingestion started')
        for pdf in self.loader.list_items():
            cleaned_text = self.processor.process(pdf)
            self.writer.write(pdf.stem, cleaned_text)
        logger.info('Ingestion finished')