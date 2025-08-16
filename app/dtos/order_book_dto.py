from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class OrderBookDTO:
    """호가창(오더북) 데이터 전송 객체.

    Parameters
    ----------
    ticker: 심볼 문자열 (예: BTC/USDT)
    bids: 매수 호가 리스트 [[price, size], ...]
    asks: 매도 호가 리스트 [[price, size], ...]
    timestamp: 타임스탬프(ms)
    nonce: 오더북 넘버(있을 경우)
    raw: 거래소 원본 응답 데이터
    """

    ticker: str
    bids: list[list[float]]
    asks: list[list[float]]
    timestamp: int | None
    nonce: int | None
    raw: dict[str, list[list[float]] | int | None]
