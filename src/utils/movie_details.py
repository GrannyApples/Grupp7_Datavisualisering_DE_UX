def parse_movie_details(data) -> dict:
    credits = data.get("credits") or {}
    cast = credits.get("cast") or []
    crew = credits.get("crew") or []

    def clean(v):
        if v == "" or v == "null":
            return None
        return v

    def to_int(v):
        try:
            return int(v)
        except (TypeError, ValueError):
            return None

    def to_float(v):
        try:
            return float(v)
        except (TypeError, ValueError):
            return None

    # Director extraction
    director = None
    for c in crew:
        if c.get("job") == "Director":
            director = c.get("name")
            break

    collection = data.get("belongs_to_collection") or {}

    return {
        "movie": {
            "movie_id": data["id"],
            "title": clean(data.get("title")),
            "original_title": clean(data.get("original_title")),
            "original_language": clean(data.get("original_language")),
            "overview": clean(data.get("overview")),
            "tagline": clean(data.get("tagline")),
            "status": clean(data.get("status")),
            "homepage": clean(data.get("homepage")),
            "imdb_id": clean(data.get("imdb_id")),

            "runtime": to_int(data.get("runtime")),
            "budget": to_int(data.get("budget")),
            "revenue": to_int(data.get("revenue")),

            "popularity": to_float(data.get("popularity")),
            "vote_average": to_float(data.get("vote_average")),
            "vote_count": to_int(data.get("vote_count")),

            "release_date": clean(data.get("release_date")),

            "adult": data.get("adult"),
            "video": data.get("video"),

            "poster_path": clean(data.get("poster_path")),
            "backdrop_path": clean(data.get("backdrop_path")),

            "collection_id": collection.get("id"),
            "collection_name": clean(collection.get("name")),

            "origin_country": data.get("origin_country") or [],
            "genres": [g.get("id") for g in data.get("genres") or []],

            "director": director,
        },

        "cast": [
            {
                "movie_id": data["id"],
                "actor_id": c.get("id"),
                "actor_name": clean(c.get("name")),
                "original_name": clean(c.get("original_name")),
                "character": clean(c.get("character")),
                "cast_id": c.get("cast_id"),
                "credit_id": c.get("credit_id"),
                "cast_order": c.get("order"),
                "gender": c.get("gender"),
                "popularity": to_float(c.get("popularity")),
                "profile_path": clean(c.get("profile_path")),
                "known_for_department": clean(c.get("known_for_department")),
                "adult": c.get("adult"),
            }
            for c in cast
        ],

        "crew": [
            {
                "movie_id": data["id"],
                "person_id": c.get("id"),
                "name": clean(c.get("name")),
                "original_name": clean(c.get("original_name")),
                "credit_id": c.get("credit_id"),
                "job": clean(c.get("job")),
                "department": clean(c.get("department")),
                "gender": c.get("gender"),
                "popularity": to_float(c.get("popularity")),
                "profile_path": clean(c.get("profile_path")),
                "known_for_department": clean(c.get("known_for_department")),
                "adult": c.get("adult"),
            }
            for c in crew
        ],

        "production_companies": [
            {
                "movie_id": data["id"],
                "company_id": c.get("id"),
                "name": clean(c.get("name")),
                "origin_country": clean(c.get("origin_country")),
                "logo_path": clean(c.get("logo_path")),
            }
            for c in data.get("production_companies") or []
        ],

        "production_countries": [
            {
                "movie_id": data["id"],
                "iso_3166_1": clean(c.get("iso_3166_1")),
                "name": clean(c.get("name")),
            }
            for c in data.get("production_countries") or []
        ],

        "spoken_languages": [
            {
                "movie_id": data["id"],
                "iso_639_1": clean(l.get("iso_639_1")),
                "name": clean(l.get("name")),
                "english_name": clean(l.get("english_name")),
            }
            for l in data.get("spoken_languages") or []
        ],
    }