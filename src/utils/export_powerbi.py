from src.utils.paths import project_path
import os


def export_for_powerbi(repo):
    output_dir = project_path("data/powerbi")
    os.makedirs(output_dir, exist_ok=True)

    tables = [
        "movies",
        "movie_details",
        "movie_cast",
        "movie_crew",
        "movie_genres",
        "genres",
        "production_companies",
        "production_countries",
        "spoken_languages",
        "movie_origin_countries",
    ]

    for table in tables:
        df = repo.conn.execute(f"SELECT * FROM {table}").fetchdf()
        df.to_csv(output_dir / f"{table}.csv", index=False)
        print(f"✅ {table}.csv ({len(df)} rows)")

    print(f"\n🎬 Export done → {output_dir}")