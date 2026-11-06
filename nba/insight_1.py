"""Season-level home-win rates for recorded NBA regular-season games."""

from pathlib import Path
import sqlite3

import pandas as pd

QUERY_PATH = Path(__file__).resolve().parent.parent / "queries/insight_1.sql"


def home_win_trend(connection: sqlite3.Connection) -> pd.DataFrame:
    """Query rates and reject duplicate eligible game IDs."""
    duplicate = connection.execute(
        """SELECT game_id FROM game
           WHERE season_type = 'Regular Season'
             AND season_id GLOB '2[0-9][0-9][0-9][0-9]'
             AND CAST(SUBSTR(season_id, 2, 4) AS INTEGER) >= 1980
             AND game_id IS NOT NULL AND pts_home IS NOT NULL
             AND pts_away IS NOT NULL AND pts_home != pts_away
           GROUP BY game_id HAVING COUNT(*) > 1 LIMIT 1"""
    ).fetchone()
    if duplicate:
        raise ValueError(f"Duplicate eligible game ID: {duplicate[0]}")
    result = pd.read_sql_query(
        QUERY_PATH.read_text(encoding="utf-8"), connection
    )
    if result.empty:
        raise ValueError("No eligible regular-season games found")
    return result
