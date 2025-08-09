from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class OrderResultDTO:
    """order placement result."""

    exchange: str
    order_id: str
    status: str
    filled: float
    remaining: float
    price: float | None
