import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


def home_lead_hist(df: pd.DataFrame) -> None:
    leads = df["half_home_lead"]
    bins = np.arange(start=leads.min(), stop=leads.max() + 1, step=1)
    sns.histplot(df, x="half_home_lead", bins=bins)


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


def graph_wingspan_ratio(df: pd.DataFrame, position: str) -> None:
    sns.histplot(df, x="wingspan/height")
    plt.axvline(x=df["wingspan/height"].mean(), color="red")
    plt.title("Wingspan/height for all positions")


def graph_position_boxplot(
    df: pd.DataFrame,
    x: str,
) -> None:
    positions = ["PG", "SG", "SF", "PF", "C"]
    df_filtered = df[df["position"].isin(positions)]
    order = list(
        df_filtered.groupby("position")[x].median().sort_values().index
    )
    sns.boxplot(df_filtered, x=x, hue_order=order, hue="position")


def graph_mean_ppg_over_career(df: pd.DataFrame) -> None:
    df["career_length"] = df.groupby("player_id")["tenure"].transform("max")

    # Filter for lengths with > 100 datapoints
    len_counts = df["career_length"].value_counts()
    df["num_with_career_length"] = df["career_length"].apply(
        lambda x: len_counts[x]
    )
    df = df[df["num_with_career_length"] >= 100]
    sns.lineplot(
        data=df,
        x="tenure",
        y="ppg",
        hue="career_length",
        estimator="median",  # average across everything
        errorbar=None,
        palette="crest",
    )
    plt.title("Median ppg for player throughout career")
