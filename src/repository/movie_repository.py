import os
import duckdb
import pandas as pd
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
               movie_id          INTEGER PRIMARY KEY,
               title             VARCHAR,
               original_title    VARCHAR,
               original_language VARCHAR,
               overview          VARCHAR,
               tagline           VARCHAR,
               status            VARCHAR,
               homepage          VARCHAR,
               imdb_id           VARCHAR,
               runtime           INTEGER,
               budget            BIGINT,
               revenue           BIGINT,
               popularity        FLOAT,
               vote_average      FLOAT,
               vote_count        INTEGER,
               release_date      DATE,
               adult             BOOLEAN,
               video             BOOLEAN,
               poster_path       VARCHAR,
               backdrop_path     VARCHAR,
               collection_id     INTEGER,
               collection_name   VARCHAR,
               director          VARCHAR,
               last_updated      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
           )
        """)

        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS movie_cast (
                movie_id             INTEGER,
                actor_id             INTEGER,
                actor_name           VARCHAR,
                original_name        VARCHAR,
                character            VARCHAR,
                cast_id              INTEGER,
                credit_id            VARCHAR,
                cast_order           INTEGER,
                gender               INTEGER,
                popularity           FLOAT,
                profile_path         VARCHAR,
                known_for_department VARCHAR,
                adult                BOOLEAN
            )
        """)

        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS movie_crew (
                movie_id             INTEGER,
                person_id            INTEGER,
                name                 VARCHAR,
                original_name        VARCHAR,
                credit_id            VARCHAR,
                job                  VARCHAR,
                department           VARCHAR,
                gender               INTEGER,
                popularity           FLOAT,
                profile_path         VARCHAR,
                known_for_department VARCHAR,
                adult                BOOLEAN
            )
        """)

        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS production_companies (
                movie_id       INTEGER,
                company_id     INTEGER,
                name           VARCHAR,
                origin_country VARCHAR,
                logo_path      VARCHAR
            )
        """)

        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS production_countries (
                movie_id    INTEGER,
                iso_3166_1  VARCHAR,
                name        VARCHAR
            )
        """)

        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS spoken_languages (
                movie_id     INTEGER,
                iso_639_1    VARCHAR,
                name         VARCHAR,
                english_name VARCHAR
            )
        """)

        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS movie_origin_countries (
                movie_id     INTEGER,
                country_code VARCHAR
            )
        """)


    def drop_all_tables(self):
        tables = [
            "movie_cast", "movie_crew", "movie_details",
            "production_companies", "production_countries",
            "spoken_languages", "movie_origin_countries",
            "movies", "movie_genres", "genres"
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


    def insert_movie_details(self, details: dict):
        self.conn.execute("""
            INSERT OR REPLACE INTO movie_details (
                movie_id, title, original_title, original_language,
                overview, tagline, status, homepage, imdb_id,
                runtime, budget, revenue, popularity, vote_average, vote_count,
                release_date, adult, video, poster_path, backdrop_path,
                collection_id, collection_name, director
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, [
            details["movie_id"],       details.get("title"),
            details.get("original_title"),  details.get("original_language"),
            details.get("overview"),   details.get("tagline"),
            details.get("status"),     details.get("homepage"),
            details.get("imdb_id"),    details.get("runtime"),
            details.get("budget"),     details.get("revenue"),
            details.get("popularity"), details.get("vote_average"),
            details.get("vote_count"), details.get("release_date"),
            details.get("adult"),      details.get("video"),
            details.get("poster_path"),    details.get("backdrop_path"),
            details.get("collection_id"),  details.get("collection_name"),
            details.get("director"),
        ])

    def insert_movie_cast(self, cast_list: list):
        if not cast_list:
            return
        self.conn.executemany("""
            INSERT INTO movie_cast
            SELECT ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            WHERE NOT EXISTS (
                SELECT 1 FROM movie_cast WHERE movie_id = ? AND credit_id = ?
            )
        """, [(
            c["movie_id"],          c.get("actor_id"),
            c.get("actor_name"),    c.get("original_name"),
            c.get("character"),     c.get("cast_id"),
            c.get("credit_id"),     c.get("cast_order"),
            c.get("gender"),        c.get("popularity"),
            c.get("profile_path"),  c.get("known_for_department"),
            c.get("adult"),
            # dedup keys
            c["movie_id"], c.get("credit_id"),
        ) for c in cast_list])

    def insert_movie_crew(self, crew_list: list):
        if not crew_list:
            return
        self.conn.executemany("""
            INSERT INTO movie_crew
            SELECT ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            WHERE NOT EXISTS (
                SELECT 1 FROM movie_crew WHERE movie_id = ? AND credit_id = ?
            )
        """, [(
            c["movie_id"],          c.get("person_id"),
            c.get("name"),          c.get("original_name"),
            c.get("credit_id"),     c.get("job"),
            c.get("department"),    c.get("gender"),
            c.get("popularity"),    c.get("profile_path"),
            c.get("known_for_department"), c.get("adult"),
            # dedup keys
            c["movie_id"], c.get("credit_id"),
        ) for c in crew_list])

    def insert_production_companies(self, companies: list):
        if not companies:
            return
        self.conn.executemany("""
               INSERT INTO production_companies
               SELECT ?, ?, ?, ?, ?
               WHERE NOT EXISTS (
                   SELECT 1 FROM production_companies
                   WHERE movie_id = ? AND company_id = ?
               )
           """, [(
            c["movie_id"], c.get("company_id"),
            c.get("name"), c.get("origin_country"),
            c.get("logo_path"),
            c["movie_id"], c.get("company_id"),
        ) for c in companies])

    def insert_production_countries(self, countries: list):
        if not countries:
            return
        self.conn.executemany("""
               INSERT INTO production_countries
               SELECT ?, ?, ?
               WHERE NOT EXISTS (
                   SELECT 1 FROM production_countries
                   WHERE movie_id = ? AND iso_3166_1 = ?
               )
           """, [(
            c["movie_id"], c.get("iso_3166_1"), c.get("name"),
            c["movie_id"], c.get("iso_3166_1"),
        ) for c in countries])

    def insert_spoken_languages(self, languages: list):
        if not languages:
            return
        self.conn.executemany("""
               INSERT INTO spoken_languages
               SELECT ?, ?, ?, ?
               WHERE NOT EXISTS (
                   SELECT 1 FROM spoken_languages
                   WHERE movie_id = ? AND iso_639_1 = ?
               )
           """, [(
            l["movie_id"], l.get("iso_639_1"),
            l.get("name"), l.get("english_name"),
            l["movie_id"], l.get("iso_639_1"),
        ) for l in languages])

    def insert_movie_origin_countries(self, movie_id: int, country_codes: list):
        if not country_codes:
            return
        for code in country_codes:
            self.conn.execute("""
                   INSERT INTO movie_origin_countries
                   SELECT ?, ?
                   WHERE NOT EXISTS (
                       SELECT 1 FROM movie_origin_countries
                       WHERE movie_id = ? AND country_code = ?
                   )
               """, [movie_id, code, movie_id, code])


    # CACHE (MOVIE DETAILS)

    def get_movie_details(self, movie_id):
        df = self.conn.execute("""
            SELECT * FROM movie_details WHERE movie_id = ?
        """, [movie_id]).fetchdf()

        if df.empty:
            return None

        row = dict(df.iloc[0])

        cleaned_row = {
            k: (None if pd.isna(v) else v)
            for k, v in row.items()
        }

        return MovieDetailsSchema.model_validate(cleaned_row)

    ##Analytics for EDA

    def get_full_movie_details(self, movie_id: int):
        movie = self.get_movie_details(movie_id)

        cast = self.conn.execute("""
            SELECT actor_id, actor_name, original_name, character,
                   cast_order, gender, popularity, known_for_department
            FROM movie_cast WHERE movie_id = ? ORDER BY cast_order
        """, [movie_id]).fetchdf()

        crew = self.conn.execute("""
            SELECT person_id, name, original_name, job, department,
                   gender, popularity, known_for_department
            FROM movie_crew WHERE movie_id = ?
        """, [movie_id]).fetchdf()

        companies = self.conn.execute("""
            SELECT company_id, name, origin_country
            FROM production_companies WHERE movie_id = ?
        """, [movie_id]).fetchdf()

        countries = self.conn.execute("""
            SELECT iso_3166_1, name FROM production_countries WHERE movie_id = ?
        """, [movie_id]).fetchdf()

        languages = self.conn.execute("""
            SELECT iso_639_1, name, english_name
            FROM spoken_languages WHERE movie_id = ?
        """, [movie_id]).fetchdf()

        return {
            "movie":                movie.model_dump() if movie else None,
            "cast":                 cast,
            "crew":                 crew,
            "production_companies": companies,
            "production_countries": countries,
            "spoken_languages":     languages,
        }




    def close(self):
        self.conn.close()