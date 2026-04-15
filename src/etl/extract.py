import time
from src.services.tmdb_service import TMDBService

class Extract:
    def __init__(self):
        self.service = TMDBService()

    def fetch_movies(self, pages=25):
        return self.service.get_all_fantasy_movies(max_pages=pages)
