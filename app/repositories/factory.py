import re
from typing import Type

from app.repositories.github import GithubRepository


class RepositoryFactory:
    def __init__(self, github_client: GithubRepository):
        self.github_client = github_client

    def get_client(self, url: str) -> Type[GithubRepository]:
        """
        Returns a repository client based on the provided URL.

        :param url: The URL of the repository.
        :type url: str
        :return: The repository client.
        :rtype: Type[GithubRepository]
        """
        if re.match(r"https://github\.com/[\w-]+/[\w-]+", url):
            return self.github_client
        raise ValueError("Invalid repository URL")
