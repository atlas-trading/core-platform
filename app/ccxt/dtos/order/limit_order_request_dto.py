from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class LimitOrderRequestDTO:
    ticker: str
    amount: float
    price: float
