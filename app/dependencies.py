from fastapi import Depends

from app.config import config
from app.repositories.factory import RepositoryFactory
from app.repositories.github import GithubRepository
from app.services.github_service import RepositoryService


def get_github_client():
    """
    Creates and returns an instance of GithubRepository.

    This function initializes a GithubRepository object using the
    GitHub API key from the configuration settings.

    :return: An instance of GithubRepository.
    :rtype: GithubRepository
    """
    return GithubRepository(config.GITHUB_API_KEY)


def get_repository_client_factory(
    github_client: GithubRepository = Depends(get_github_client),
) -> RepositoryFactory:
    """
    Creates and returns an instance of RepositoryFactory.

    This function initializes a RepositoryFactory object using the
    provided GithubRepository object.

    :param github_client: An instance of GithubRepository.
    :type github_client: GithubRepository
    :return: An instance of RepositoryFactory.
    :rtype: RepositoryFactory
    """
    return RepositoryFactory(github_client)


def get_repository_service(
    client_factory: RepositoryFactory = Depends(get_repository_client_factory),
) -> RepositoryFactory:
    """
    Provides a RepositoryService instance using a repository client factory.

    This function sets up a RepositoryService by utilizing a RepositoryFactory
    for client creation, allowing for seamless access to repository files and content.

    :param client_factory: An instance of RepositoryFactory for creating repository clients.
    :type client_factory: RepositoryFactory
    :return: A configured RepositoryService instance.
    :rtype: RepositoryService
    """
    return RepositoryService(client_factory)
