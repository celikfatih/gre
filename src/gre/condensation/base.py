from abc import ABC, abstractmethod


class LLMProvider(ABC):
    @abstractmethod
    async def agenerate(self, prompt: str) -> str:
        '''Generates text from the LLM asynchronously.'''
        pass


class ResponseValidator(ABC):
    @abstractmethod
    def validate(self, response: str) -> bool:
        '''Validates the LLM response format.'''
        pass
    
    @abstractmethod
    def clean(self, response: str) -> str:
        '''Cleans/fixes the response if possible, or returns the original.'''
        pass


class CondensationPipeline(ABC):
    @abstractmethod
    async def arun(self, input_text: str) -> str:
        '''Runs the condensation process on input text asynchronously.'''
        pass
