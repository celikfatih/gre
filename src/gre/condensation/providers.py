from litellm import completion
from tenacity import retry, stop_after_attempt, wait_exponential

from gre.logger.logger import get_logger
from gre.condensation.base import LLMProvider
from gre.config.llm_config import LLMConfig


class LiteLLMProvider(LLMProvider):
    def __init__(self, config: LLMConfig):
        self.config = config
        self.logger = get_logger(self.__class__.__name__)


    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def generate(self, prompt: str) -> str:
        try:
            self.logger.info(f'Generating content with model: {self.config.model}')
            response = completion(
                model=self.config.model,
                messages=[{'role': 'user', 'content': prompt}],
                api_key=self.config.api_key,
                api_base=self.config.api_base,
                api_version=self.config.api_version,
            )
            return response.choices[0].message.content
        except Exception as e:
            self.logger.error(f'LiteLLM completion failed: {e}')
            raise e
