from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st

# ensure project root is on sys.path for `app` imports when run via streamlit
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))


def _import_services():
    # defer project imports to avoid E402 and ensure sys.path is set
    from app.core.config import settings
    from app.core.container import AppContainer
    from app.marketdata.service import MarketDataService
    from app.services.portfolio_service import PortfolioService

    return settings, AppContainer, PortfolioService, MarketDataService


def _discover_strategy_names() -> list[str]:
    """discover available strategy class names under app.strategies.*.

    returns a list like ["noop", ...].
    """
    import importlib
    import inspect
    import pkgutil

    try:
        import app.strategies as strategies_pkg
        from app.strategies.base import Strategy
    except Exception:
        return ["noop"]

    names: list[str] = []
    for _, modname, _ in pkgutil.iter_modules(
        strategies_pkg.__path__, strategies_pkg.__name__ + "."
    ):
        try:
            module = importlib.import_module(modname)
        except Exception:
            continue
        for _, obj in inspect.getmembers(module, inspect.isclass):
            try:
                if issubclass(obj, Strategy) and obj is not Strategy:
                    names.append(getattr(obj, "name", obj.__name__).lower())
            except Exception:
                continue
    return sorted(set(names)) or ["noop"]


@st.cache_data(ttl=5)
def _run_portfolio(_exchanges: list[str]) -> Any:
    settings, AppContainer, PortfolioService, _ = _import_services()
    container = AppContainer()
    service: PortfolioService = container.portfolio_service()
    return asyncio.run(service.fetch_portfolio(_exchanges))


def _run_ticker_once(_exchange: str, _ticker: str, _transport: str) -> Any:
    # do not cache: we want a fresh tick each click
    settings, AppContainer, _PortfolioService, MarketDataService = _import_services()
    container = AppContainer()
    md: MarketDataService = container.marketdata_service()
    return asyncio.run(md.fetch_ticker(_exchange, _ticker, _transport))


def main() -> None:
    settings, AppContainer, PortfolioService, MarketDataService = _import_services()
    st.set_page_config(page_title=settings.app_name, layout="wide")
    st.title("portfolio overview")

    exchanges = st.multiselect(
        "exchanges",
        options=["binance", "bybit"],
        default=["binance", "bybit"],
    )
    if not exchanges:
        st.info("select at least one exchange")
        st.stop()

    data = _run_portfolio(exchanges)

    # tabs: overview + per-strategy placeholders
    strategy_names = _discover_strategy_names()
    tabs = st.tabs(["overview", *strategy_names])

    # overview tab content
    with tabs[0]:
        st.subheader("total balances (aggregated)")
        agg_total: dict[str, float] = {}
        agg_free: dict[str, float] = {}
        agg_used: dict[str, float] = {}
        for snap in data.get("exchanges", []):
            balances = snap.get("balances", {}) or {}
            for k, v in (balances.get("total", {}) or {}).items():
                agg_total[k] = agg_total.get(k, 0.0) + float(v or 0)
            for k, v in (balances.get("free", {}) or {}).items():
                agg_free[k] = agg_free.get(k, 0.0) + float(v or 0)
            for k, v in (balances.get("used", {}) or {}).items():
                agg_used[k] = agg_used.get(k, 0.0) + float(v or 0)
        agg_df = (
            pd.DataFrame({"total": agg_total, "free": agg_free, "used": agg_used})
            .fillna(0)
            .sort_index()
        )
        st.dataframe(agg_df)

        st.divider()
        st.subheader("by exchange")
        for snap in data.get("exchanges", []):
            name = snap.get("exchange")
            st.markdown(f"### {name}")
            if snap.get("error"):
                st.error(snap["error"])
                continue
            balances = snap.get("balances", {})
            total = balances.get("total", {})
            free = balances.get("free", {})
            used = balances.get("used", {})
            df = pd.DataFrame({"total": total, "free": free, "used": used}).fillna(0)
            st.dataframe(df.sort_index())

            positions = pd.DataFrame(snap.get("positions", []))
            if not positions.empty:
                st.dataframe(positions)
            else:
                st.caption("no positions or not supported")

    # strategy tabs: placeholders for now
    for i, strat in enumerate(strategy_names, start=1):
        with tabs[i]:
            st.subheader(f"strategy: {strat}")
            col1, col2, col3, col4 = st.columns([1, 2, 2, 2])
            with col1:
                exchange = st.selectbox("exchange", ["binance", "bybit"], key=f"ex-{strat}")
            with col2:
                ticker = st.text_input("ticker", value="BTC/USDT", key=f"tk-{strat}")
            with col3:
                transport = st.selectbox("transport", ["ws", "rest"], index=0, key=f"tp-{strat}")
            with col4:
                run_btn = st.button("fetch", key=f"run-{strat}")

            placeholder = st.empty()
            if run_btn:
                try:
                    tick = _run_ticker_once(exchange, ticker, transport)
                    placeholder.json(tick)
                except Exception as e:
                    placeholder.error(str(e))


if __name__ == "__main__":
    main()
