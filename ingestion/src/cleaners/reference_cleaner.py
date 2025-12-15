import re


class ReferenceCleaner:
    PATTERNS = [
        r"\nREFERENCES\b",
        r"\nReferences\b",
        r"\nBIBLIOGRAPHY\b"
    ]

    def clean(self, text: str) -> str:
        for pattern in self.PATTERNS:
            match = re.search(pattern, text)
            if match:
                return text[:match.start()]
        
        return text