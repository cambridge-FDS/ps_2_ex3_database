"""NBA Insight 4: Monthly distribution of recorded games."""

from pathlib import Path
import sqlite3

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure

INSIGHT_4_SQL = (
    Path(__file__).resolve().parent.parent / "queries" / "insight_4.sql"
)


def get_monthly_game_counts(
    connection: sqlite3.Connection,
    sql_path: Path = INSIGHT_4_SQL,
) -> pd.DataFrame:
    """Load monthly game counts using the saved SQL query."""
    query = sql_path.read_text(encoding="utf-8")
    result = pd.read_sql_query(query, connection)

    if result.empty:
        raise ValueError("No game records were returned.")

    return result.sort_values("month").reset_index(drop=True)


def plot_monthly_game_counts(
    data: pd.DataFrame,
) -> tuple[Figure, Axes]:
    """Plot recorded NBA games by calendar month."""
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.bar(
        data["month"],
        data["number_of_games"],
    )

    ax.set_title("Recorded NBA Games by Calendar Month")
    ax.set_xlabel("Month")
    ax.set_ylabel("Number of recorded games")
    ax.set_xticks(range(1, 13))
    ax.grid(axis="y", alpha=0.25)

    fig.tight_layout()
    return fig, ax
