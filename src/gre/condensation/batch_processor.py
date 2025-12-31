from pathlib import Path
from typing import Optional, List
from gre.logger.logger import get_logger
from gre.condensation.pipeline import ReviewCondensationPipeline


import asyncio

class BatchCondensationProcessor:
    def __init__(self, pipeline: ReviewCondensationPipeline):
        self.pipeline = pipeline
        self.logger = get_logger(self.__class__.__name__)


    async def aprocess_directory(self, input_dir: str, output_dir: str) -> None:
        '''
        Processes all text files in the input directory and saves the results to the output directory asynchronously.
        '''
        input_path = Path(input_dir)
        output_path = Path(output_dir)

        if not input_path.exists():
            self.logger.error(f'Input directory does not exist: {input_path}')
            return

        self.logger.info(f'Ensuring output directory exists: {output_path}')
        output_path.mkdir(parents=True, exist_ok=True)

        files = list(input_path.glob('*.txt'))
        self.logger.info(f'Found {len(files)} files to process in {input_path}')

        # We can process files in parallel using gather, or with a semaphore to limit concurrency if needed.
        # GraphRag config has 'concurrent_requests', but that's per LLM instance usually.
        # Let's process them concurrently.
        tasks = [self._aprocess_single_file(file_path, output_path) for file_path in files]
        await asyncio.gather(*tasks)


    async def _aprocess_single_file(self, file_path: Path, output_path: Path) -> None:
        try:
            self.logger.info(f'Processing file: {file_path.name}')
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            condensed_content = await self.pipeline.arun(content)

            output_file = output_path / f'condensed_{file_path.name}'
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(condensed_content)

            self.logger.info(f'Saved condensed file to: {output_file}')

        except Exception as e:
            self.logger.error(f'Error processing file {file_path.name}: {e}')
