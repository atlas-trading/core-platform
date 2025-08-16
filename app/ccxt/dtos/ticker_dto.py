from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class TickerDTO:
    symbol: str  # BTC/USDT:USDT
    timestamp: int  # 17553623278
    datetime: str  # 2025-08-16T16:38:43.278Z
    high: float  # 117859.4
    low: float  # 116812.0
    open: float  # 117080.8
    close: float  # 117700.0
    last: float  # 117700.0
    previous_close: float | None
    vwap: float  # 117428.01
    change: float  # 619.2
    percentage: float  # 0.529
    average: float  # 117390.4
    base_volume: float  # 66556.723
    quote_volume: float  # 7815623475.78
    mark_price: float | None
    index_price: float | None
    bid: float | None
    bid_volume: float | None
    ask: float | None
    ask_volume: float | None
    # info (original data from exchange)
