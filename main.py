from src.etl.extract import Extract
from src.etl.transform import Transform
from src.etl.load import Load
from src.utils.file_utils import ensure_folder

def run_pipeline():
    ensure_folder("data/raw")
    ensure_folder("data/processed")
    ensure_folder("data/db")

    extractor = Extract()
    raw_data = extractor.fetch_movies(pages=25)

    transformer = Transform()
    df = transformer.to_dataframe(raw_data)

    df.to_csv("data/processed/movies.csv", index=False)

    loader = Load()
    loader.load_movies(df)
    print("ETL pipeline finished!")

if __name__ == "__main__":
    run_pipeline()
