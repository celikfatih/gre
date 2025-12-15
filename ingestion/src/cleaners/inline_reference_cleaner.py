import re


class InlineReferenceCleaner:
    def __init__(self, min_block_size: int = 3):
        self.min_block_size = min_block_size
    

    def clean(self, text: str) -> str:
        lines = text.split('\n')

        start_idx = int(len(lines) * 0.7)
        tail = lines[start_idx:]

        ref_indices: list[int] = []

        for i, line in enumerate(tail):
            if re.match(r'^\s*\[\d+\]\s+', line):
                ref_indices.append(start_idx + i)

        
        if len(ref_indices) < self.min_block_size:
            return text

        cut_index = min(ref_indices)
        return '\n'.join(lines[:cut_index])