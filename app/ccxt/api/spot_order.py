from __future__ import annotations

from typing import Any

from app.ccxt.domain.exchange import Exchange
from app.ccxt.dtos.balance_dto import AssetBalanceDTO, BalanceDTO
from app.ccxt.dtos.order.limit.limit_order_request_dto import LimitOrderRequestDTO
from app.ccxt.dtos.order.limit.limit_order_response_dto import LimitOrderResponseDTO
from app.ccxt.dtos.order.market.market_order_request_dto import MarketOrderRequestDTO
from app.ccxt.dtos.order.market.market_order_response_dto import MarketOrderResponseDTO


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
    # Spot Limit Order
    # ---------------------------------------------------------
    async def open_limit_order(self, limit_order: LimitOrderRequestDTO) -> LimitOrderResponseDTO:
        limit_buy_order = await self._client.create_limit_buy_order(
            symbol=limit_order.ticker,
            amount=limit_order.amount,
            price=limit_order.price,
            params={"timeInForce": limit_order.time_in_force.value},
        )

        return LimitOrderResponseDTO(
            timestamp=limit_buy_order.get("timestamp"),
            datetime=limit_buy_order.get("datetime"),
            price=limit_buy_order.get("price"),
            average=limit_buy_order.get("average"),
            amount=limit_buy_order.get("amount"),
            filled=limit_buy_order.get("filled"),
            remaining=limit_buy_order.get("remaining"),
            cost=limit_buy_order.get("cost"),
            fee=limit_buy_order.get("fee").get("cost") if limit_buy_order.get("fee") else None,
        )

    async def close_limit_order(self, limit_order: LimitOrderRequestDTO) -> LimitOrderResponseDTO:
        limit_sell_order = await self._client.create_limit_sell_order(
            symbol=limit_order.ticker,
            amount=limit_order.amount,
            price=limit_order.price,
            params={"timeInForce": limit_order.time_in_force.value},
        )

        return LimitOrderResponseDTO(
            timestamp=limit_sell_order.get("timestamp"),
            datetime=limit_sell_order.get("datetime"),
            price=limit_sell_order.get("price"),
            average=limit_sell_order.get("average"),
            amount=limit_sell_order.get("amount"),
            filled=limit_sell_order.get("filled"),
            remaining=limit_sell_order.get("remaining"),
            cost=limit_sell_order.get("cost"),
            fee=limit_sell_order.get("fee").get("cost") if limit_sell_order.get("fee") else None,
        )

    # ---------------------------------------------------------
    # Spot Market Order
    # ---------------------------------------------------------
    async def open_market_order(
        self, market_order: MarketOrderRequestDTO
    ) -> MarketOrderResponseDTO:
        market_buy_order = await self._client.create_market_buy_order(
            symbol=market_order.ticker, amount=market_order.amount
        )

        return MarketOrderResponseDTO(
            timestamp=market_buy_order.get("timestamp"),
            datetime=market_buy_order.get("datetime"),
            price=market_buy_order.get("price"),
            average=market_buy_order.get("average"),
            amount=market_buy_order.get("amount"),
            filled=market_buy_order.get("filled"),
            remaining=market_buy_order.get("remaining"),
            cost=market_buy_order.get("cost"),
            fee=market_buy_order.get("fee").get("cost") if market_buy_order.get("fee") else None,
        )

    async def close_market_order(
        self, limit_order: MarketOrderRequestDTO
    ) -> MarketOrderResponseDTO:
        market_sell_order = await self._client.create_market_sell_order(
            symbol=limit_order.ticker, amount=limit_order.amount
        )
        return MarketOrderResponseDTO(
            timestamp=market_sell_order.get("timestamp"),
            datetime=market_sell_order.get("datetime"),
            price=market_sell_order.get("price"),
            average=market_sell_order.get("average"),
            amount=market_sell_order.get("amount"),
            filled=market_sell_order.get("filled"),
            remaining=market_sell_order.get("remaining"),
            cost=market_sell_order.get("cost"),
            fee=market_sell_order.get("fee").get("cost") if market_sell_order.get("fee") else None,
        )
