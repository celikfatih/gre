class LineNormalizer:
    def normalize(self, text: str) -> str:
        lines = text.split('\n')
        normalized: list[str] = []

        i = 0
        while i < len(lines):
            current = lines[i].strip()

            if (
                i + 1 < len(lines)
                and current
                and not current.endswith('.')
                and lines[i + 1].strip()
                and lines[i + 1].strip()[0].islower()
            ):
                merged = current + ' ' + lines[i + 1].strip()
                normalized.append(merged)
                i += 2
            else: 
                normalized.append(current)
                i += 1
        
        return '\n'.join(normalized)