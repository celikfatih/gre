import re

from cleaners.base import BaseCleaner

STOP_MARKERS = [
    r"\babstract\b",
    r"\bintroduction\b",
]

METADATA_PATTERNS = [
    r"corresponding author",
    r"e-mail",
    r"received",
    r"accepted",
    r"doi",
    r"©",
    r"elsevier",
    r"ieee",
    r"authorized licensed use",
]


class FrontMatterCleaner(BaseCleaner):
    def __init__(self) -> None:
        super().__init__()

    
    def clean(self, text: str) -> str:
        lines = text.splitlines()
        output: list[str] = []
        stop_found: bool = False

        for idx, line in enumerate(lines):
            if any(re.search(m, line, re.IGNORECASE) for m in STOP_MARKERS):
                output.append(line)
                output.extend(line[idx + 1:])
                self.log_info(
                    'Front-matter end detected | line_no=%d | trigger=\'%s\'',
                    idx,
                    line[:120])
                stop_found = True
                break
            
            if any(re.search(p, line, re.IGNORECASE) for p in METADATA_PATTERNS):
                self.logger.info(
                    'Front-matter metadata removed | line_no=%d | text="%s"',
                    idx,
                    line[:120]
                )
                continue

            output.append(line)
        
        if not stop_found:
            self.log_warning('Front-matter stop marker not found')

        
        return '\n'.join(output)
