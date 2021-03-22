"""Function for generating fake data."""


from cmdstanpy import CmdStanModel
import numpy as np
import pandas as pd

from .model_configurations_to_try import SIMPLE_POSTERIOR as TRUE_MODEL_CONFIG


# True values for each variable in your program's `parameters` block. Make sure
# that the dimensions agree with `TRUE_MODEL_FILE`!
TRUE_PARAM_VALUES = {
    "mu": 0.1,
    "cutpoint_diffs": [0.5, 1.0, 0.6, 0.8, 1.2, 0.5, 0.6, 0.4, 0.9],
}


def generate_fake_measurements(real_data: pd.DataFrame) -> pd.DataFrame:
    """Fake a table of measurements by simulating from the true model.

    You will need to customise this function to make sure it matches the data
    generating process you want to simulate from.

    :param real_data: dataframe of real data to copy

    """
    true_param_values = TRUE_PARAM_VALUES.copy()
    true_param_values["ability"] = np.random.normal(
        0, 1, real_data["name"].nunique()
    )
    fake_data = real_data.copy()
    fake_data["score"] = 0
    name_to_ability = dict(
        zip(pd.factorize(fake_data["name"])[1], true_param_values["ability"])
    )
    fake_data["true_ability"] = fake_data["name"].map(name_to_ability)
    model = CmdStanModel(stan_file=TRUE_MODEL_CONFIG.stan_file)
    stan_input = TRUE_MODEL_CONFIG.stan_input_function(fake_data)
    mcmc = model.sample(
        stan_input, inits=true_param_values, fixed_param=True, iter_sampling=1
    )
    return fake_data.assign(score=mcmc.stan_variable("yrep")[0] - 6)
