from src.services.tmdb_service import TMDBService

class Extract:
    def __init__(self):
        self.service = TMDBService()

    def fetch_movies(self):
        return self.service.get_fantasy_movies()