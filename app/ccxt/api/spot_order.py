from __future__ import annotations

from typing import Any

from app.ccxt.domain.exchange import Exchange
from app.ccxt.dtos.balance_dto import AssetBalanceDTO, BalanceDTO


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
    async def open_limit_order(self) -> list[dict[str, Any]]:
        return await self._client.fetch_open_orders()

    async def close_limit_order(self) -> list[dict[str, Any]]:
        return await self._client.fetch_closed_orders()

    async def open_market_order(self) -> None:
        pass

    async def close_market_order(self) -> None:
        pass
