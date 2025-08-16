from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class FutureFundingRateDTO:
    market_price: float  # 117700.0 (price of current exchanges)
    index_price: float  # 117700.0 (average price of various exchanges)
    interest_rate: float  # 0.0003 (interest rate for the funding period)
    funding_rate: float  # 0.000072 (funding rate for the period)
    funding_timestamp: int  # 1755362327800
    funding_datetime: str  # 2025-08-16T16:38:43.278Z
    next_funding_rate: float | None = None  # optional: -0.000018
    interval: str | None = None  # optional: 8h
