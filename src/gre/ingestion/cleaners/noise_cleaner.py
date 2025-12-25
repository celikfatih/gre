import re

from gre.ingestion.cleaners.base import BaseCleaner


class NoiseCleaner(BaseCleaner):
    def __init__(self):
        super().__init__()

    def clean(self, text: str) -> str:
        lines = text.split('\n')
        cleaned_lines = []
        removed_count = 0

        for line in lines:
            stripped = line.strip()
            
            # 1. Empty lines (preserve structure, or clean? existing logic usually handles this, 
            # but let's just focus on artifacts. If we return empty string it gets filtered later usually,
            # but here we are rebuilding the string)
            # Actually, standard is to preserve empty lines if they were paragraphs, but artifacts should go.
            
            if not stripped:
                cleaned_lines.append(line)
                continue

            # 2. Check for Page Number Artifacts like ]85[ or ] 85 [
            # Also simple bracketed numbers if they are invalid? No, inline refs are valid.
            # User specifically showed ]85[.
            if re.match(r'^\]\s*\d+\s*\[$', stripped):
                self.log_debug('Removing page artifact line = \'%s\'', stripped)
                removed_count += 1
                continue

            # 3. Check for Symbol-only lines
            # If line has NO alphanumeric characters (a-z, 0-9), it's likely noise like * * * or •
            # Exception: punctuation-only lines might be rare valid separators, but user wants them gone.
            if not re.search(r'[a-zA-Z0-9]', stripped):
                 self.log_debug('Removing symbol-only line = \'%s\'', stripped)
                 removed_count += 1
                 continue

            cleaned_lines.append(line)

        if removed_count > 0:
            self.log_info('Removed noise lines | count=%d', removed_count)
            
        return '\n'.join(cleaned_lines)
