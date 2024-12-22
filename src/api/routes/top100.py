from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Query
from starlette import status

from src.core.enums import RepositorySort, SortOrder
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
    sort_by: Annotated[
        RepositorySort | None, Query(example=RepositorySort.STARS)
    ] = RepositorySort.STARS,
    sort_order: Annotated[SortOrder, Query(example=SortOrder.DESC)] = SortOrder.DESC,
) -> list[Repository]:
    """
    Retrieve a list of top GitHub repositories sorted by stars.
    Returns detailed information about each repository including:
    - Current and previous ranking
    - Number of stars, watchers, and forks
    - Number of open issues
    - Primary programming language

    The results can be sorted by various fields such as stars, watchers,
    forks, open issues, language, or current position.
    """
    return await service.get_top_repositories(sort_by, sort_order, limit)
