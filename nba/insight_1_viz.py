"""Plot season-level home-win rates, leaving missing seasons as gaps."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import pandas as pd


def plot_home_win_trend(
    trend: pd.DataFrame,
    output_path: str | Path = "figures/insight_1_home_win_rate.png",
) -> Figure:
    """Save and return the figure; the x-axis uses season start years."""
    if trend.empty:
        raise ValueError("The trend dataframe is empty")
    series = trend.set_index("season_start_year")["home_win_pct"].sort_index()
    series = series.reindex(
        range(int(series.index.min()), int(series.index.max()) + 1)
    )
    fig, ax = plt.subplots(figsize=(11, 5.2))
    ax.plot(
        series.index.tolist(), series.tolist(), color="#216a80", linewidth=2.4
    )
    ax.scatter(
        series.index.tolist(), series.tolist(), color="#216a80", s=13, zorder=3
    )
    ax.axhline(50, color="#8c8c8c", linestyle="--", linewidth=1)
    ax.set_title(
        "How often did NBA home teams win?",
        loc="left",
        fontsize=15,
        fontweight="bold",
    )
    ax.set_ylabel("Home wins (% of eligible games)")
    ax.set_xlabel("Regular season (start year)")
    ax.set_ylim(45, 75)
    ax.grid(axis="y", alpha=0.22)
    ax.spines[["top", "right"]].set_visible(False)
    if 2012 in series.index and pd.isna(series.loc[2012]):
        ax.axvspan(2011.7, 2012.3, color="#e5a65b", alpha=0.35)
        ax.annotate("2012–13 missing", (2012, 69), ha="center", fontsize=9)
    fig.tight_layout()
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180, bbox_inches="tight")
    return fig
