from pathlib import Path
from typing import Any

from gre.ingestion.loader.pdf_loader import PdfLoader
from gre.ingestion.loader.text_extractor import TextExtractor
from gre.logger.logger import get_logger
from gre.ingestion.post.text_writer import TextWriter
from gre.ingestion.pre.layout_repairer import LayoutRepairer
from gre.ingestion.cleaners.front_matter_cleaner import FrontMatterCleaner
from gre.ingestion.cleaners.header_footer_cleaner import HeaderFooterCleaner
from gre.ingestion.cleaners.publication_metadata_cleaner import PublicationMetadataCleaner
from gre.ingestion.cleaners.reference_cleaner import ReferenceCleaner
from gre.ingestion.cleaners.inline_reference_cleaner import InlineReferenceCleaner
from gre.ingestion.cleaners.noise_cleaner import NoiseCleaner
from gre.ingestion.post.line_normalizer import LineNormalizer
from gre.ingestion.processor import PdfIngestionProcessor
from gre.ingestion.batch_runner import BatchIngestionRunner


def run(input_dir: str, output_dir: str):
    loader = PdfLoader(Path(input_dir))
    writer = TextWriter(Path(output_dir))

    extractor = TextExtractor()
    layout_repairer = LayoutRepairer()

    cleaners: list[Any] = [
        FrontMatterCleaner(),
        HeaderFooterCleaner(),
        PublicationMetadataCleaner(),
        ReferenceCleaner(),
        InlineReferenceCleaner(),
        NoiseCleaner()
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
    
    runner.run()