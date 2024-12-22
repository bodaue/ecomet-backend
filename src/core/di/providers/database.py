from collections.abc import AsyncIterable

import asyncpg
from asyncpg import Pool, Connection
from dishka import Provider, provide, Scope

from src.core.settings import Settings


class DatabaseProvider(Provider):
    @provide(scope=Scope.APP)
    async def provide_pool(self, settings: Settings) -> Pool:
        return await asyncpg.create_pool(settings.postgres.build_dsn())

    @provide(scope=Scope.REQUEST)
    async def provide_connection(self, pool: Pool) -> AsyncIterable[Connection]:
        async with pool.acquire() as conn:
            yield conn
