from __future__ import annotations

from typing import Any

from app.ccxt.domain.exchange import Exchange
from app.ccxt.dtos.order.limit_order_request_dto import LimitOrderRequestDTO


class FutureOrder:
    def __init__(self, exchange: Exchange) -> None:
        self._client = exchange.client

        if not exchange.is_future():
            raise ValueError("Exchange must be a future market type.")

    # ---------------------------------------------------------
    # Future Order Methods
    # ---------------------------------------------------------
    async def open_long_limit_order(
        self, limit_order: LimitOrderRequestDTO
    ) -> list[dict[str, Any]]:
        return await self._client.create_limit_buy_order(
            symbol=limit_order.ticker, amount=limit_order.amount, price=limit_order.price
        )

    async def open_short_limit_order(
        self, limit_order: LimitOrderRequestDTO
    ) -> list[dict[str, Any]]:
        return await self._client.create_limit_sell_order(
            symbol=limit_order.ticker, amount=limit_order.amount, price=limit_order.price
        )

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
