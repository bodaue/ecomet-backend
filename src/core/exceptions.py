from fastapi import HTTPException, status


class RepositoryNotFound(HTTPException):
    def __init__(self, owner: str, repo: str) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Repository {owner}/{repo} not found",
        )


class InvalidDateRange(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="End date must be greater than start date",
        )
