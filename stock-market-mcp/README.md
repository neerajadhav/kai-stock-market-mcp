# Stock Market MCP Server

A comprehensive Model Context Protocol (MCP) server for Indian stock market data powered by yfinance. Focused on NSE/BSE markets while supporting global stocks.

## Features

### 📊 Stock Data Tools (yfinance powered, Indian market focused)
- **get_stock_quote**: Get current stock price, change, and volume (NSE/BSE optimized)
- **get_stock_history**: Historical price data for technical analysis (Indian stocks)
- **get_stock_info**: Indian company information and key statistics
- **get_multiple_stock_quotes**: Batch quotes for multiple Indian/global symbols

### 📈 Market Analysis (Indian market indices and NIFTY 50 focus)
- **get_market_indices**: Major Indian indices (NIFTY 50, SENSEX, BANK NIFTY) + global indices
- **get_market_movers**: Top gainers/losers from NIFTY 50 watchlist
- **compare_stocks**: Side-by-side comparison with Indian market focus

### 📊 Chart Generation (matplotlib powered, NSE/BSE optimized)
- **create_stock_chart**: Generate price chart for Indian stocks over specified duration
- **create_comparison_chart**: Generate comparison chart for multiple Indian stocks

## Project Structure

```
stock-market-mcp/
├── stock_market_server.py    # Main server entry point
├── auth.py                   # Authentication provider
├── models.py                 # Data models and schemas
├── services/                 # Business logic layer
│   ├── stock_service.py      # Stock data operations
│   ├── market_data_service.py # Market data operations
│   └── chart_service.py      # Chart generation
└── tools/                    # MCP tool definitions
    ├── stock_tools.py        # Stock-related tools
    ├── market_analysis_tools.py # Market analysis tools
    └── chart_tools.py        # Chart generation tools
```

## Setup

1. Create a `.env` file with:
```
AUTH_TOKEN=your_auth_token_here
MY_NUMBER=your_validation_number_here
```

2. Install dependencies:
```bash
pip install fastmcp python-dotenv pydantic yfinance matplotlib pandas
```

3. Run the server:
```bash
python stock_market_server.py
```

The server will start on `http://0.0.0.0:8087`

## Architecture

- **Indian Market Focus**: Optimized for NSE/BSE stocks while supporting global markets
- **yfinance Integration**: All market data powered by Yahoo Finance through yfinance
- **Indian Indices**: NIFTY 50, SENSEX, BANK NIFTY, and other NSE indices
- **NIFTY 50 Watchlist**: Predefined list of top Indian companies for market movers
- **matplotlib Charts**: Visual chart generation with Indian market styling
- **Modular Design**: Separated into services and tools for better maintainability
- **Service Layer**: Business logic abstracted into dedicated service classes
- **Tool Layer**: MCP tools that interact with yfinance and matplotlib services
- **Models**: Strongly typed data models using Pydantic
- **Authentication**: Bearer token authentication with JWT support

## Next Steps

1. Implement yfinance integration for all stock data tools
2. Implement matplotlib chart generation with proper styling
3. Add error handling for invalid symbols and API failures  
4. Implement caching to reduce API calls
5. Add technical indicators using yfinance historical data
6. Expand chart types (candlestick, volume, moving averages)
7. Expand market movers with sector-based watchlists

## Contributing

All tool implementations are currently stubbed with "Implementation pending" messages. Each tool is properly structured and ready for actual implementation.
