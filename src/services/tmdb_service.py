import requests
from src.core.config import TMDB_API_KEY, BASE_URL

class TMDBService:
    """Fetches fantasy movies from TMDB"""

    def get_fantasy_movies(self, page=1):
        url = f"{BASE_URL}/discover/movie"
        params = {
            "api_key": TMDB_API_KEY,
            "with_genres": 14,
            "page": page
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()["results"]