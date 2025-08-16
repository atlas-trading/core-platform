from __future__ import annotations

from typing import Any

from app.ccxt.domain.exchange import Exchange
from app.ccxt.dtos.ohlcv_dto import CandleDTO
from app.ccxt.dtos.order_book_dto import OrderBookDTO, PriceLevelDTO
from app.ccxt.dtos.status_dto import StatusDTO
from app.ccxt.dtos.ticker_dto import TickerDTO


class MarketData:
    def __init__(self, exchange: Exchange) -> None:
        self._client = exchange.client

    async def load_markets(self) -> dict[str, Any]:
        return await self._client.load_markets()

    async def fetch_markets(self) -> list[dict[str, Any]]:
        return await self._client.fetch_markets()

    async def fetch_ticker(self, ticker: str) -> TickerDTO:
        ticker_info: dict[str, Any] = await self._client.fetch_ticker(ticker)

        return TickerDTO(
            symbol=ticker_info["symbol"],
            timestamp=ticker_info["timestamp"],
            datetime=ticker_info["datetime"],
            high=ticker_info["high"],
            low=ticker_info["low"],
            open=ticker_info["open"],
            close=ticker_info["close"],
            last=ticker_info["last"],
            previous_close=ticker_info.get("previousClose"),
            vwap=ticker_info["vwap"],
            change=ticker_info["change"],
            percentage=ticker_info["percentage"],
            average=ticker_info.get("average"),
            base_volume=ticker_info["baseVolume"],
            quote_volume=ticker_info["quoteVolume"],
            mark_price=ticker_info.get("markPrice"),
            index_price=ticker_info.get("indexPrice"),
            bid=ticker_info.get("bid"),
            bid_volume=ticker_info.get("bidVolume"),
            ask=ticker_info.get("ask"),
            ask_volume=ticker_info.get("askVolume"),
        )

    async def fetch_order_book(self, ticker: str, limit: int | None = None) -> OrderBookDTO:
        order_book: dict[str, Any] = await self._client.fetch_order_book(symbol=ticker, limit=limit)
        return OrderBookDTO(
            asks=[
                PriceLevelDTO(price=price, amount=amount) for price, amount in order_book["asks"]
            ],
            bids=[
                PriceLevelDTO(price=price, amount=amount) for price, amount in order_book["bids"]
            ],
            symbol=order_book["symbol"],
            timestamp=order_book["timestamp"],
            datetime=order_book["datetime"],
            nonce=order_book["nonce"],
        )

    async def fetch_candles(
        self, ticker: str, timeframe: str, since: int | None = None, limit: int | None = None
    ) -> list[CandleDTO]:
        """
        timeframe: '1m', '3m', '5m', '15m', '1h', '4h', '1d', '1w', '1M'
        """
        candles: list[list[Any]] = await self._client.fetch_ohlcv(
            symbol=ticker, timeframe=timeframe, since=since, limit=limit
        )

        return [
            CandleDTO(
                timestamp=candle[0],
                open=candle[1],
                high=candle[2],
                low=candle[3],
                close=candle[4],
                volume=candle[5],
            )
            for candle in candles
        ]

    async def fetch_status(self) -> StatusDTO:
        if hasattr(self._client, "fetch_status"):
            status: dict[str, Any] = await self._client.fetch_status()

            return StatusDTO(
                status=status["status"],
                updated=status.get("updated"),
                eta=status.get("eta"),
                url=status.get("url"),
            )
        else:
            raise NotImplementedError("This exchange does not support fetching status.")
