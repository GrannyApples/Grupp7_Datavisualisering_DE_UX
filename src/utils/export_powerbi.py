from src.utils.paths import project_path
import duckdb
from src.core.config import DUCKDB_PATH
from src.utils.file_utils import ensure_folder


def export_for_powerbi(repo):


    conn = repo.conn

    movies = conn.execute("SELECT * FROM movies").fetchdf()
    details = conn.execute("SELECT * FROM movie_details").fetchdf()
    cast = conn.execute("SELECT * FROM movie_cast").fetchdf()
    crew = conn.execute("SELECT * FROM movie_crew").fetchdf()
    genres = conn.execute("SELECT * FROM genres").fetchdf()

    movies.to_csv("data/powerbi/movies.csv", index=False)
    details.to_csv("data/powerbi/movie_details.csv", index=False)
    cast.to_csv("data/powerbi/movie_cast.csv", index=False)
    crew.to_csv("data/powerbi/movie_crew.csv", index=False)
    genres.to_csv("data/powerbi/genres.csv", index=False)




def export_for_powerbi_joined():
    joined = project_path("data/powerbi/joined")
    joined.mkdir(parents=True, exist_ok=True)
    conn = duckdb.connect(DUCKDB_PATH)

    conn.execute(f"""
        COPY (
            SELECT
                m.movie_id, m.title, m.release_date, m.release_year,
                m.rating, m.popularity, m.category,
                d.runtime, d.budget, d.revenue, d.director, d.overview,
                CASE
                    WHEN d.budget > 0 AND d.revenue > 0
                    THEN ROUND((d.revenue - d.budget) * 100.0 / d.budget, 2)
                    ELSE NULL
                END AS roi_percent
            FROM movies m
            LEFT JOIN movie_details d ON m.movie_id = d.movie_id
        ) TO '{joined}/movies_enriched.csv' (HEADER, DELIMITER ',')
    """)
    print("✅ movies_enriched.csv")

    conn.execute(f"""
        COPY (
            SELECT mg.movie_id, g.genre_name
            FROM movie_genres mg
            JOIN genres g ON mg.genre_id = g.genre_id
        ) TO '{joined}/movie_genres_joined.csv' (HEADER, DELIMITER ',')
    """)
    print("✅ movie_genres_joined.csv")

    conn.execute(f"""
        COPY (
            SELECT movie_id, actor_name, character, cast_order
            FROM movie_cast
            WHERE cast_order <= 10
            ORDER BY movie_id, cast_order
        ) TO '{joined}/cast_top10.csv' (HEADER, DELIMITER ',')
    """)
    print("✅ cast_top10.csv")

    conn.execute(f"""
        COPY (
            SELECT movie_id, name, job
            FROM movie_crew
            ORDER BY movie_id
        ) TO '{joined}/crew_joined.csv' (HEADER, DELIMITER ',')
    """)
    print("✅ crew_joined.csv")

    conn.execute(f"""
        COPY (
            SELECT
                g.genre_name,
                COUNT(DISTINCT m.movie_id)  AS total_movies,
                ROUND(AVG(m.rating), 2)     AS avg_rating,
                ROUND(AVG(m.popularity), 2) AS avg_popularity,
                ROUND(AVG(d.revenue), 0)    AS avg_revenue,
                ROUND(AVG(d.budget), 0)     AS avg_budget
            FROM movies m
            JOIN movie_genres mg   ON m.movie_id = mg.movie_id
            JOIN genres g          ON mg.genre_id = g.genre_id
            LEFT JOIN movie_details d ON m.movie_id = d.movie_id
            GROUP BY g.genre_name
            ORDER BY total_movies DESC
        ) TO '{joined}/genre_summary.csv' (HEADER, DELIMITER ',')
    """)
    print("✅ genre_summary.csv")

    conn.close()
    print("\n🎬 Joined exports done → {joined}/")

if __name__ == "__main__":


    export_for_powerbi_joined()