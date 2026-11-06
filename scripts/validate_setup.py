"""Smoke-test the installed environment; optionally check the real database."""

import argparse
import hashlib
import importlib.metadata
import sqlite3
import sys
import tempfile
from pathlib import Path

import duckdb
import nbformat
from jupyter_client import KernelManager
from matplotlib.figure import Figure

from nba.data_loader import connect_database
import nba.visualisation  # noqa: F401
import nba.wrangling  # noqa: F401


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data", type=Path, help="path to the NBA SQLite file"
    )
    args = parser.parse_args()

    print(f"Python {sys.version.split()[0]}: {sys.executable}")
    for package in ("pandas", "kaggle", "jupyterlab", "ps2-nba"):
        print(f"{package}: {importlib.metadata.version(package)}")
    for filename in ("warm_up.ipynb", "analysis.ipynb"):
        nbformat.validate(nbformat.read(filename, as_version=4))
    with sqlite3.connect(":memory:") as db:
        assert db.execute("SELECT 1").fetchone() == (1,)
    with duckdb.connect(":memory:") as db:
        assert db.execute("SELECT 1").fetchone() == (1,)
    print("Notebook format, SQLite and DuckDB: OK")

    with tempfile.TemporaryDirectory() as folder:
        figure = Figure()
        figure.subplots().plot([0, 1], [0, 1])
        figure.savefig(Path(folder) / "smoke.png")
    print("Package imports and headless plot: OK")

    manager = KernelManager()
    manager.start_kernel()
    client = manager.client()
    try:
        client.start_channels()
        client.wait_for_ready(timeout=60)
        code = (
            "import sys, pandas, nba.data_loader\n"
            "from pathlib import Path\n"
            f"assert Path(sys.executable).resolve() == "
            f"Path({sys.executable!r}).resolve()\n"
            "assert pandas.DataFrame({'x': [1, 2]}).x.sum() == 3"
        )
        if args.data:
            code += (
                "\nfrom nba.data_loader import connect_database\n"
                f"db = connect_database({str(args.data.resolve())!r})\n"
                "assert not pandas.read_sql_query("
                "'SELECT * FROM game LIMIT 10', db).empty\n"
                "db.close()"
            )
        msg_id = client.execute(code)
        while True:
            message = client.get_shell_msg(timeout=30)
            if message["parent_header"].get("msg_id") == msg_id:
                if message["content"]["status"] != "ok":
                    raise RuntimeError(str(message["content"]))
                break
    finally:
        client.stop_channels()
        manager.shutdown_kernel(now=True)
    print("Fresh Jupyter kernel: OK")

    if args.data:
        connection = connect_database(args.data)
        try:
            count = connection.execute("SELECT COUNT(*) FROM game").fetchone()[
                0
            ]
        finally:
            connection.close()
        if count < 1:
            raise RuntimeError("The game table contains no data")
        print(f"game rows: {count}")
        with args.data.open("rb") as database_file:
            checksum = hashlib.file_digest(database_file, "sha256").hexdigest()
        print(f"Database SHA-256: {checksum}")


if __name__ == "__main__":
    main()
