from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class OrderResultDTO:
    """주문 접수/체결 결과 데이터 전송 객체.

    Parameters
    ----------
    exchange: 거래소 식별자
    order_id: 거래소 주문 ID
    status: 주문 상태 문자열
    filled: 체결 수량
    remaining: 미체결 수량
    price: 체결 가격(지정가/평균가 등), 없을 수 있음
    """

    exchange: str
    order_id: str
    status: str
    filled: float
    remaining: float
    price: float | None
