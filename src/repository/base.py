from typing import Any, TypeVar, Generic

from asyncpg import Pool

Model = TypeVar("Model")


class BaseRepository(Generic[Model]):
    def __init__(self, pool: Pool) -> None:
        self._pool = pool

    async def _fetch_all(self, query: str, *args: Any) -> list[T]:
        async with self._pool.acquire() as conn:
            result = await conn.fetch(query, *args)
            return [dict(row) for row in result]
