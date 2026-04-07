import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
DUCKDB_PATH = "data/db/movies.duckdb"
BASE_URL = "https://api.themoviedb.org/3"