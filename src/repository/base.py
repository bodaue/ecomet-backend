from typing import Any, TypeVar, Generic

from asyncpg import Pool

Model = TypeVar("Model")


class BaseRepository(Generic[Model]):
    def __init__(self, pool: Pool, model: type[Model]) -> None:
        self._pool = pool
        self._model = model

    async def _fetch_all(self, query: str, *args: Any) -> list[Model]:
        async with self._pool.acquire() as conn:
            result = await conn.fetch(query, *args)
            return [self._model.model_validate(dict(row)) for row in result]

    async def _fetch_one(self, query: str, *args: Any) -> Model | None:
        async with self._pool.acquire() as conn:
            result = await conn.fetchrow(query, *args)
            return self._model.model_validate(dict(result)) if result else None
