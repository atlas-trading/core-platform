from __future__ import annotations

from dataclasses import dataclass

from app.core.config import Settings
from app.exchanges.base import ExchangeFactory


@dataclass(slots=True, frozen=True)
class ExchangeSnapshotDTO:
    exchange: str
    balances: dict[str, object] | None
    positions: list[dict[str, object]] | None
    error: str | None = None


@dataclass(slots=True, frozen=True)
class PortfolioDTO:
    exchanges: list[ExchangeSnapshotDTO]


class PortfolioService:
    """service to aggregate balances and positions across exchanges."""

    def __init__(self, exchange_factory: ExchangeFactory, config: Settings):
        self._factory = exchange_factory
        self._config = config

    async def fetch_exchange_snapshot(self, exchange_name: str) -> ExchangeSnapshotDTO:
        """fetch balances and positions for a single exchange."""
        client = self._factory.create(exchange_name)
        try:
            balances = await client.fetch_balance()
            try:
                positions = await client.fetch_positions(None)
            except Exception:
                positions = []
            return ExchangeSnapshotDTO(
                exchange=exchange_name, balances=balances, positions=positions
            )
        finally:
            try:
                await client.close()
            except Exception:
                pass

    async def fetch_portfolio(self, exchanges: list[str]) -> PortfolioDTO:
        """aggregate balances and positions across provided exchanges."""
        snapshots: list[ExchangeSnapshotDTO] = []
        for name in exchanges:
            try:
                snapshots.append(await self.fetch_exchange_snapshot(name))
            except Exception as err:  # best-effort per exchange
                snapshots.append(
                    ExchangeSnapshotDTO(
                        exchange=name, balances=None, positions=None, error=str(err)
                    )
                )
        return PortfolioDTO(exchanges=snapshots)
