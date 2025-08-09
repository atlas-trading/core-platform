from __future__ import annotations

from dependency_injector import containers, providers

from app.core.config import Settings, settings
from app.exchanges.base import ExchangeFactory
from app.marketdata.service import MarketDataService
from app.risk.manager import RiskManager
from app.services.portfolio_service import PortfolioService
from app.services.trading_service import TradingService


class AppContainer(containers.DeclarativeContainer):
    """di container.

    - binds settings, exchange factory, risk manager, and service layer
    """

    wiring_config = containers.WiringConfiguration(
        packages=[
            "app.routers",
            "app.services",
        ]
    )

    config = providers.Singleton(Settings, **settings.model_dump())

    exchange_factory = providers.Singleton(ExchangeFactory, config=config)

    risk_manager = providers.Factory(RiskManager, config=config)

    trading_service = providers.Factory(
        TradingService,
        exchange_factory=exchange_factory,
        risk_manager=risk_manager,
    )

    marketdata_service = providers.Factory(
        MarketDataService,
        exchange_factory=exchange_factory,
        config=config,
    )

    portfolio_service = providers.Factory(
        PortfolioService,
        exchange_factory=exchange_factory,
        config=config,
    )
