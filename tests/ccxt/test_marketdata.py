from __future__ import annotations

import pytest

from app.ccxt.api.marketdata import MarketData
from app.ccxt.domain.exchange import Binance
from app.ccxt.dtos.order_book_dto import OrderBookDTO, PriceLevelDTO
from app.ccxt.dtos.ticker_dto import TickerDTO


@pytest.mark.asyncio
async def test_load_markets() -> None:
    exchange = Binance()
    api = MarketData(exchange)

    try:
        markets = await api.load_markets()

        assert markets is not None
        assert isinstance(markets, dict)
        assert len(markets) > 0

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

        assert markets is not None
        assert isinstance(markets, list)
        assert len(markets) > 0

        btc_market = next((m for m in markets if m["id"] == "BTCUSDT"), None)
        assert btc_market is not None
        assert btc_market["quote"] == "USDT"
        assert btc_market["base"] == "BTC"
        assert btc_market["active"]

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


@pytest.mark.asyncio
async def test_fetch_order_book() -> None:
    exchange = Binance()
    api = MarketData(exchange)

    try:
        order_book = await api.fetch_order_book("BTC/USDT")

        # verify order book
        assert isinstance(order_book, OrderBookDTO)
        assert order_book.symbol == "BTC/USDT"
        assert isinstance(order_book.timestamp, int)
        assert isinstance(order_book.datetime, str)
        assert order_book.datetime.endswith("Z")  # ISO 8601 UTC

        assert len(order_book.bids) > 0
        assert len(order_book.asks) > 0

        # verify price level
        first_bid = order_book.bids[0]
        first_ask = order_book.asks[0]

        assert isinstance(first_bid, PriceLevelDTO)
        assert isinstance(first_ask, PriceLevelDTO)
        assert isinstance(first_bid.price, float)
        assert isinstance(first_bid.amount, float)
        assert isinstance(first_ask.price, float)
        assert isinstance(first_ask.amount, float)

        assert first_bid.price > order_book.bids[1].price  # ask price is higher than bid price
        assert first_ask.price < order_book.asks[1].price  # bid price is lower than ask price

        assert first_ask.price > first_bid.price  # ask price is higher than bid price

        assert first_bid.amount > 0
        assert first_ask.amount > 0

    finally:
        await exchange.close()
