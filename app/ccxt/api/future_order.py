from __future__ import annotations

from typing import Any

from app.ccxt.domain.exchange import Exchange


class FutureOrder:
    def __init__(self, exchange: Exchange) -> None:
        self._client = exchange.client

    # ---------------------------------------------------------
    # Future Order Methods
    # ---------------------------------------------------------
    async def open_long_limit_order(self) -> list[dict[str, Any]]:
        return await self._client.fetch_open_long_orders()

    async def open_short_limit_order(self) -> list[dict[str, Any]]:
        return await self._client.fetch_open_short_orders()

    async def close_long_limit_order(self) -> list[dict[str, Any]]:
        return await self._client.fetch_closed_long_orders()

    async def close_short_limit_order(self) -> list[dict[str, Any]]:
        return await self._client.fetch_closed_short_orders()

    async def open_long_market_order(self) -> None:
        pass

    async def open_short_market_order(self) -> None:
        pass

    async def close_long_market_order(self) -> None:
        pass

    async def close_short_market_order(self) -> None:
        pass
