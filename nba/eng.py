import pandas as pd
import numpy as np
from nba.db import connect


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


def compute_wingspan_ratio(combine_df: pd.DataFrame) -> pd.DataFrame:
    combine_df["wingspan/height"] = (
        combine_df["wingspan"] / combine_df["height_wo_shoes"]
    )
    return combine_df


def filter_complete_careers(
    df: pd.DataFrame, start_year: int, end_year: int
) -> pd.DataFrame:
    con = connect()
    query = f"""
        SELECT person_id
        FROM common_player_info
        WHERE (from_year >= {start_year}) AND (to_year <= {end_year})
    """
    valid_ids = pd.read_sql_query(query, con)
    con.close()
    return df[df["player_id"].isin(valid_ids["person_id"].astype(int))]


def compute_career_gp(df: pd.DataFrame) -> pd.Series:
    return df.groupby("player_id")["gp"].sum()


def get_seasons_played(df: pd.DataFrame) -> pd.Series:
    return df.groupby("player_id")["season"].nunique().rename("num_seasons")


def add_gp_to_combine(career_df: pd.DataFrame) -> pd.DataFrame:
    con = connect()
    query = """
        SELECT *
        FROM draft_combine_stats
    """
    combine_df = pd.read_sql_query(query, con)
    combine_df["player_id"] = combine_df["player_id"].astype(int)
    con.close()
    career_gp = compute_career_gp(career_df)
    career_seasons = get_seasons_played(career_df)
    df = pd.concat([career_gp, career_seasons], axis=1).reset_index()
    return combine_df.merge(df, how="inner", on="player_id")


def add_player_tenure_and_ppg(career_df: pd.DataFrame) -> pd.DataFrame:
    career_df["tenure"] = career_df["season"] - career_df.groupby("player_id")[
        "season"
    ].transform("min")
    career_df["ppg"] = career_df["pts"] / career_df["gp"]
    return career_df
