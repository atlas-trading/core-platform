from __future__ import annotations

from typing import Any

from app.ccxt.domain.exchange import Exchange
from app.ccxt.dtos.order_book_dto import OrderBookDTO, PriceLevelDTO
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

    async def fetch_order_book(self, ticker: str) -> OrderBookDTO:
        order_book: dict[str, Any] = await self._client.fetch_order_book(symbol=ticker)
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
