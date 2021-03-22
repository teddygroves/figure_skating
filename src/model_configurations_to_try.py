"""Define a list of ModelConfiguration objects called MODEL_CONFIGURATIONS."""

import os
from .util import get_99_pct_params_ln, get_99_pct_params_n
from .model_configuration import ModelConfiguration
from .pandas_to_cmdstanpy import get_stan_input
from .cmdstanpy_to_arviz import get_infd_kwargs


# Location of this file
HERE = os.path.dirname(os.path.abspath(__file__))

SIMPLE_MODEL_FILE = os.path.join(HERE, "stan", "simple.stan")
PRIORS = {
    "prior_mu": [0.5, 0.3],
    "prior_cutpoint_diffs": [0.9, 0.4],
}
# Configure cmdstanpy.CmdStanModel.sample
SAMPLE_KWARGS = dict(
    show_progress=True,
    save_warmup=False,
    iter_warmup=2000,
    iter_sampling=2000,
)

# Configuration of model.stan with an interaction between covariates A and B.
SIMPLE_PRIOR = ModelConfiguration(
    name="simple_prior",
    stan_file=SIMPLE_MODEL_FILE,
    stan_input_function=lambda df: get_stan_input(df, PRIORS, likelihood=False),
    infd_kwargs_function=lambda df: get_infd_kwargs(df, SAMPLE_KWARGS),
    sample_kwargs=SAMPLE_KWARGS,
)
SIMPLE_POSTERIOR = ModelConfiguration(
    name="simple_posterior",
    stan_file=SIMPLE_MODEL_FILE,
    stan_input_function=lambda df: get_stan_input(df, PRIORS, likelihood=True),
    infd_kwargs_function=lambda df: get_infd_kwargs(df, SAMPLE_KWARGS),
    sample_kwargs=SAMPLE_KWARGS,
)

# A list of model configurations to test
MODEL_CONFIGURATIONS = [SIMPLE_PRIOR, SIMPLE_POSTERIOR]
