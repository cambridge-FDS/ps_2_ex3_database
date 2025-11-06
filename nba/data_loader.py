import kaggle
import os
import json
from pathlib import Path
import click
import concurrent.futures
from nba_api.stats.endpoints import leaguedashplayerstats
import pandas as pd


def kaggle_api_key(
    user_name: str | None = None, api_key: str | None = None
) -> None:
    """
    Function that takes the kaggle API key as input and saves it to
    ~/.kaggle/kaggle.json if it doesn't exist
    """
    if user_name is not None and api_key is not None:
        # Create ~/.kaggle directory if it doesn't exist
        kaggle_dir = Path.home() / ".kaggle"
        kaggle_dir.mkdir(parents=True, exist_ok=True)

        # Path to kaggle.json
        kaggle_json = kaggle_dir / "kaggle.json"

        # Create the JSON content
        api_config = {"username": user_name, "key": api_key}

        # Write the config file if it doesn't exist
        if not kaggle_json.exists():
            with open(kaggle_json, "w") as f:
                json.dump(api_config, f)

            # Set file permissions to be readable only by the user
            os.chmod(
                kaggle_json, 0o600
            )  # read and write permission only for the user
            print(f"Kaggle API key has been saved to {kaggle_json}")


def kaggle_download_data(dataset: str) -> None:
    """
    Function that downloads the NBA database from Kaggle
    """
    # Create the data directory if it doesn't exist
    root_path = Path(__file__).parent.parent
    data_path = root_path / "data"
    data_path.mkdir(parents=True, exist_ok=True)

    kaggle.api.authenticate()
    kaggle.api.dataset_download_files(dataset, path=data_path, unzip=True)
    print(f"Data has been downloaded to {data_path}")


# Retrieve career stats one id
def query_league_stats(season: int, timeout: int = 30) -> pd.DataFrame:
    career = leaguedashplayerstats.LeagueDashPlayerStats(
        season=season, timeout=timeout
    )
    df: pd.DataFrame = career.get_data_frames()[0]
    return df


# Run stats queries in parallel
def download_yearly_stats(
    seasons: list[int], max_workers: int, timeout: int = 30
) -> None:
    # We can use a with statement to ensure threads are cleaned up promptly
    root_path = Path(__file__).parent.parent
    data_path = root_path / "data"
    dfs = []
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=max_workers
    ) as executor:
        # Start the load operations and mark each future with its URL
        future_to_df = {
            executor.submit(
                query_league_stats, season, timeout=timeout
            ): season
            for season in seasons
        }
        for future in concurrent.futures.as_completed(future_to_df):
            season = future_to_df[future]
            try:
                df = future.result()
                df["season"] = season
                df.columns = df.columns.str.lower()
                dfs.append(df)
            except Exception as exc:
                print("%r generated an exception: %s" % (season, exc))

    all_players = pd.concat(dfs)
    all_players.to_csv(f"{data_path}/season_player_stats.csv")


@click.command()  # type: ignore
@click.option(  # type: ignore
    "--dataset",
    "-d",
    required=True,
    help='Kaggle dataset identifier (e.g., "username/dataset-name")',
)
@click.option(  # type: ignore
    "--user-name",
    "-u",
    required=False,
    help="Your Kaggle username",
)
@click.option(
    "--api-key", "-k", required=False, help="Your Kaggle API key"
)  # type: ignore
def main(
    dataset: str,
    user_name: str | None = None,
    api_key: str | None = None,
) -> None:
    kaggle_api_key(user_name=user_name, api_key=api_key)
    kaggle_download_data(dataset=dataset)


if __name__ == "__main__":
    main()
