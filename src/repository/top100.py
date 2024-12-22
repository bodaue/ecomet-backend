from asyncpg import Pool

from src.models.repository import Repository
from src.repository.base import BaseRepository


class Top100Repository(BaseRepository[Repository]):
    def __init__(self, pool: Pool) -> None:
        super().__init__(pool, Repository)

    async def get_top_repos(self, limit: int = 100) -> list[Repository]:
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
            ORDER BY stars DESC
            LIMIT $1
        """
        return await self._fetch_all(query, limit)
