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


def add_attendance_groups(df: pd.DataFrame) -> pd.DataFrame:
    """Put each game into an attendance group."""
    df_copy = df.copy()

    df_copy["attendance_group"] = pd.cut(
        df_copy["attendance"],
        bins=[0, 15000, 17500, 20000, 30000],
        labels=["< 15k", "15k-17.5k", "17.5k-20k", "> 20k"],
    )

    return df_copy


def add_crowd_situation(df: pd.DataFrame) -> pd.DataFrame:
    """Label games as normal season, empty arena or with fans (2020-21)."""
    df_copy = df.copy()

    # Missing attendance in 2020-21 = empty arena (COVID)
    is_covid_season = df_copy["season_id"] == "22020"
    no_fans = df_copy["attendance"].fillna(0) == 0

    df_copy["situation"] = "Normal seasons (2015-19)"
    df_copy.loc[is_covid_season & no_fans, "situation"] = "2020-21: no fans"
    df_copy.loc[is_covid_season & ~no_fans, "situation"] = "2020-21: fans"

    # Fix the order of the bars in the plot
    df_copy["situation"] = pd.Categorical(
        df_copy["situation"],
        categories=[
            "Normal seasons (2015-19)",
            "2020-21: fans",
            "2020-21: no fans",
        ],
    )

    return df_copy


def plot_home_win_rate_by_group(
    df: pd.DataFrame, group_col: str, title: str, xlabel: str
) -> None:
    """Bar chart of the home team win rate (in %) for each group."""
    df_copy = df.copy()

    # 'W' -> 1, 'L' -> 0, so the mean is the share of home wins
    df_copy["is_win"] = df_copy["wl_home"].map({"W": 1, "L": 0})
    win_rate = df_copy.groupby(group_col, observed=True)["is_win"].mean() * 100

    # Plot
    plt.figure(figsize=(10, 6))
    sns.set_theme(style="whitegrid")

    bars = plt.bar(win_rate.index.astype(str), win_rate.tolist())
    plt.bar_label(bars, fmt="%.1f%%")  # write the value on each bar

    # Reference line: 50% = no home advantage
    plt.axhline(50, color="red", linestyle="--", label="No home advantage")

    # Title and labels
    plt.title(title, fontsize=14, pad=15)
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel("Home team win rate (%)", fontsize=12)
    plt.ylim(0, 100)
    plt.legend()

    plt.tight_layout()
    plt.show()
