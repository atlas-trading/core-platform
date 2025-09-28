from __future__ import annotations

from typing import Any

from app.ccxt.domain.exchange import Exchange
from app.ccxt.dtos.balance_dto import AssetBalanceDTO, BalanceDTO
from app.ccxt.dtos.order.limit.limit_order_request_dto import LimitOrderRequestDTO
from app.ccxt.dtos.order.limit.limit_order_response_dto import LimitOrderResponseDTO
from app.ccxt.dtos.order.market.market_order_request_dto import MarketOrderRequestDTO
from app.ccxt.dtos.order.market.market_order_response_dto import MarketOrderResponseDTO


class FutureOrder:
    def __init__(self, exchange: Exchange) -> None:
        self._client = exchange.client

        if not exchange.is_future():
            raise ValueError("Exchange must be a future market type.")

    async def fetch_balance(self) -> BalanceDTO:
        """
        거래소 계정의 선물 자산 잔고를 조회합니다.
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
    # Future Limit Order
    # ---------------------------------------------------------
    async def open_long_limit_order(
        self, limit_order: LimitOrderRequestDTO
    ) -> LimitOrderResponseDTO:
        long_order = await self._client.create_limit_buy_order(
            symbol=limit_order.ticker,
            amount=limit_order.amount,
            price=limit_order.price,
            params={"timeInForce": limit_order.time_in_force.value},
        )

        return LimitOrderResponseDTO(
            timestamp=long_order.get("timestamp"),
            datetime=long_order.get("datetime"),
            price=long_order.get("price"),
            average=long_order.get("average"),
            amount=long_order.get("amount"),
            filled=long_order.get("filled"),
            remaining=long_order.get("remaining"),
            cost=long_order.get("cost"),
            fee=long_order.get("fee").get("cost") if long_order.get("fee") else None,
        )

    async def open_short_limit_order(
        self, limit_order: LimitOrderRequestDTO
    ) -> LimitOrderResponseDTO:
        short_order = await self._client.create_limit_sell_order(
            symbol=limit_order.ticker,
            amount=limit_order.amount,
            price=limit_order.price,
            params={"timeInForce": limit_order.time_in_force.value},
        )

        return LimitOrderResponseDTO(
            timestamp=short_order.get("timestamp"),
            datetime=short_order.get("datetime"),
            price=short_order.get("price"),
            average=short_order.get("average"),
            amount=short_order.get("amount"),
            filled=short_order.get("filled"),
            remaining=short_order.get("remaining"),
            cost=short_order.get("cost"),
            fee=short_order.get("fee").get("cost") if short_order.get("fee") else None,
        )

    async def close_long_limit_order(
        self, limit_order: LimitOrderRequestDTO
    ) -> LimitOrderResponseDTO:
        close_long_order = await self._client.create_limit_sell_order(
            symbol=limit_order.ticker,
            amount=limit_order.amount,
            price=limit_order.price,
            params={"timeInForce": limit_order.time_in_force.value},
        )

        return LimitOrderResponseDTO(
            timestamp=close_long_order.get("timestamp"),
            datetime=close_long_order.get("datetime"),
            price=close_long_order.get("price"),
            average=close_long_order.get("average"),
            amount=close_long_order.get("amount"),
            filled=close_long_order.get("filled"),
            remaining=close_long_order.get("remaining"),
            cost=close_long_order.get("cost"),
            fee=close_long_order.get("fee").get("cost") if close_long_order.get("fee") else None,
        )

    async def close_short_limit_order(
        self, limit_order: LimitOrderRequestDTO
    ) -> LimitOrderResponseDTO:
        close_short_order = await self._client.create_limit_buy_order(
            symbol=limit_order.ticker,
            amount=limit_order.amount,
            price=limit_order.price,
            params={"timeInForce": limit_order.time_in_force.value},
        )

        return LimitOrderResponseDTO(
            timestamp=close_short_order.get("timestamp"),
            datetime=close_short_order.get("datetime"),
            price=close_short_order.get("price"),
            average=close_short_order.get("average"),
            amount=close_short_order.get("amount"),
            filled=close_short_order.get("filled"),
            remaining=close_short_order.get("remaining"),
            cost=close_short_order.get("cost"),
            fee=close_short_order.get("fee").get("cost") if close_short_order.get("fee") else None,
        )

    # ---------------------------------------------------------
    # Future Market Order
    # ---------------------------------------------------------
    async def open_long_market_order(
        self, market_order: MarketOrderRequestDTO
    ) -> MarketOrderResponseDTO:
        long_market_order = await self._client.create_market_buy_order(
            symbol=market_order.ticker, amount=market_order.amount
        )

        return MarketOrderResponseDTO(
            timestamp=long_market_order.get("timestamp"),
            datetime=long_market_order.get("datetime"),
            price=long_market_order.get("price"),
            average=long_market_order.get("average"),
            amount=long_market_order.get("amount"),
            filled=long_market_order.get("filled"),
            remaining=long_market_order.get("remaining"),
            cost=long_market_order.get("cost"),
            fee=long_market_order.get("fee").get("cost") if long_market_order.get("fee") else None,
        )

    async def open_short_market_order(
        self, market_order: MarketOrderRequestDTO
    ) -> MarketOrderResponseDTO:
        short_market_order = await self._client.create_market_sell_order(
            symbol=market_order.ticker, amount=market_order.amount
        )

        return MarketOrderResponseDTO(
            timestamp=short_market_order.get("timestamp"),
            datetime=short_market_order.get("datetime"),
            price=short_market_order.get("price"),
            average=short_market_order.get("average"),
            amount=short_market_order.get("amount"),
            filled=short_market_order.get("filled"),
            remaining=short_market_order.get("remaining"),
            cost=short_market_order.get("cost"),
            fee=(
                short_market_order.get("fee").get("cost") if short_market_order.get("fee") else None
            ),
        )

    async def close_long_market_order(
        self, market_order: MarketOrderRequestDTO
    ) -> MarketOrderResponseDTO:
        close_long_market_order = await self._client.create_market_sell_order(
            symbol=market_order.ticker, amount=market_order.amount
        )

        return MarketOrderResponseDTO(
            timestamp=close_long_market_order.get("timestamp"),
            datetime=close_long_market_order.get("datetime"),
            price=close_long_market_order.get("price"),
            average=close_long_market_order.get("average"),
            amount=close_long_market_order.get("amount"),
            filled=close_long_market_order.get("filled"),
            remaining=close_long_market_order.get("remaining"),
            cost=close_long_market_order.get("cost"),
            fee=(
                close_long_market_order.get("fee").get("cost")
                if close_long_market_order.get("fee")
                else None
            ),
        )

    async def close_short_market_order(
        self, market_order: MarketOrderRequestDTO
    ) -> MarketOrderResponseDTO:
        close_short_market_order = await self._client.create_market_buy_order(
            symbol=market_order.ticker, amount=market_order.amount
        )

        return MarketOrderResponseDTO(
            timestamp=close_short_market_order.get("timestamp"),
            datetime=close_short_market_order.get("datetime"),
            price=close_short_market_order.get("price"),
            average=close_short_market_order.get("average"),
            amount=close_short_market_order.get("amount"),
            filled=close_short_market_order.get("filled"),
            remaining=close_short_market_order.get("remaining"),
            cost=close_short_market_order.get("cost"),
            fee=(
                close_short_market_order.get("fee").get("cost")
                if close_short_market_order.get("fee")
                else None
            ),
        )
