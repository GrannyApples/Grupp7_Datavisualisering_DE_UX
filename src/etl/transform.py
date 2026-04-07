# src/etl/transform.py

import pandas as pd
from src.schemas.movie_schema import MovieSchema


class Transform:

    @staticmethod
    def to_dataframe(data):
        validated_rows = []
        invalid_count = 0

        for movie in data:
            try:
                validated = MovieSchema(
                    movie_id=movie.get("id"),
                    title=movie.get("title"),
                    release_date=movie.get("release_date"),
                    rating=movie.get("vote_average"),
                    popularity=movie.get("popularity")
                )

                validated_rows.append(validated.model_dump())

            except Exception as e:
                invalid_count += 1

        print(f"Valid rows: {len(validated_rows)}")
        print(f"Invalid rows skipped: {invalid_count}")

        df = pd.DataFrame(validated_rows)
        df["release_year"] = pd.to_datetime(
            df["release_date"], errors="coerce"
        ).dt.year

        return df