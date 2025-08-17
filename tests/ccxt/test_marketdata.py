from __future__ import annotations

from collections.abc import AsyncGenerator
from datetime import UTC, datetime

import pytest
import pytest_asyncio

from app.ccxt.api.marketdata import MarketData
from app.ccxt.domain.exchange import Binance
from app.ccxt.dtos.candle_dto import CandleDTO
from app.ccxt.dtos.future_funding_rate_dto import FutureFundingRateDTO
from app.ccxt.dtos.order_book_dto import OrderBookDTO, PriceLevelDTO
from app.ccxt.dtos.position_dto import PositionDTO
from app.ccxt.dtos.status_dto import StatusDTO
from app.ccxt.dtos.ticker_dto import TickerDTO
from app.ccxt.enums.market_type import MarketType


@pytest_asyncio.fixture
async def market_data() -> AsyncGenerator[MarketData, None]:
    exchange = Binance(market_type=MarketType.FUTURE)
    api = MarketData(exchange)

    yield api

    await exchange.close()


@pytest.mark.asyncio
async def test_load_markets(market_data: MarketData) -> None:
    markets = await market_data.load_markets()

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


@pytest.mark.asyncio
async def test_fetch_markets(market_data: MarketData) -> None:
    markets = await market_data.fetch_markets()

    assert markets is not None
    assert isinstance(markets, list)
    assert len(markets) > 0

    btc_market = next((m for m in markets if m["id"] == "BTCUSDT"), None)
    assert btc_market is not None
    assert btc_market["quote"] == "USDT"
    assert btc_market["base"] == "BTC"
    assert btc_market["active"]


@pytest.mark.asyncio
async def test_fetch_ticker(market_data: MarketData) -> None:
    ticker = await market_data.fetch_ticker("BTC/USDT")

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


@pytest.mark.asyncio
async def test_fetch_order_book(market_data: MarketData) -> None:
    order_book = await market_data.fetch_order_book("BTC/USDT")

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


@pytest.mark.asyncio
async def test_fetch_candles(market_data: MarketData) -> None:
    # fetch last 3 candles
    candles = await market_data.fetch_candles("BTC/USDT", timeframe="1m", limit=3)

    # verify candles list
    assert isinstance(candles, list)
    assert len(candles) == 3

    # verify each candle
    for candle in candles:
        # type check
        assert isinstance(candle, CandleDTO)

        # timestamp validation
        assert isinstance(candle.timestamp, int)
        dt = datetime.fromtimestamp(candle.timestamp / 1000, tz=UTC)
        assert dt.second == 0  # minute candles start at 0 seconds

        # OHLCV type check
        assert isinstance(candle.open, float)
        assert isinstance(candle.high, float)
        assert isinstance(candle.low, float)
        assert isinstance(candle.close, float)
        assert isinstance(candle.volume, float)

        # price range validation
        assert candle.high >= candle.open
        assert candle.high >= candle.close
        assert candle.low <= candle.open
        assert candle.low <= candle.close
        assert candle.volume >= 0

    # verify chronological order
    timestamps = [c.timestamp for c in candles]
    assert timestamps == sorted(timestamps)  # ascending order


@pytest.mark.asyncio
async def test_fetch_status(market_data: MarketData) -> None:
    status = await market_data.fetch_status()

    # verify status DTO
    assert isinstance(status, StatusDTO)

    # verify status field
    assert isinstance(status.status, str)
    assert status.status in ("ok", "maintenance", "shutdown")

    # verify optional fields
    if status.updated is not None:
        assert isinstance(status.updated, int)
        dt = datetime.fromtimestamp(status.updated / 1000, tz=UTC)
        assert dt < datetime.now(UTC)  # timestamp should be in the past

    if status.url is not None:
        assert isinstance(status.url, str)
        assert status.url.startswith("http")
        assert "binance" in status.url.lower()


@pytest.mark.asyncio
async def test_fetch_funding_rate(market_data: MarketData) -> None:
    funding_rate = await market_data.fetch_funding_rate("BTC/USDT:USDT")  # 선물 마켓 심볼

    # verify funding rate DTO
    assert isinstance(funding_rate, FutureFundingRateDTO)

    # verify required fields
    assert isinstance(funding_rate.market_price, float)
    assert isinstance(funding_rate.index_price, float)
    assert isinstance(funding_rate.interest_rate, float)
    assert isinstance(funding_rate.funding_rate, float)
    assert isinstance(funding_rate.funding_timestamp, int)
    assert isinstance(funding_rate.funding_datetime, str)

    # verify price fields
    assert funding_rate.market_price > 0
    assert funding_rate.index_price > 0

    # verify rate fields (can be positive or negative)
    assert -1 < funding_rate.interest_rate < 1  # typically small
    assert -1 < funding_rate.funding_rate < 1  # typically small

    # verify timestamp and datetime
    dt = datetime.fromtimestamp(funding_rate.funding_timestamp / 1000, tz=UTC)
    assert dt > datetime.now(UTC)  # funding time is in the future
    assert funding_rate.funding_datetime.endswith("Z")  # ISO 8601 UTC


@pytest.mark.asyncio
async def test_fetch_positions(market_data: MarketData) -> None:
    # positions = await market_data.fetch_positions(["BTC/USDT:USDT"])
    positions = await market_data.fetch_positions()

    # verify positions list
    assert isinstance(positions, list)

    # if there are open positions
    for position in positions:
        # verify position DTO
        assert isinstance(position, PositionDTO)

        # verify required fields
        assert isinstance(position.symbol, str)
        assert position.side in ("long", "short")
        assert isinstance(position.size, float)
        assert isinstance(position.notional, float)
        assert isinstance(position.leverage, float)
        assert isinstance(position.entry_price, float)
        assert isinstance(position.mark_price, float)

        # verify optional fields
        if position.liquidation_price is not None:
            assert isinstance(position.liquidation_price, float)
            assert position.liquidation_price > 0

        if position.margin_mode is not None:
            assert position.margin_mode in ("cross", "isolated")

        if position.unrealized_pnl is not None:
            assert isinstance(position.unrealized_pnl, float)

        if position.percentage is not None:
            assert isinstance(position.percentage, float)

        # verify values
        assert position.size > 0
        assert position.notional > 0
        assert position.leverage > 0
        assert position.entry_price > 0
        assert position.mark_price > 0
