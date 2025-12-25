import re

from gre.ingestion.cleaners.base import BaseCleaner


PATTERNS = [
    r"(?im)\bREFERENCES\s*$",
    r"(?im)\bBIBLIOGRAPHY\s*$"
]


class ReferenceCleaner(BaseCleaner):
    def __init__(self):
        super().__init__()

    def clean(self, text: str) -> str:
        for pattern in PATTERNS:
            # We want to find *all* matches because the first one might be a false positive
            # e.g. "We discuss References in Section 2... \nReferences"
            for match in re.finditer(pattern, text):
                # Verify content *after* the match candidate
                candidate_start = match.start()
                following_text = text[match.end():]
                
                # Check for Citation Density
                # Look for at least 2 markers of type [1], [12], (1) or 1. 2.
                # We limit the search to the first 1000 chars to avoid scanning entire doc
                search_window = following_text[:1000]
                
                citation_markers = len(re.findall(r"\[\d+\]", search_window))
                numbered_list = len(re.findall(r"^\s*\d+\.\s", search_window, re.MULTILINE))
                
                if citation_markers >= 2 or numbered_list >= 2:
                    self.log_info('Reference section found (verified) | index=%d', candidate_start)
                    truncated_text = text[:candidate_start]
                    self.log_info('Reference section truncated | chars=%d', len(text) - len(truncated_text))
                    return truncated_text
                else:
                    self.log_info('Potential reference match skipped (validation failed) | index=%d', candidate_start)
        
        return text