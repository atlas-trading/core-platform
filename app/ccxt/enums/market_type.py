from enum import Enum


class MarketType(str, Enum):
    SPOT = "spot"
    FUTURE = "future"
