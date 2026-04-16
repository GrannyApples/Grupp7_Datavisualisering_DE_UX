def parse_movie_details(data) -> dict:
    credits = data.get("credits") or {}

    cast = credits.get("cast") or []
    crew = credits.get("crew") or []

    return {
        "movie": {
            "movie_id": data["id"],
            "runtime": data.get("runtime"),
            "budget": data.get("budget"),
            "revenue": data.get("revenue"),
            "overview": data.get("overview"),
            "director": next(
                (c.get("name") for c in crew if c.get("job") == "Director"),
                None
            )
        },

        "cast": [
            {
                "movie_id": data["id"],
                "actor_name": c.get("name"),
                "character": c.get("character"),
                "cast_order": c.get("order")
            }
            for c in credits.get("cast", [])
        ],

        "crew": [
            {
                "movie_id": data["id"],
                "name": c.get("name"),
                "job": c.get("job")
            }
            for c in crew
        ]
    }