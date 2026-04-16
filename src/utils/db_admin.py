import duckdb
from src.core.config import DUCKDB_PATH

def reset_database():
    conn = duckdb.connect(DUCKDB_PATH)

    tables = [
        "movie_cast",
        "movie_crew",
        "movie_details",
        "movies",
        "movie_genres",
        "genres"
    ]

    for table in tables:
        conn.execute(f"DROP TABLE IF EXISTS {table}")
        print(f"Dropped: {table}")

    conn.close()
    print("Database reset complete.")