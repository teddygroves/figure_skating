"""Plotting functions."""

import arviz as az
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns


def plot_marginals(
    infd: az.InferenceData,
    var_name: str,
    ax: plt.Axes,
    true_values: pd.Series = None,
):
    """Plot marginal 10%-90% intervals, with true values if available."""
    qs = infd.posterior[var_name].to_series().unstack().quantile([0.1, 0.9]).T
    qs = qs.sort_values(0.9)
    y = np.linspace(*ax.get_ylim(), len(qs))
    ax.set_yticks(y)
    ax.set_yticklabels(qs.index)
    ax.hlines(
        y, qs[0.1], qs[0.9], color="tab:blue", label="90% marginal interval"
    )
    if true_values is not None:
        qs["truth"] = true_values
        qs["truth_in_interval"] = (qs["truth"] < qs[0.9]) & (
            qs["truth"] > qs[0.1]
        )
        ax.scatter(
            qs["truth"], y, marker="|", color="red", label="True ability"
        )
    ax.legend(frameon=False)
    return ax


def plot_ppc(infd: az.InferenceData, scores: pd.DataFrame, ax: plt.Axes):
    """Plot observed scores vs predictive distributions."""
    ix = scores.sort_values("score").index
    obs_score = scores.sort_values("score")["score"].values
    bins = (
        infd.posterior_predictive["yrep"]
        .to_series()
        .subtract(6)
        .astype(int)
        .reset_index()
        .groupby(["measurement", "yrep"])
        .size()
        .unstack()
        .pipe(lambda df: df.div(df.sum(axis=1), axis=0))
        .reindex(ix)
        .set_index(obs_score)
        .rename_axis("Observed score")
        .rename_axis("Predicted score", axis=1)
        .T
    )
    ax = sns.heatmap(
        bins, cmap="YlGnBu", ax=ax, cbar_kws={"label": "Modelled probability"}
    )
    ax.invert_yaxis()
    return ax
