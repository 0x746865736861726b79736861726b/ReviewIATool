import pytest
from unittest.mock import AsyncMock
from app.services.review_service import CodeReviewService


@pytest.mark.asyncio
async def test_review_code_single_file(mocker):
    mock_llm_client = AsyncMock()
    mock_llm_client.send_request.return_value = "Mocked AI review."

    service = CodeReviewService(llm_client=mock_llm_client)

    files = [{"path": "file1.py", "content": "print('Hello, world!')"}]
    repo_name = "test-repo"

    response = await service.review_code(files, repo_name)

    assert response == "Mocked AI review."
    mock_llm_client.send_request.assert_called_once_with(
        [
            {"role": "system", "content": "You are a code reviewer."},
            {"role": "user", "content": "Review the following code: test-repo"},
            {"role": "user", "content": "File: file1.py\n\nprint('Hello, world!')"},
        ]
    )


@pytest.mark.asyncio
async def test_review_code_multiple_files(mocker):
    """
    Tests the review_code method with multiple files input.
    """
    mock_llm_client = AsyncMock()
    mock_llm_client.send_request.return_value = "Mocked AI review for multiple files."

    service = CodeReviewService(llm_client=mock_llm_client)

    files = [
        {"path": "file1.py", "content": "print('Hello, world!')"},
        {"path": "utils/helpers.py", "content": "def helper():\n    pass"},
    ]
    repo_name = "multi-file-repo"

    response = await service.review_code(files, repo_name)

    assert response == "Mocked AI review for multiple files."
    mock_llm_client.send_request.assert_called_once_with(
        [
            {"role": "system", "content": "You are a code reviewer."},
            {"role": "user", "content": "Review the following code: multi-file-repo"},
            {"role": "user", "content": "File: file1.py\n\nprint('Hello, world!')"},
            {
                "role": "user",
                "content": "File: utils/helpers.py\n\ndef helper():\n    pass",
            },
        ]
    )


@pytest.mark.asyncio
async def test_review_code_empty_files(mocker):
    """
    Tests the review_code method with an empty list of files.

    This test ensures that the review_code method can handle an input
    where no files are provided, and it should correctly call the
    send_request method with only the system and repository name messages.

    :param mocker: The mocker fixture for mocking dependencies.
    :return: None
    """
    mock_llm_client = AsyncMock()
    mock_llm_client.send_request.return_value = "Mocked AI review for empty input."

    service = CodeReviewService(llm_client=mock_llm_client)

    files = []
    repo_name = "empty-repo"

    response = await service.review_code(files, repo_name)

    assert response == "Mocked AI review for empty input."
    mock_llm_client.send_request.assert_called_once_with(
        [
            {"role": "system", "content": "You are a code reviewer."},
            {"role": "user", "content": "Review the following code: empty-repo"},
        ]
    )
