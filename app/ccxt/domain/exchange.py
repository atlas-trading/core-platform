from __future__ import annotations

import ccxt.async_support as ccxt

from app.ccxt.enums.exchange_type import ExchangeType
from app.ccxt.enums.market_type import MarketType
from app.core.config import (
    BINANCE_API_KEY,
    BINANCE_API_SECRET,
    BINANCE_TESTNET_API_KEY,
    BINANCE_TESTNET_API_SECRET,
    BYBIT_API_KEY,
    BYBIT_API_SECRET,
)


class Exchange:
    def __init__(
        self,
        exchange_id: str,
        api_key: str,
        secret: str,
        market_type: MarketType,
    ) -> None:
        self._client = getattr(ccxt, exchange_id)(
            {
                "apiKey": api_key,
                "secret": secret,
                "enableRateLimit": True,
                "options": {"defaultType": market_type},
            }
        )

    @property
    def client(self) -> ccxt.Exchange:
        return self._client

    def is_future(self) -> bool:
        return self._client.options.get("defaultType") == MarketType.FUTURE

    def is_spot(self) -> bool:
        return self._client.options.get("defaultType") == MarketType.SPOT

    async def close(self) -> None:
        if hasattr(self._client, "close"):
            await self._client.close()


class Binance(Exchange):
    def __init__(self, market_type: MarketType) -> None:
        super().__init__(ExchangeType.BINANCE, BINANCE_API_KEY, BINANCE_API_SECRET, market_type)


class BinanceTestnet(Exchange):
    def __init__(self, market_type: MarketType) -> None:
        super().__init__(
            ExchangeType.BINANCE, BINANCE_TESTNET_API_KEY, BINANCE_TESTNET_API_SECRET, market_type
        )
        self._client.set_sandbox_mode(True)


class Bybit(Exchange):
    def __init__(self, market_type: MarketType) -> None:
        super().__init__(ExchangeType.BYBIT, BYBIT_API_KEY, BYBIT_API_SECRET, market_type)
