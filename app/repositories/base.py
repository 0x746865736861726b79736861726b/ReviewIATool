from abc import ABC, abstractmethod


class BaseRepository(ABC):
    @abstractmethod
    async def get_repository_files(self, onwer: str, repo: str) -> dict:
        pass

    @abstractmethod
    async def get_file_content(self, owner: str, repo: str, path: str) -> str:
        pass
