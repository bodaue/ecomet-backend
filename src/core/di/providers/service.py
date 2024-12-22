from dishka import Provider, Scope, provide

from src.service.activity import ActivityService
from src.service.top_100 import Top100Service


class ServiceProvider(Provider):
    scope = Scope.REQUEST

    top_100_service = provide(Top100Service)
    activity_service = provide(ActivityService)
