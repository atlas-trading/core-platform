from __future__ import annotations

import pytest

from app.ccxt.api.marketdata import MarketData
from app.ccxt.domain.exchange import Binance


@pytest.mark.asyncio
async def test_load_markets() -> None:
    exchange = Binance()
    api = MarketData(exchange)

    try:
        markets = await api.load_markets()

        # 기본 검증
        assert markets is not None
        assert isinstance(markets, dict)
        assert len(markets) > 0

        # BTC/USDT 마켓 검증
        btc_market = markets.get("BTC/USDT")
        assert btc_market is not None
        assert btc_market["id"] == "BTCUSDT"
        assert btc_market["quote"] == "USDT"
        assert btc_market["base"] == "BTC"
        assert "limits" in btc_market
        assert "precision" in btc_market

    finally:
        await exchange.close()


@pytest.mark.asyncio
async def test_fetch_markets() -> None:
    exchange = Binance()
    api = MarketData(exchange)

    try:
        markets = await api.fetch_markets()

        # 기본 검증
        assert markets is not None
        assert isinstance(markets, list)
        assert len(markets) > 0

        # BTC/USDT 마켓 찾기
        btc_market = next((m for m in markets if m["id"] == "BTCUSDT"), None)
        assert btc_market is not None
        assert btc_market["quote"] == "USDT"
        assert btc_market["base"] == "BTC"
        assert btc_market["active"]  # 거래 가능 여부

    finally:
        await exchange.close()


@pytest.mark.asyncio
async def test_fetch_ticker() -> None:
    exchange = Binance()
    api = MarketData(exchange)

    try:
        ticker = await api.fetch_ticker("BTC/USDT")

        # 기본 검증
        assert ticker is not None
        assert isinstance(ticker, dict)

        # 필수 필드 검증
        assert "last" in ticker or "close" in ticker  # 최근가
        assert "bid" in ticker  # 매수호가
        assert "ask" in ticker  # 매도호가
        assert "high" in ticker  # 고가
        assert "low" in ticker  # 저가
        assert "baseVolume" in ticker  # 거래량 (base currency)
        assert "timestamp" in ticker  # 타임스탬프

        # 가격 타입 검증
        last = float(ticker.get("last") or ticker.get("close") or 0)
        assert last > 0
        assert float(ticker["bid"] or 0) >= 0  # 호가 없을 수 있음
        assert float(ticker["ask"] or 0) >= 0
        assert float(ticker["baseVolume"]) > 0

    finally:
        await exchange.close()
