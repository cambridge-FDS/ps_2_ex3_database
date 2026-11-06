-- Three-point volume, shot share and data coverage by regular season.
-- 2012-13 is added by the calendar CTE because it is absent from this copy.
WITH RECURSIVE season_calendar(season_start_year) AS (
    SELECT 1981
    UNION ALL
    SELECT season_start_year + 1
    FROM season_calendar
    WHERE season_start_year < 2022
),
season_games AS (
    SELECT
        CAST(SUBSTR(season_id, 2, 4) AS INTEGER) AS season_start_year,
        COUNT(*) AS games_in_database
    FROM game
    WHERE season_id GLOB '2[0-9][0-9][0-9][0-9]'
    GROUP BY season_id
),
three_point_games AS (
    SELECT
        CAST(SUBSTR(season_id, 2, 4) AS INTEGER) AS season_start_year,
        COUNT(*) AS games_with_3pa_data,
        AVG((fg3a_home + fg3a_away) / 2.0)
            AS avg_three_pa_per_team_game
    FROM game
    WHERE season_id GLOB '2[0-9][0-9][0-9][0-9]'
      AND fg3a_home IS NOT NULL
      AND fg3a_away IS NOT NULL
    GROUP BY season_id
),
complete_attempt_games AS (
    SELECT
        CAST(SUBSTR(season_id, 2, 4) AS INTEGER) AS season_start_year,
        COUNT(*) AS games_with_complete_attempts,
        100.0 * SUM(fg3a_home + fg3a_away)
            / SUM(fga_home + fga_away) AS three_pa_share_pct
    FROM game
    WHERE season_id GLOB '2[0-9][0-9][0-9][0-9]'
      AND fg3a_home IS NOT NULL
      AND fg3a_away IS NOT NULL
      AND fga_home IS NOT NULL
      AND fga_away IS NOT NULL
    GROUP BY season_id
)
SELECT
    '2' || calendar.season_start_year AS season_id,
    calendar.season_start_year,
    COALESCE(games.games_in_database, 0) AS games_in_database,
    COALESCE(threes.games_with_3pa_data, 0) AS games_with_3pa_data,
    COALESCE(complete.games_with_complete_attempts, 0)
        AS games_with_complete_attempts,
    CASE
        WHEN games.games_in_database > 0
        THEN 100.0 * threes.games_with_3pa_data / games.games_in_database
    END AS three_pa_data_coverage_pct,
    threes.avg_three_pa_per_team_game,
    complete.three_pa_share_pct
FROM season_calendar AS calendar
LEFT JOIN season_games AS games USING (season_start_year)
LEFT JOIN three_point_games AS threes USING (season_start_year)
LEFT JOIN complete_attempt_games AS complete USING (season_start_year)
ORDER BY calendar.season_start_year;
