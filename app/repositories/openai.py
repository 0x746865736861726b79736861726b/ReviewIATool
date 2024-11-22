from typing import List

from openai import AsyncOpenAI

from app.repositories.base_llm_client import BaseLLMClient


class OpenAIClient(BaseLLMClient):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = AsyncOpenAI(self.api_key)

    async def send_request(self, message: List[dict]) -> str:
        response = await self.client.chat.completion.create(
            model="gpt-3.5-turbo",
            messages=message,
            max_tokens=1500,
            temperature=0.2,
        )
        return response["choices"][0]["message"]["content"]
