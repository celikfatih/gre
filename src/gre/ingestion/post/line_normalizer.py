import re

from gre.logger.logger import get_logger


class LineNormalizer:
    def __init__(self) -> None:
        self.logger = get_logger(self.__class__.__name__)
        self.source_id: str | None = None


    def normalize(self, text: str) -> str:
        original_len = len(text)
        self.logger.info('file=%s | Normalization started | input_chars=%d', self.source_id, original_len)

        # Pre-filter: Remove page separator artifacts
        lines = text.split('\n')
        filtered_lines = []
        page_separators_removed = 0

        for line in lines:
            if re.match(r'^=== PAGE \d+ ===$', line.strip()):
                page_separators_removed += 1
                continue
            filtered_lines.append(line)
            
        lines = filtered_lines
        normalized: list[str] = []

        i = 0
        hyphens_fixed = 0
        paragraphs_merged = 0

        while i < len(lines):
            current = lines[i].strip()
            
            # Preserve empty lines as paragraph breaks
            if not current:
                normalized.append('')
                i += 1
                continue

            # Look ahead
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                
                # Scenario 1: De-hyphenation (e.g., "environ-" + "ment")
                if current.endswith('-') and next_line:
                    merged = current[:-1] + next_line
                    normalized.append(merged)
                    i += 2
                    hyphens_fixed += 1
                    continue
                
                # Scenario 2: Sentence merge (no terminal punct + lowercase next)
                # Ensure next line is not empty (paragraph break)
                if (
                    next_line 
                    and not current.endswith(('.', '?', '!')) 
                    and next_line[0].islower()
                ):
                    merged = current + ' ' + next_line
                    normalized.append(merged)
                    i += 2
                    paragraphs_merged += 1
                    continue

            normalized.append(current)
            i += 1
        
        result = '\n'.join(normalized)
        
        self.logger.info(
            'file=%s | Normalization finished | output_chars=%d | pages_removed=%d | hyphens_fixed=%d | merged_lines=%d',
            self.source_id,
            len(result),
            page_separators_removed,
            hyphens_fixed,
            paragraphs_merged
        )
        return result


    def set_source(self, source_id: str) -> None:
        self.source_id = source_id