from __future__ import annotations

from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.core.container import AppContainer
from app.services.trading_service import TradingService

router = APIRouter(prefix="/trading", tags=["trading"])


class OrderIn(BaseModel):
    """Order input schema."""

    exchange: str = Field(examples=["binance", "bybit"])
    symbol: str = Field(examples=["BTC/USDT"])
    side: str = Field(examples=["buy", "sell"])
    type: str = Field(examples=["market", "limit"])
    amount: float
    price: float | None = None


@router.post("/orders")
@inject
async def place_order(
    data: OrderIn,
    service: Annotated[TradingService, Depends(Provide[AppContainer.trading_service])],
):
    """Create order API."""
    result = await service.place_order(
        exchange_name=data.exchange,
        symbol=data.symbol,
        side=data.side,
        order_type=data.type,
        amount=data.amount,
        price=data.price,
    )
    return result
