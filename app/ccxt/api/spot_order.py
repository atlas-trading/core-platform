from __future__ import annotations

from typing import Any

from app.ccxt.domain.exchange import Exchange
from app.ccxt.dtos.balance_dto import AssetBalanceDTO, BalanceDTO
from app.ccxt.dtos.order.limit_order_request_dto import LimitOrderRequestDTO
from app.ccxt.dtos.order.limit_order_response_dto import LimitOrderResponseDTO
from app.ccxt.dtos.order.market_order_request_dto import MarketOrderRequestDTO
from app.ccxt.dtos.order.market_order_response_dto import MarketOrderResponseDTO


class SpotOrder:
    def __init__(self, exchange: Exchange) -> None:
        self._client = exchange.client

        if not exchange.is_spot():
            raise ValueError("Exchange must be a spot market type.")

    async def fetch_balance(self) -> BalanceDTO:
        """
        거래소 계정의 자산 잔고를 조회합니다.
        """
        balance_info: dict[str, Any] = await self._client.fetch_balance()

        # TODO(yeonghwan): balance doesn't show position information.
        balances = {
            currency: AssetBalanceDTO(
                free=float(info["free"]),
                used=float(info["used"]),
                total=float(info["total"]),
            )
            for currency, info in balance_info.items()
            if isinstance(info, dict)  # 'free', 'used', 'total' 키를 가진 딕셔너리만 처리
            and all(key in info for key in ["free", "used", "total"])
        }

        return BalanceDTO(
            balances=balances,
            timestamp=balance_info.get("timestamp"),
            datetime=balance_info.get("datetime"),
        )

    # ---------------------------------------------------------
    # Spot Order Methods
    # ---------------------------------------------------------
    async def open_limit_order(self, limit_order: LimitOrderRequestDTO) -> list[dict[str, Any]]:
        limit_buy_order = await self._client.create_limit_buy_order(
            symbol=limit_order.ticker, amount=limit_order.amount, price=limit_order.price
        )

        return limit_buy_order

    async def close_limit_order(self, limit_order: LimitOrderRequestDTO) -> LimitOrderResponseDTO:
        order_result = await self._client.create_limit_sell_order(
            symbol=limit_order.ticker, amount=limit_order.amount, price=limit_order.price
        )

        return LimitOrderResponseDTO(
            timestamp=order_result.timestamp,
            datetime=order_result.datetime,
            price=order_result.price,
            average=order_result.average,
            amount=order_result.amount,
            filled=order_result.filled,
            remaining=order_result.remaining,
            cost=order_result.cost,
        )

    async def open_market_order(self) -> None:
        pass

    async def close_market_order(
        self, limit_order: MarketOrderRequestDTO
    ) -> MarketOrderResponseDTO:
        order_result = await self._client.create_market_sell_order(
            symbol=limit_order.ticker, amount=limit_order.amount
        )
        return MarketOrderResponseDTO(
            timestamp=order_result.timestamp,
            datetime=order_result.datetime,
            price=order_result.price,
            average=order_result.average,
            amount=order_result.amount,
            filled=order_result.filled,
            remaining=order_result.remaining,
            cost=order_result.cost,
            fee=order_result.fee["cost"],
        )
