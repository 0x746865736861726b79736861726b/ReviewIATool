import re
import base64
from typing import List

from app.repositories.factory import RepositoryFactory


class RepositoryService:
    def __init__(self, client_factory: RepositoryFactory):
        """
        Initializes the RepositoryService with a client factory.

        This constructor sets up the client factory to be used for fetching
        repository files and content.

        :param client_factory: The client factory for creating repository clients.
        :type client_factory: RepositoryFactory
        """
        self.client_factory = client_factory

    async def fetch_files_and_content(self, url: str) -> List[dict]:
        """
        Fetches files and their content from a repository URL.

        This asynchronous method retrieves a list of files from a given
        repository URL and decodes their content from base64.

        :param url: The URL of the repository to fetch files from.
        :type url: str
        :return: A list of dictionaries, each containing the file's name,
                path, and decoded content.
        :rtype: List[dict]
        """
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
        """
        Parses a GitHub repository URL to extract the owner and repository name.

        :param url: The URL to parse.
        :type url: str
        :return: A tuple containing the owner and repository name.
        :rtype: tuple[str, str]
        :raises ValueError: If the URL does not match the expected format.
        """
        pattern = f"https://github\.com/(?P<owner>[\w-]+)/(?P<repo>[\w-]+)"
        match = re.match(pattern, url)

        if not match:
            raise ValueError(f"Invalid repository URL: {url}")
        return match.group("owner"), match.group("repo")

    def _decode_base64(self, base64_content: str) -> str:
        """
        Decodes a string of base64 content into a regular string.

        This method attempts to decode a string of base64 content and return
        the decoded string. If the decoding fails for any reason, the
        original string is returned.

        :param base64_content: The string of base64 content to decode.
        :type base64_content: str
        :return: The decoded string, or the original string if decoding fails.
        :rtype: str
        """
        try:
            decoded_content = base64.b64decode(base64_content).decode("utf-8")
            return decoded_content
        except Exception:
            return base64_content
