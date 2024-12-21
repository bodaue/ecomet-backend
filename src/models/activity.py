from datetime import datetime

from pydantic import BaseModel


class Activity(BaseModel):
    date: datetime
    commits: int
    authors: list[str]
