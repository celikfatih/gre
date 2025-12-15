import re

from cleaners.base import BaseCleaner


BODY_START_RE = re.compile(r'\b(relevant|this|these|in this|we|our|the study|the paper|results|findings|method|approach|information)\b', re.IGNORECASE)
YEAR_RE = re.compile(r'\b(19|20)\d{2}\b')
HEADER_HINT_RE = re.compile(r'(et al\.|journal|transactions|ieee|vol\.|volume|\(\d{4}\)\d+|[A-Z][a-z]+[A-Z][A-Za-z]+)', re.IGNORECASE)


class LineNormalizerCleaner(BaseCleaner):
    def __init__(self) -> None:
        super().__init__()


    def clean(self, text: str) -> str:
        output: list[str] = []

        for line in text.split('\n'):
            split = self._maybe_split_header_body(line)
            output.extend(split)

        return '\n'.join(output)
            

    
    def _maybe_split_header_body(self, line: str) -> list[str]:
        if len(line) < 90:
            return [line]

        if not YEAR_RE.search(line):
            return [line]
        
        if not HEADER_HINT_RE.search(line):
            return [line]
        
        for m in BODY_START_RE.finditer(line):
            if m.start() > 50:
                header = line[:m.start()].rstrip()
                body = line[m.start():].lstrip()

                self.log_info(
                    'Line split: header-body detected | header_len=%d | body_start=\'%s\'',
                    len(header),
                    body[:40]
                )

                return [header, body]
        
        return [line]
        