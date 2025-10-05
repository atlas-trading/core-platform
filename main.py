import asyncio

from app.ccxt.api.spot_order import SpotOrder
from app.ccxt.domain.exchange import BinanceSpotTestnet
from app.ccxt.dtos.order.limit.limit_order_request_dto import LimitOrderRequestDTO
from app.ccxt.enums.market_type import MarketType
from app.ccxt.enums.time_in_force import TimeInForce


async def main() -> None:
    try:
        exchange = BinanceSpotTestnet(market_type=MarketType.SPOT)
        spot_order = SpotOrder(exchange=exchange)

        limit_order = LimitOrderRequestDTO(
            ticker="BTC/USDT",  # XRP/USDT 페어
            amount=0.1,  # 5 XRP (최소 주문 금액을 맞추기 위해 수량 증가)
            price=30000,  # 리밋 가격
            time_in_force=TimeInForce.GTC,
        )

        # 잔고 및 포지션 확인
        balance = await spot_order.fetch_balance()
        print("잔고 정보:", balance)

        response = await spot_order.open_limit_order(limit_order)
        print("주문 응답:", response)

    except Exception as e:
        print(f"에러 발생: {e}")

    finally:
        # 거래소 연결 종료
        await exchange.close()


if __name__ == "__main__":
    # 비동기 이벤트 루프 실행
    asyncio.run(main())
