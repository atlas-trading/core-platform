from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any

import ccxt.async_support as ccxt

from app.common.enums import MarginMode, OrderSide, OrderType
from app.core.config import Settings


@dataclass(slots=True, frozen=True)
class OrderRequest:
    """order request dto.

    Attributes:
        ticker: trading pair in ccxt format (e.g., "BTC/USDT").
        side: Order side, one of "buy" or "sell".
        type: Order type, typically "limit" or "market".
        amount: Base asset quantity to buy/sell.
        price: Limit price for limit orders; ignored for market orders.
        params: Exchange-specific extra parameters (e.g., timeInForce, reduceOnly).
    """

    ticker: str
    side: OrderSide
    type: OrderType
    amount: float
    price: float | None = None
    params: dict[str, Any] | None = None


@dataclass(slots=True, frozen=True)
class OrderResponse:
    """order response dto.

    Attributes:
        id: Exchange order identifier.
        ticker: trading pair.
        status: Order status (e.g., "open", "closed", "canceled").
        filled: Executed base amount.
        remaining: Remaining base amount.
        price: Average execution price if available, else limit price or None.
        info: Raw exchange response payload for downstream use.
    """

    id: str
    ticker: str
    status: str
    filled: float
    remaining: float
    price: float | None
    info: dict[str, Any]


