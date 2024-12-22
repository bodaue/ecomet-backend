import asyncpg
from asyncpg import Pool
from dishka import Provider, provide, Scope

from src.core.settings import Settings


class DatabaseProvider(Provider):
    @provide(scope=Scope.APP)
    async def provide_pool(self, settings: Settings) -> Pool:
        return await asyncpg.create_pool(settings.postgres.build_dsn())
