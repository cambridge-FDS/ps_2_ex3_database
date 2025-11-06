import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.discrete.discrete_model import BinaryResultsWrapper
from statsmodels.stats.contrast import ContrastResults


def run_halftime_log_reg(
    df: pd.DataFrame,
) -> tuple[BinaryResultsWrapper, ContrastResults]:
    df["abs_half_home_lead"] = np.abs(df["half_home_lead"])
    endog = df["home_win"]
    exog = sm.add_constant(df[["half_home_lead", "abs_half_home_lead"]])

    model = sm.Logit(endog, exog).fit()

    R = np.array([[1, 0, 0], [0, 0, 1]])
    wald_results = model.wald_test(R)
    return (model, wald_results)
