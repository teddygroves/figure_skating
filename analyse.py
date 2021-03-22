import os
import arviz as az
import pandas as pd
from src.plotting import plot_marginals, plot_ppc
from matplotlib import pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
PREPARED_DATA_CSV = os.path.join(
    HERE, "data", "prepared", "scores_prepared.csv"
)
PLOT_DIR = os.path.join(HERE, "results", "plots")
NCDF_FILE = os.path.join(
    HERE,
    "results",
    "infd",
    "infd_real_study-20210322173057-simple_prior.ncdf",
)


def main():
    infd = az.from_netcdf(NCDF_FILE)
    scores = pd.read_csv(PREPARED_DATA_CSV)
    # true_abilities = scores.groupby("name")["true_ability"].first()

    f, ax = plt.subplots(figsize=[6, 16])
    ax = plot_marginals(infd, "ability", ax)
    f.savefig(os.path.join(PLOT_DIR, "marginals.png"), bbox_inches="tight")

    f, ax = plt.subplots(figsize=[20, 10])
    ax = plot_ppc(infd, scores, ax)
    f.savefig(os.path.join(PLOT_DIR, "ppc.png"), bbox_inches="tight")


if __name__ == "__main__":
    main()
