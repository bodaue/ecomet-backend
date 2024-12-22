from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Query
from starlette import status

from src.models.repository import Repository
from src.service.top_100 import Top100Service

router = APIRouter(prefix="/api/repos", tags=["Top repositories"])


@router.get(
    "/top100",
    summary="Get Top Github Repositories",
    status_code=status.HTTP_200_OK,
)
@inject
async def get_top_repositories(
    service: FromDishka[Top100Service],
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
) -> list[Repository]:
    """
    Retrieve a list of top GitHub repositories sorted by stars.
    Returns detailed information about each repository including:
    - Current and previous ranking
    - Number of stars, watchers, and forks
    - Number of open issues
    - Primary programming language
    """
    return await service.get_top_repositories(limit)
