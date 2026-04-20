import pandas as pd
from src.schemas.movie_schema import MovieSchema


GENRE_MAP = {
    12: "Adventure",
    14: "Fantasy",
    16: "Animation",
    28: "Action",
    27: "Horror",
    35: "Comedy",
    10751: "Family",
    878: "Sci-Fi",
    53: "Thriller",
    80: "Crime",
    18: "Drama",
    10749: "Romance"
}


def get_category_from_genres(genre_ids):
    """
    Data-driven kategorisering baserad på TMDb genre_ids.
    Prioriteringsordning är viktig för balans.
    """

    if not genre_ids:
        return "Unknown"

    
    if 14 in genre_ids and (27 in genre_ids or 53 in genre_ids):
        return "Dark Fantasy"

    
    if 14 in genre_ids and 10751 in genre_ids and 16 in genre_ids:
        return "Fairy Tale"

    
    if 14 in genre_ids and 28 in genre_ids and 10751 not in genre_ids:
        return "Sword and Sorcery"

    
    if 14 in genre_ids:
        return "Fantasy Epic"

    return "Other"


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
                    popularity=movie.get("popularity"),
                    genre_ids=movie.get("genre_ids", [])
                )

                row = validated.model_dump()
                genre_ids = row["genre_ids"] or []

                
                genre_names = [
                    GENRE_MAP.get(gid)
                    for gid in genre_ids
                    if gid in GENRE_MAP
                ]

                row["genres"] = ", ".join(genre_names) if genre_names else "Unknown"

                
                row["category"] = get_category_from_genres(genre_ids)

                validated_rows.append(row)

            except Exception:
                invalid_count += 1

        print(f"Valid rows: {len(validated_rows)}")
        print(f"Invalid rows skipped: {invalid_count}")

        df = pd.DataFrame(validated_rows)

        
        df["release_year"] = pd.to_datetime(
            df["release_date"], errors="coerce"
        ).dt.year

        
        df["rating"] = df["rating"].round(1)

        return df

    def clean_value(v):
        if v == "" or v == "null":
            return None
        return v