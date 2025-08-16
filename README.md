# Core Trading Platform

Trading platform built with Python/FastAPI, supporting multiple exchanges via CCXT.

## Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) for dependency management
- API keys for supported exchanges (Binance, Bybit)

## Setup Guide

Install dependencies using uv:
```bash
# Install uv if not already installed
pip install -U uv

# Create virtual environment and install dependencies
uv venv
uv sync
uv sync --group dev  # for development dependencies
```

### Required environment variables

```
# Exchange API Keys
BINANCE_API_KEY=your_binance_api_key
BINANCE_API_SECRET=your_binance_api_secret
BYBIT_API_KEY=your_bybit_api_key
BYBIT_API_SECRET=your_bybit_api_secret
```
