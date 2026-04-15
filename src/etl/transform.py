import pandas as pd
from src.schemas.movie_schema import MovieSchema

# 🔹 Mapping från genre_id → namn (endast för visualisering)
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

    # 🔴 1. Dark Fantasy (mörk ton)
    if 14 in genre_ids and (27 in genre_ids or 53 in genre_ids):
        return "Dark Fantasy"

    # 🟢 2. Fairy Tale (familj + animation)
    if 14 in genre_ids and 10751 in genre_ids and 16 in genre_ids:
        return "Fairy Tale"

    # 🟡 3. Sword and Sorcery (action fantasy, ej familj)
    if 14 in genre_ids and 28 in genre_ids and 10751 not in genre_ids:
        return "Sword and Sorcery"

    # 🔵 4. Default fantasy
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

                # 🔹 Skapa läsbar genre-text (för UI / Power BI)
                genre_names = [
                    GENRE_MAP.get(gid)
                    for gid in genre_ids
                    if gid in GENRE_MAP
                ]

                row["genres"] = ", ".join(genre_names) if genre_names else "Unknown"

                # 🔹 Data-driven kategori (VIKTIGASTE)
                row["category"] = get_category_from_genres(genre_ids)

                validated_rows.append(row)

            except Exception:
                invalid_count += 1

        print(f"Valid rows: {len(validated_rows)}")
        print(f"Invalid rows skipped: {invalid_count}")

        df = pd.DataFrame(validated_rows)

        # 🔹 Feature engineering
        df["release_year"] = pd.to_datetime(
            df["release_date"], errors="coerce"
        ).dt.year

        # 🔹 Snyggare rating (för dashboards)
        df["rating"] = df["rating"].round(1)

        return df