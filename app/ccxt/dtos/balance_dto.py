from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class AssetBalanceDTO:
    free: float  # 사용 가능한 수량
    used: float  # 주문 등에 사용중인 수량
    total: float  # 전체 수량 (free + used)


@dataclass(slots=True, frozen=True)
class BalanceDTO:
    """
    거래소 계정의 자산 잔고 정보

    Example:
        {
            "BTC": AssetBalanceDTO(free=0.1, used=0.05, total=0.15),
            "USDT": AssetBalanceDTO(free=1000.0, used=500.0, total=1500.0),
        }
    """

    balances: dict[str, AssetBalanceDTO]  # 자산별 잔고 정보
    timestamp: int | None = None  # 마지막 업데이트 시간 (밀리초)
    datetime: str | None = None  # ISO 8601 형식의 타임스탬프
