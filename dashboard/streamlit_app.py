from __future__ import annotations

import asyncio
from typing import Any

import pandas as pd
import streamlit as st

from app.core.config import settings
from app.core.container import AppContainer
from app.services.portfolio_service import PortfolioService


@st.cache_data(ttl=5)
def _run(coro: Any) -> Any:
    return asyncio.run(coro)


def main() -> None:
    st.set_page_config(page_title=settings.app_name, layout="wide")
    st.title("portfolio overview")

    container = AppContainer()
    service: PortfolioService = container.portfolio_service()  # type: ignore[assignment]

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
