from __future__ import annotations

from typing import Any

from app.exchanges.base import ExchangeFactory, OrderRequest
from app.risk.manager import RiskManager


class TradingService:
    """Service that orchestrates the order placement flow."""

    def __init__(self, exchange_factory: ExchangeFactory, risk_manager: RiskManager):
        self._exchange_factory = exchange_factory
        self._risk_manager = risk_manager

    async def place_order(
        self,
        exchange_name: str,
        symbol: str,
        side: str,
        order_type: str,
        amount: float,
        price: float | None,
    ) -> dict[str, Any]:
        exchange = self._exchange_factory.create(exchange_name)

        ticker = await exchange.fetch_ticker(symbol)
        last_price = float(ticker.get("last") or ticker.get("close") or 0) or None

        request = OrderRequest(
            symbol=symbol, side=side, type=order_type, amount=amount, price=price
        )
        self._risk_manager.validate_order(request, last_price)

        response = await exchange.create_order(request)

        if response.remaining and response.remaining > 0:
            await self._risk_manager.on_partial_fill(request, response)

        return {
            "exchange": exchange.id(),
            "order_id": response.id,
            "status": response.status,
            "filled": response.filled,
            "remaining": response.remaining,
            "price": response.price,
        }
