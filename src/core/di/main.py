from dishka import AsyncContainer, make_async_container

from src.core.di.providers.core import CoreProvider
from src.core.di.providers.database import DatabaseProvider
from src.core.di.providers.repository import RepositoryProvider
from src.core.di.providers.service import ServiceProvider


def container_factory() -> AsyncContainer:
    return make_async_container(
        CoreProvider(),
        DatabaseProvider(),
        RepositoryProvider(),
        ServiceProvider(),
    )
