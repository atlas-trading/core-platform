from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class LimitOrderResponseDTO:
    timestamp: int  # 1755365820000
    datetime: str  # 2025-08-16T16:38:43.278Z
    price: float  # float price in quote currency
    average: float  # average price of filled order
    amount: float
    filled: float
    remaining: float
    cost: float  # filled * price
