from pydantic import BaseModel


class RepoOut(BaseModel):
    """
    Схема для отображения репозитория (таблица top100).
    """

    repo: str
    owner: str
    position_cur: int
    position_prev: int | None
    stars: int
    watchers: int
    forks: int
    open_issues: int
    language: str | None


class RepoSortParams(BaseModel):
    """
    Схема для валидации/получения параметров сортировки.
    """

    sort_by: str = "stars"
    order: str = "desc"

    class Config:
        schema_extra = {"example": {"sort_by": "stars", "order": "asc"}}

    def get_valid_sort_field(self) -> str:
        valid_fields = {"stars", "forks", "watchers"}
        return self.sort_by if self.sort_by in valid_fields else "stars"

    def get_valid_order(self) -> str:
        return "asc" if self.order.lower() == "asc" else "desc"
