from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class CandleDTO:
    timestamp: int  # 1755365820000
    open: float  # 117666.3
    high: float  # 117666.4
    low: float  # 117620.6
    close: float  # 117648.2
    volume: float  # 143.549
