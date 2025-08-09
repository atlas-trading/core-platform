from __future__ import annotations

import argparse
import asyncio
from collections.abc import Iterable
from typing import Any

import ccxt.async_support as ccxt


def _build_rest_client(exchange_id: str) -> Any:
    cls = getattr(ccxt, exchange_id)
    return cls({"enableRateLimit": True})


def _build_ws_client(exchange_id: str) -> Any:
    import ccxt.pro as ccxtpro  # local import to avoid hard dependency if unused

    cls = getattr(ccxtpro, exchange_id)
    return cls({"enableRateLimit": True})


async def _watch_ws(exchange_id: str, ticker: str, max_ticks: int) -> None:
    client = _build_ws_client(exchange_id)
    try:
        for i in range(max_ticks):
            tick = await client.watch_ticker(ticker)
            print(
                f"[{exchange_id}] {ticker} #{i+1}: last={tick.get('last')} bid={tick.get('bid')} ask={tick.get('ask')} ts={tick.get('timestamp')}"
            )
    finally:
        try:
            await client.close()  # type: ignore[attr-defined]
        except Exception:
            pass


async def _poll_rest(exchange_id: str, ticker: str, max_ticks: int, interval_sec: float) -> None:
    client = _build_rest_client(exchange_id)
    try:
        for i in range(max_ticks):
            tick = await client.fetch_ticker(ticker)
            print(
                f"[{exchange_id}] {ticker} #{i+1}: last={tick.get('last')} bid={tick.get('bid')} ask={tick.get('ask')} ts={tick.get('timestamp')}"
            )
            await asyncio.sleep(interval_sec)
    finally:
        try:
            await client.close()  # type: ignore[attr-defined]
        except Exception:
            pass


async def run_printer(
    exchanges: Iterable[str],
    ticker: str,
    transport: str = "ws",
    max_ticks: int = 5,
    interval_sec: float = 1.0,
) -> None:
    tasks: list[asyncio.Task[None]] = []
    for ex in exchanges:
        ex_id = ex.lower().strip()
        if transport == "ws":
            tasks.append(asyncio.create_task(_watch_ws(ex_id, ticker, max_ticks)))
        elif transport == "rest":
            tasks.append(asyncio.create_task(_poll_rest(ex_id, ticker, max_ticks, interval_sec)))
        else:  # auto
            try:
                tasks.append(asyncio.create_task(_watch_ws(ex_id, ticker, max_ticks)))
            except Exception:
                tasks.append(
                    asyncio.create_task(_poll_rest(ex_id, ticker, max_ticks, interval_sec))
                )
    if not tasks:
        return
    await asyncio.gather(*tasks, return_exceptions=False)


def main() -> None:
    parser = argparse.ArgumentParser(description="print ticker updates for given exchanges")
    parser.add_argument("--exchanges", nargs="+", default=["binance", "bybit"], help="exchange ids")
    parser.add_argument("--ticker", default="BTC/USDT", help="trading pair, e.g., BTC/USDT")
    parser.add_argument(
        "--transport",
        choices=["auto", "ws", "rest"],
        default="ws",
        help="prefer websocket when available, otherwise rest polling",
    )
    parser.add_argument(
        "--max-ticks", type=int, default=5, help="number of ticks to print per exchange"
    )
    parser.add_argument("--interval", type=float, default=1.0, help="rest polling interval seconds")
    args = parser.parse_args()

    asyncio.run(
        run_printer(
            exchanges=args.exchanges,
            ticker=args.ticker,
            transport=args.transport,
            max_ticks=args.max_ticks,
            interval_sec=args.interval,
        )
    )


if __name__ == "__main__":
    main()
