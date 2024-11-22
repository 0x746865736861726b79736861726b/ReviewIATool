from fastapi import Depends

from app.config import config
from app.repositories.factory import RepositoryFactory
from app.repositories.github import GithubRepository
from app.services.github_service import RepositoryService


def get_github_client():
    return GithubRepository(config.GITHUB_API_KEY)


def get_repository_client_factory(
    github_client: GithubRepository = Depends(get_github_client),
) -> RepositoryFactory:
    return RepositoryFactory(github_client)


def get_repository_service(
    client_factory: RepositoryFactory = Depends(get_repository_client_factory),
) -> RepositoryFactory:
    return RepositoryService(client_factory)
