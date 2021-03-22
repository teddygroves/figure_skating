"""Get an input to cmdstanpy.CmdStanModel.sample from a pd.DataFrame."""

from src.util import one_encode
from typing import List, Dict
import pandas as pd

N_GRADE = 11


def get_stan_input(
    scores: pd.DataFrame,
    priors: Dict,
    likelihood: bool,
) -> Dict:
    """Get an input to cmdstanpy.CmdStanModel.sample.

    :param measurements: a pandas DataFrame whose rows represent measurements

    :param model_config: a dictionary with keys "priors", "likelihood" and
    "x_cols".

    """
    return {
        **priors,
        **{
            "N": len(scores),
            "N_skater": scores["name"].nunique(),
            "N_grade": N_GRADE,
            "skater": one_encode(scores["name"]).values,
            "y": scores["score"].astype(int).add(6).values,
            "N_test": len(scores),
            "skater_test": one_encode(scores["name"]).values,
            "y_test": scores["score"].astype(int).add(6).values,
            "likelihood": int(likelihood),
        },
    }
