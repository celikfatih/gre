import re

from gre.ingestion.cleaners.base import BaseCleaner


STOP_MARKERS = [
    r'=== PAGE 2 ===',
]

METADATA_PATTERNS = [
    r'corresponding author',
    r'e-mail',
    r'received',
    r'accepted',
    r'available online',
    r'doi',
    r'©',
    r'elsevier',
    r'ieee',
    r'authorized licensed use',
    r'url:',
    r'http',
    r'ScienceDirect',
    r'journal homepage',
    r'Contents lists available at',
]


class FrontMatterCleaner(BaseCleaner):
    def __init__(self) -> None:
        super().__init__()

    
    def clean(self, text: str) -> str:
        lines = text.splitlines()
        output: list[str] = []
        stop_cleaning: bool = False

        for idx, line in enumerate(lines):
            # Safety brake: Stop cleaning after Page 1 or 500 lines
            if idx > 500 or '=== PAGE 2 ===' in line:
                stop_cleaning = True
            
            if stop_cleaning:
                output.append(line)
                continue
            
            # Remove metadata lines if they match patterns
            if any(re.search(p, line, re.IGNORECASE) for p in METADATA_PATTERNS):
                self.logger.info(
                    'Front-matter metadata removed | line_no=%d | text=\'%s\'',
                    idx,
                    line[:120]
                )
                continue

            output.append(line)
        
        return '\n'.join(output)
