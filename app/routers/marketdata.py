from __future__ import annotations

from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from app.core.container import AppContainer
from app.marketdata.service import MarketDataService

router = APIRouter(prefix="/marketdata", tags=["market-data"])


@router.get("/ticker")
@inject
async def get_ticker(
    market_data_service: Annotated[
        MarketDataService, Depends(Provide[AppContainer.marketdata_service])
    ],
    symbol: str = Query(..., examples=["BTC/USDT"]),
    exchange: str = Query("binance"),
    transport: str = Query("auto", pattern="^(auto|ws|rest)$"),
):
    return await market_data_service.fetch_ticker(exchange, symbol, transport=transport)


@router.get("/orderbook")
@inject
async def get_order_book(
    market_data_service: Annotated[
        MarketDataService, Depends(Provide[AppContainer.marketdata_service])
    ],
    symbol: str = Query(...),
    limit: int | None = Query(None),
    exchange: str = Query("binance"),
    transport: str = Query("auto", pattern="^(auto|ws|rest)$"),
):
    return await market_data_service.fetch_order_book(
        exchange, symbol, limit=limit, transport=transport
    )


@router.get("/ohlcv")
@inject
async def get_ohlcv(
    market_data_service: Annotated[
        MarketDataService, Depends(Provide[AppContainer.marketdata_service])
    ],
    symbol: str = Query(...),
    timeframe: str = Query("1m"),
    since: int | None = Query(None),
    limit: int | None = Query(None),
    exchange: str = Query("binance"),
):
    return await market_data_service.fetch_ohlcv(
        exchange, symbol, timeframe=timeframe, since=since, limit=limit
    )
