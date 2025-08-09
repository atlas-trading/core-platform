from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True, frozen=True)
class TickerDTO:
    ticker: str
    last: float | None
    bid: float | None
    ask: float | None
    timestamp: int | None
    raw: dict[str, Any]


@dataclass(slots=True, frozen=True)
class OrderBookDTO:
    ticker: str
    bids: list[list[float]]
    asks: list[list[float]]
    timestamp: int | None
    nonce: int | None
    raw: dict[str, Any]


@dataclass(slots=True, frozen=True)
class OHLCVItemDTO:
    ts: int
    open: float
    high: float
    low: float
    close: float
    volume: float


@dataclass(slots=True, frozen=True)
class OHLCVDTO:
    ticker: str
    timeframe: str
    candles: list[OHLCVItemDTO]
    raw: list[list[float | int | None]]
