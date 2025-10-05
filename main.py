import asyncio

from app.ccxt.api.spot_order import SpotOrder
from app.ccxt.domain.exchange import Binance
from app.ccxt.enums.market_type import MarketType


async def test_spot() -> None:
    """Spot 거래소 테스트"""
    print("=== Spot 거래소 테스트 ===")
    exchange = Binance(market_type=MarketType.SPOT)
    spot_order = SpotOrder(exchange=exchange)

    try:
        # API 연결 테스트
        print("=== API 연결 테스트 ===")
        try:
            ticker = await exchange.client.fetch_ticker("BTC/USDT")
            print(f"✅ API 연결 성공: BTC/USDT 가격 = {ticker['last']}")
        except Exception as e:
            print(f"❌ API 연결 실패: {e}")
            return

        # 잔고 조회
        print("\n=== 잔고 조회 ===")
        balance = await spot_order.fetch_balance()
        print("잔고 정보:", balance)

        # Spot 보유 자산(포지션) 조회
        print("\n=== Spot 보유 자산 조회 ===")
        try:
            positions = await spot_order.fetch_spot_positions()
            if positions:
                print("보유 자산:")
                for pos in positions:
                    print(
                        f"  {pos['symbol']}: {pos['amount']} (USDT 가치: {pos['value_usdt']:.2f})"
                    )
            else:
                print("보유 자산이 없습니다.")
        except Exception as e:
            print(f"❌ 보유 자산 조회 실패: {e}")

    except Exception as e:
        print(f"Spot 테스트 에러: {e}")
    finally:
        await exchange.close()


async def main() -> None:
    """메인 함수 - Spot과 Future 테스트"""
    await test_spot()


if __name__ == "__main__":
    # 비동기 이벤트 루프 실행
    asyncio.run(main())
