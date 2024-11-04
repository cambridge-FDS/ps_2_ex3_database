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
