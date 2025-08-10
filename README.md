# Stock Market MCP Server

A comprehensive Model Context Protocol (MCP) server for Indian and global stock market data powered by yfinance. Features intelligent symbol resolution, real-time data, and advanced chart generation for both NSE/BSE and international markets.

## Key Features

### Intelligent Symbol Resolution
- **Smart Name-to-Symbol Conversion**: Use company names like "Reliance", "Apple", "TCS" instead of exact symbols
- **Fuzzy Matching**: Handles typos and partial names with confidence scoring
- **Context-Aware**: Prioritizes Indian stocks (.NS/.BO) for regional users
- **Multi-Format Support**: Accepts both exact symbols (RELIANCE.NS) and natural names (Reliance)

### Real-Time Stock Data
- **Live Quotes**: Current prices, changes, volume, and market cap
- **Historical Data**: Price history with configurable timeframes (1d to 10y+)
- **Company Profiles**: Detailed fundamentals, financial metrics, and business information
- **Multiple Stock Support**: Batch processing for portfolio analysis
- **Fast Quotes**: Quick price checks without full company details

### Advanced Chart Generation
- **Professional Charts**: High-quality matplotlib visualizations with financial styling
- **Multiple Chart Types**: Price charts, candlestick charts, volume analysis, and comparisons
- **Technical Indicators**: Moving averages (MA20, MA50), VWAP, volume trends
- **Comparative Analysis**: Multi-stock performance visualization
- **Export Ready**: PNG format charts suitable for reports and presentations

### Comprehensive Financial Analysis
- **Financial Statements**: Income statements, balance sheets, and cash flow analysis
- **Earnings Intelligence**: Historical earnings, upcoming dates, and analyst estimates
- **Analyst Coverage**: Buy/sell/hold recommendations and price targets
- **Ownership Analysis**: Institutional holdings, mutual funds, and major shareholders
- **Market Research**: Revenue forecasts and earnings predictions

### Indian Market Optimization
- **NSE/BSE Focus**: Specialized support for Indian stock exchanges
- **Currency Formatting**: Rupee (₹) symbols and Indian number formats (Crores/Lakhs)
- **NIFTY 50 Integration**: Pre-loaded watchlist for market movers and screening
- **Major Indices**: Real-time NIFTY 50, SENSEX, BANK NIFTY, and sectoral indices
- **Popular Stocks**: 100+ pre-configured Indian companies for instant access

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

## Available Tools

### Stock Data Tools (12 tools)
- **get_stock_quote**: Real-time stock prices with intelligent symbol resolution
- **get_multiple_stock_quotes**: Batch quotes for multiple stocks simultaneously
- **get_stock_info**: Comprehensive company information and financial metrics
- **get_stock_history**: Historical price data with multiple timeframes
- **get_stock_fast_info**: Quick price checks for rapid analysis
- **get_stock_news**: Latest company news and market updates
- **get_stock_dividends**: Dividend history and yield analysis
- **get_stock_splits**: Stock split and bonus share history
- **search_stocks**: Find stocks by company name with search suggestions
- **resolve_symbol**: Smart company name to symbol conversion
- **get_income_statement**: Revenue, profit, and expense analysis
- **get_balance_sheet**: Assets, liabilities, and equity breakdown
- **get_cashflow_statement**: Operating, investing, and financing cash flows
- **get_earnings_data**: Quarterly and annual earnings history
- **get_earnings_dates**: Upcoming earnings calendar and estimates

### Market Analysis Tools (8 tools)
- **get_market_indices**: Major Indian indices (NIFTY 50, SENSEX, BANK NIFTY) and global markets
- **get_market_movers**: Top gainers and losers from NIFTY 50 constituents
- **compare_stocks**: Side-by-side financial comparison with key metrics
- **get_analyst_recommendations**: Buy/sell/hold ratings from analysts
- **get_analyst_price_targets**: Consensus price predictions and upside potential
- **get_major_holders**: Institutional and mutual fund ownership analysis
- **get_earnings_estimates**: EPS forecasts and analyst consensus
- **get_revenue_estimates**: Revenue predictions and growth expectations

### Chart Generation Tools (4 tools)
- **create_stock_chart**: Professional price charts with moving averages
- **create_comparison_chart**: Multi-stock performance comparison charts
- **create_candlestick_chart**: Detailed OHLC candlestick charts for technical analysis
- **create_volume_analysis_chart**: Advanced volume analysis with VWAP indicators

### Market Screening Tools (1 tool)
- **screen_stocks**: Filter stocks by criteria (most active, gainers, losers, market cap)

## Usage Examples

### Smart Symbol Resolution
- Get real-time quote: `get_stock_quote("Reliance")` or `get_stock_quote("RELIANCE.NS")`
- Historical data: `get_stock_history("TCS", "1y")` or `get_stock_history("Tata Consultancy", "1y")`
- Company information: `get_stock_info("Apple")` or `get_stock_info("AAPL")`
- Multiple quotes: `get_multiple_stock_quotes("Reliance,TCS,Infosys")` or exact symbols

