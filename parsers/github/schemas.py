from datetime import datetime

from pydantic import BaseModel, Field


class GitHubOwner(BaseModel):
    login: str


class GitHubRepo(BaseModel):
    name: str
    owner: GitHubOwner  # изменили тип на GitHubOwner
    stars: int = Field(alias="stargazers_count")
    watchers: int = Field(alias="watchers_count")
    forks: int = Field(alias="forks_count")
    language: str | None = None
    open_issues: int = Field(alias="open_issues_count")

    @property
    def owner_login(self) -> str:
        return self.owner.login


class GitHubCommit(BaseModel):
    sha: str
    author: str
    date: datetime
