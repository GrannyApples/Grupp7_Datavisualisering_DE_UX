import requests
import time
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

    def get_all_fantasy_movies(self, max_pages=25):
        """Hämtar upp till max_pages * 20 filmer (TMDB ger 20/sida)"""
        all_movies = []
        for page in range(1, max_pages + 1):
            results = self.get_fantasy_movies(page=page)
            all_movies.extend(results)
            print(f"Hämtade sida {page} – totalt {len(all_movies)} filmer")
            time.sleep(0.3)  # rate limit skydd
        return all_movies
