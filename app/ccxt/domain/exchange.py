from __future__ import annotations

import ccxt.async_support as ccxt

from app.ccxt.enums.exchange_id import ExchangeID
from app.core.config import BINANCE_API_KEY, BINANCE_API_SECRET, BYBIT_API_KEY, BYBIT_API_SECRET


class Exchange:
    def __init__(self, exchange_id: str, api_key: str, secret: str) -> None:
        self._client = getattr(ccxt, exchange_id)(
            {
                "apiKey": api_key,
                "secret": secret,
                "enableRateLimit": True,
                "options": {"defaultType": "future"},
            }
        )

    @property
    def client(self) -> ccxt.Exchange:
        return self._client

    async def close(self) -> None:
        if hasattr(self._client, "close"):
            await self._client.close()


class Binance(Exchange):
    def __init__(self) -> None:
        super().__init__(ExchangeID.BINANCE, BINANCE_API_KEY, BINANCE_API_SECRET)


class Bybit(Exchange):
    def __init__(self) -> None:
        super().__init__(ExchangeID.BYBIT, BYBIT_API_KEY, BYBIT_API_SECRET)
