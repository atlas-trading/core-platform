from __future__ import annotations

from dataclasses import dataclass

from app.dtos.ohlcv_item_dto import OHLCVItemDTO


@dataclass(slots=True, frozen=True)
class OHLCVDTO:
    """캔들(OHLCV) 묶음 데이터 전송 객체.

    Parameters
    ----------
    ticker: 심볼 문자열 (예: BTC/USDT)
    timeframe: 타임프레임 문자열 (예: 1m, 1h)
    candles: OHLCVItemDTO 리스트
    raw: 거래소 원본 응답 데이터 [[ts, open, high, low, close, volume], ...]
    """

    ticker: str
    timeframe: str
    candles: list[OHLCVItemDTO]
    raw: list[list[float | int | None]]
