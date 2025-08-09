from typing import Annotated, List
from pydantic import Field
from models import RichToolDescription
from services.stock_service import StockService

def register_stock_tools(mcp):
    """Register all yfinance-powered stock tools"""
    
    GET_STOCK_QUOTE_DESCRIPTION = RichToolDescription(
        description="Get current stock quote with price, change, and volume using yfinance. Focused on Indian market (NSE/BSE) but supports global stocks",
        use_when="When user asks for current stock price, quote, or basic stock information for Indian or global stocks",
        side_effects="Fetches real-time stock data from Yahoo Finance via yfinance. For Indian stocks, use .NS (NSE) or .BO (BSE) suffix"
    )

    @mcp.tool(description=GET_STOCK_QUOTE_DESCRIPTION.model_dump_json())
    async def get_stock_quote(
        symbol: Annotated[str, Field(description="Stock symbol (e.g., RELIANCE.NS, TCS.NS, INFY.BO for Indian stocks, or AAPL, GOOGL for global stocks)")]
    ) -> str:
        """Get current stock quote for Indian or global stocks using yfinance"""
        # TODO: Implement yfinance functionality with Indian market focus
        return f"📊 Stock quote for {symbol.upper()} via yfinance (Indian market focused) - Implementation pending"

    GET_STOCK_HISTORY_DESCRIPTION = RichToolDescription(
        description="Get historical stock price data using yfinance for technical analysis. Optimized for Indian market (NSE/BSE) stocks",
        use_when="When user wants to see stock price history, charts, or perform technical analysis for Indian or global stocks",
        side_effects="Fetches historical price data from Yahoo Finance via yfinance. Indian stocks should use .NS or .BO suffix"
    )

    @mcp.tool(description=GET_STOCK_HISTORY_DESCRIPTION.model_dump_json())
    async def get_stock_history(
        symbol: Annotated[str, Field(description="Stock symbol with exchange suffix (e.g., RELIANCE.NS, TCS.BO for Indian stocks)")],
        period: Annotated[str, Field(description="Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)")] = "1y"
    ) -> str:
        """Get historical stock price data for Indian/global stocks using yfinance"""
        # TODO: Implement yfinance functionality with Indian market focus
        return f"📈 Historical data for {symbol.upper()} over {period} via yfinance (Indian market focused) - Implementation pending"

    GET_STOCK_INFO_DESCRIPTION = RichToolDescription(
        description="Get comprehensive Indian company information and key statistics using yfinance. Primary focus on NSE/BSE listed companies",
        use_when="When user wants detailed Indian company information, market cap, PE ratio, and other fundamentals",
        side_effects="Fetches comprehensive stock information from Yahoo Finance. Best results with Indian stocks using .NS/.BO suffix"
    )

    @mcp.tool(description=GET_STOCK_INFO_DESCRIPTION.model_dump_json())
    async def get_stock_info(
        symbol: Annotated[str, Field(description="Stock symbol with exchange (e.g., RELIANCE.NS, INFY.BO for Indian companies)")]
    ) -> str:
        """Get comprehensive Indian/global company information using yfinance"""
        # TODO: Implement yfinance functionality with Indian market focus
        return f"🏢 Company info for {symbol.upper()} via yfinance (Indian market focused) - Implementation pending"

    GET_MULTIPLE_QUOTES_DESCRIPTION = RichToolDescription(
        description="Get stock quotes for multiple Indian/global symbols at once using yfinance. Optimized for NSE/BSE stocks",
        use_when="When user wants to check multiple Indian or global stocks simultaneously",
        side_effects="Fetches multiple stock quotes efficiently via yfinance. Indian stocks work best with .NS/.BO suffix"
    )

    @mcp.tool(description=GET_MULTIPLE_QUOTES_DESCRIPTION.model_dump_json())
    async def get_multiple_stock_quotes(
        symbols: Annotated[str, Field(description="Comma-separated stock symbols (e.g., 'RELIANCE.NS,TCS.BO,INFY.NS' for Indian stocks)")]
    ) -> str:
        """Get quotes for multiple Indian/global stocks using yfinance"""
        symbol_list = [s.strip().upper() for s in symbols.split(',')]
        # TODO: Implement yfinance functionality with Indian market focus
        return f"📊 Quotes for {', '.join(symbol_list)} via yfinance (Indian market focused) - Implementation pending"
