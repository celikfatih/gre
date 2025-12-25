from gre.ingestion.loader.pdf_loader import PdfLoader
from gre.ingestion.post.text_writer import TextWriter
from gre.ingestion.processor import PdfIngestionProcessor
from gre.logger.logger import get_logger


class BatchIngestionRunner:
    def __init__(self, loader: PdfLoader, processor: PdfIngestionProcessor, writer: TextWriter) -> None:
        self.loader = loader
        self.processor = processor
        self.writer = writer
        self.logger = get_logger(self.__class__.__name__)
    

    def run(self):
        self.logger.info('Ingestion started')
        for pdf in self.loader.list_items():
            cleaned_text = self.processor.process(pdf)
            self.writer.write(pdf.stem, cleaned_text)
        self.logger.info('Ingestion finished')