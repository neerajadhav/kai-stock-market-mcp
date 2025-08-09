from typing import Annotated
from pydantic import Field
from models import RichToolDescription
from services.market_data_service import MarketDataService

def register_market_analysis_tools(mcp):
    """Register all yfinance-powered market analysis tools"""
    
    GET_MARKET_INDICES_DESCRIPTION = RichToolDescription(
        description="Get current values of major Indian market indices (NIFTY 50, SENSEX, NIFTY BANK) and global indices using yfinance",
        use_when="When user wants to check Indian market performance or compare with global markets",
        side_effects="Fetches real-time Indian market index data via yfinance (^NSEI, ^BSESN, ^NSEBANK)"
    )

    @mcp.tool(description=GET_MARKET_INDICES_DESCRIPTION.model_dump_json())
    async def get_market_indices() -> str:
        """Get major Indian market indices performance using yfinance"""
        # TODO: Implement yfinance functionality with Indian indices focus
        return "📊 Major Indian market indices (NIFTY, SENSEX, BANK NIFTY) via yfinance - Implementation pending"

    GET_MARKET_MOVERS_DESCRIPTION = RichToolDescription(
        description="Get Indian market movers from predefined NIFTY 50 and popular Indian stock watchlists using yfinance",
        use_when="When user wants to see which Indian stocks are moving the most",
        side_effects="Fetches stock data for popular Indian stocks and calculates top movers"
    )

    @mcp.tool(description=GET_MARKET_MOVERS_DESCRIPTION.model_dump_json())
    async def get_market_movers(
        type: Annotated[str, Field(description="Type of movers: 'gainers', 'losers'")] = "gainers"
    ) -> str:
        """Get top Indian market movers from NIFTY 50 watchlist using yfinance"""
        # TODO: Implement yfinance functionality with Indian stocks focus
        return f"🚀 Top Indian market {type} via yfinance - Implementation pending"

    COMPARE_STOCKS_DESCRIPTION = RichToolDescription(
        description="Compare multiple Indian/global stocks side by side with key metrics using yfinance. Optimized for NSE/BSE comparisons",
        use_when="When user wants to compare different Indian or global stocks for investment decisions",
        side_effects="Fetches and compares stock data via yfinance. Best results with Indian stocks using .NS/.BO suffix"
    )

    @mcp.tool(description=COMPARE_STOCKS_DESCRIPTION.model_dump_json())
    async def compare_stocks(
        symbols: Annotated[str, Field(description="Comma-separated stock symbols to compare (e.g., 'RELIANCE.NS,TCS.BO,INFY.NS')")]
    ) -> str:
        """Compare multiple Indian/global stocks with key metrics using yfinance"""
        symbol_list = [s.strip().upper() for s in symbols.split(',')]
        # TODO: Implement yfinance functionality with Indian market focus
        return f"⚖️ Comparison of {', '.join(symbol_list)} via yfinance (Indian market focused) - Implementation pending"
