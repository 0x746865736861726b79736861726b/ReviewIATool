from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_repository_service
from app.schemas.request import ReviewRequest
from app.services.github_service import RepositoryService

router = APIRouter(prefix="/review", tags=["Review"])


@router.get("/")
async def review(
    repo_url, repository_service: RepositoryService = Depends(get_repository_service)
):
    try:
        files = await repository_service.fetch_files_and_content(str(repo_url))
        return {"files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
