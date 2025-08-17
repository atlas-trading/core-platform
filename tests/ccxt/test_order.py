from __future__ import annotations

from collections.abc import AsyncGenerator
from datetime import UTC, datetime

import pytest
import pytest_asyncio

from app.ccxt.api.spot_order import Order
from app.ccxt.domain.exchange import Binance
from app.ccxt.dtos.balance_dto import AssetBalanceDTO, BalanceDTO
from app.ccxt.enums.market_type import MarketType


@pytest_asyncio.fixture
async def order() -> AsyncGenerator[Order, None]:
    exchange = Binance(market_type=MarketType.SPOT)
    api = Order(exchange)

    yield api

    await exchange.close()


@pytest.mark.asyncio
async def test_fetch_balance(order: Order) -> None:
    balance = await order.fetch_balance()

    # verify balance DTO
    assert isinstance(balance, BalanceDTO)
    assert isinstance(balance.balances, dict)

    # verify timestamp and datetime if present
    if balance.timestamp is not None:
        assert isinstance(balance.timestamp, int)
        dt = datetime.fromtimestamp(balance.timestamp / 1000, tz=UTC)
        assert dt < datetime.now(UTC)  # timestamp should be in the past

    if balance.datetime is not None:
        assert isinstance(balance.datetime, str)
        assert balance.datetime.endswith("Z")  # ISO 8601 UTC

    # verify balances if present
    for currency, asset_balance in balance.balances.items():
        assert isinstance(currency, str)
        assert isinstance(asset_balance, AssetBalanceDTO)
        assert isinstance(asset_balance.free, float)
        assert isinstance(asset_balance.used, float)
        assert isinstance(asset_balance.total, float)

        assert asset_balance.free >= 0
        assert asset_balance.used >= 0
        assert asset_balance.total >= 0
        assert (
            abs(asset_balance.total - (asset_balance.free + asset_balance.used)) < 0.00001
        )  # floating point 오차 허용
