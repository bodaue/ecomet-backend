from asyncpg import Connection

from src.core.enums import RepositorySort, SortOrder
from src.models.repository import Repository
from src.repository.base import BaseRepository


class Top100Repository(BaseRepository[Repository]):
    def __init__(self, conn: Connection) -> None:
        super().__init__(conn, Repository)

    async def get_top_repos(
        self,
        sort_by: RepositorySort,
        sort_order: SortOrder,
        limit: int,
    ) -> list[Repository]:
        query = """
            SELECT
                repo,
                owner,
                position_cur,
                position_prev,
                stars,
                watchers,
                forks,
                open_issues,
                language
            FROM top100
        """
        if sort_by:
            query += f" ORDER BY {sort_by.value} {sort_order.upper()}"
        else:
            query += " ORDER BY stars DESC"

        query += " LIMIT $1"
        return await self._fetch_all(query, limit)
