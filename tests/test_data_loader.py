import sqlite3
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from zipfile import BadZipFile, ZipFile

from nba.data_loader import connect_database, kaggle_download_data


class DatabaseTests(unittest.TestCase):
    def test_missing_file_is_not_created(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "missing.sqlite"
            with self.assertRaises(FileNotFoundError):
                connect_database(path)
            self.assertFalse(path.exists())

    def test_invalid_file_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "invalid.sqlite"
            path.write_text("not a database")
            with self.assertRaises(ValueError):
                connect_database(path)

    def test_existing_database_is_read_only(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "test #1.sqlite"
            with sqlite3.connect(path) as db:
                db.execute("CREATE TABLE game (id INTEGER)")
            db = connect_database(path)
            try:
                self.assertEqual(
                    db.execute("SELECT count(*) FROM game").fetchone(), (0,)
                )
                with self.assertRaises(sqlite3.OperationalError):
                    db.execute("CREATE TABLE forbidden (id INTEGER)")
            finally:
                db.close()


class DownloadTests(unittest.TestCase):
    def archive(self, name: str, content: bytes) -> io.BytesIO:
        result = io.BytesIO()
        with ZipFile(result, "w") as archive:
            archive.writestr(name, content)
        result.seek(0)
        return result

    def test_public_archive_installs_valid_database(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            fixture = Path(folder) / "fixture.sqlite"
            with sqlite3.connect(fixture) as db:
                db.execute("CREATE TABLE game (id INTEGER)")
            response = self.archive("nba.sqlite", fixture.read_bytes())
            target = Path(folder) / "data"
            with patch("nba.data_loader.urlopen", return_value=response):
                kaggle_download_data("wyattowalsh/basketball", target)
            db = connect_database(target / "nba.sqlite")
            try:
                self.assertEqual(
                    db.execute("SELECT count(*) FROM game").fetchone(), (0,)
                )
            finally:
                db.close()

    def test_missing_member_leaves_no_database(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            response = self.archive("other.txt", b"text")
            with patch("nba.data_loader.urlopen", return_value=response):
                with self.assertRaises(KeyError):
                    kaggle_download_data("wyattowalsh/basketball", folder)
            self.assertFalse((Path(folder) / "nba.sqlite").exists())

    def test_existing_database_is_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "nba.sqlite"
            path.write_bytes(b"existing")
            with patch("nba.data_loader.urlopen") as request:
                with self.assertRaises(FileExistsError):
                    kaggle_download_data("wyattowalsh/basketball", folder)
                request.assert_not_called()
            self.assertEqual(path.read_bytes(), b"existing")

    def test_invalid_archive_does_not_report_success(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            with patch(
                "nba.data_loader.urlopen", return_value=io.BytesIO(b"bad")
            ):
                with self.assertRaises(BadZipFile):
                    kaggle_download_data("wyattowalsh/basketball", folder)
            self.assertFalse((Path(folder) / "nba.sqlite").exists())

    def test_invalid_dataset_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(ValueError):
                kaggle_download_data("owner/name?bad=1", folder)


if __name__ == "__main__":
    unittest.main()
