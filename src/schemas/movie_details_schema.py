from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MovieDetailsSchema(BaseModel):
    movie_id: int
    runtime: Optional[int]
    budget: Optional[int]
    revenue: Optional[int]
    overview: Optional[str]
    director: Optional[str]
    last_updated: Optional[datetime] = None