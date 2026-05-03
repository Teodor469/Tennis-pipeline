import duckdb
from pathlib import Path

def get_connection():
    db_path = Path(__file__).parent.parent / "data/gold/tennis.db"
    return duckdb.connect(str(db_path))