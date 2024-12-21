from datetime import date

from src.models.activity import Activity
from src.repository.base import BaseRepository


class ActivityRepository(BaseRepository[Activity]):
    async def get_repo_activity(
        self, owner: str, repo: str, since: date, until: date
    ) -> list[Activity]:
        query = """
            SELECT
                date,
                commits,
                authors
            FROM activity
            WHERE
                owner = $1
                AND repo = $2
                AND date BETWEEN $3 AND $4
            ORDER BY date
        """
        return await self._fetch_all(query, owner, repo, since, until)
