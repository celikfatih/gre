import re

from cleaners.base import BaseCleaner


class InlineReferenceCleaner(BaseCleaner):
    def __init__(self, min_block_size: int = 3):
        super().__init__()
        self.min_block_size = min_block_size
    

    def clean(self, text: str) -> str:
        lines = text.split('\n')

        start_idx = int(len(lines) * 0.7)
        tail = lines[start_idx:]

        ref_indices: list[int] = []

        for i, line in enumerate(tail):
            if re.match(r'^\s*\[\d+\]\s+', line):
                ref_indices.append(start_idx + i)

        
        processed_text = text
        if len(ref_indices) >= self.min_block_size:
            cut_index = min(ref_indices)
            self.log_info('Truncating inline references | starting line=%d | lines removed=%d', cut_index + 1, len(lines) - cut_index)
            processed_text = '\n'.join(lines[:cut_index])
        elif ref_indices:
             self.log_debug('Found candidates=%d fewer than threshold=%d', len(ref_indices), self.min_block_size)

        # Remove inline citations like [1], [1, 2], [1-3]
        # Regex explanation:
        # \[          Literal [
        # \d+         One or more digits
        # (?:         Non-capturing group for subsequent numbers
        #   [,\-]     Comma or dash separator
        #   \s*       Optional whitespace
        #   \d+       Next number
        # )*          Repeat 0 or more times
        # \]          Literal ]
        pattern = r'\[\d+(?:[,\-]\s*\d+)*\]'
        cleaned_text, count = re.subn(pattern, '', processed_text)
        
        if count > 0:
            self.log_info('Removed inline citations | count=%d', count)
            
        return cleaned_text