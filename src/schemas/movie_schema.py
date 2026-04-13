from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import date, datetime

class MovieSchema(BaseModel):
    movie_id: int
    title: str
    release_date: Optional[date] = None
    rating: float = Field(ge=0, le=10)
    popularity: float
    genre_ids: Optional[List[int]] = []

    @field_validator("release_date", mode="before")
    @classmethod
    def parse_date(cls, v):
        if not v or v == "":
            return None
        try:
            return datetime.strptime(v, "%Y-%m-%d").date()
        except:
            return None
