from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CastMember(BaseModel):
    movie_id: int
    actor_name: Optional[str]
    character: Optional[str]
    cast_order: Optional[int]


class CrewMember(BaseModel):
    movie_id: int
    name: Optional[str]
    job: Optional[str]


class MovieDetailsSchema(BaseModel):
    movie_id: int
    runtime: Optional[int]
    budget: Optional[int]
    revenue: Optional[int]
    overview: Optional[str]
    director: Optional[str]
    last_updated: Optional[datetime] = None