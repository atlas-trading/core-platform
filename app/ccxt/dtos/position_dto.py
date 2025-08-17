from dataclasses import dataclass
from typing import Literal


@dataclass(slots=True, frozen=True)
class PositionDTO:
    symbol: str  # "BTC/USDT:USDT"
    side: Literal["long", "short"]  # "long" or "short"
    size: float  # 0.123 (BTC)
    notional: float  # 12345.67 (USDT)
    leverage: float  # 10.0
    entry_price: float  # 50000.0
    mark_price: float  # 50100.0
    liquidation_price: float | None = None  # optional: 45000.0
    margin_mode: Literal["cross", "isolated"] | None = None  # optional: "cross" or "isolated"
    unrealized_pnl: float | None = None  # optional: 123.45
    percentage: float | None = None  # optional: 2.47 (profit/loss percentage)