class Exchange(ABC):
    """exchange interface (SOLID: ISP, DIP)."""

    @abstractmethod
    def id(self) -> str:
        """Return exchange identifier."""

    @abstractmethod
    async def fetch_ticker(self, ticker: str) -> dict[str, Any]:
        """fetch ticker data for a ticker.

        args:
            ticker: trading pair (e.g., "BTC/USDT").

        returns:
            a dict commonly containing: "symbol", "last", "bid", "ask", "high", "low",
            "baseVolume", "quoteVolume", "timestamp", and exchange-specific fields in "info".

        example:
            await exchange.fetch_ticker("BTC/USDT")
        """

    @abstractmethod
    async def create_order(self, request: OrderRequest) -> OrderResponse:
        """create an order from a structured request.

        args:
            request: Structured order request with ticker, side, type, amount, price, params.

        returns:
            an ``OrderResponse`` summarizing the created order with raw payload in ``info``.
        """

    @abstractmethod
    async def cancel_order(self, ticker: str, order_id: str) -> dict[str, Any]:
        """cancel an order by id.

        args:
            ticker: trading pair the order belongs to.
            order_id: Exchange order identifier to cancel.

        returns:
            raw exchange response as a dict.
        """

    @abstractmethod
    async def fetch_balance(self) -> dict[str, Any]:
        """fetch account balances.

        returns:
            a dict with "total", "free", "used" maps by currency and underlying raw "info".
        """

    # --- Order book / OHLCV / trades ---
    @abstractmethod
    async def fetch_order_book(self, ticker: str, limit: int | None = None) -> dict[str, Any]:
        """fetch order book (L2) for a ticker.

        args:
            ticker: trading pair.
            limit: Optional depth limit (exchange-dependent).

        returns:
            a dict with keys "bids" and "asks" (lists of [price, amount]),
            plus optional "timestamp" and "nonce".
        """

    @abstractmethod
    async def fetch_ohlcv(
        self, ticker: str, timeframe: str = "1m", since: int | None = None, limit: int | None = None
    ) -> list[list[float | int | None]]:
        """fetch ohlcv candle data.

        args:
            ticker: trading pair.
            timeframe: Candle timeframe (e.g., "1m", "5m", "1h", "1d").
            since: Milliseconds timestamp to start from (inclusive), exchange-dependent.
            limit: Max number of candles to return.

        returns:
            a list of candles, each as ``[timestamp, open, high, low, close, volume]``.
        """

    @abstractmethod
    async def fetch_trades_public(
        self, ticker: str, since: int | None = None, limit: int | None = None
    ) -> list[dict[str, Any]]:
        """fetch recent public trades for a ticker.

        args:
            ticker: trading pair.
            since: Milliseconds timestamp to start from (inclusive).
            limit: Max number of trades.

        returns:
            a list of trade dicts commonly including: "id", "timestamp", "price", "amount",
            "side", "cost", and raw "info".
        """

    @abstractmethod
    async def fetch_my_trades(
        self, ticker: str, since: int | None = None, limit: int | None = None
    ) -> list[dict[str, Any]]:
        """fetch account's trade history (private) for a ticker.

        args:
            ticker: trading pair.
            since: Milliseconds timestamp to start from (inclusive).
            limit: Max number of trades.

        returns:
            a list of trade dicts (same shape as public trades, but scoped to the account).
        """

    # --- Orders ---
    @abstractmethod
    async def fetch_order(self, order_id: str, ticker: str | None = None) -> dict[str, Any]:
        """fetch an order by id.

        args:
            order_id: Exchange order identifier.
            ticker: optional trading pair (some exchanges require it).

        returns:
            an order dict with status, filled, remaining, price, and raw "info".
        """

    @abstractmethod
    async def fetch_open_orders(self, ticker: str | None = None) -> list[dict[str, Any]]:
        """fetch currently open orders.

        args:
            ticker: optional trading pair to filter by.

        returns:
            a list of order dicts in an "open" state.
        """

    @abstractmethod
    async def fetch_closed_orders(self, ticker: str | None = None) -> list[dict[str, Any]]:
        """fetch closed (filled or canceled) orders.

        args:
            ticker: optional trading pair to filter by.

        returns:
            a list of order dicts in a terminal state.
        """

    @abstractmethod
    async def cancel_all_orders(self, ticker: str | None = None) -> list[dict[str, Any]]:
        """cancel all open orders.

        args:
            ticker: optional trading pair to scope cancellation (recommended).

        returns:
            a list of exchange responses for canceled orders (shape varies by exchange).
        """

    # --- Account / positions ---
    @abstractmethod
    async def fetch_positions(self, symbols: Iterable[str] | None = None) -> list[dict[str, Any]]:
        """fetch derivative positions if supported by the exchange.

        args:
            symbols: Optional list of symbols to filter by.

        returns:
            a list of position dicts typically with: "symbol", "side", "contracts/size",
            "entryPrice", "leverage", "unrealizedPnl", and raw "info". Shape varies.
        """

    @abstractmethod
    async def fetch_leverage_tiers(
        self, symbols: Iterable[str] | None = None
    ) -> list[dict[str, Any]]:
        """fetch leverage tiers / margin requirements.

        args:
            symbols: Optional list of symbols to filter by.

        returns:
            a list of tier dicts with fields like: "tier", "maxLeverage",
            "maintenanceMarginRate", "minNotional", "maxNotional" (exchange-dependent).
        """

    # --- Derivatives / futures ---
    @abstractmethod
    async def set_leverage(self, leverage: int, ticker: str | None = None) -> Any:
        """set leverage value for a ticker or account.

        args:
            leverage: Target leverage (e.g., 10).
            ticker: optional trading pair (required on many derivatives exchanges).

        returns:
            raw exchange response confirming the change, or raises if unsupported.
        """

    @abstractmethod
    async def set_margin_mode(self, margin_mode: MarginMode, ticker: str | None = None) -> Any:
        """switch margin mode (isolated or cross).

        args:
            margin_mode: One of MarginMode.ISOLATED or MarginMode.CROSS (exchange-specific casing may apply).
            ticker: optional trading pair (often required for isolated mode).

        returns:
            raw exchange response confirming the change, or raises if unsupported.
        """

    @abstractmethod
    async def fetch_funding_rate(self, ticker: str) -> dict[str, Any]:
        """fetch current (or next) funding rate for a ticker.

        args:
            ticker: trading pair.

        returns:
            a dict with fields like: "symbol", "fundingRate", "timestamp",
            possibly "nextFundingRate" and "nextFundingTimestamp".
        """

    # --- Exchange / account status ---
    @abstractmethod
    async def load_markets(self) -> dict[str, Any]:
        """load market metadata and trading specifications.

        returns:
            a dict keyed by symbol with market specification objects (price/amount precisions,
            limits, contract/spot flags, quote/base currencies, etc.).
        """

    @abstractmethod
    async def fetch_status(self) -> dict[str, Any]:
        """fetch exchange api status.

        returns:
            a dict typically with "status" (e.g., "ok", "maintenance"), "updated", and "eta/msg".
        """

    @abstractmethod
    async def close(self) -> None:
        """release underlying network resources if any."""


