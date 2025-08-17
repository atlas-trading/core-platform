from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class MarketOrderRequestDTO:
    ticker: str
    amount: float
