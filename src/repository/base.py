from typing import Any, TypeVar, Generic

from asyncpg import Connection

Model = TypeVar("Model")


class BaseRepository(Generic[Model]):
    def __init__(self, conn: Connection, model: type[Model]) -> None:
        self._conn = conn
        self._model = model

    async def _fetch_all(self, query: str, *args: Any) -> list[Model]:
        result = await self._conn.fetch(query, *args)
        return [self._model.model_validate(dict(row)) for row in result]

    async def _fetch_one(self, query: str, *args: Any) -> Model | None:
        result = await self._conn.fetchrow(query, *args)
        return self._model.model_validate(dict(result)) if result else None
