"""Visualisation for insight 2: the three-point revolution."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import pandas as pd


def plot_three_point_trend(
    trend: pd.DataFrame,
    output_path: str | Path = "figures/insight_2_three_point_revolution.png",
) -> Figure:
    """Plot attempts, shot share and data coverage for each season."""
    if trend.empty:
        raise ValueError("The trend dataframe is empty.")

    fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
    years = trend["season_start_year"]
    attempts = trend["avg_three_pa_per_team_game"]
    share = trend["three_pa_share_pct"]
    coverage = trend["three_pa_data_coverage_pct"]

    axes[0].plot(years, attempts, color="#e4572e", linewidth=2.8)
    axes[0].fill_between(years, attempts, color="#e4572e", alpha=0.13)
    axes[0].set_ylabel("3-point attempts\nper team per game")
    axes[0].annotate(
        f"{attempts.iloc[0]:.1f}",
        (years.iloc[0], attempts.iloc[0]),
        xytext=(8, 8),
        textcoords="offset points",
        fontweight="bold",
    )
    axes[0].annotate(
        f"{attempts.iloc[-1]:.1f}",
        (years.iloc[-1], attempts.iloc[-1]),
        xytext=(-34, 8),
        textcoords="offset points",
        fontweight="bold",
    )
    first = trend.iloc[0]
    matched_games = int(first["games_with_complete_attempts"])
    axes[0].annotate(
        f"3PA data: {int(first['games_with_3pa_data'])}/"
        f"{int(first['games_in_database'])} games",
        (years.iloc[0], attempts.iloc[0]),
        xytext=(48, 28),
        textcoords="offset points",
        arrowprops={"arrowstyle": "->", "color": "#555555"},
        fontsize=9,
    )

    axes[1].plot(years, share, color="#2878b5", linewidth=2.8)
    axes[1].fill_between(years, share, color="#2878b5", alpha=0.13)
    axes[1].set_ylabel("3PA share of FGA\n(complete attempt rows)")
    axes[1].set_xlabel("NBA season (start year)")
    axes[1].annotate(
        f"{share.iloc[0]:.1f}%",
        (years.iloc[0], share.iloc[0]),
        xytext=(8, 8),
        textcoords="offset points",
        fontweight="bold",
    )
    axes[1].annotate(
        f"Share uses {matched_games} matched games",
        (years.iloc[0], share.iloc[0]),
        xytext=(105, 60),
        textcoords="offset points",
        arrowprops={"arrowstyle": "->", "color": "#555555"},
        bbox={
            "boxstyle": "round,pad=0.2",
            "facecolor": "white",
            "alpha": 0.85,
        },
        fontsize=9,
    )

    axes[2].plot(years, coverage, color="#4b8b3b", linewidth=2.2)
    axes[2].scatter(years.iloc[0], coverage.iloc[0], color="#4b8b3b", zorder=3)
    axes[2].set_ylabel("Games with 3PA\ndata (%)")
    axes[2].set_xlabel("NBA season (start year)")
    axes[2].set_ylim(0, 105)
    axes[2].annotate(
        f"{coverage.iloc[0]:.1f}%",
        (years.iloc[0], coverage.iloc[0]),
        xytext=(8, 8),
        textcoords="offset points",
        fontweight="bold",
    )

    # The calendar row has null metrics for the absent 2012-13 season, so
    # matplotlib leaves a visible break in each line across that season.
    for axis in axes:
        axis.axvspan(2011.5, 2012.5, color="#777777", alpha=0.12)
        axis.axvline(2012, color="#777777", linestyle="--", linewidth=1)
    axes[0].text(
        2012,
        0.96,
        "2012–13 missing",
        transform=axes[0].get_xaxis_transform(),
        ha="center",
        va="top",
        fontsize=9,
        color="#555555",
    )
    axes[1].annotate(
        f"{share.iloc[-1]:.1f}%",
        (years.iloc[-1], share.iloc[-1]),
        xytext=(-42, 8),
        textcoords="offset points",
        fontweight="bold",
    )

    fig.suptitle(
        "The three-point revolution: from a few tries to nearly 4 in 10 shots",
        fontsize=16,
        fontweight="bold",
        y=0.99,
    )
    for axis in axes:
        axis.grid(axis="y", color="#d9d9d9", linewidth=0.8)
        axis.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(rect=(0, 0, 1, 0.96))

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180, bbox_inches="tight")
    return fig
