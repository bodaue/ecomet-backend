from datetime import date

from asyncpg import Connection

from src.models.activity import Activity
from src.repository.base import BaseRepository


class ActivityRepository(BaseRepository[Activity]):
    def __init__(self, conn: Connection) -> None:
        super().__init__(conn, Activity)

    async def get_repo_activity(
        self, owner: str, repo: str, since: date, until: date
    ) -> list[Activity]:
        query = """
            WITH repo AS (
                SELECT id
                FROM top100
                WHERE owner = $1 AND repo = $2
            )
            SELECT
                a.date,
                a.commits,
                a.authors,
                a.repository_id
            FROM activity a
            JOIN repo r ON r.id = a.repository_id
            WHERE date BETWEEN $3 AND $4
            ORDER BY date
        """
        return await self._fetch_all(query, owner, repo, since, until)
