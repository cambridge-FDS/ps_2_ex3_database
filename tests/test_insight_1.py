"""Check the home-win denominator, exclusions and duplicate guard."""

import sqlite3
import unittest

from nba.insight_1 import home_win_trend


class HomeWinTrendTests(unittest.TestCase):
    def setUp(self) -> None:
        self.db = sqlite3.connect(":memory:")
        self.db.execute(
            "CREATE TABLE game (season_id TEXT, season_type TEXT, "
            "game_id TEXT, pts_home REAL, pts_away REAL)"
        )
        self.db.executemany(
            "INSERT INTO game VALUES (?, ?, ?, ?, ?)",
            [
                ("22022", "Regular Season", "a", 100, 90),
                ("22022", "Regular Season", "b", 90, 100),
                ("22022", "Regular Season", "c", None, 100),
                ("22022", "Regular Season", "d", 100, 100),
                ("42022", "Playoffs", "e", 100, 90),
            ],
        )

    def tearDown(self) -> None:
        self.db.close()

    def test_rate_uses_only_complete_decided_regular_season_games(
        self,
    ) -> None:
        row = home_win_trend(self.db).iloc[0]
        self.assertEqual(row["games"], 2)
        self.assertEqual(row["home_wins"], 1)
        self.assertEqual(row["home_win_pct"], 50.0)

    def test_duplicate_game_id_is_rejected(self) -> None:
        self.db.execute(
            "INSERT INTO game VALUES ('22022', 'Regular Season', 'a', 100, 90)"
        )
        with self.assertRaisesRegex(ValueError, "Duplicate eligible game ID"):
            home_win_trend(self.db)


if __name__ == "__main__":
    unittest.main()
