import re
import base64
from typing import List

from app.repositories.factory import RepositoryFactory


class RepositoryService:
    def __init__(self, client_factory: RepositoryFactory):
        self.client_factory = client_factory

    async def fetch_files_and_content(self, url: str) -> List[dict]:
        client = self.client_factory.get_client(url)
        owner, repo = self._parse_url(url)

        files = await client.get_repository_files(owner, repo)
        result = []

        for file in files:
            if file["type"] == "file":
                content = await client.get_file_content(owner, repo, file["path"])
                encoded_content = self._decode_base64(content)
                result.append(
                    {
                        "name": file["name"],
                        "path": file["path"],
                        "content": encoded_content,
                    }
                )

        return result

    def _parse_url(self, url: str) -> tuple[str, str]:
        pattern = f"https://github\.com/(?P<owner>[\w-]+)/(?P<repo>[\w-]+)"
        match = re.match(pattern, url)

        if not match:
            raise ValueError(f"Invalid repository URL: {url}")
        return match.group("owner"), match.group("repo")

    def _decode_base64(self, base64_content: str) -> str:
        try:
            decoded_content = base64.b64decode(base64_content).decode("utf-8")
            return decoded_content
        except Exception:
            return base64_content
