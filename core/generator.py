from __future__ import annotations

import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

from core.GeneratedMetrics import GeneratedMetrics
from core.config_loader import index_by
from core.metrics import add_derived_metrics


def set_random_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)


def random_float(low: float, high: float) -> float:
    return float(np.random.uniform(low, high))


def random_int(low: int, high: int) -> int:
    return int(np.random.randint(low, high + 1))


def calculate_metrics(
    campaign: dict,
    product: dict,
    keyword: dict,
) -> GeneratedMetrics:
    base_impressions = random_int(*campaign["base_impressions"])
    base_ctr = random_float(*campaign["base_ctr"])
    base_cvr = random_float(*campaign["base_cvr"])
    base_cpc = random_float(*campaign["base_cpc"])

    ctr = base_ctr * keyword["ctr_modifier"]
    cvr = base_cvr * keyword["cvr_modifier"] * product["conversion_modifier"]
    cpc = base_cpc * keyword["cpc_modifier"]

    ctr *= random_float(0.85, 1.15)
    cvr *= random_float(0.80, 1.20)
    cpc *= random_float(0.90, 1.10)

    ctr = max(0.0001, ctr)
    cvr = max(0.0001, cvr)
    cpc = max(0.05, cpc)

    impressions = base_impressions
    clicks = int(round(impressions * ctr))
    orders = int(round(clicks * cvr))

    spend = round(clicks * cpc, 2)

    price_multiplier = random_float(0.90, 1.10)
    average_order_value = product["base_price"] * price_multiplier
    sales = round(orders * average_order_value, 2)

    # bid = controllable max bid
    # cpc = observed actual cost per click
    bid = round(cpc * random_float(1.05, 1.35), 2)

    return GeneratedMetrics(
        impressions=impressions,
        clicks=clicks,
        spend=spend,
        orders=orders,
        sales=sales,
        bid=bid,
    )


def generate_dataset(
    campaigns: list[dict],
    products: list[dict],
    keywords: list[dict],
    campaign_structure: dict,
    days: int = 30,
) -> pd.DataFrame:
    product_by_asin = index_by(products, "asin")
    keyword_by_target = index_by(keywords, "keyword_target")

    rows = []
    start_date = datetime.today() - timedelta(days=days)

    for day_offset in range(days):
        current_date = start_date + timedelta(days=day_offset)

        for campaign in campaigns:
            campaign_id = campaign["campaign_id"]

            if campaign_id not in campaign_structure:
                raise ValueError(f"No campaign structure found for: {campaign_id}")

            structure = campaign_structure[campaign_id]

            for asin, keyword_targets in structure.items():
                if asin not in product_by_asin:
                    raise ValueError(f"Unknown ASIN in campaign structure: {asin}")

                product = product_by_asin[asin]

                for keyword_target in keyword_targets:
                    if keyword_target not in keyword_by_target:
                        raise ValueError(
                            f"Unknown keyword target in campaign structure: {keyword_target}"
                        )

                    keyword = keyword_by_target[keyword_target]

                    metrics = calculate_metrics(
                        campaign=campaign,
                        product=product,
                        keyword=keyword,
                    )

                    rows.append(
                        {
                            "date": current_date.strftime("%Y-%m-%d"),
                            "market": campaign["market"],

                            "campaign_id": campaign["campaign_id"],
                            "campaign_name": campaign["campaign_name"],

                            "asin": product["asin"],
                            "product_name": product["product_name"],

                            "keyword_target": keyword["keyword_target"],

                            # Raw Amazon Ads-like metrics
                            "impressions": metrics.impressions,
                            "clicks": metrics.clicks,
                            "spend": metrics.spend,
                            "orders": metrics.orders,
                            "sales": metrics.sales,

                            # Controllable parameters
                            "bid": metrics.bid,
                            "daily_budget": campaign["daily_budget"],
                        }
                    )

    df = pd.DataFrame(rows)

    # Derived metrics are always calculated in one place.
    # df = add_derived_metrics(df, overwrite=True)

    return df