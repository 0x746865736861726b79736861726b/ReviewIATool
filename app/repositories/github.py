from app.utils.http_client import HttpClient
from app.repositories.base import BaseRepository


class GithubRepository(BaseRepository):
    def __init__(self, token: str):
        self.http_client = HttpClient(
            "https://api.github.com",
            {"Authorization": f"token {token}"},
        )

    async def get_repository_files(self, owner: str, repo: str, path: str = "") -> dict:
        files = await self.http_client.get(f"/repos/{owner}/{repo}/contents/{path}")
        all_files = []

        for file in files:
            if file["type"] == "file":
                all_files.append(file)
            elif file["type"] == "dir":

                sub_files = await self.get_repository_files(owner, repo, file["path"])
                all_files.extend(sub_files)

        return all_files

    async def get_file_content(self, owner: str, repo: str, path: str) -> str:
        file_data = await self.http_client.get(f"/repos/{owner}/{repo}/contents/{path}")
        return file_data.get("content", "")
