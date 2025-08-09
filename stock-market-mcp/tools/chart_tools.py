from typing import Annotated
from pydantic import Field
from mcp.types import ImageContent
from ..models import RichToolDescription
from ..services.chart_service import ChartService

def register_chart_tools(mcp):
    """Register all matplotlib chart generation tools"""
    
    CREATE_STOCK_CHART_DESCRIPTION = RichToolDescription(
        description="Generate a matplotlib price chart for Indian/global stocks over specified duration. Optimized for NSE/BSE stocks",
        use_when="When user wants to visualize Indian stock price movement, trends, or technical analysis",
        side_effects="Creates and returns a PNG chart image using matplotlib and yfinance data. Best results with .NS/.BO suffix"
    )

    @mcp.tool(description=CREATE_STOCK_CHART_DESCRIPTION.model_dump_json())
    async def create_stock_chart(
        symbol: Annotated[str, Field(description="Stock symbol to chart (e.g., RELIANCE.NS, TCS.BO for Indian stocks, or AAPL for global)")],
        period: Annotated[str, Field(description="Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)")] = "1y"
    ) -> list[ImageContent]:
        """Generate a price chart for Indian/global stocks using matplotlib"""
        # TODO: Implement matplotlib chart generation with Indian market focus
        return [ImageContent(
            type="image",
            mimeType="image/png", 
            data="placeholder_base64_data"
        )]

    CREATE_COMPARISON_CHART_DESCRIPTION = RichToolDescription(
        description="Generate a matplotlib comparison chart showing multiple Indian/global stocks on the same timeline. Optimized for NSE/BSE comparisons",
        use_when="When user wants to compare performance of multiple Indian or global stocks visually",
        side_effects="Creates and returns a PNG comparison chart using matplotlib and yfinance data. Indian stocks work best with .NS/.BO suffix"
    )

    @mcp.tool(description=CREATE_COMPARISON_CHART_DESCRIPTION.model_dump_json())
    async def create_comparison_chart(
        symbols: Annotated[str, Field(description="Comma-separated stock symbols to compare (e.g., 'RELIANCE.NS,TCS.BO,INFY.NS' for Indian stocks)")],
        period: Annotated[str, Field(description="Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)")] = "1y"
    ) -> list[ImageContent]:
        """Generate a comparison chart for multiple Indian/global stocks using matplotlib"""
        symbol_list = [s.strip().upper() for s in symbols.split(',')]
        # TODO: Implement matplotlib comparison chart generation with Indian market focus
        return [ImageContent(
            type="image",
            mimeType="image/png",
            data="placeholder_base64_data"
        )]
