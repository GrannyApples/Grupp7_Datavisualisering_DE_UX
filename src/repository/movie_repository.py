import os
import duckdb
from src.core.config import DUCKDB_PATH

GENRE_MAP = {
    12: "Adventure", 14: "Fantasy", 16: "Animation",
    28: "Action", 27: "Horror", 35: "Comedy",
    10751: "Family", 878: "Sci-Fi", 53: "Thriller",
    80: "Crime", 18: "Drama", 10749: "Romance"
}

class MovieRepository:
    def __init__(self, db_path=DUCKDB_PATH):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = duckdb.connect(db_path)

    def create_table(self):
        self.conn.execute("DROP TABLE IF EXISTS movie_genres")
        self.conn.execute("DROP TABLE IF EXISTS genres")
        self.conn.execute("DROP TABLE IF EXISTS movies")

        self.conn.execute("""
            CREATE TABLE movies (
                movie_id INTEGER,
                title VARCHAR,
                release_date DATE,
                rating FLOAT,
                popularity FLOAT,
                release_year INTEGER,
                genres VARCHAR,
                category VARCHAR
            )
        """)

        self.conn.execute("""
            CREATE TABLE genres (
                genre_id INTEGER PRIMARY KEY,
                genre_name VARCHAR
            )
        """)

        self.conn.execute("""
            CREATE TABLE movie_genres (
                movie_id INTEGER,
                genre_id INTEGER
            )
        """)

        
        for genre_id, genre_name in GENRE_MAP.items():
            self.conn.execute(
                "INSERT INTO genres VALUES (?, ?)",
                [genre_id, genre_name]
            )

    def insert_dataframe(self, df):
        # Spara movies
        movies_df = df[["movie_id", "title", "release_date", "rating",
                        "popularity", "release_year", "genres", "category"]]
        self.conn.register("df_temp", movies_df)
        self.conn.execute("INSERT INTO movies SELECT * FROM df_temp")

        
        import ast
        for _, row in df.iterrows():
            try:
                genre_ids = ast.literal_eval(str(row["genre_ids"]))
                for gid in genre_ids:
                    if gid in GENRE_MAP:
                        self.conn.execute(
                            "INSERT INTO movie_genres VALUES (?, ?)",
                            [row["movie_id"], gid]
                        )
            except:
                pass

    def get_all_movies(self):
        return self.conn.execute("SELECT * FROM movies").fetchdf()

    def close(self):
        self.conn.close()
