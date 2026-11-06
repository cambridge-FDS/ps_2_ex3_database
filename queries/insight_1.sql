-- Home wins in recorded regular-season games, starting in 1980-81.
-- Each eligible row is one game; no joins or team-game duplication.
SELECT
    CAST(SUBSTR(season_id, 2, 4) AS INTEGER) AS season_start_year,
    COUNT(*) AS games,
    SUM(CASE WHEN pts_home > pts_away THEN 1 ELSE 0 END) AS home_wins,
    100.0 * SUM(CASE WHEN pts_home > pts_away THEN 1 ELSE 0 END)
        / COUNT(*) AS home_win_pct
FROM game
WHERE season_type = 'Regular Season'
  AND season_id GLOB '2[0-9][0-9][0-9][0-9]'
  AND CAST(SUBSTR(season_id, 2, 4) AS INTEGER) >= 1980
  AND game_id IS NOT NULL
  AND pts_home IS NOT NULL
  AND pts_away IS NOT NULL
  AND pts_home != pts_away
GROUP BY season_id
ORDER BY season_start_year;
