## Just run `main` to add DuckDB

Make sure you have a `.env` file in the project root with your API key:

    TMDB_API_KEY=YOUR_API_KEY

## Clean database reset

If you want a fresh/clean database, run the following:

```python
from src.utils.db_admin import reset_database

reset_database()
```

You can execute this in an EDA cell.
Just remove it after executing it so you don't end up wiping the database, everytime you run your EDA