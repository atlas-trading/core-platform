from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class PriceLevelDTO:
    price: float  # 117700.1
    amount: float  # 10.601`


@dataclass(slots=True, frozen=True)
class OrderBookDTO:
    asks: list[PriceLevelDTO]  # [[117700.1, 10.601], ..., [117766.6, 0.514]]
    bids: list[PriceLevelDTO]  # [[117700.0, 989.123], ..., [117634.9, 0.03]]
    symbol: str  # BTC/USDT
    datetime: str  # 2025-08-16T16:38:43.278Z
    timestamp: int  # 17553623278
    nonce: int  # 8358168772439