### Market Analysis
- Index tracking: `get_market_indices()`
- Market movers: `get_market_movers("gainers")`
- Stock comparison: `compare_stocks("RELIANCE.NS,TCS.NS")` or `compare_stocks("Reliance,TCS")`
- Analyst research: `get_analyst_recommendations("HDFC Bank")`
- Price targets: `get_analyst_price_targets("Apple")`

### Chart Generation  
- Price chart: `create_stock_chart("Reliance", "6mo")` or `create_stock_chart("RELIANCE.NS", "6mo")`
- Comparison chart: `create_comparison_chart("TCS,Infosys", "1y")`
- Candlestick chart: `create_candlestick_chart("Apple", "3mo")`
- Volume analysis: `create_volume_analysis_chart("HDFC Bank", "6mo")`

### Financial Analysis
- Earnings data: `get_earnings_data("Microsoft")`
- Financial statements: `get_income_statement("TCS")`
- Ownership analysis: `get_major_holders("Reliance")`
- Dividend history: `get_stock_dividends("HDFC Bank")`

### Information Tools (3 tools)
- **get_mcp_capabilities**: Comprehensive guide to all features and capabilities
- **get_mcp_help**: Quick help and common usage examples
- **get_supported_stocks**: List of pre-loaded Indian and global companies

## Technical Implementation

### Architecture
- **Service-Oriented Design**: Modular architecture with dedicated service layers
- **yfinance Integration**: Real-time data from Yahoo Finance API with intelligent caching
- **FastMCP Framework**: High-performance MCP server implementation with async support
- **Pydantic Models**: Type-safe data validation and serialization throughout
- **Bearer Authentication**: Secure token-based authentication system

### Market Coverage
- **Indian Markets**: Full support for NSE (.NS) and BSE (.BO) listed securities
- **Global Markets**: Support for major international exchanges (NASDAQ, NYSE, LSE, etc.)
- **Market Indices**: Real-time tracking of 20+ Indian and global indices
- **Symbol Universe**: 1000+ pre-loaded popular stocks with intelligent name resolution

### Data Services
- **Real-time Quotes**: Live pricing, volume, market cap, and change data
- **Historical Analysis**: Comprehensive historical data with 10+ timeframe options
- **Technical Indicators**: Moving averages, VWAP, volume analysis, and volatility metrics
- **Financial Metrics**: P/E ratios, P/B ratios, EPS, dividend yields, beta, and growth rates
- **News Integration**: Latest company news and market-moving events

### Visualization & Charts
- **Professional Charts**: High-quality matplotlib charts optimized for financial data
- **Multiple Chart Types**: Line charts, candlestick charts, volume analysis, and comparisons
- **Technical Analysis**: Built-in technical indicators and trend analysis
- **Export Formats**: PNG charts suitable for reports, presentations, and analysis

## API Reference

### Stock Data Tools
| Tool | Description | Parameters | Example Usage |
|------|-------------|------------|---------------|
| `get_stock_quote` | Real-time stock quote with intelligent resolution | `symbol` (company name or exact symbol) | `get_stock_quote("Reliance")` |
| `get_multiple_stock_quotes` | Batch stock quotes | `symbols` (comma-separated names/symbols) | `get_multiple_stock_quotes("TCS,Infosys,Apple")` |
| `get_stock_info` | Comprehensive company information | `symbol` (company name or exact symbol) | `get_stock_info("HDFC Bank")` |
| `get_stock_history` | Historical price data | `symbol`, `period` (1d-10y) | `get_stock_history("Apple", "6mo")` |
| `search_stocks` | Find stocks by name | `query` (search term) | `search_stocks("Tata")` |
| `resolve_symbol` | Convert company name to exact symbol | `query` (company name) | `resolve_symbol("Bharti Airtel")` |

### Financial Analysis Tools
| Tool | Description | Parameters | Example Usage |
|------|-------------|------------|---------------|
| `get_income_statement` | Revenue and profit analysis | `symbol` | `get_income_statement("Microsoft")` |
| `get_balance_sheet` | Assets and liabilities | `symbol` | `get_balance_sheet("TCS")` |
| `get_cashflow_statement` | Cash flow analysis | `symbol` | `get_cashflow_statement("Apple")` |
| `get_earnings_data` | Earnings history | `symbol` | `get_earnings_data("Reliance")` |
| `get_stock_dividends` | Dividend history | `symbol` | `get_stock_dividends("HDFC Bank")` |

### Market Analysis Tools
| Tool | Description | Parameters | Example Usage |
|------|-------------|------------|---------------|
| `get_market_indices` | Major market indices | None | `get_market_indices()` |
| `get_market_movers` | Top gainers/losers | `type` (gainers/losers) | `get_market_movers("gainers")` |
| `compare_stocks` | Multi-stock comparison | `symbols` (comma-separated) | `compare_stocks("Reliance,TCS")` |
| `get_analyst_recommendations` | Analyst ratings | `symbol` | `get_analyst_recommendations("Apple")` |
| `get_analyst_price_targets` | Price predictions | `symbol` | `get_analyst_price_targets("Microsoft")` |

