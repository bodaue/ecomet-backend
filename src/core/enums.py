from enum import Enum


class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"


class RepositorySort(str, Enum):
    STARS = "stars"
    WATCHERS = "watchers"
    FORKS = "forks"
    OPEN_ISSUES = "open_issues"
    LANGUAGE = "language"
    POSITION = "position_cur"
