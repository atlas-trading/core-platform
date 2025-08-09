from __future__ import annotations

from typing import Any

from app.core.config import Settings
from app.exchanges.base import ExchangeFactory


class PortfolioService:
    """service to aggregate balances and positions across exchanges."""

    def __init__(self, exchange_factory: ExchangeFactory, config: Settings):
        self._factory = exchange_factory
        self._config = config

    async def fetch_exchange_snapshot(self, exchange_name: str) -> dict[str, Any]:
        """fetch balances and positions for a single exchange.

        returns:
            dict with keys: "exchange", "balances", "positions"
        """
        client = self._factory.create(exchange_name)
        try:
            balances = await client.fetch_balance()
            try:
                positions = await client.fetch_positions(None)
            except Exception:
                positions = []
            return {
                "exchange": exchange_name,
                "balances": balances,
                "positions": positions,
            }
        finally:
            try:
                await client.close()
            except Exception:
                pass

    async def fetch_portfolio(self, exchanges: list[str]) -> dict[str, Any]:
        """aggregate balances and positions across provided exchanges."""
        snapshots: list[dict[str, Any]] = []
        for name in exchanges:
            try:
                snapshots.append(await self.fetch_exchange_snapshot(name))
            except Exception as err:  # best-effort per exchange
                snapshots.append({"exchange": name, "error": str(err)})
        return {"exchanges": snapshots}