### Chart Generation Tools
| Tool | Description | Parameters | Example Usage |
|------|-------------|------------|---------------|
| `create_stock_chart` | Professional price chart | `symbol`, `period` | `create_stock_chart("TCS", "1y")` |
| `create_comparison_chart` | Multi-stock comparison chart | `symbols`, `period` | `create_comparison_chart("Apple,Microsoft", "6mo")` |
| `create_candlestick_chart` | OHLC candlestick chart | `symbol`, `period` | `create_candlestick_chart("Reliance", "3mo")` |
| `create_volume_analysis_chart` | Volume analysis with VWAP | `symbol`, `period` | `create_volume_analysis_chart("HDFC Bank", "6mo")` |

### Supported Timeframes
- **Intraday**: `1d`, `5d` (hourly data)
- **Short-term**: `1mo`, `3mo`, `6mo` (daily data)
- **Medium-term**: `1y`, `2y` (daily data)
- **Long-term**: `5y`, `10y` (weekly data)
- **Special**: `ytd` (year-to-date), `max` (all available data)

### Symbol Formats & Examples
- **Indian Stocks**: Use company names or add `.NS` for NSE, `.BO` for BSE
  - Examples: `"Reliance"` → `RELIANCE.NS`, `"TCS"` → `TCS.NS`, `"HDFC Bank"` → `HDFCBANK.NS`
- **Global Stocks**: Use company names or standard ticker symbols
  - Examples: `"Apple"` → `AAPL`, `"Microsoft"` → `MSFT`, `"Google"` → `GOOGL`
- **Market Indices**: Yahoo Finance index symbols
  - Indian: `^NSEI` (NIFTY 50), `^BSESN` (SENSEX), `^NSEBANK` (BANK NIFTY)
  - Global: `^GSPC` (S&P 500), `^DJI` (Dow Jones), `^IXIC` (NASDAQ)

### Smart Resolution Examples
- **Indian Companies**: "Reliance Industries", "Tata Consultancy", "HDFC Bank", "Bharti Airtel"
- **Global Companies**: "Apple Inc", "Microsoft Corporation", "Alphabet", "Amazon"
- **Abbreviations**: "TCS", "HUL", "L&T", "SBI", "ICICI"
- **Partial Names**: "Reliance", "Infosys", "HDFC"

## Development Status

### Current Implementation (v2.0+)
- **Complete yfinance Integration**: All 25+ stock data tools fully implemented with error handling
- **Intelligent Symbol Resolution**: Advanced fuzzy matching with 100+ pre-loaded companies  
- **Advanced Chart Generation**: Professional matplotlib charts with technical indicators
- **Comprehensive Financial Data**: Real-time quotes, historical data, earnings, and analyst coverage
- **Multi-Market Support**: Seamless Indian (NSE/BSE) and global market integration
- **Production Ready**: Robust error handling, data validation, and performance optimization

### Recent Updates (2024)
- Full implementation of intelligent symbol resolution system
- Added 15+ new financial analysis tools (earnings, recommendations, price targets)
- Enhanced chart generation with volume analysis and VWAP indicators
- Comprehensive Indian market coverage with NIFTY 50 focus
- Professional chart styling and advanced data visualization
- Robust error handling and graceful fallback mechanisms
- Smart caching and performance optimizations

### Tool Coverage
- **Stock Data**: 12 tools covering quotes, history, news, dividends, splits
- **Financial Analysis**: 8 tools for earnings, statements, and analyst coverage  
- **Market Analysis**: 8 tools for indices, movers, comparisons, and research
- **Chart Generation**: 4 tools for various chart types and technical analysis
- **Utilities**: 4 tools for search, resolution, help, and capabilities

## Contributing

This project uses modern Python development practices:

### Development Setup
```bash
# Clone and install development dependencies
git clone <repository-url>
cd stock-market-mcp
pip install -e ".[dev]"
```

### Code Quality & Standards
- **Formatting**: Black code formatter with 120-character line limit
- **Import Organization**: isort for consistent import ordering  
- **Type Safety**: mypy type checking with strict mode
- **Testing**: pytest framework for comprehensive test coverage
- **Documentation**: Comprehensive docstrings and API documentation

### Code Architecture
- **Async/Await**: Non-blocking operations throughout for high performance
- **Service Layer**: Dedicated services for stock data, market data, and chart generation
- **Model Validation**: Pydantic models for type-safe data validation
- **Error Handling**: Comprehensive error handling with graceful degradation
- **Caching**: Intelligent caching to reduce API calls and improve response times

## Docker & Deployment

### Quick Start with Docker

```bash
# Build and run locally
docker build -t stock-market-mcp .
docker run -p 8087:8087 \
  -e AUTH_TOKEN=your-token \
  -e MY_NUMBER=91xxxxxxxxxx \
  stock-market-mcp
```

### Railway Deployment

This application is optimized for Railway hosting with:

- Dockerfile-based deployment
- Dynamic port binding
- Health check endpoints
- Minimal Docker image

See [RAILWAY_DEPLOY.md](RAILWAY_DEPLOY.md) for detailed deployment instructions.

### Local Development with Docker Compose

```bash
# Copy environment variables
cp .env.example .env
# Edit .env with your values

# Start the service
docker-compose up --build
```
