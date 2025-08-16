from __future__ import annotations

import pytest

from app.ccxt.api.marketdata import MarketData
from app.ccxt.domain.exchange import Binance
from app.ccxt.dtos.ticker_dto import TickerDTO


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

        assert isinstance(ticker, TickerDTO)
        assert ticker.symbol == "BTC/USDT:USDT"

        assert ticker.timestamp is not None
        assert ticker.datetime is not None
        assert ticker.high is not None
        assert ticker.low is not None
        assert ticker.last is not None
        assert ticker.base_volume is not None
        assert ticker.quote_volume is not None

        assert ticker.last > 0
        assert ticker.high > 0
        assert ticker.low > 0
        assert ticker.base_volume > 0

        if ticker.mark_price is not None:
            assert ticker.mark_price > 0
        if ticker.index_price is not None:
            assert ticker.index_price > 0

        if ticker.bid is not None:
            assert ticker.bid > 0
        if ticker.ask is not None:
            assert ticker.ask > 0

    finally:
        await exchange.close()
