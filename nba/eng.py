import pandas as pd
import numpy as np


def add_halftime_features(df: pd.DataFrame) -> pd.DataFrame:
    np.random.seed(42)
    df["pts_half_home"] = df["pts_qtr1_home"].astype(int) + df[
        "pts_qtr2_home"
    ].astype(int)
    df["pts_half_away"] = df["pts_qtr1_away"].astype(int) + df[
        "pts_qtr2_away"
    ].astype(int)
    df["half_home_lead"] = df["pts_half_home"] - df["pts_half_away"]
    df["home_win"] = np.where(df["pts_home"] > df["pts_away"], 1, 0)

    random = np.random.choice([-1, 1])
    df["half_random_lead"] = df["half_home_lead"] * random
    df["random_win"] = df["home_win"] * random + 1
    return df


def compute_halftime_win_probabilities(
    df: pd.DataFrame, random: bool
) -> pd.Series:
    if random:
        group_col = "half_random_lead"
        win_col = "random_win"
    else:
        group_col = "half_home_lead"
        win_col = "home_win"
    win_probs = df.groupby(group_col)[win_col].mean()
    return win_probs
