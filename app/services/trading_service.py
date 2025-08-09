from __future__ import annotations

from app.common.enums import OrderSide, OrderType
from app.dto.trading import OrderResultDTO
from app.exchanges.base import ExchangeFactory, OrderRequest
from app.risk.manager import RiskManager


class TradingService:
    """service that orchestrates the order placement flow."""

    def __init__(self, exchange_factory: ExchangeFactory, risk_manager: RiskManager):
        self._exchange_factory = exchange_factory
        self._risk_manager = risk_manager

    async def place_order(
        self,
        exchange_name: str,
        ticker: str,
        side: str,
        order_type: str,
        amount: float,
        price: float | None,
    ) -> OrderResultDTO:
        exchange = self._exchange_factory.create(exchange_name)

        t = await exchange.fetch_ticker(ticker)
        last_price = float(t.get("last") or t.get("close") or 0) or None

        request = OrderRequest(
            ticker=ticker,
            side=OrderSide(side),
            type=OrderType(order_type),
            amount=amount,
            price=price,
        )
        self._risk_manager.validate_order(request, last_price)

        response = await exchange.create_order(request)

        if response.remaining and response.remaining > 0:
            await self._risk_manager.on_partial_fill(request, response)

        return OrderResultDTO(
            exchange=exchange.id(),
            order_id=response.id,
            status=response.status,
            filled=response.filled,
            remaining=response.remaining,
            price=response.price,
        )
