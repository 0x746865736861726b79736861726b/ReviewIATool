from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_repository_service
from app.schemas.request import ReviewRequest
from app.services.github_service import RepositoryService

# from app.services.review_service import CodeReviewService

router = APIRouter(prefix="/review", tags=["Review"])


@router.get("/")
async def review(
    repo_url, repository_service: RepositoryService = Depends(get_repository_service)
):
    """
    Retrieves a list of files from a given GitHub repository URL.

    This endpoint will fetch all files from a given repository URL and return
    a list of dictionaries containing the file name, path, and content.

    :param repo_url: The URL of the GitHub repository to fetch files from.
    :type repo_url: str
    :return: A list of dictionaries containing the file name, path, and content.
    :rtype: List[dict]
    :raises HTTPException: If the repository URL is invalid or if an error
        occurs while fetching the files.
    """
    try:
        files = await repository_service.fetch_files_and_content(str(repo_url))
        return {"files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
