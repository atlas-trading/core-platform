from __future__ import annotations

from typing import Any

from app.ccxt.domain.exchange import Exchange


class MarketData:
    def __init__(self, exchange: Exchange) -> None:
        self._client = exchange.client

    async def load_markets(self) -> dict[str, Any]:
        return await self._client.load_markets()

    async def fetch_markets(self) -> list[dict[str, Any]]:
        return await self._client.fetch_markets()

    async def fetch_ticker(self, ticker: str) -> dict[str, Any]:
        return await self._client.fetch_ticker(ticker)
