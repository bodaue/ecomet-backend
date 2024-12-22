from collections.abc import AsyncGenerator
from datetime import date, datetime
from http import HTTPStatus
from types import TracebackType
from typing import Any
from urllib.parse import urljoin

import aiohttp

from cloud_function.github.auth import GitHubAuth
from cloud_function.github.schemas import GitHubRepo, GitHubCommit
from cloud_function.github.settings import ParserSettings


class GitHubClient:
    API_BASE_URL = "https://api.github.com"
    ITEMS_PER_PAGE = 100

    def __init__(self, settings: ParserSettings) -> None:
        self._auth = GitHubAuth(
            access_token=settings.github.access_token.get_secret_value()
        )
        self._session: aiohttp.ClientSession | None = None

    async def __aenter__(self) -> "GitHubClient":
        self._session = aiohttp.ClientSession(headers=self._auth.get_headers())
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if self._session:
            await self._session.close()
            self._session = None

    def _build_url(self, endpoint: str) -> str:
        """Build a full URL for the GitHub API endpoint"""
        return urljoin(f"{self.API_BASE_URL}/", endpoint.lstrip("/"))

    async def _make_request(self, method: str, endpoint: str, **kwargs: Any) -> dict:
        """Make an authenticated request to the GitHub API"""
        if not self._session:
            msg = "Client not initialized. Use 'async with' context manager"
            raise RuntimeError(msg)

        url = self._build_url(endpoint)
        async with self._session.request(method, url, **kwargs) as response:
            response.raise_for_status()
            return await response.json()

    async def get_top_repositories(
        self, language: str | None = None, limit: int = ITEMS_PER_PAGE
    ) -> AsyncGenerator[GitHubRepo, None]:
        """Get top repositories sorted by stars"""
        params = {
            "q": f"language:{language}" if language else "stars:>1",
            "sort": "stars",
            "order": "desc",
            "per_page": min(limit, self.ITEMS_PER_PAGE),
        }

        data = await self._make_request("GET", "search/repositories", params=params)

        for i, item in enumerate(data["items"]):
            if i >= limit:
                break
            yield GitHubRepo.model_validate(item)

    async def get_repository_activity(
        self, owner: str, repo: str, since: date, until: date
    ) -> AsyncGenerator[GitHubCommit, None]:
        """Get commit activity for a repository in a date range"""
        params = {
            "since": since.isoformat(),
            "until": until.isoformat(),
            "per_page": 100,
        }

        page = 1
        while True:
            params["page"] = page
            try:
                data = await self._make_request(
                    "GET", f"repos/{owner}/{repo}/commits", params=params
                )
            except aiohttp.ClientResponseError as e:
                if e.status == HTTPStatus.NOT_FOUND:
                    break
                raise

            if not data:
                break

            for commit in data:
                author = (
                    commit["author"]["login"]
                    if commit["author"]
                    else commit["commit"]["author"]["name"]
                )
                yield GitHubCommit(
                    sha=commit["sha"],
                    author=author,
                    date=datetime.fromisoformat(
                        commit["commit"]["author"]["date"].replace("Z", "+00:00")
                    ),
                )

            if len(data) < self.ITEMS_PER_PAGE:
                break

            page += 1
