from abc import ABC, abstractmethod


class BaseValidator(ABC):
    @abstractmethod
    def validate(self, url: str) -> bool:
        pass