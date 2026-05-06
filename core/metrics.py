from __future__ import annotations

import numpy as np
import pandas as pd


REQUIRED_RAW_COLUMNS = [
    "impressions",
    "clicks",
    "spend",
    "orders",
    "sales",
]


def validate_raw_metrics(df: pd.DataFrame) -> None:
    missing = [col for col in REQUIRED_RAW_COLUMNS if col not in df.columns]

    if missing:
        raise ValueError(
            f"Missing required raw metric columns: {missing}. "
            f"Required columns are: {REQUIRED_RAW_COLUMNS}"
        )


def safe_divide(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    result = numerator / denominator.replace(0, np.nan)
    return result.fillna(0.0)


def add_derived_metrics(df: pd.DataFrame, overwrite: bool = True) -> pd.DataFrame:
    """
    Adds CTR, CVR, CPC, ROAS and ACoS.

    If overwrite=True, existing derived metrics are recalculated.
    This is recommended because raw metrics should be the source of truth.
    """
    validate_raw_metrics(df)

    result = df.copy()

    calculated = {
        "ctr": safe_divide(result["clicks"], result["impressions"]),
        "cvr": safe_divide(result["orders"], result["clicks"]),
        "cpc": safe_divide(result["spend"], result["clicks"]),
        "roas": safe_divide(result["sales"], result["spend"]),
        "acos": safe_divide(result["spend"], result["sales"]),
    }

    for metric_name, metric_values in calculated.items():
        if overwrite or metric_name not in result.columns:
            result[metric_name] = metric_values

    return result