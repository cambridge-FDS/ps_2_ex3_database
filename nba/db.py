import sqlite3 as sql
import pandas as pd
from pathlib import Path


def connect() -> sql.Connection:
    data_path = Path.cwd() / "data" / "nba.sqlite"
    con = sql.connect(data_path)
    return con


def query_line_score(
    connection: sql.Connection, start_year: int, end_year: int
) -> pd.DataFrame:
    query = """
        SELECT *
        FROM line_score
        WHERE game_date_est >= ?
          AND game_date_est < ?
    """
    params = (
        f"{start_year}-01-01 00:00:00",
        f"{end_year}-01-01 00:00:00",
    )
    return pd.read_sql_query(query, connection, params=params)
