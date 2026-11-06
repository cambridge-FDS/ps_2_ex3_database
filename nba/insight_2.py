"""Data query and wrangling for insight 2: the three-point revolution."""

from pathlib import Path
import sqlite3

import pandas as pd

INSIGHT_2_SQL = (
    Path(__file__).resolve().parent.parent / "queries" / "insight_2.sql"
)


def three_point_trend(connection: sqlite3.Connection) -> pd.DataFrame:
    """Return season-level team three-point volume and shot share."""
    query = INSIGHT_2_SQL.read_text(encoding="utf-8")
    trend = pd.read_sql_query(query, connection)
    trend["season"] = trend["season_start_year"].map(
        lambda year: f"{year}-{str(year + 1)[-2:]}"
    )
    return trend


def three_point_summary(
    trend: pd.DataFrame,
) -> dict[str, float | int | str]:
    """Summarise the first-to-last season change in three-point shooting."""
    observed = trend.dropna(subset=["avg_three_pa_per_team_game"])
    if observed.empty:
        raise ValueError(
            "No seasons with three-point attempt data were found."
        )
    first = observed.iloc[0]
    last = observed.iloc[-1]
    return {
        "first_season": str(first["season"]),
        "last_season": str(last["season"]),
        "first_attempts": float(first["avg_three_pa_per_team_game"]),
        "last_attempts": float(last["avg_three_pa_per_team_game"]),
        "first_share_pct": float(first["three_pa_share_pct"]),
        "last_share_pct": float(last["three_pa_share_pct"]),
        "first_games_in_database": int(first["games_in_database"]),
        "first_games_with_3pa_data": int(first["games_with_3pa_data"]),
        "first_games_with_complete_attempts": int(
            first["games_with_complete_attempts"]
        ),
        "first_coverage_pct": float(first["three_pa_data_coverage_pct"]),
        "attempts_multiple": float(
            last["avg_three_pa_per_team_game"]
            / first["avg_three_pa_per_team_game"]
        ),
    }
