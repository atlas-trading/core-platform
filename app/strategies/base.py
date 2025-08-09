from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Strategy(ABC):
    """Strategy interface.

    - Provides interface-based extensibility to follow the Open-Closed Principle
    """

    name: str

    @abstractmethod
    async def on_tick(self, market_data: dict[str, Any]) -> None:
        """Handle realtime market data events."""

    @abstractmethod
    async def generate_order(self) -> dict[str, Any] | None:
        """Generate order signal."""


class NoopStrategy(Strategy):
    """Example strategy: no operation."""

    name = "noop"

    async def on_tick(self, market_data: dict[str, Any]) -> None:
        return None

    async def generate_order(self) -> dict[str, Any] | None:
        return None
