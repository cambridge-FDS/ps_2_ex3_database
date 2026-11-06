# NBA data entry

The dataset is `wyattowalsh/basketball` on Kaggle and contains `nba.sqlite`.
Data is local to each clone and is not committed. From the repository root,
install the environment and package as shown in the README, then run:

```bash
pixi run -e nba python -m nba.data_loader
```

The loader downloads the public compressed archive from Kaggle, extracts only
`nba.sqlite`, validates it, and places it in `data/`. It requires no Kaggle
credentials for the current public endpoint. The assignment separately requires
a Kaggle account and generated API key; anonymous download does not replace that
personal setup task. It refuses to overwrite an existing database; move or rename an
old copy if you deliberately want a new one. Allow enough disk space for both
the archive and extracted database: the archive observed in November 2026 was
about 731 MB and the database about 2.35 GB; sizes can change.

If the public endpoint becomes unavailable, download manually from the
[Kaggle page](https://www.kaggle.com/datasets/wyattowalsh/basketball) or use
the [official Kaggle API](https://github.com/Kaggle/kaggle-api), and place
`nba.sqlite` in `data/`. Follow Kaggle's authentication instructions if
required, and never put tokens in command arguments, notebooks, logs, commits,
or pull requests. Dataset updates can change results: agree on the same version
and compare the file's SHA-256 hash across team members before combining
analyses. To use another local output folder, pass `--destination PATH`.

The copy verified on 2026-11-04 is 2,349,588,480 bytes, with SHA-256:

```text
65b6412234d2d8817678d04f7cd2548aec82fec02b6c5b86679cade7572c21c7
```

`pixi run -e nba validate --data data/nba.sqlite` prints the local hash. A newer
download may differ; agree on the same copy before integrating results. Git
ignores `.csv` and `.sqlite` files as required by the exercise. Teammates can
download independently or share this file outside Git and compare its hash.

Open the database from the repository root, or provide your own path:

```python
from nba.data_loader import connect_database

con = connect_database("data/nba.sqlite")
# Use con with pandas.read_sql_query(...) or sqlite3, then close it.
con.close()
```

The helper checks that the file exists and is a SQLite database and opens it
read-only. It raises an error rather than silently creating a new empty database.
The caller closes the connection. Relative paths use the current working
directory, including in Jupyter. Start Jupyter from the repository root and
select the project's Pixi Python kernel. If the file is missing, check the
extract location and name; if access fails, check local file permissions.

Check the actual data without changing it:

```bash
pixi run -e nba python -c "from nba.data_loader import connect_database; c = connect_database(); print(c.execute('SELECT COUNT(*) FROM game').fetchone()); c.close()"
```

Run the environment smoke checks, optionally including the downloaded database:

```bash
pixi run -e nba validate
pixi run -e nba validate --data data/nba.sqlite
pixi run -e nba python -m unittest discover -s tests -v
```

## How the command line works

**`__main__` guard.** Running `python -m nba.data_loader` sets the module's
`__name__` to `"__main__"`, so the guard calls `main()` to start the command.
When a notebook imports the module, its name is `nba.data_loader` and the guard
is skipped. The notebook can use `connect_database` without starting a download.

**Click.** `@click.command()` turns `main` into a command, and `@click.option()`
defines the `--dataset` (`-d`) and `--destination` options. Click parses the
arguments, supplies defaults for omitted options, and converts the destination
to a `Path`. It passes these values to `main()`, which calls
`kaggle_download_data(dataset, destination)`.
In the original course loader, `-u` (`--user-name`) supplies the Kaggle username,
`-k` (`--api-key`) supplies the Kaggle API key, and `-d` (`--dataset`) supplies
the required dataset identifier in `owner/dataset-name` form.
