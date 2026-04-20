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

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()



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

        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS movie_cast (
                movie_id INTEGER,
                actor_name VARCHAR,
                character VARCHAR,
                cast_order INTEGER
            )
        """)

        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS movie_crew (
                movie_id INTEGER,
                name VARCHAR,
                job VARCHAR
            )
        """)


    def drop_all_tables(self):
        tables = [
            "movie_cast",
            "movie_crew",
            "movie_details",
            "movies",
            "movie_genres",
            "genres"
        ]

        for table in tables:
            try:
                self.conn.execute(f"DROP TABLE IF EXISTS {table}")
                print(f"Dropped table: {table}")
            except Exception as e:
                print(f"Could not drop {table}: {e}")

    # SEED DATA
    def seed_genres(self):
        existing = self.conn.execute("SELECT COUNT(*) FROM genres").fetchone()[0]

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
            WHERE movie_id NOT IN (SELECT movie_id FROM movies)
        """)

    def insert_movie_genres(self, df):
        import ast
        for _, row in df.iterrows():
            try:
                genre_ids = ast.literal_eval(str(row["genre_ids"]))
                for gid in genre_ids:
                    self.conn.execute("""
                        INSERT INTO movie_genres
                        SELECT ?, ?
                        WHERE NOT EXISTS (
                            SELECT 1 FROM movie_genres WHERE movie_id = ? AND genre_id = ?
                        )
                    """, [row["movie_id"], gid, row["movie_id"], gid])
            except:
                pass


    def insert_movie_details(self, details):
        self.conn.execute("""
            INSERT OR REPLACE INTO movie_details (
                movie_id, runtime, budget, revenue, overview, director
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, [
            details["movie_id"],
            details["runtime"],
            details["budget"],
            details["revenue"],
            details["overview"],
            details["director"]
        ])

    def insert_movie_cast(self, cast_list):
        if not cast_list:
            return
        self.conn.executemany("""
            INSERT INTO movie_cast
            SELECT ?, ?, ?, ?
            WHERE NOT EXISTS (
                SELECT 1 FROM movie_cast WHERE movie_id = ? AND cast_order = ?
            )
        """, [(c["movie_id"], c["actor_name"], c["character"], c["cast_order"],
               c["movie_id"], c["cast_order"]) for c in cast_list])

    def insert_movie_crew(self, crew_list):
        if not crew_list:
            return
        self.conn.executemany("""
            INSERT INTO movie_crew
            SELECT ?, ?, ?
            WHERE NOT EXISTS (
                SELECT 1 FROM movie_crew WHERE movie_id = ? AND name = ? AND job = ?
            )
        """, [(c["movie_id"], c["name"], c["job"],
               c["movie_id"], c["name"], c["job"]) for c in crew_list])
    # CACHE (MOVIE DETAILS)

    def get_movie_details(self, movie_id):
        df = self.conn.execute("""
            SELECT * FROM movie_details WHERE movie_id = ?
        """, [movie_id]).fetchdf()

        if df.empty:
            return None

        row = dict(df.iloc[0])

        return MovieDetailsSchema.model_validate(row)

    ##Analytics for EDA

    def get_full_movie_details(self, movie_id: int):
        movie = self.get_movie_details(movie_id)

        cast = self.conn.execute("""
            SELECT actor_name, character, cast_order
            FROM movie_cast
            WHERE movie_id = ?
            ORDER BY cast_order
        """, [movie_id]).fetchdf()

        crew = self.conn.execute("""
            SELECT name, job
            FROM movie_crew
            WHERE movie_id = ?
        """, [movie_id]).fetchdf()

        return {
            "movie": movie.model_dump() if movie else None,
            "cast": cast,
            "crew": crew
        }




    def close(self):
        self.conn.close()