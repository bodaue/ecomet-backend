from dishka import Provider, Scope, provide

from src.repository.activity import ActivityRepository
from src.repository.top100 import Top100Repository


class RepositoryProvider(Provider):
    scope = Scope.REQUEST

    top100_repository = provide(Top100Repository)
    activity_repository = provide(ActivityRepository)
