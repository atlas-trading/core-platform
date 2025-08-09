from __future__ import annotations

from app.core.config import Settings
from app.exchanges.base import OrderRequest, OrderResponse


class RiskManager:
    """Basic risk management.

    - Validate order notional limits
    - Provide hooks for partial fill handling (hedge/rollback)
    """

    def __init__(self, config: Settings):
        self._config = config

    def validate_order(self, request: OrderRequest, last_price: float | None) -> None:
        """Validate order notional against configured limits."""
        if last_price is None:
            return
        notional = abs(request.amount * last_price)
        if notional > self._config.max_order_usd:
            raise ValueError(
                f"Order notional exceeded: {notional:.2f} > {self._config.max_order_usd:.2f} USD"
            )

    async def on_partial_fill(self, request: OrderRequest, response: OrderResponse) -> None:
        """Hook invoked after partial fill.

        In real use, extend to place hedge or rollback orders.
        """
        _ = (request, response)
        return None
