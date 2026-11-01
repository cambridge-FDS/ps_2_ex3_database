import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    df_copy = df.copy()

    # Convert 'game_date' into datetimeformat and extract the year
    df_copy["game_date"] = pd.to_datetime(df_copy["game_date"])
    df_copy["year"] = df_copy["game_date"].dt.year

    # Drop rows with missing values
    df_copy = df_copy.dropna().reset_index(drop=True)

    return df_copy


def plot_yearly_game_count(df: pd.DataFrame) -> None:
    df_copy = df.copy()

    # Group by year and count the number of games for each year
    yearly_game_count = (
        df_copy.groupby("year").size().reset_index(name="game_count")
    )

    # Plot
    plt.figure(figsize=(10, 6))
    sns.set_theme(style="whitegrid")

    ax = sns.lineplot(
        data=yearly_game_count,
        x="year",
        y="game_count",
        marker="o",
        linewidth=2,
    )

    # Title and labels
    ax.set_title("Number of Games per Year", fontsize=14, pad=15)
    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel("Number of Games", fontsize=12)

    plt.tight_layout()
    plt.show()


def plot_yearly_home_win_rate(df: pd.DataFrame) -> None:
    df_copy = df.copy()

    # One hot encoding 'wl_home' ('W' -> 1, 'L' -> 0)
    df_copy["is_win"] = df_copy["wl_home"].map({"W": 1, "L": 0})

    # Group by year and calculate the mean win rate of home teams for each year
    yearly_win_rate = df_copy.groupby("year")["is_win"].mean().reset_index()

    # Plot
    plt.figure(figsize=(10, 6))
    sns.set_theme(style="whitegrid")

    ax = sns.lineplot(
        data=yearly_win_rate, x="year", y="is_win", marker="o", linewidth=2
    )

    # Title and labels
    ax.set_title("Yearly Home Team Win Rate", fontsize=14, pad=15)
    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel("Win Rate ('W' Ratio)", fontsize=12)

    plt.tight_layout()
    plt.show()
