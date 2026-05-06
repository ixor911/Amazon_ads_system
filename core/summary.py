from __future__ import annotations

import pandas as pd

from core.metrics import add_derived_metrics


def summarize_by(
    df: pd.DataFrame,
    group_cols: list[str],
) -> pd.DataFrame:
    summary = (
        df.groupby(group_cols)
        .agg(
            impressions=("impressions", "sum"),
            clicks=("clicks", "sum"),
            spend=("spend", "sum"),
            orders=("orders", "sum"),
            sales=("sales", "sum"),
            avg_bid=("bid", "mean"),
            avg_daily_budget=("daily_budget", "mean"),
        )
        .reset_index()
    )

    summary = add_derived_metrics(summary, overwrite=True)

    return summary.round(
        {
            "spend": 2,
            "sales": 2,
            "avg_bid": 2,
            "avg_daily_budget": 2,
            "ctr": 5,
            "cvr": 5,
            "cpc": 2,
            "roas": 2,
            "acos": 2,
        }
    )


def print_dataset_summary(df: pd.DataFrame) -> None:
    print("\nPreview:")
    print(df.head(10).to_string(index=False))

    print("\nDataset shape:")
    print(df.shape)

    print("\nRows per campaign:")
    print(df["campaign_id"].value_counts())

    print("\nRows per product:")
    print(df["asin"].value_counts())

    print("\nRows per keyword target:")
    print(df["keyword_target"].value_counts())

    print("\nCampaign-level summary:")
    print(
        summarize_by(
            df,
            ["campaign_id", "campaign_name"],
        ).to_string(index=False)
    )

    print("\nProduct-level summary:")
    print(
        summarize_by(
            df,
            ["asin", "product_name"],
        ).to_string(index=False)
    )

    print("\nKeyword-level summary:")
    print(
        summarize_by(
            df,
            ["keyword_target"],
        ).to_string(index=False)
    )

    print("\nCampaign + Product summary:")
    print(
        summarize_by(
            df,
            ["campaign_id", "asin", "product_name"],
        ).to_string(index=False)
    )