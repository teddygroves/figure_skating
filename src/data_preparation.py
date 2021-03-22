"""Provides a function prepare_data."""

import pandas as pd

from .util import make_columns_lower_case

COLS_THAT_MUST_BE_NON_NULL = ["score"]
ELEMENTS = ["3A"]


def filter_data(data: pd.DataFrame) -> pd.Series:
    return data["element"].isin(ELEMENTS)


def prepare_data(raw_data: pd.DataFrame) -> pd.DataFrame:
    """Takes in raw data, returns prepared data.

    :param raw_data: pd.DataFrame of raw data
    ::
    """
    out = (
        raw_data.copy()
        .pipe(make_columns_lower_case)
        .loc[filter_data]
        .dropna(subset=COLS_THAT_MUST_BE_NON_NULL)
        .drop_duplicates()
        .reset_index(drop=True)
    )
    out["attempt_id"] = pd.factorize(
        out["event"].str.cat(out["name"]).str.cat(out["order"].astype(str))
    )[0]
    return out
