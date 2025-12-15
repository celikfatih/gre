import re

from logger.logger import get_logger


HEADER_BODY_KEYS = ['Keywords:', 'Abstract', 'Highlights', 'Introduction', 'Background', 'Conclusion']
DE_HYPHEN_RE = re.compile(r'(\w+)-\n([a-z])')
LINE_UNWRAP_RE = re.compile(r'([^\.\?\!\n])\n([a-z])')


class LayoutRepairer:
    def __init__(self) -> None:
        self.logger = get_logger(self.__class__.__name__)
        self.source_id: str | None = None

    
    def process(self, text: str) -> str:
        original_len = len(text)

        self.logger.info(
            'Layout repair started | file=%s | chars=%d',
            self.source_id,
            original_len
        )

        text = self._merge_spaces(text)
        text = self._split_knows_sections(text)
        text = self._split_header_body_lines(text)
        text = self._de_hyphenation(text)
        text = self._line_unwrap(text)
        text = self._reduce_multiple_blanks(text)

        fixed_len = len(text)
        self.logger.info(
            'Layout repair finished | file=%s | chars=%d | chars_after=%d | chars_diff=%d',
            self.source_id,
            original_len,
            fixed_len,
            original_len - fixed_len
        )
        return text


    def _reduce_multiple_blanks(self, text: str) -> str:
        return re.sub(r'\n{3,}', '\n\n', text)


    def _line_unwrap(self, text: str) -> str:
        text = LINE_UNWRAP_RE.sub(lambda m: m.group(1) + ' ' + m.group(2), text)
        return text
    

    def _de_hyphenation(self, text: str) -> str:
        text = DE_HYPHEN_RE.sub(lambda m: m.group(1) + m.group(2), text)
        return text


    def _split_header_body_lines(self, text: str) -> str:
        for key in HEADER_BODY_KEYS:
            pattern = re.compile(rf'\n({re.escape(key)})', re.IGNORECASE)
            text = pattern.sub(r'\n\n\1', text)

        return text


    def _merge_spaces(self, text: str) -> str:
        original = text

        text = re.sub(
            r'(?:\b[A-Za-z]\s){4,}[A-Za-z]',
            lambda m: m.group(0).replace(' ', ''),
            text
        )   

        if text != original:
            self.logger.info('file=%s | Spaces-character words normalized', self.source_id)

        return text
    

    def _split_knows_sections(self, text: str) -> str:
        text = re.sub(
            r'\b([A-Z]{5,})\b',
            self._split_sections,
            text
        )
        return text


    def _split_sections(self, match: re.Match[str]):
        token = match.group(1)
        sections = [
            "ABSTRACT",
            "INTRODUCTION",
            "ARTICLE",
            "INFO",
            "METHOD",
            "RESULT",
            "CONCLUSION",
            "REFERENCES"
        ]

        result = token
        for sec in sections:
            result = result.replace(sec, f' {sec} ')

        result = re.sub(r'\s+', ' ', result)

        if result != token:
            self.logger.info(
                'Section header split | file=%s | before=\'%s\' | after=\'%s\'',
                self.source_id,
                token,
                result.strip()
            )

        return result.strip()


    def set_source(self, source_id: str) -> None:
        self.source_id = source_id