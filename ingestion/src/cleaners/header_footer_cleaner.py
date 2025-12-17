from collections import Counter
import re
from difflib import SequenceMatcher
from typing import List, Tuple, Set

from cleaners.base import BaseCleaner


class HeaderFooterCleaner(BaseCleaner):
    PAGE_RE = re.compile(r"(=== PAGE \d+ ===)")

    def __init__(self, min_repeats: int = 3, boundary_lines: int = 3) -> None:
        super().__init__()
        self.min_repeats = min_repeats
        self.boundary_lines = boundary_lines

    def clean(self, text: str) -> str:
        pages = self._split_pages(text)
        candidates = self._find_candidates(pages)
        
        # Determine normalized forms of candidates
        norm_candidates = {self._normalize(c): c for c in candidates}
        
        cleaned_pages = []
        
        for page_header, page_body in pages:
            cleaned_text = self._clean_page(page_body, norm_candidates)
            
            if page_header:
                cleaned_pages.append(f"{page_header}\n{cleaned_text}")
            else:
                cleaned_pages.append(cleaned_text)
                
        return "\n".join(cleaned_pages)

    def _find_candidates(self, pages: List[Tuple[str, str]]) -> Set[str]:
        boundary_lines = []
        # Sample lines for candidate detection
        for _, body in pages:
            lines = [l.strip() for l in body.splitlines() if l.strip()]
            boundary_lines.extend(lines[:self.boundary_lines])
            boundary_lines.extend(lines[-self.boundary_lines:])
            
        frequency = Counter(boundary_lines)
        valid_candidates = {
            line for line, count in frequency.items() 
            if count >= self.min_repeats
        }
        
        for cand in valid_candidates:
             self.logger.info("Candidate found: '%s' (repeats=%d)", cand[:50], frequency[cand])
             
        return valid_candidates

    def _clean_page(self, text: str, norm_candidates: dict[str, str]) -> str:
        lines = text.splitlines()
        if not lines:
            return text
            
        # 1. Clean Top
        clean_start_idx = 0
        for i in range(min(len(lines), self.boundary_lines)):
            original = lines[i]
            if not original.strip():
                clean_start_idx = i + 1
                continue

            # Check for page number artifacts first
            if re.search(r"^\W*\]\d+\[\W*$", original):
                 self.logger.info("Removed page number artifact: '%s'", original[:50])
                 clean_start_idx = i + 1
                 continue
                
            cleaned_line = self._remove_artifact(original, norm_candidates)
            
            if cleaned_line != original:
                # Artifact found and removed
                if not cleaned_line.strip():
                    self.logger.info("Removed header line: '%s'", original[:50])
                    clean_start_idx = i + 1
                    continue
                else:
                    self.logger.info("Trimmed merged header: '%s' -> '%s'", original[:50], cleaned_line[:50])
                    lines[i] = cleaned_line
                    # Stop after modifying a merged line
                    clean_start_idx = i
                    break
            else:
                # No artifact found, stop
                break

        # 2. Clean Bottom
        clean_end_limit = len(lines)
        for i in range(len(lines) - 1, max(len(lines) - 1 - self.boundary_lines, -1), -1):
            original = lines[i]
            if not original.strip():
                clean_end_limit = i
                continue

            # Check for page number artifacts first
            if re.search(r"^\W*\]\d+\[\W*$", original):
                 self.logger.info("Removed page number artifact: '%s'", original[:50])
                 clean_end_limit = i
                 continue

            cleaned_line = self._remove_artifact(original, norm_candidates)
            
            if cleaned_line != original:
                if not cleaned_line.strip():
                    self.logger.info("Removed footer line: '%s'", original[:50])
                    clean_end_limit = i
                else:
                    self.logger.info("Trimmed merged footer: '%s' -> '%s'", original[:50], cleaned_line[:50])
                    lines[i] = cleaned_line
                    # If we trimmed it, we keep it but don't look further up (usually)
                    clean_end_limit = i + 1
                    break
            else:
                break
                
        kept_lines = lines[clean_start_idx:clean_end_limit]
        return "\n".join(kept_lines).strip()

    def _remove_artifact(self, line: str, norm_candidates: dict[str, str]) -> str:
        """
        Uses Longest Common Substring (LCS) to find and remove significant
        overlaps between the line and any candidate.
        """
        norm_line = self._normalize(line)
        if len(norm_line) < 5: 
            return line
            
        # Check for page number artifacts like ]27[
        # if re.search(r"^\W*\]\d+\[\W*$", line):
        #      return ""
            
        best_match_ratio = 0
        best_lcs_block = None
        
        # Find best overlapping candidate
        for norm_cand in norm_candidates:
            # Quick check: is the norm_line strictly contained? 
            # Or is norm_cand contained in norm_line?
            # Or do they share a big chunk?
            
            # Using SequenceMatcher to find the longest common block
            matcher = SequenceMatcher(None, norm_line, norm_cand)
            match = matcher.find_longest_match(0, len(norm_line), 0, len(norm_cand))
            
            # Use raw length of overlap as metric
            # If overlap is significant (e.g. > 12 chars), we consider it a match
            if match.size > 12:
                # We found a significant overlap. 
                # Now we need to map normalized indices back to original string to cut it.
                cleaned = self._excise_span(line, match.a, match.a + match.size)
                
                # Residue Check: If we removed > 40% of the line (remaining is < 60%), 
                # just kill the whole line to avoid leaving "Journal..." type artifacts.
                if len(cleaned) < 0.6 * len(line):
                    return ""
                    
                return cleaned
                
        return line

    def _excise_span(self, original: str, norm_start: int, norm_end: int) -> str:
        """
        Maps normalized start/end indices back to original string indices and removes the span.
        """
        norm_idx = 0
        orig_start = -1
        orig_end = -1
        
        # Iterate original string to find mapping
        for i, char in enumerate(original):
            if char.isspace():
                continue
                
            # If we are at the start of the match
            if norm_idx == norm_start:
                orig_start = i
            
            # Increment normalized index
            norm_idx += 1
            
            # If we just finished the match
            if norm_idx == norm_end:
                orig_end = i + 1
                break
        
        if orig_start != -1 and orig_end != -1:
            # Cut it out
            return (original[:orig_start] + original[orig_end:]).strip()
            
        return original

    def _normalize(self, text: str) -> str:
        return re.sub(r"\s+", "", text).lower()

    def _split_pages(self, text: str) -> List[Tuple[str, str]]:
        parts = self.PAGE_RE.split(text)
        if len(parts) == 1:
            return [("", text)]
        
        pages = []
        it = iter(parts)
        for part in it:
            if self.PAGE_RE.match(part):
                header = part.strip()
                content = next(it, "")
                pages.append((header, content))
        return pages