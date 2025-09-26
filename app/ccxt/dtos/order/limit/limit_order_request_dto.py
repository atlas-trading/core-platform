from dataclasses import dataclass

from app.ccxt.enums.time_in_force import TimeInForce


@dataclass(slots=True, frozen=True)
class LimitOrderRequestDTO:
    ticker: str
    amount: float
    price: float
    time_in_force: TimeInForce = TimeInForce.GTC
