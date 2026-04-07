from src.services.tmdb_service import TMDBService

class Extract:
    def __init__(self):
        self.service = TMDBService()

    def fetch_movies(self, pages=5):
        all_movies = []

        for page in range(1, pages + 1):
            data = self.service.get_fantasy_movies(page=page)
            all_movies.extend(data)

        return all_movies