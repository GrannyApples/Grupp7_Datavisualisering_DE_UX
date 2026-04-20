from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
from pydantic import field_validator


class MovieDetailsSchema(BaseModel):
    movie_id: int
    title: Optional[str] = None
    original_title: Optional[str] = None
    original_language: Optional[str] = None
    overview: Optional[str] = None
    tagline: Optional[str] = None
    status: Optional[str] = None
    homepage: Optional[str] = None
    imdb_id: Optional[str] = None
    runtime: Optional[int] = None
    budget: Optional[int] = None
    revenue: Optional[int] = None
    popularity: Optional[float] = None
    vote_average: Optional[float] = None
    vote_count: Optional[int] = None
    release_date: Optional[date] = None
    adult: Optional[bool] = None
    video: Optional[bool] = None
    poster_path: Optional[str] = None
    backdrop_path: Optional[str] = None
    collection_id: Optional[int] = None
    collection_name: Optional[str] = None
    origin_country: Optional[List[str]] = None
    genres: Optional[List[int]] = None
    director: Optional[str] = None
    last_updated: Optional[datetime] = None


    @field_validator("release_date", mode="before")
    @classmethod
    def parse_date(cls, v):
        if not v or v == "":
            return None
        try:
            return date.fromisoformat(v)
        except:
            return None

class CastMember(BaseModel):
    movie_id: int
    actor_id: Optional[int] = None
    actor_name: Optional[str] = None
    original_name: Optional[str] = None
    character: Optional[str] = None
    cast_id: Optional[int] = None
    credit_id: Optional[str] = None
    cast_order: Optional[int] = None
    gender: Optional[int] = None
    popularity: Optional[float] = None
    profile_path: Optional[str] = None
    known_for_department: Optional[str] = None
    adult: Optional[bool] = None


class CrewMember(BaseModel):
    movie_id: int
    person_id: Optional[int] = None
    name: Optional[str] = None
    original_name: Optional[str] = None
    credit_id: Optional[str] = None
    job: Optional[str] = None
    department: Optional[str] = None
    gender: Optional[int] = None
    popularity: Optional[float] = None
    profile_path: Optional[str] = None
    known_for_department: Optional[str] = None
    adult: Optional[bool] = None


class ProductionCompany(BaseModel):
    movie_id: int
    company_id: Optional[int] = None
    name: Optional[str] = None
    origin_country: Optional[str] = None
    logo_path: Optional[str] = None


class ProductionCountry(BaseModel):
    movie_id: int
    iso_3166_1: Optional[str] = None
    name: Optional[str] = None


class SpokenLanguage(BaseModel):
    movie_id: int
    iso_639_1: Optional[str] = None
    name: Optional[str] = None
    english_name: Optional[str] = None