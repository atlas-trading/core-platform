from __future__ import annotations

import asyncio
from typing import Any

from app.common.enums import Transport
from app.core.config import Settings
from app.exchanges.base import ExchangeFactory


class MarketDataService:
    """provides market data with websocket-preferred, rest-fallback behavior."""

    def __init__(self, exchange_factory: ExchangeFactory, config: Settings):
        self._factory = exchange_factory
        self._config = config

    async def _try_ws(self, exchange_name: str, method: str, *args: Any, **kwargs: Any) -> Any:
        try:
            import ccxt.pro as ccxtpro  # type: ignore

            cls = getattr(ccxtpro, exchange_name)
            client = cls({"enableRateLimit": True})
        except Exception:
            return None
        try:
            coro = getattr(client, method)(*args, **kwargs)
            async with asyncio.timeout(2.0):
                return await coro
        except Exception:
            return None
        finally:
            try:
                await client.close()  # type: ignore[func-returns-value]
            except Exception:
                pass

    async def fetch_ticker(
        self, exchange_name: str, symbol: str, transport: Transport = Transport.AUTO
    ) -> dict[str, Any]:
        if transport in (Transport.AUTO, Transport.WS):
            ws = await self._try_ws(exchange_name, "watch_ticker", symbol)
            if ws is not None:
                return ws
        client = self._factory.create(exchange_name)
        return await client.fetch_ticker(symbol)

    async def fetch_order_book(
        self,
        exchange_name: str,
        symbol: str,
        limit: int | None = None,
        transport: Transport = Transport.AUTO,
    ) -> dict[str, Any]:
        if transport in (Transport.AUTO, Transport.WS):
            ws = await self._try_ws(exchange_name, "watch_order_book", symbol)
            if ws is not None:
                return ws
        client = self._factory.create(exchange_name)
        return await client.fetch_order_book(symbol, limit=limit)

    async def fetch_ohlcv(
        self,
        exchange_name: str,
        symbol: str,
        timeframe: str = "1m",
        since: int | None = None,
        limit: int | None = None,
    ) -> list[list[float | int | None]]:
        client = self._factory.create(exchange_name)
        return await client.fetch_ohlcv(symbol, timeframe=timeframe, since=since, limit=limit)
