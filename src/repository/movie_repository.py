import os
import duckdb
from src.core.config import DUCKDB_PATH

class MovieRepository:
    def __init__(self, db_path=DUCKDB_PATH):
        # Ensure folder exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        self.conn = duckdb.connect(db_path)

    def create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS movies (
                movie_id INTEGER,
                title VARCHAR,
                release_date DATE,
                rating FLOAT,
                popularity FLOAT,
                release_year INTEGER
            )
        """)

    def insert_dataframe(self, df):
        self.conn.register("df_temp", df)
        self.conn.execute("INSERT INTO movies SELECT * FROM df_temp")

    def get_all_movies(self):
        return self.conn.execute("SELECT * FROM movies").fetchdf()

    def close(self):
        self.conn.close()