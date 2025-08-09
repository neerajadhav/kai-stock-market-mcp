# Stock Market MCP Server

A comprehensive Model Context Protocol (MCP) server for Indian stock market data powered by yfinance. Optimized for NSE/BSE markets with full global stock support.

## Features

### Stock Data Tools
- **get_stock_quote**: Real-time stock prices, changes, and volume data
- **get_stock_history**: Historical price data with technical analysis support
- **get_stock_info**: Comprehensive company fundamentals and financial metrics
- **get_multiple_stock_quotes**: Batch processing for multiple stock symbols

### Market Analysis
- **get_market_indices**: Major Indian indices (NIFTY 50, SENSEX, BANK NIFTY) and global markets
- **get_market_movers**: Top gainers/losers from NIFTY 50 constituent stocks
- **compare_stocks**: Side-by-side financial comparison with key metrics

### Advanced Chart Generation
- **create_stock_chart**: Price charts with moving averages and volume analysis
- **create_comparison_chart**: Multi-stock performance comparison charts
- **create_candlestick_chart**: Detailed OHLC candlestick charts for technical analysis
- **create_volume_analysis_chart**: Advanced volume analysis with VWAP and VPT indicators

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

## Installation and Setup

### Prerequisites
- Python 3.11 or higher
- Environment variables configuration

### Quick Start
1. Clone the repository and navigate to the project directory

2. Create environment configuration:
```bash
cp .env.example .env
```

3. Configure your `.env` file:
```env
AUTH_TOKEN=your_secure_auth_token_here
MY_NUMBER=your_validation_number_here
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Start the server:
```bash
python stock_market_server.py
```

The server will be available at `http://0.0.0.0:8087`

## Usage Examples

### Stock Data Queries
- Get real-time quote: `get_stock_quote("RELIANCE.NS")`
- Historical data: `get_stock_history("TCS.NS", "1y")`
- Company information: `get_stock_info("INFY.NS")`
- Multiple quotes: `get_multiple_stock_quotes("RELIANCE.NS,TCS.NS,INFY.NS")`

### Market Analysis
- Index tracking: `get_market_indices()`
- Market movers: `get_market_movers("gainers")`
- Stock comparison: `compare_stocks("RELIANCE.NS,TCS.NS")`

### Chart Generation
- Price chart: `create_stock_chart("RELIANCE.NS", "6mo")`
- Comparison chart: `create_comparison_chart("RELIANCE.NS,TCS.NS", "1y")`
- Candlestick chart: `create_candlestick_chart("RELIANCE.NS", "3mo")`

## Technical Implementation

### Architecture
- **Service-Oriented Design**: Modular architecture with dedicated service layers
- **yfinance Integration**: Real-time data from Yahoo Finance API
- **FastMCP Framework**: High-performance MCP server implementation
- **Pydantic Models**: Type-safe data validation and serialization
- **Bearer Authentication**: Secure token-based authentication system

### Market Coverage
- **Indian Markets**: Full support for NSE (.NS) and BSE (.BO) listed securities
- **Global Markets**: Support for major international exchanges
- **Market Indices**: Real-time tracking of major Indian and global indices
- **NIFTY 50 Focus**: Specialized tools for India's benchmark index constituents

### Data Services
- **Real-time Quotes**: Live pricing, volume, and market cap data
- **Historical Analysis**: Comprehensive historical data with multiple timeframes
- **Technical Indicators**: Moving averages, VWAP, volume analysis, and volatility metrics
- **Financial Metrics**: P/E ratios, P/B ratios, EPS, dividend yields, and beta calculations

### Visualization
- **Professional Charts**: High-quality matplotlib charts with financial styling
- **Multiple Chart Types**: Line charts, candlestick charts, and volume analysis
- **Comparative Analysis**: Multi-stock performance visualization
- **Technical Analysis**: Advanced charting with technical indicators

## API Reference

### Stock Data Tools
| Tool | Description | Parameters |
|------|-------------|------------|
| `get_stock_quote` | Real-time stock quote | `symbol` (string) |
| `get_stock_history` | Historical price data | `symbol` (string), `period` (string) |
| `get_stock_info` | Company fundamentals | `symbol` (string) |
| `get_multiple_stock_quotes` | Batch stock quotes | `symbols` (comma-separated string) |

### Market Analysis Tools
| Tool | Description | Parameters |
|------|-------------|------------|
| `get_market_indices` | Major market indices | None |
| `get_market_movers` | Top gainers/losers | `type` (gainers/losers) |
| `compare_stocks` | Multi-stock comparison | `symbols` (comma-separated string) |

### Chart Generation Tools
| Tool | Description | Parameters |
|------|-------------|------------|
| `create_stock_chart` | Basic price chart | `symbol` (string), `period` (string) |
| `create_comparison_chart` | Multi-stock chart | `symbols` (comma-separated), `period` (string) |
| `create_candlestick_chart` | OHLC candlestick chart | `symbol` (string), `period` (string) |
| `create_volume_analysis_chart` | Volume analysis chart | `symbol` (string), `period` (string) |

### Supported Timeframes
- `1d`, `5d`, `1mo`, `3mo`, `6mo`, `1y`, `2y`, `5y`, `10y`, `ytd`, `max`

### Symbol Formats
- **Indian Stocks**: Add `.NS` for NSE or `.BO` for BSE (e.g., `RELIANCE.NS`, `TCS.BO`)
- **Global Stocks**: Use standard symbols (e.g., `AAPL`, `GOOGL`, `MSFT`)
- **Indices**: Use Yahoo Finance index symbols (e.g., `^NSEI`, `^BSESN`, `^GSPC`)

## Development Status

### Current Implementation
- **Complete yfinance Integration**: All stock data tools are fully implemented
- **Advanced Chart Generation**: Professional matplotlib charts with technical indicators
- **Comprehensive Market Data**: Real-time indices, market movers, and comparative analysis
- **Production Ready**: Error handling, data validation, and performance optimization

### Recent Updates
- Full implementation of all MCP tools with yfinance backend
- Advanced charting capabilities with technical analysis
- Comprehensive Indian market coverage with NIFTY 50 focus
- Professional chart styling and data visualization
- Robust error handling and data validation

## Contributing

This project uses modern Python development practices:

### Development Setup
```bash
pip install -e ".[dev]"
```

### Code Quality Tools
- **Black**: Code formatting
- **isort**: Import organization
- **mypy**: Type checking
- **pytest**: Testing framework

### Code Style
- Line length: 120 characters
- Type hints required
- Pydantic models for data validation
- Async/await for non-blocking operations
