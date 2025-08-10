from typing import Annotated
from pydantic import Field
from mcp.types import ImageContent
from models import RichToolDescription
from services.chart_service import ChartService
from services.symbol_resolver import SymbolResolver

# Create a global symbol resolver instance
symbol_resolver = SymbolResolver()

def register_chart_tools(mcp):
    """Register all matplotlib chart generation tools"""
    
    CREATE_STOCK_CHART_DESCRIPTION = RichToolDescription(
        description="Generate a matplotlib price chart for Indian/global stocks over specified duration. Supports both exact symbols AND company names with intelligent auto-resolution. Optimized for NSE/BSE stocks",
        use_when="When user wants to visualize Indian stock price movement, trends, or technical analysis using either exact symbols OR company names",
        side_effects="Creates and returns a PNG chart image using matplotlib and yfinance data. Automatically resolves company names to correct symbols."
    )

    @mcp.tool(description=CREATE_STOCK_CHART_DESCRIPTION.model_dump_json())
    async def create_stock_chart(
        symbol: Annotated[str, Field(description="Stock symbol OR company name (e.g., 'RELIANCE.NS', 'Reliance', 'Apple' - will auto-resolve)")],
        period: Annotated[str, Field(description="Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)")] = "1y"
    ) -> list[ImageContent]:
        """Generate a price chart for Indian/global stocks using matplotlib with smart symbol resolution"""
        try:
            # Smart symbol resolution
            resolved_symbol, resolution_message = await symbol_resolver.smart_resolve(symbol, context="indian")
            
            if not resolved_symbol:
                raise ValueError(f"Could not resolve symbol '{symbol}': {resolution_message}")
            
            chart_service = ChartService()
            chart_base64 = await chart_service.create_stock_chart(resolved_symbol, period)
            
            return [ImageContent(
                type="image",
                mimeType="image/png", 
                data=chart_base64
            )]
        except Exception as e:
            # Return error as text-based chart if image generation fails
            error_message = f"❌ Error generating chart for {symbol}: {str(e)}"
            # For now, we'll raise the exception since we can't return text content from an ImageContent function
            raise ValueError(error_message)

    CREATE_COMPARISON_CHART_DESCRIPTION = RichToolDescription(
        description="Generate a matplotlib comparison chart showing multiple Indian/global stocks on the same timeline. Supports both exact symbols AND company names with intelligent auto-resolution. Optimized for NSE/BSE comparisons",
        use_when="When user wants to compare performance of multiple Indian or global stocks visually using either exact symbols OR company names",
        side_effects="Creates and returns a PNG comparison chart using matplotlib and yfinance data. Automatically resolves company names to correct symbols."
    )

    @mcp.tool(description=CREATE_COMPARISON_CHART_DESCRIPTION.model_dump_json())
    async def create_comparison_chart(
        symbols: Annotated[str, Field(description="Comma-separated stock symbols OR company names to compare (e.g., 'RELIANCE.NS,TCS.BO,INFY.NS' or 'Reliance,TCS,Infosys' - will auto-resolve)")],
        period: Annotated[str, Field(description="Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)")] = "1y"
    ) -> list[ImageContent]:
        """Generate a comparison chart for multiple Indian/global stocks using matplotlib with smart symbol resolution"""
        try:
            # Smart symbol resolution for multiple symbols
            resolved_symbols, resolution_message = await symbol_resolver.resolve_multiple_symbols(symbols, prefer_indian=True)
            
            if not resolved_symbols:
                raise ValueError(f"Could not resolve any symbols from '{symbols}': {resolution_message}")
            
            chart_service = ChartService()
            chart_base64 = await chart_service.create_comparison_chart(resolved_symbols, period)
            
            return [ImageContent(
                type="image",
                mimeType="image/png",
                data=chart_base64
            )]
        except Exception as e:
            # Return error message - raise exception since we can't return text from ImageContent function
            error_message = f"❌ Error generating comparison chart for {symbols}: {str(e)}"
            raise ValueError(error_message)

    CREATE_CANDLESTICK_CHART_DESCRIPTION = RichToolDescription(
        description="Generate a detailed candlestick chart for Indian/global stocks showing OHLC data. Supports both exact symbols AND company names with intelligent auto-resolution. Optimized for NSE/BSE technical analysis",
        use_when="When user wants detailed price action analysis or technical trading charts for Indian stocks using either exact symbols OR company names",
        side_effects="Creates and returns a PNG candlestick chart using matplotlib. Automatically resolves company names to correct symbols. Best for shorter periods and technical analysis"
    )

    @mcp.tool(description=CREATE_CANDLESTICK_CHART_DESCRIPTION.model_dump_json())
    async def create_candlestick_chart(
        symbol: Annotated[str, Field(description="Stock symbol OR company name to chart (e.g., 'RELIANCE.NS', 'Reliance', 'TCS' - will auto-resolve)")],
        period: Annotated[str, Field(description="Time period (1d, 5d, 1mo, 3mo, 6mo recommended for candlestick charts)")] = "3mo"
    ) -> list[ImageContent]:
        """Generate a candlestick chart for detailed Indian/global stock analysis with smart symbol resolution"""
        try:
            # Smart symbol resolution
            resolved_symbol, resolution_message = await symbol_resolver.smart_resolve(symbol, context="indian")
            
            if not resolved_symbol:
                raise ValueError(f"Could not resolve symbol '{symbol}': {resolution_message}")
            
            chart_service = ChartService()
            chart_base64 = await chart_service.create_candlestick_chart(resolved_symbol, period)
            
            return [ImageContent(
                type="image",
                mimeType="image/png",
                data=chart_base64
            )]
        except Exception as e:
            error_message = f"❌ Error generating candlestick chart for {symbol}: {str(e)}"
            raise ValueError(error_message)

    CREATE_VOLUME_ANALYSIS_CHART_DESCRIPTION = RichToolDescription(
        description="Generate a comprehensive volume analysis chart with VWAP and volume trends for Indian/global stocks. Supports both exact symbols AND company names with intelligent auto-resolution",
        use_when="When user wants to analyze volume patterns, VWAP, or volume-price relationships for Indian stocks using either exact symbols OR company names",
        side_effects="Creates and returns a PNG volume analysis chart with multiple indicators using matplotlib. Automatically resolves company names to correct symbols"
    )

    @mcp.tool(description=CREATE_VOLUME_ANALYSIS_CHART_DESCRIPTION.model_dump_json())
    async def create_volume_analysis_chart(
        symbol: Annotated[str, Field(description="Stock symbol OR company name to analyze (e.g., 'RELIANCE.NS', 'Reliance', 'TCS' - will auto-resolve)")],
        period: Annotated[str, Field(description="Time period (3mo, 6mo, 1y recommended for volume analysis)")] = "6mo"
    ) -> list[ImageContent]:
        """Generate a volume analysis chart for Indian/global stocks with smart symbol resolution"""
        try:
            # Smart symbol resolution
            resolved_symbol, resolution_message = await symbol_resolver.smart_resolve(symbol, context="indian")
            
            if not resolved_symbol:
                raise ValueError(f"Could not resolve symbol '{symbol}': {resolution_message}")
            
            chart_service = ChartService()
            chart_base64 = await chart_service.create_volume_analysis_chart(resolved_symbol, period)
            
            return [ImageContent(
                type="image",
                mimeType="image/png",
                data=chart_base64
            )]
        except Exception as e:
            error_message = f"❌ Error generating volume analysis chart for {symbol}: {str(e)}"
            raise ValueError(error_message)
