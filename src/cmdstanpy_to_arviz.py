"""Functions for turning cmdstanpy output into arviz InferenceData objects."""

from typing import List, Dict
import pandas as pd


def get_infd_kwargs(scores: pd.DataFrame, sample_kwargs: Dict) -> Dict:
    """Get a dictionary of keyword arguments to arviz.from_cmdstanpy.

    :param scores: pandas dataframe whose rows represent
    measurements. Must be the same as was used for `get_stan_input`.

    :param x_cols: list of columns of `measurements` representing real-valued
    covariates. Must be the same as was used for `get_stan_input`.

    :param sample_kwargs: dictionary of keyword arguments that were passed to
    cmdstanpy.CmdStanModel.sample.

    """
    return dict(
        log_likelihood="llik",
        observed_data={"y": scores["score"].astype(int).add(6).values},
        posterior_predictive="yrep",
        coords={
            "skater_name": pd.factorize(scores["name"])[1],
            "cutpoint": list(range(-4, 6)),
            "measurement": scores.index,
        },
        dims={
            "cutpoints": ["cutpoint"],
            "yrep": ["measurement"],
            "ability": ["skater_name"],
        },
        save_warmup=sample_kwargs["save_warmup"],
    )
