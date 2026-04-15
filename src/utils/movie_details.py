def parse_movie_details(data) -> dict:
    return {
        "movie_id": data["id"],
        "runtime": data.get("runtime"),
        "budget": data.get("budget"),
        "revenue": data.get("revenue"),
        "overview": data.get("overview"),
        "director": next(
            (c["name"] for c in data.get("credits", {}).get("crew", [])
             if c.get("job") == "Director"),
            None
        )
    }