class CcxtExchange(Exchange):
    """Default implementation based on ccxt."""

    def __init__(self, ccxt_client: Any):
        self._client = ccxt_client

    def id(self) -> str:
        return str(self._client.id)

    async def fetch_ticker(self, ticker: str) -> dict[str, Any]:
        return await self._client.fetch_ticker(ticker)

    async def create_order(self, request: OrderRequest) -> OrderResponse:
        order = await self._client.create_order(
            request.ticker,
            request.type,
            request.side,
            request.amount,
            request.price,
            request.params,
        )
        return OrderResponse(
            id=str(order.get("id")),
            symbol=order.get("symbol", request.ticker),
            status=order.get("status", "open"),
            filled=float(order.get("filled", 0) or 0),
            remaining=float(order.get("remaining", 0) or 0),
            price=order.get("price"),
            info=order,
        )

    async def cancel_order(self, ticker: str, order_id: str) -> dict[str, Any]:
        return await self._client.cancel_order(order_id, ticker)

    async def fetch_balance(self) -> dict[str, Any]:
        return await self._client.fetch_balance()

    async def fetch_order_book(self, ticker: str, limit: int | None = None) -> dict[str, Any]:
        return await self._client.fetch_order_book(ticker, limit=limit)

    async def fetch_ohlcv(
        self, ticker: str, timeframe: str = "1m", since: int | None = None, limit: int | None = None
    ) -> list[list[float | int | None]]:
        return await self._client.fetch_ohlcv(ticker, timeframe=timeframe, since=since, limit=limit)

    async def fetch_trades_public(
        self, ticker: str, since: int | None = None, limit: int | None = None
    ) -> list[dict[str, Any]]:
        return await self._client.fetch_trades(ticker, since=since, limit=limit)

    async def fetch_my_trades(
        self, ticker: str, since: int | None = None, limit: int | None = None
    ) -> list[dict[str, Any]]:
        return await self._client.fetch_my_trades(ticker, since=since, limit=limit)

    async def fetch_order(self, order_id: str, ticker: str | None = None) -> dict[str, Any]:
        return await self._client.fetch_order(order_id, ticker)

    async def fetch_open_orders(self, ticker: str | None = None) -> list[dict[str, Any]]:
        return await self._client.fetch_open_orders(ticker)

    async def fetch_closed_orders(self, ticker: str | None = None) -> list[dict[str, Any]]:
        return await self._client.fetch_closed_orders(ticker)

    async def cancel_all_orders(self, ticker: str | None = None) -> list[dict[str, Any]]:
        return await self._client.cancel_all_orders(ticker)

    async def fetch_positions(self, symbols: Iterable[str] | None = None) -> list[dict[str, Any]]:
        if hasattr(self._client, "fetch_positions"):
            return await self._client.fetch_positions(symbols)
        return []

    async def fetch_leverage_tiers(
        self, symbols: Iterable[str] | None = None
    ) -> list[dict[str, Any]]:
        if hasattr(self._client, "fetch_leverage_tiers"):
            return await self._client.fetch_leverage_tiers(symbols)
        return []

    async def set_leverage(self, leverage: int, ticker: str | None = None) -> Any:
        if hasattr(self._client, "set_leverage"):
            return await self._client.set_leverage(leverage, ticker)
        raise NotImplementedError("set_leverage is not supported by this exchange")

    async def set_margin_mode(self, margin_mode: str, ticker: str | None = None) -> Any:
        if hasattr(self._client, "set_margin_mode"):
            return await self._client.set_margin_mode(margin_mode, ticker)
        raise NotImplementedError("set_margin_mode is not supported by this exchange")

    async def fetch_funding_rate(self, ticker: str) -> dict[str, Any]:
        if hasattr(self._client, "fetch_funding_rate"):
            return await self._client.fetch_funding_rate(ticker)
        raise NotImplementedError("fetch_funding_rate is not supported by this exchange")

    async def load_markets(self) -> dict[str, Any]:
        return await self._client.load_markets()

    async def fetch_status(self) -> dict[str, Any]:
        if hasattr(self._client, "fetch_status"):
            return await self._client.fetch_status()
        return {"status": "ok"}

    async def close(self) -> None:
        close_fn = getattr(self._client, "close", None)
        if callable(close_fn):
            await close_fn()


class ExchangeFactory:
    """Exchange instance factory.

    - Builds authenticated ccxt clients from settings
    - Provides factory to select exchange at runtime
    """

    def __init__(self, config: Settings):
        self._config = config

    def create(self, name: str) -> Exchange:
        lname = name.lower()
        if lname == "binance":
            client = ccxt.binance(
                {
                    "apiKey": self._config.binance_api_key,
                    "secret": self._config.binance_api_secret,
                    "enableRateLimit": True,
                    "options": {"defaultType": "future"},
                }
            )
            return CcxtExchange(client)
        if lname == "bybit":
            client = ccxt.bybit(
                {
                    "apiKey": self._config.bybit_api_key,
                    "secret": self._config.bybit_api_secret,
                    "enableRateLimit": True,
                    "options": {"defaultType": "future"},
                }
            )
            return CcxtExchange(client)
        raise ValueError(f"Unsupported exchange: {name}")
