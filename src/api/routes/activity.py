# src/api/v1/activity.py
from datetime import date
from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Query
from starlette import status

from src.models.activity import Activity
from src.service.activity import ActivityService

router = APIRouter(prefix="/api/repos", tags=["Repository Activity"])


@router.get(
    "/{owner}/{repo}/activity",
    summary="Get Repository Activity",
    responses={
        404: {"description": "Repository not found"},
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def get_repository_activity(
    service: FromDishka[ActivityService],
    owner: str,
    repo: str,
    since: Annotated[date, Query(description="Start Date")],
    until: Annotated[date, Query(description="End Date")],
) -> list[Activity]:
    """
    Retrieve the activity statistics for a specific GitHub repository
    within a given time period.
    The activity includes:
    - Number of commits per day
    - List of contributing authors
    - Daily activity breakdown
    """
    return await service.get_repository_activity(
        owner=owner, repo=repo, since=since, until=until
    )
