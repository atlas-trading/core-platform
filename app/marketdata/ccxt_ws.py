from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any

import ccxt.pro as ccxtpro  # type: ignore


class WsStream:
    """Thin wrapper over ccxt.pro streaming methods to standardize usage."""

    def __init__(self, client: Any):
        self._client = client

    async def ticker(self, symbol: str) -> AsyncIterator[dict[str, Any]]:
        while True:
            yield await self._client.watch_ticker(symbol)

    async def order_book(self, symbol: str) -> AsyncIterator[dict[str, Any]]:
        while True:
            yield await self._client.watch_order_book(symbol)

    async def trades(self, symbol: str) -> AsyncIterator[list[dict[str, Any]]]:
        while True:
            yield await self._client.watch_trades(symbol)


def build_ws_client(exchange_id: str, **kwargs: Any) -> Any:
    """Construct ccxt.pro client dynamically by id."""
    cls = getattr(ccxtpro, exchange_id)
    return cls(kwargs)
