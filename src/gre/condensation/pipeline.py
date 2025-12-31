from pathlib import Path
from typing import Optional

from gre.logger.logger import get_logger
from gre.condensation.base import CondensationPipeline, LLMProvider, ResponseValidator


class ReviewCondensationPipeline(CondensationPipeline):
    def __init__(
        self, 
        llm: LLMProvider, 
        validator: ResponseValidator, 
        prompt_path: str = 'prompts/review_condense.txt'
    ):
        self.llm = llm
        self.validator = validator
        self.prompt_template = self._load_prompt(prompt_path)
        self.logger = get_logger(self.__class__.__name__)


    def _load_prompt(self, path: str) -> str:
        try:
            with open(path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            self.logger.error(f'Prompt file not found at {path}')
            raise
        

    async def arun(self, input_text: str) -> str:
        '''
        Runs the condensation process asynchronously: 
        1. Formats the prompt with input text.
        2. Calls LLM.
        3. Validates response.
        '''
        if not input_text or not input_text.strip():
            self.logger.warning('Empty input text provided.')
            return ''

        # Format the prompt
        # Assuming the prompt has a placeholder {input_text}
        try:
            formatted_prompt = self.prompt_template.replace('{input_text}', input_text)
        except Exception as e:
            self.logger.error(f'Error formatting prompt: {e}')
            raise
        
        # Generate with retries handled by the provider
        # frequency_penalty to reduce repetition
        # temperature=0.0 for deterministic structure
        response = await self.llm.agenerate(
            formatted_prompt, 
            temperature=0.0,
            frequency_penalty=0.5
        )
        
        # Clean response
        cleaned_response = self.validator.clean(response)

        # Validate
        if not self.validator.validate(cleaned_response):
            self.logger.warning('LLM response failed validation. Returning raw response but marked as invalid in logs.')
            # Depending on policy, we might retry or return valid part. 
            # For now returning the response but logging the failure.
        
        return cleaned_response
