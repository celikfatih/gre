import re
from cleaners.base import BaseCleaner


class HeaderNormalizerCleaner(BaseCleaner):
    def __init__(self) -> None:
        super().__init__()
        

    def clean(self, text: str) -> str:
        original = text

        text = re.sub(
            r'(?:\b[A-Za-z]\s){4,}[A-Za-z]',
            self._merge_spaces,
            text
        )   

        if text != original:
            self.log_info('Spaces-character words normalized')
        
        text = re.sub(
            r'\b([A-Z]{5,})\b',
            self._split_knows_sections,
            text
        )
        
        return text


    def _merge_spaces(self, match: re.Match[str]):
        return match.group(0).replace(' ', '')
    

    def _split_knows_sections(self, match: re.Match[str]):
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

        if result != token:
            self.log_info(
                'Section header split | before=\'%s\' | after=\'%s\'',
                token,
                result.strip()
            )

        return result.strip()