import sqlite3 as sql
import pandas as pd
import statsmodels.api as sm


# 1. Insights ___________
def three_pointer_regression(games : pd.DataFrame) -> sm.regression.linear_model.RegressionResultsWrapper:
    # Drop all rows where fg3_pct_home is NULL
    games = games.dropna(subset=['home_win', 'fg3a_share'])
    # Regress the home_win column on the fg3_pct_home column
    X = games['fg3a_share']
    X = sm.add_constant(X)
    y = games['home_win']
    model = sm.OLS(y, X).fit()
    # return the coefficient of fg3_pct_home
    return model

def select_games(con: sql.Connection) -> pd.DataFrame:
    query = """
    SELECT *
    FROM game
    """
    games = pd.read_sql(query, con)
    return games

def create_fg3a_data(games: pd.DataFrame) -> pd.DataFrame:
    """
    Function that creates a new column fg3a_share which is the ratio of fg3m_home to fg3a_home
    Args:
        games: DataFrame containing the games data
    Returns:
        DataFrame with a new column fg3a_share
    """
    # Delete all games before 1990
    games['game_date'] = pd.to_datetime(games['game_date'])
    games = games[games['game_date'] >= '1990-01-01']
    # Create a new column which is 1 if wl_home is 'W' and 0 otherwise
    games['home_win'] = (games['wl_home'] == 'W').astype(int)
    # Define a new column fg3a_share which fga_home / fg3a_home
    games['fg3a_share'] = games['fg3m_home'] / games['fg3a_home']
    return games

def run_regressions(data: pd.DataFrame) -> pd.DataFrame:
    """
    Function that runs a regression of home_win on fg3a_share
    Args:
        data: DataFrame containing the fg3a data
    Returns:
        DataFrame with the regression results
    """
    model_results = pd.DataFrame(columns=['year', 'fg3a_share_coefficient', 'p_value', 'r2', 'se_min', 'se_max'])
    # Group by year and run the regression for each season
    for year, data in data.groupby(data['game_date'].dt.year):
        # Drop all rows where fg3_pct_home is NULL
        data = data.dropna(subset=['home_win', 'fg3a_share'])
        model = three_pointer_regression(data)

        # Ensure se_min is smaller than se_max
        conf_int = model.conf_int().loc['fg3a_share']
        se_min, se_max = sorted(conf_int)

        # Create a temporary DataFrame for each year’s results and concatenate
        temp_df = pd.DataFrame({
            'year': [year],
            'fg3a_share_coefficient': [model.params['fg3a_share']],
            'p_value': [model.pvalues['fg3a_share']],
            'r2': [model.rsquared],
            'se_min': [se_min],
            'se_max': [se_max]
        })
        model_results = pd.concat([model_results, temp_df], ignore_index=True)
    # Ensure the columns are numeric
    model_results['year'] = pd.to_numeric(model_results['year'])
    model_results['se_min'] = pd.to_numeric(model_results['se_min'])
    model_results['se_max'] = pd.to_numeric(model_results['se_max'])
    return model_results

# 2. Insights ___________
def get_avg_fg3_data(con: sql.Connection) -> pd.DataFrame:
    query = """
    SELECT strftime('%Y', game_date) AS year, AVG(fg3_pct_home) AS avg_fg3_pct_home
    FROM game
    WHERE strftime('%Y', game_date) >= '1990'
    GROUP BY year;
    """
    data = pd.read_sql(query, con)
    data['year'] = pd.to_numeric(data['year'])
    return data

# 3. Insights ___________
def create_team_win_statistics(con: sql.Connection) -> None:
    # Drop the table if it already exists
    con.execute("DROP TABLE IF EXISTS team_win_statistics")
    query = """
    CREATE TABLE team_win_statistics AS
    SELECT
        game.team_id_home AS team_id,
        game.game_id AS game_id,
        game.game_date AS date,
        CASE WHEN game.wl_home = 'W' THEN 1 ELSE 0 END AS win
    FROM game
    ORDER BY team_id, date;
    """
    con.execute(query)

    query = """
    ALTER TABLE team_win_statistics
    ADD COLUMN team_name TEXT;
    """
    con.execute(query)

    query = """
    UPDATE team_win_statistics
    SET team_name = (
        SELECT team_details.nickname
        FROM team_details
        WHERE team_details.team_id = team_win_statistics.team_id
    );
    """
    con.execute(query)

    query="""
    ALTER TABLE team_win_statistics
    ADD COLUMN ma_41 FLOAT;
    """
    con.execute(query)

    return None


def create_team_win_statistics_with_ma(con: sql.Connection) -> None:
    # Drop the table if it already exists
    con.execute("DROP TABLE IF EXISTS team_win_statistics_with_ma")
    query = """
    CREATE TABLE team_win_statistics_with_ma AS
    SELECT
        team_id,
        game_id,
        date,
        win,
        team_name,
        ROUND(SUM(win) OVER (
            PARTITION BY team_name
            ORDER BY date
            ROWS BETWEEN 40 PRECEDING AND CURRENT ROW
        ) / 41.0, 3) AS ma_41
    FROM team_win_statistics
    ORDER BY team_id, date;
    """
    con.execute(query)


    # Delete all teams where the team_name is NULL
    query = """
    DELETE FROM team_win_statistics_with_ma
    WHERE team_name IS NULL;
    """
    con.execute(query)
    return None


def get_ma41_data(con: sql.Connection) -> pd.DataFrame:
    """
    Creates and returns a DataFrame containing the moving average of wins for each team over the last 41 home games.
    Args:
        con: SQLite connection
    Returns:
        DataFrame: DataFrame containing the moving average of wins for each team over the last 41 home games.
    """
    # First, create the ordinary win statistics table
    create_team_win_statistics(con)
    # Then, create the table containing moving average
    create_team_win_statistics_with_ma(con)

    # Select all data from the team_win_statistics_with_ma table
    query = """
    SELECT *
    FROM team_win_statistics_with_ma
    """
    data = pd.read_sql(query, con)

    # Return the entire team_win_statistics_with_ma table
    return data



def clean_ma_data(data: pd.DataFrame, teams: list) -> pd.DataFrame:
    """
    A function that cleans the moving average data by transforming the date column to a datetime object,
    dropping all rows before 2008 and all rows where team_name is NULL, filtering the data to only include the teams in the list,
    and dropping the first 41 rows of each group.
    Args:
        data: DataFrame containing the moving average data
        teams: List of teams to include in the data
    Returns:
        DataFrame: Cleaned DataFrame containing the moving average data
    """

    # Transform the date column to a datetime object
    data['date'] = pd.to_datetime(data['date'])

    # Drop all rows before 2008 and all rows where team_name is NULL
    data = data[data['date'] >= '2008-01-01']
    data = data.dropna(subset=['team_name'])

    # Filter the data to only include the teams in the list
    data = data[data['team_name'].isin(teams)]

    # Drop the first 41 rows of each group
    data = data.apply(lambda x: x.iloc[41:])

    return data
