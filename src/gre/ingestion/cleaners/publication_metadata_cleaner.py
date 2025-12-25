import re
from typing import Any

from gre.ingestion.cleaners.base import BaseCleaner


class PublicationMetadataCleaner(BaseCleaner):
    KEY_PATTERNS = [
        r"Manuscript\s+received",
        r"\baccepted\b",
        r"date\s+of\s+publication",
        r"date\s+of\s+current\s+version",
        r"Associate\s+Editor",
        r"Corresponding\s+author",
        r"\be-mail\b",
        r"\bGrant\b",
        r"\bsupported\s+by\b"
    ]


    def __init__(self) -> None:
        super().__init__()

    
    def clean(self, text: str) -> str:
        lines = text.split('\n')
        cleaned: list[Any] = []

        buffer: list[str] = []
        metadata_score = 0

        removed_blocks = 0
        removed_lines = 0

        def flush_buffer():
            nonlocal buffer, metadata_score, removed_blocks, removed_lines
            if metadata_score < 2:
                cleaned.extend(buffer)
                self.log_info(
                    'Metadata block kept | lines=%d score=%d',
                    len(buffer),
                    metadata_score,
                )
            else:
                removed_blocks += 1
                removed_lines += len(buffer)
                self.log_info(
                    'Metadata block removed | lines=%d score=%d',
                    len(buffer),
                    metadata_score,
                )
            buffer = []
            metadata_score = 0
        
        for line in lines:
            buffer.append(line)

            for pattern in self.KEY_PATTERNS:
                if re.search(pattern, line, re.IGNORECASE):
                    metadata_score += 1
            
            if not line.strip():
                flush_buffer()
        
        flush_buffer()

        output = '\n'.join(cleaned)

        removed_ratio = 1 - (len(output) / max(len(text), 1))

        if removed_ratio > 0.5:
            self.log_error(
                'PublicationMetadataCleaner aborted | excessive removal | removed_ratio=%.2f',
                removed_ratio
            )
            return text

        return output