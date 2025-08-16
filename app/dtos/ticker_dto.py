from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True, frozen=True)
class TickerDTO:
    """티커 스냅샷 데이터 전송 객체.

    Parameters
    ----------
    ticker: 심볼 문자열 (예: BTC/USDT)
    last: 최종 체결가
    bid: 매수호가
    ask: 매도호가
    timestamp: 타임스탬프(ms)
    raw: 거래소 원본 응답 데이터
    """

    ticker: str
    last: float | None
    bid: float | None
    ask: float | None
    timestamp: int | None
    raw: dict[str, Any]
