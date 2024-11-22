from typing import List
from abc import ABC, abstractmethod


class BaseLLMClient(ABC):
    @abstractmethod
    async def send_request(self, messages: List[dict]) -> str:
        pass
