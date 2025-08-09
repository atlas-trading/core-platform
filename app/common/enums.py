from __future__ import annotations

from enum import Enum


class OrderSide(str, Enum):
    BUY = "buy"
    SELL = "sell"


class OrderType(str, Enum):
    MARKET = "market"
    LIMIT = "limit"


class MarginMode(str, Enum):
    ISOLATED = "isolated"
    CROSS = "cross"


class Transport(str, Enum):
    AUTO = "auto"
    WS = "ws"
    REST = "rest"
