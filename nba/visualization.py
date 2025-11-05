import pandas as pd
import seaborn as sns


def graph_both_win_rates(
    home_series: pd.Series, random_series: pd.Series
) -> None:
    merged = (
        pd.concat(
            [home_series, random_series],
            keys=[home_series.name, random_series.name],
        )
        .rename_axis(["grouping", "half_lead"])
        .reset_index(name="prob_win")
    )
    sns.lineplot(merged, x="half_lead", y="prob_win", hue="grouping")
