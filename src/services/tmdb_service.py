import requests
import time
import sys
from src.core.config import TMDB_API_KEY, BASE_URL
from src.repository.movie_repository import MovieRepository
from src.utils.movie_details import parse_movie_details
from src.schemas.movie_details_schema import MovieDetailsSchema

class TMDBService:
    def __init__(self):
        self.repo = MovieRepository()

    """Fetches fantasy movies from TMDB"""

    def get_fantasy_movies(self, page=1):
        url = f"{BASE_URL}/discover/movie"
        params = {
            "api_key": TMDB_API_KEY,
            "with_genres": 14,
            "page": page
        }
        return self._safe_request(url, params)



    def get_all_fantasy_movies(self, max_pages=25):
        """Hämtar upp till max_pages * 20 filmer (TMDB ger 20/sida)"""
        all_movies = []
        start_time = time.time()

        for page in range(1, max_pages + 1):
            data = self.get_fantasy_movies(page)
            results = data.get("results", [])
            if not results:
                break

            all_movies.extend(results)
            elapsed = time.time() - start_time
            sys.stdout.write(
                f"\rFetching pages: {page}/{max_pages} | "
                f"Movies: {len(all_movies)} | "
                f"Time: {elapsed:.1f}s"
            )
            sys.stdout.flush()
        print()
        return all_movies

    def get_movie_details(self, movie_id: int):

        #Check cache
        cached = self.repo.get_movie_details(movie_id)
        if cached:
            print(f"Cache hit for movie {movie_id}")
            return cached


        url = f"{BASE_URL}/movie/{movie_id}"
        params = {
            "api_key": TMDB_API_KEY,
            "append_to_response": "credits"
        }
        data = self._safe_request(url, params)

        parsed = parse_movie_details(data)
        validated = MovieDetailsSchema(**parsed)
        self.repo.insert_movie_details(validated.model_dump())

        return validated


    def _safe_request(self, url, params, retries=3):
        for attempt in range(retries):
            response = requests.get(url, params=params)

            if response.status_code == 429:
                wait_time = int(response.headers.get("Retry-After", 2))
                print(f"Rate limited. Sleeping {wait_time}s...")
                time.sleep(wait_time)
                continue

            if response.status_code >= 500:
                wait_time = 1 * (attempt + 1)
                print(f"Server error {response.status_code}. Retrying in {wait_time}s...")
                time.sleep(wait_time)
                continue

            response.raise_for_status()
            return response.json()

        raise Exception("Max retries exceeded for TMDB request")