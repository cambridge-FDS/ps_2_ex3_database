"""Download the public Kaggle dataset and open its SQLite database safely."""

from pathlib import Path
import re
import shutil
import sqlite3
import tempfile
from urllib.request import urlopen
from zipfile import ZipFile

import click

DEFAULT_DATASET = "wyattowalsh/basketball"
DEFAULT_DATABASE = Path("data/nba.sqlite")


def connect_database(
    path: str | Path = DEFAULT_DATABASE,
) -> sqlite3.Connection:
    """Open an existing valid SQLite file read-only, without creating a file.

    Relative paths use the current working directory. The caller owns the
    returned connection and should close it when finished.
    """
    database = Path(path).expanduser().resolve()
    if not database.is_file():
        raise FileNotFoundError(f"Database file not found: {database}")
    with database.open("rb") as file:
        if file.read(16) != b"SQLite format 3\x00":
            raise ValueError(f"Not a valid SQLite database: {database}")
    connection = sqlite3.connect(f"{database.as_uri()}?mode=ro", uri=True)
    try:
        connection.execute("SELECT name FROM sqlite_master LIMIT 1").fetchone()
    except sqlite3.DatabaseError:
        connection.close()
        raise ValueError(f"Not a valid SQLite database: {database}") from None
    return connection


def kaggle_download_data(
    dataset: str, destination: str | Path = "data"
) -> None:
    """Download the public archive and safely install its SQLite file."""
    if not re.fullmatch(r"[A-Za-z0-9_-]+/[A-Za-z0-9_-]+", dataset):
        raise ValueError("Dataset must have the form owner/dataset-slug")
    target = Path(destination)
    target.mkdir(parents=True, exist_ok=True)
    database = target / "nba.sqlite"
    if database.exists():
        raise FileExistsError(f"Database already exists: {database}")
    url = f"https://www.kaggle.com/api/v1/datasets/download/{dataset}"
    with tempfile.TemporaryDirectory(dir=target) as folder:
        archive = Path(folder) / "dataset.zip"
        extracted = Path(folder) / "nba.sqlite"
        with urlopen(url, timeout=60) as response, archive.open("wb") as out:
            shutil.copyfileobj(response, out)
        with ZipFile(archive) as zipped, zipped.open("nba.sqlite") as source:
            with extracted.open("wb") as out:
                shutil.copyfileobj(source, out)
        connection = connect_database(extracted)
        connection.close()
        # Linking creates the final file atomically and fails if it exists.
        # The temporary directory is on the same filesystem as the destination.
        database.hardlink_to(extracted)
    click.echo(f"Database downloaded to {database.resolve()}")


@click.command()
@click.option("--dataset", "-d", default=DEFAULT_DATASET, show_default=True)
@click.option(
    "--destination",
    type=click.Path(path_type=Path),
    default="data",
    show_default=True,
)
def main(dataset: str, destination: Path) -> None:
    """Download nba.sqlite from a Kaggle dataset."""
    kaggle_download_data(dataset, destination)


if __name__ == "__main__":
    main()
