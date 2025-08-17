import asyncio

from app.ccxt.api.spot_order import SpotOrder
from app.ccxt.domain.exchange import Binance
from app.ccxt.dtos.order.limit_order_request_dto import LimitOrderRequestDTO
from app.ccxt.enums.market_type import MarketType


async def main() -> None:
    # Binance 선물 거래소 인스턴스 생성
    exchange = Binance(market_type=MarketType.SPOT)

    try:
        # FutureOrder 인스턴스 생성
        spot_order = SpotOrder(exchange=exchange)

        # XRP/USDT 리밋 오더 생성
        limit_order = LimitOrderRequestDTO(
            ticker="XRP/USDT",  # XRP/USDT 페어
            amount=2.0,  # 5 XRP (최소 주문 금액을 맞추기 위해 수량 증가)
            price=3.2,  # 지정가 3.1178 USDT
        )

        # 롱 포지션 리밋 오더 실행
        response = await spot_order.close_market_order(limit_order)
        print("주문 응답:", response)

    except Exception as e:
        print(f"에러 발생: {e}")

    finally:
        # 거래소 연결 종료
        await exchange.close()


if __name__ == "__main__":
    # 비동기 이벤트 루프 실행
    asyncio.run(main())
