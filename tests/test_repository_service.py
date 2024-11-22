import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.github_service import RepositoryService


@pytest.mark.asyncio
async def test_fetch_files_and_content(mocker):
    """
    Tests the fetch_files_and_content method of RepositoryService.

    This test creates a mock GithubRepository client and a mock RepositoryFactory,
    and then uses the RepositoryService to fetch files and content from a test
    repository. The test asserts that the correct files and content are returned,
    and that the mock client and factory are called correctly.

    :return: None
    """
    mock_client = AsyncMock()
    mock_client.get_repository_files.return_value = [
        {"type": "file", "name": "file1.txt", "path": "file1.txt"},
        {"type": "file", "name": "file2.txt", "path": "file2.txt"},
    ]
    mock_client.get_file_content.side_effect = [
        "VGhpcyBpcyBhIHRlc3QgZmlsZSAxLg==",  # Base64: "This is a test file 1."
        "VGhpcyBpcyBhIHRlc3QgZmlsZSAyLg==",  # Base64: "This is a test file 2."
    ]

    mock_factory = MagicMock()
    mock_factory.get_client.return_value = mock_client

    service = RepositoryService(mock_factory)

    url = "https://github.com/test-user/test-repo"
    result = await service.fetch_files_and_content(url)

    assert result == [
        {"name": "file1.txt", "path": "file1.txt", "content": "This is a test file 1."},
        {"name": "file2.txt", "path": "file2.txt", "content": "This is a test file 2."},
    ]

    mock_factory.get_client.assert_called_once_with(url)
    mock_client.get_repository_files.assert_called_once_with("test-user", "test-repo")
    assert mock_client.get_file_content.call_count == 2
    mock_client.get_file_content.assert_any_call("test-user", "test-repo", "file1.txt")
    mock_client.get_file_content.assert_any_call("test-user", "test-repo", "file2.txt")


def test_parse_url():
    """
    Тестує метод _parse_url на правильний парсинг URL.
    """
    mock_factory = MagicMock()
    service = RepositoryService(mock_factory)

    url = "https://github.com/test-user/test-repo"
    owner, repo = service._parse_url(url)
    assert owner == "test-user"
    assert repo == "test-repo"

    with pytest.raises(ValueError, match="Invalid repository URL: invalid-url"):
        service._parse_url("invalid-url")


def test_decode_base64():
    """
    Тестує метод _decode_base64 на правильне декодування.
    """
    mock_factory = MagicMock()
    service = RepositoryService(mock_factory)

    base64_content = "VGhpcyBpcyBhIHRlc3Q="
    decoded = service._decode_base64(base64_content)
    assert decoded == "This is a test"

    invalid_content = "invalid-base64"
    decoded = service._decode_base64(invalid_content)
    assert decoded == "invalid-base64"
