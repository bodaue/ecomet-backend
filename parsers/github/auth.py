from typing import Any


class GitHubAuth:
    def __init__(self, access_token: str) -> None:
        self._access_token = access_token

    def get_headers(self) -> dict[str, Any]:
        """Return headers with authorization token"""
        return {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"Bearer {self._access_token}",
        }
