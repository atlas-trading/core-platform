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
    from app.services.portfolio_service import PortfolioService

    return settings, AppContainer, PortfolioService


@st.cache_data(ttl=5)
def _run(coro: Any) -> Any:
    return asyncio.run(coro)


def main() -> None:
    settings, AppContainer, PortfolioService = _import_services()
    st.set_page_config(page_title=settings.app_name, layout="wide")
    st.title("portfolio overview")

    container = AppContainer()
    service: PortfolioService = container.portfolio_service()

    exchanges = st.multiselect(
        "exchanges",
        options=["binance", "bybit"],
        default=["binance", "bybit"],
    )
    if not exchanges:
        st.info("select at least one exchange")
        st.stop()

    data = _run(service.fetch_portfolio(exchanges))

    for snap in data.get("exchanges", []):
        name = snap.get("exchange")
        st.subheader(f"{name}")
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


if __name__ == "__main__":
    main()
