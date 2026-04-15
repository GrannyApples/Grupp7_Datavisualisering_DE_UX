from src.repository.movie_repository import MovieRepository

class Load:
    def __init__(self):
        self.repo = MovieRepository()

    def load_movies(self, df):
        self.repo.insert_movies(df)
        self.repo.insert_movie_genres(df)
        self.repo.close()