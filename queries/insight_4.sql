-- Insight 4
-- Which months have the most recorded NBA games?

SELECT
    CAST(strftime('%m', game_date) AS INTEGER) AS month,
    COUNT(*) AS number_of_games
FROM game
WHERE game_date IS NOT NULL
  AND strftime('%m', game_date) IS NOT NULL
GROUP BY CAST(strftime('%m', game_date) AS INTEGER)
ORDER BY month;
