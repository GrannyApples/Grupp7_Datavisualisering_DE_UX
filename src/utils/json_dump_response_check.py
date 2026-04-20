import json
import requests
from src.core.config import TMDB_API_KEY, BASE_URL


def reduce_to_schema(obj):
    """
    Recursively reduces JSON to schema-like structure:
    - dicts stay
    - lists become single representative item (or {})
    - values become type placeholders if needed
    """

    if isinstance(obj, dict):
        return {k: reduce_to_schema(v) for k, v in obj.items()}

    elif isinstance(obj, list):
        if len(obj) == 0:
            return []
        # keep only ONE example item
        return [reduce_to_schema(obj[0])]

    else:
        # replace actual values with type names (optional but useful for schemas)
        return type(obj).__name__


movie_id = 129

url = f"{BASE_URL}/movie/{movie_id}"
params = {
    "api_key": TMDB_API_KEY,
    "append_to_response": "credits"
}

response = requests.get(url, params=params)
data = response.json()

schema = reduce_to_schema(data)

print(json.dumps(schema, indent=2))