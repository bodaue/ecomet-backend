from src.core.enums import RepositorySort, SortOrder
from src.models.repository import Repository
from src.repository.top100 import Top100Repository


class Top100Service:
    def __init__(self, top_100_repository: Top100Repository) -> None:
        self._top_100_repository = top_100_repository

    async def get_top_repositories(
        self, sort_by: RepositorySort, sort_order: SortOrder, limit: int
    ) -> list[Repository]:
        return await self._top_100_repository.get_top_repos(sort_by, sort_order, limit)
