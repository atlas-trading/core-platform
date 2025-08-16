from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class OHLCVItemDTO:
    """단일 캔들(OHLCV) 데이터 전송 객체.

    Parameters
    ----------
    ts: 타임스탬프(ms)
    open: 시가
    high: 고가
    low: 저가
    close: 종가
    volume: 거래량
    """

    ts: int
    open: float
    high: float
    low: float
    close: float
    volume: float
