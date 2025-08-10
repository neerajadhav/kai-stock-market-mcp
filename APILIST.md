# Essential yfinance APIs for MCP Implementation

## Core Stock Data (High Priority)
    yfinance.Ticker.history              # Price history - essential for charts and analysis
    yfinance.Ticker.info                 # Company information - critical for stock details
    yfinance.Ticker.fast_info            # Quick price and basic data access
    yfinance.Ticker.news                 # Latest stock news
    yfinance.Ticker.dividends            # Dividend history
    yfinance.Ticker.splits               # Stock splits data

## Financial Statements (High Priority)
    yfinance.Ticker.income_stmt          # Income statement
    yfinance.Ticker.balance_sheet        # Balance sheet  
    yfinance.Ticker.cashflow             # Cash flow statement
    yfinance.Ticker.earnings             # Earnings data
    yfinance.Ticker.earnings_dates       # Earnings calendar

## Analysis Data (Medium Priority)
    yfinance.Ticker.recommendations      # Analyst recommendations
    yfinance.Ticker.analyst_price_targets # Price targets
    yfinance.Ticker.earnings_estimate    # Earnings estimates
    yfinance.Ticker.revenue_estimate     # Revenue estimates
    yfinance.Ticker.major_holders        # Major shareholders
    yfinance.Ticker.institutional_holders # Institutional ownership

## Utility Functions (High Priority)
    yfinance.download                    # Bulk data download
    yfinance.search                      # Symbol search
    Ticker                              # Core ticker class
    Tickers                             # Multiple tickers

## Screener (Medium Priority)
    yfinance.screen                      # Stock screening

# APIs NOT Recommended for MCP (Eliminated)

## Redundant/Duplicate APIs (use simpler versions instead)
    yfinance.Ticker.get_* methods        # Use property versions instead
    yfinance.Ticker.quarterly_*          # Too specific, use main methods with parameters
    yfinance.Ticker.ttm_*               # Trailing twelve months - too specific

## Less Critical/Niche APIs
    yfinance.Ticker.get_isin            # ISIN codes - rarely needed
    yfinance.Ticker.get_history_metadata # Metadata - low priority
    yfinance.Ticker.actions             # Combined actions - splits/dividends separately is clearer
    yfinance.Ticker.capital_gains       # Niche use case
    yfinance.Ticker.get_shares_full     # Detailed shares data - rarely needed
    yfinance.Ticker.calendar            # Earnings calendar - covered by earnings_dates
    yfinance.Ticker.sec_filings         # SEC filings - complex, low usage
    yfinance.Ticker.recommendations_summary # Covered by recommendations
    yfinance.Ticker.upgrades_downgrades # Subset of recommendations
    yfinance.Ticker.sustainability      # ESG data - niche
    yfinance.Ticker.earnings_history    # Historical earnings - covered by earnings
    yfinance.Ticker.eps_trend           # EPS trends - too specific
    yfinance.Ticker.eps_revisions       # EPS revisions - too specific  
    yfinance.Ticker.growth_estimates    # Growth estimates - niche
    yfinance.Ticker.funds_data          # Fund-specific data
    yfinance.Ticker.insider_purchases   # Insider trading - niche
    yfinance.Ticker.insider_transactions # Insider trading - niche
    yfinance.Ticker.insider_roster_holders # Insider data - niche
    yfinance.Ticker.mutualfund_holders  # Mutual fund holders - niche

## Complex/Advanced Features
    Sector                              # Sector data - complex implementation
    Industry                            # Industry data - complex implementation  
    WebSocket                           # Real-time streaming - complex
    AsyncWebSocket                      # Async streaming - complex
    EquityQuery                         # Complex querying - advanced feature
    FundQuery                           # Fund querying - niche
    yfinance.enable_debug_mode          # Development utility
    yfinance.set_tz_cache_location      # Configuration utility
    FundsData                           # Fund-specific class
    PriceHistory                        # Internal class
    Lookup                              # Symbol lookup - covered by search