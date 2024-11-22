from app.utils.http_client import HttpClient
from app.repositories.base import BaseRepository


class GithubRepository(BaseRepository):
    def __init__(self, token: str):
        self.http_client = HttpClient(
            "https://api.github.com",
            {"Authorization": f"token {token}"},
        )

    async def get_repository_files(self, owner: str, repo: str) -> dict:
        return await self.http_client.get(f"/repos/{owner}/{repo}/contents")

    async def get_file_content(self, owner: str, repo: str, path: str) -> str:
        file_data = await self.http_client.get(f"/repos/{owner}/{repo}/contents/{path}")
        return file_data.get("content", "")
