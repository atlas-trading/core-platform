from __future__ import annotations

from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from app.common.enums import Transport
from app.core.container import AppContainer
from app.marketdata.service import MarketDataService

router = APIRouter(prefix="/marketdata", tags=["market-data"])


@router.get("/ticker")
@inject
async def get_ticker(
    market_data_service: Annotated[
        MarketDataService, Depends(Provide[AppContainer.marketdata_service])
    ],
    ticker: str = Query(..., examples=["BTC/USDT"]),
    exchange: str = Query("binance"),
    transport: Transport = Transport.AUTO,
):
    return await market_data_service.fetch_ticker(exchange, ticker, transport=transport)


@router.get("/orderbook")
@inject
async def get_order_book(
    market_data_service: Annotated[
        MarketDataService, Depends(Provide[AppContainer.marketdata_service])
    ],
    ticker: str = Query(...),
    limit: int | None = Query(None),
    exchange: str = Query("binance"),
    transport: Transport = Transport.AUTO,
):
    return await market_data_service.fetch_order_book(
        exchange, ticker, limit=limit, transport=transport
    )


@router.get("/ohlcv")
@inject
async def get_ohlcv(
    market_data_service: Annotated[
        MarketDataService, Depends(Provide[AppContainer.marketdata_service])
    ],
    ticker: str = Query(...),
    timeframe: str = Query("1m"),
    since: int | None = Query(None),
    limit: int | None = Query(None),
    exchange: str = Query("binance"),
):
    return await market_data_service.fetch_ohlcv(
        exchange, ticker, timeframe=timeframe, since=since, limit=limit
    )
