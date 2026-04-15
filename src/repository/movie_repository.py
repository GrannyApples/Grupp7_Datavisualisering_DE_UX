import os
import duckdb
from src.core.config import DUCKDB_PATH
from src.schemas.movie_details_schema import MovieDetailsSchema


GENRE_MAP = {
    12: "Adventure", 14: "Fantasy", 16: "Animation",
    28: "Action", 27: "Horror", 35: "Comedy",
    10751: "Family", 878: "Sci-Fi", 53: "Thriller",
    80: "Crime", 18: "Drama", 10749: "Romance"
}


class MovieRepository:
    def __init__(self, db_path=DUCKDB_PATH):
        self.conn = duckdb.connect(db_path)
        self.create_tables()
        self.seed_genres()

    # SCHEMA

    def create_tables(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS movies (
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
            CREATE TABLE IF NOT EXISTS genres (
                genre_id INTEGER PRIMARY KEY,
                genre_name VARCHAR
            )
        """)

        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS movie_genres (
                movie_id INTEGER,
                genre_id INTEGER
            )
        """)

        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS movie_details (
                movie_id INTEGER PRIMARY KEY,
                runtime INTEGER,
                budget BIGINT,
                revenue BIGINT,
                overview VARCHAR,
                director VARCHAR,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


    # SEED DATA

    def seed_genres(self):
        existing = self.conn.execute("SELECT COUNT(*) FROM genres").fetchdf().iloc[0].to_dict()

        if existing == 0:
            for gid, name in GENRE_MAP.items():
                self.conn.execute("""
                    INSERT INTO genres (genre_id, genre_name)
                    VALUES (?, ?)
                """, [gid, name])


    # MOVIES INSERT

    def insert_movies(self, df):
        movies_df = df[[
            "movie_id", "title", "release_date", "rating",
            "popularity", "release_year", "genres", "category"
        ]]

        self.conn.register("temp_movies", movies_df)
        self.conn.execute("""
            INSERT INTO movies
            SELECT * FROM temp_movies
        """)

    def insert_movie_genres(self, df):
        import ast

        for _, row in df.iterrows():
            try:
                genre_ids = ast.literal_eval(str(row["genre_ids"]))

                for gid in genre_ids:
                    self.conn.execute("""
                        INSERT INTO movie_genres VALUES (?, ?)
                    """, [row["movie_id"], gid])
            except:
                pass


    # CACHE (MOVIE DETAILS)

    def get_movie_details(self, movie_id):
        df = self.conn.execute("""
            SELECT * FROM movie_details WHERE movie_id = ?
        """, [movie_id]).fetchdf()

        if df.empty:
            return None

        row = dict(df.iloc[0])

        return MovieDetailsSchema.model_validate(row)

    def insert_movie_details(self, details):
        self.conn.execute("""
            INSERT INTO movie_details (
                movie_id, runtime, budget, revenue, overview, director
            )
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(movie_id) DO NOTHING
        """, [
            details["movie_id"],
            details["runtime"],
            details["budget"],
            details["revenue"],
            details["overview"],
            details["director"]
        ])

    def close(self):
        self.conn.close()