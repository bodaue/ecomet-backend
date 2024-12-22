import datetime

from pydantic import BaseModel


class Activity(BaseModel):
    date: datetime.date
    commits: int
    authors: list[str]
