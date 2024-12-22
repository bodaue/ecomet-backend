from datetime import date

from src.core.exceptions import RepositoryNotFound, InvalidDateRange
from src.models.activity import Activity
from src.repository.activity import ActivityRepository


class ActivityService:
    def __init__(self, activity_repository: ActivityRepository) -> None:
        self._activity_repository = activity_repository

    async def get_repository_activity(
        self, owner: str, repo: str, since: date, until: date
    ) -> list[Activity]:
        if until < since:
            raise InvalidDateRange

        result = await self._activity_repository.get_repo_activity(
            owner=owner, repo=repo, since=since, until=until
        )
        if not result:
            raise RepositoryNotFound(owner=owner, repo=repo)
        return result
