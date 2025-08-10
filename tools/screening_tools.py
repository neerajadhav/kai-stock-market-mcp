from typing import Annotated
from pydantic import Field
from models import RichToolDescription
from services.market_data_service import MarketDataService

def register_screening_tools(mcp):
    """Register all yfinance-powered screening tools"""
    
    SCREEN_STOCKS_DESCRIPTION = RichToolDescription(
        description="Screen stocks using yfinance screen functionality. Filter stocks by various criteria",
        use_when="When user wants to find stocks matching specific criteria like market cap, sector, or financial metrics",
        side_effects="Uses yfinance screen functionality to filter stocks based on specified criteria"
    )

    @mcp.tool(description=SCREEN_STOCKS_DESCRIPTION.model_dump_json())
    async def screen_stocks(
        screener_type: Annotated[str, Field(description="Type of screening: 'most_active', 'gainers', 'losers', 'trending', 'small_cap', 'mid_cap', 'large_cap'")] = "most_active"
    ) -> str:
        """Screen stocks using yfinance screening functionality"""
        try:
            market_service = MarketDataService()
            screened_stocks = await market_service.screen_stocks(screener_type)
            
            if not screened_stocks:
                return f"📊 No stocks found for screening type '{screener_type}'"
            
            result = f"📊 **Stock Screening Results: {screener_type.title().replace('_', ' ')}**\n\n"
            
            # Show top results
            top_results = screened_stocks[:20] if len(screened_stocks) > 20 else screened_stocks
            
            result += f"**Top {len(top_results)} Stocks:**\n\n"
            
            if screener_type in ['gainers', 'losers']:
                result += "| **Symbol** | **Name** | **Price** | **Change** | **% Change** | **Volume** |\n"
                result += "|---|---|---|---|---|---|\n"
                
                for stock in top_results:
                    symbol = stock.get('symbol', 'N/A')
                    name = stock.get('shortName', stock.get('longName', 'N/A'))[:20] + "..." if len(stock.get('shortName', '')) > 20 else stock.get('shortName', 'N/A')
                    price = stock.get('regularMarketPrice', 0)
                    change = stock.get('regularMarketChange', 0)
                    change_pct = stock.get('regularMarketChangePercent', 0)
                    volume = stock.get('regularMarketVolume', 0)
                    
                    price_str = f"${price:.2f}" if price else "N/A"
                    change_str = f"{change:+.2f}" if change else "N/A"
                    change_pct_str = f"{change_pct:+.2f}%" if change_pct else "N/A"
                    volume_str = f"{volume:,}" if volume else "N/A"
                    
                    result += f"| **{symbol}** | {name} | {price_str} | {change_str} | {change_pct_str} | {volume_str} |\n"
            
            elif screener_type == 'most_active':
                result += "| **Symbol** | **Name** | **Price** | **Volume** | **Market Cap** |\n"
                result += "|---|---|---|---|---|\n"
                
                for stock in top_results:
                    symbol = stock.get('symbol', 'N/A')
                    name = stock.get('shortName', stock.get('longName', 'N/A'))[:20] + "..." if len(stock.get('shortName', '')) > 20 else stock.get('shortName', 'N/A')
                    price = stock.get('regularMarketPrice', 0)
                    volume = stock.get('regularMarketVolume', 0)
                    market_cap = stock.get('marketCap', 0)
                    
                    price_str = f"${price:.2f}" if price else "N/A"
                    volume_str = f"{volume:,}" if volume else "N/A"
                    
                    if market_cap:
                        if market_cap >= 1e12:
                            mcap_str = f"${market_cap/1e12:.2f}T"
                        elif market_cap >= 1e9:
                            mcap_str = f"${market_cap/1e9:.2f}B"
                        elif market_cap >= 1e6:
                            mcap_str = f"${market_cap/1e6:.2f}M"
                        else:
                            mcap_str = f"${market_cap:,.0f}"
                    else:
                        mcap_str = "N/A"
                    
                    result += f"| **{symbol}** | {name} | {price_str} | {volume_str} | {mcap_str} |\n"
            
            else:  # For cap-based screening
                result += "| **Symbol** | **Name** | **Price** | **Market Cap** | **Sector** |\n"
                result += "|---|---|---|---|---|\n"
                
                for stock in top_results:
                    symbol = stock.get('symbol', 'N/A')
                    name = stock.get('shortName', stock.get('longName', 'N/A'))[:20] + "..." if len(stock.get('shortName', '')) > 20 else stock.get('shortName', 'N/A')
                    price = stock.get('regularMarketPrice', 0)
                    market_cap = stock.get('marketCap', 0)
                    sector = stock.get('sector', 'N/A')[:15] + "..." if len(stock.get('sector', '')) > 15 else stock.get('sector', 'N/A')
                    
                    price_str = f"${price:.2f}" if price else "N/A"
                    
                    if market_cap:
                        if market_cap >= 1e12:
                            mcap_str = f"${market_cap/1e12:.2f}T"
                        elif market_cap >= 1e9:
                            mcap_str = f"${market_cap/1e9:.2f}B"
                        elif market_cap >= 1e6:
                            mcap_str = f"${market_cap/1e6:.2f}M"
                        else:
                            mcap_str = f"${market_cap:,.0f}"
                    else:
                        mcap_str = "N/A"
                    
                    result += f"| **{symbol}** | {name} | {price_str} | {mcap_str} | {sector} |\n"
            
            # Add screening criteria info
            result += f"\n**Screening Criteria:**\n"
            criteria_info = {
                'most_active': "• Stocks with highest trading volume\n• Indicates strong investor interest and liquidity",
                'gainers': "• Stocks with largest price increases\n• Sorted by percentage change (highest first)",
                'losers': "• Stocks with largest price decreases\n• Sorted by percentage change (lowest first)",
                'trending': "• Stocks with significant price movements\n• Based on recent activity and volume",
                'small_cap': "• Market cap typically under $2 billion\n• Higher growth potential, higher risk",
                'mid_cap': "• Market cap between $2B - $10B\n• Balance of growth and stability",
                'large_cap': "• Market cap over $10 billion\n• Established companies, typically more stable"
            }
            
            result += criteria_info.get(screener_type, "• Custom screening criteria applied")
            
            result += f"\n\n**💡 Tips:**\n"
            result += f"• Use individual stock tools to get detailed analysis\n"
            result += f"• Consider market conditions when interpreting results\n"
            result += f"• Combine with fundamental analysis for better decisions\n"
            
            return result
            
        except Exception as e:
            return f"❌ Error screening stocks with '{screener_type}': {str(e)}"
