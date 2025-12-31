import asyncio
from typing import Optional

from gre.logger.logger import get_logger
from gre.condensation.base import LLMProvider

from graphrag.language_model.factory import ModelFactory
from graphrag.config.models.language_model_config import LanguageModelConfig
from graphrag.config.enums import ModelType, AuthType


class GraphRagLLMProvider(LLMProvider):
    def __init__(self, config: LanguageModelConfig):
        self.config = config
        self.logger = get_logger(self.__class__.__name__)
        self.llm = self._create_llm()


    def _create_llm(self):
        try:
            # Create the chat model using the factory
            # self.config is already a GraphRag LanguageModelConfig
            return ModelFactory.create_chat_model(
                name=self.config.model, 
                model_type=ModelType.Chat,
                config=self.config
            )
        except Exception as e:
            self.logger.critical(f"Failed to create GraphRag LLM: {e}")
            raise


    async def agenerate(self, prompt: str) -> str:
        try:
            self.logger.info(f'Generating content with model: {self.config.model}')
            
            # LitellmChatModel.chat signature: (prompt: str, history: list | None = None, **kwargs)
            response = await self.llm.achat(prompt)


            # It seems GraphRag's LitellmChatModel returns a refined string OR a response object depending on usage
            # But based on the error 'LitellmModelResponse' object has no attribute 'strip', it returns an object.
            # Inspecting 'LitellmChatModel' earlier showed it just wraps litellm.
            # If it returns a standard litellm response or similiar, we should check attributes.
            if isinstance(response, str):
                return response
            
            # Check for output attribute (GraphRag standard response)
            if hasattr(response, 'output'):
                # it might be a string or an object like LitellmModelOutput
                output = response.output
                if isinstance(output, str):
                    return output
                if hasattr(output, 'content'):
                    return output.content
                if isinstance(output, dict) and 'content' in output:
                    return output['content']
                return str(output)

            # Check for common attributes
            if hasattr(response, 'content'):
                 return response.content

            # Try to access content. Typical OpenAI/LiteLLM response structure
            try:
                return response.choices[0].message.content
            except AttributeError:
                # Fallback if structure is different
                return str(response)

        except Exception as e:
            self.logger.error(f'GraphRag LLM completion failed: {e}')
            raise e
