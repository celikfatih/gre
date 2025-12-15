from collections import Counter, defaultdict
import re
from cleaners.base import BaseCleaner


class HeaderFooterCleaner(BaseCleaner):
    PAGE_RE = re.compile(r"(=== PAGE \d+ ===)")


    def __init__(self, min_repeats: int = 3, boundary_lines: int = 3) -> None:
        super().__init__()
        self.min_repeats = min_repeats
        self.boundary_lines = boundary_lines
    

    def clean(self, text: str) -> str:
        pages = self._split_pages(text)
        candidate_lines: list[str] = []
        line_positions: defaultdict[str, list[int]] = defaultdict(list)

        for page_idx, (_, page_body) in enumerate(pages):
            lines = [l.strip() for l in page_body.split('\n') if l.strip()]
            boundaries = (
                lines[: self.boundary_lines]
                + lines[-self.boundary_lines :]
            )

            for line in boundaries:
                candidate_lines.append(line)
                line_positions[line].append(page_idx)
        
        frequency = Counter(candidate_lines)

        removable = {
            line
            for line, count in frequency.items()
            if count >= self.min_repeats
        }

        for line in removable:
            self.log_info(
                'Header/Footer candidate confirmed | repeats=%d | pages=%s | text=\'%s\'',
                frequency[line],
                line_positions[line],
                line[:120]
            )

        cleaned_pages: list[str] = []
        removed_count = 0
        total_lines = 0

        for page_header, page_body in pages:
            # Sort removable lines by length (descending) to match longest headers first
            sorted_removable = sorted(list(removable), key=len, reverse=True)

            # Apply replacement for each candidate
            cleaned_body = page_body
            for candidate in sorted_removable:
                if candidate in cleaned_body:
                    cleaned_body = cleaned_body.replace(candidate, '')
                    removed_count += 1 # Count could be inaccurate if multiple per page, but sufficient for ratio
            
            # Clean up extra newlines that might be left behind
            lines = [l.strip() for l in cleaned_body.split('\n') if l.strip()]
            page_text = '\n'.join(lines)

            if page_header:
                cleaned_pages.append(f'{page_header}\n{page_text}')
            else:
                cleaned_pages.append(page_text)

        removed_ratio = removed_count / max(total_lines, 1)
        if removed_ratio > 0.2:
            self.log_warning(
                'High header/footer removal ratio | removed ratio=%.2f',
                removed_ratio
            )
        
        return '\n'.join(cleaned_pages)
        
    
    def _split_pages(self, text: str) -> list[tuple[str, str]]:
        """
        Returns: List of (page_header, page_content)
        """
        parts = self.PAGE_RE.split(text)

        if len(parts) == 1:
            return [('', text)]
        
        pages: list[tuple[str, str]] = []
        it = iter(parts)

        for part in it:
            if self.PAGE_RE.match(part):
                header = part.strip()
                content = next(it, '')
                pages.append((header, content))
        
        return pages