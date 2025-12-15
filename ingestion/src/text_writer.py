from pathlib import Path


class TextWriter:
    def __init__(self, output_dir: Path) -> None:
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    
    def write(self, filename: str, text: str):
        path = self.output_dir / f'{filename}.txt'
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)