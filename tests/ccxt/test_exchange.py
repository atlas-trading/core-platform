from __future__ import annotations

import pytest

from app.ccxt.domain.exchange import Binance, Bybit


@pytest.mark.asyncio
async def test_binance_init() -> None:
    exchange = Binance()
    try:
        assert exchange.exchange is not None
        assert exchange.exchange.id == "binance"
    finally:
        await exchange.close()


@pytest.mark.asyncio
async def test_bybit_init() -> None:
    exchange = Bybit()
    try:
        assert exchange.exchange is not None
        assert exchange.exchange.id == "bybit"
    finally:
        await exchange.close()
