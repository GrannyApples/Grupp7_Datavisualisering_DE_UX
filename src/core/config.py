import os
from dotenv import load_dotenv
from src.utils.paths import project_path

# Load .env file
load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
DUCKDB_PATH = project_path("data/db/movies.duckdb")
BASE_URL = "https://api.themoviedb.org/3"