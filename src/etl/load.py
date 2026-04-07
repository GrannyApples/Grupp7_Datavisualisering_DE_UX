from src.repository.movie_repository import MovieRepository

class Load:
    def __init__(self):
        self.repo = MovieRepository()

    def load_movies(self, df):
        self.repo.create_table()
        self.repo.insert_dataframe(df)
        self.repo.close()