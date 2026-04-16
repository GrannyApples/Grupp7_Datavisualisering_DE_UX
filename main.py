from src.etl.extract import Extract
from src.etl.transform import Transform
from src.etl.load import Load
from src.utils.file_utils import ensure_folder
from src.utils.export_powerbi import export_for_powerbi
import pandas as pd

def run_pipeline():
    ensure_folder("data/raw")
    ensure_folder("data/processed")
    ensure_folder("data/db")
    ensure_folder("data/powerbi")

    extractor = Extract()
    raw_data = extractor.fetch_movies(pages=50)
    pd.DataFrame(raw_data).to_csv("data/raw/movies.csv", index=False)

    transformer = Transform()
    df = transformer.to_dataframe(raw_data)

    df.to_csv("data/processed/movies.csv", index=False)

    loader = Load()
    loader.load_movies(df)

    x = 10 #change this for how many movies to grab details for.
    #Just to fill top X with some data in the database
    service = extractor.service
    for movie in raw_data[:x]:
        service.get_movie_details(movie["id"])

    export_for_powerbi(loader.repo)

    loader.repo.close()
    print("ETL pipeline finished!")

if __name__ == "__main__":
    run_pipeline()
