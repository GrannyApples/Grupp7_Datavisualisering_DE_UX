def export_for_powerbi(repo):
    import pandas as pd

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