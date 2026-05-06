from dataclasses import dataclass


@dataclass(frozen=True)
class GeneratedMetrics:
    impressions: int
    clicks: int
    spend: float
    orders: int
    sales: float
    bid: float