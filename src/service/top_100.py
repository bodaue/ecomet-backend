from src.models.repository import Repository
from src.repository.top100 import Top100Repository


class Top100Service:
    def __init__(self, top_100_repository: Top100Repository) -> None:
        self._top_100_repository = top_100_repository

    async def get_top_repositories(self, limit: int = 100) -> list[Repository]:
        return await self._top_100_repository.get_top_repos(limit)
