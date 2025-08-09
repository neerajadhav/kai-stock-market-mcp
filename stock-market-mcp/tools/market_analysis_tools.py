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
        try:
            market_service = MarketDataService()
            indices = await market_service.get_market_indices()
            
            if not indices:
                return "❌ No market index data available at the moment"
            
            result = "📊 **Indian Market Indices**\n\n"
            
            for index in indices:
                change_symbol = "📈" if index.change >= 0 else "📉"
                change_sign = "+" if index.change >= 0 else ""
                
                result += f"**{index.name}**\n"
                result += f"• **Value:** {index.value:,.2f} {change_symbol}\n"
                result += f"• **Change:** {change_sign}{index.change:.2f} ({change_sign}{index.change_percent:.2f}%)\n"
                result += f"• **Symbol:** {index.symbol}\n\n"
            
            # Add market sentiment summary
            gainers = [idx for idx in indices if idx.change > 0]
            losers = [idx for idx in indices if idx.change < 0]
            
            if gainers and losers:
                result += f"**Market Sentiment:** {len(gainers)} indices up, {len(losers)} indices down"
            elif gainers:
                result += "**Market Sentiment:** 🟢 Positive (All major indices up)"
            elif losers:
                result += "**Market Sentiment:** 🔴 Negative (All major indices down)"
            else:
                result += "**Market Sentiment:** ➖ Flat (Mixed performance)"
            
            return result
            
        except Exception as e:
            return f"❌ Error fetching market indices: {str(e)}"

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
        try:
            market_service = MarketDataService()
            movers = await market_service.get_market_movers(type)
            
            if not movers:
                return f"❌ No {type} data available at the moment"
            
            type_emoji = "🚀" if type.lower() == "gainers" else "📉"
            result = f"{type_emoji} **Top 10 Indian Market {type.title()} (NIFTY 50)**\n\n"
            
            for i, stock in enumerate(movers, 1):
                change_symbol = "📈" if stock['change'] >= 0 else "📉"
                change_sign = "+" if stock['change'] >= 0 else ""
                
                # Format stock name (remove .NS suffix for display)
                display_symbol = stock['symbol'].replace('.NS', '').replace('.BO', '')
                stock_name = stock['name'][:30] + "..." if len(stock['name']) > 30 else stock['name']
                
                result += f"**{i}. {display_symbol}** - {stock_name}\n"
                result += f"• **Price:** ₹{stock['price']:.2f} {change_symbol}\n"
                result += f"• **Change:** {change_sign}{stock['change']:.2f} ({change_sign}{stock['change_percent']:.2f}%)\n"
                result += f"• **Volume:** {stock['volume']:,}\n\n"
            
            # Add summary statistics
            if type.lower() == "gainers":
                max_gainer = max(movers, key=lambda x: x['change_percent'])
                result += f"**Best Performer:** {max_gainer['symbol'].replace('.NS', '')} (+{max_gainer['change_percent']:.2f}%)"
            else:
                max_loser = min(movers, key=lambda x: x['change_percent'])
                result += f"**Worst Performer:** {max_loser['symbol'].replace('.NS', '')} ({max_loser['change_percent']:.2f}%)"
            
            return result
            
        except Exception as e:
            return f"❌ Error fetching market {type}: {str(e)}"

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
        try:
            symbol_list = [s.strip().upper() for s in symbols.split(',')]
            market_service = MarketDataService()
            comparison = await market_service.compare_stocks(symbol_list)
            
            stocks = comparison.get('stocks', [])
            if not stocks:
                return f"❌ No data available for comparison of: {', '.join(symbol_list)}"
            
            result = f"⚖️ **Stock Comparison ({len(stocks)} stocks)**\n"
            if comparison.get('comparison_date'):
                result += f"*Data as of: {comparison['comparison_date']}*\n\n"
            
            # Create comparison table
            result += "| **Metric** | " + " | ".join([f"**{stock['symbol'].replace('.NS', '').replace('.BO', '')}**" for stock in stocks]) + " |\n"
            result += "|" + "---|" * (len(stocks) + 1) + "\n"
            
            # Current Price
            prices = [f"₹{stock['current_price']:.2f}" for stock in stocks]
            result += f"| **Current Price** | {' | '.join(prices)} |\n"
            
            # Market Cap (formatted)
            market_caps = []
            for stock in stocks:
                if stock.get('market_cap'):
                    cap = stock['market_cap']
                    if cap >= 1e12:
                        market_caps.append(f"₹{cap/1e12:.2f}T")
                    elif cap >= 1e9:
                        market_caps.append(f"₹{cap/1e9:.2f}B")
                    elif cap >= 1e7:
                        market_caps.append(f"₹{cap/1e7:.2f}Cr")
                    else:
                        market_caps.append("N/A")
                else:
                    market_caps.append("N/A")
            result += f"| **Market Cap** | {' | '.join(market_caps)} |\n"
            
            # P/E Ratio
            pe_ratios = [f"{stock.get('pe_ratio', 'N/A'):.2f}" if stock.get('pe_ratio') else "N/A" for stock in stocks]
            result += f"| **P/E Ratio** | {' | '.join(pe_ratios)} |\n"
            
            # P/B Ratio
            pb_ratios = [f"{stock.get('pb_ratio', 'N/A'):.2f}" if stock.get('pb_ratio') else "N/A" for stock in stocks]
            result += f"| **P/B Ratio** | {' | '.join(pb_ratios)} |\n"
            
            # YTD Return
            ytd_returns = [f"{stock.get('ytd_return', 0):.2f}%" for stock in stocks]
            result += f"| **YTD Return** | {' | '.join(ytd_returns)} |\n"
            
            # Dividend Yield
            div_yields = [f"{(stock.get('dividend_yield', 0) * 100):.2f}%" if stock.get('dividend_yield') else "N/A" for stock in stocks]
            result += f"| **Div Yield** | {' | '.join(div_yields)} |\n"
            
            # Beta
            betas = [f"{stock.get('beta', 'N/A'):.2f}" if stock.get('beta') else "N/A" for stock in stocks]
            result += f"| **Beta** | {' | '.join(betas)} |\n"
            
            # 52-week range
            ranges = []
            for stock in stocks:
                low = stock.get('52w_low')
                high = stock.get('52w_high')
                if low and high:
                    ranges.append(f"₹{low:.0f}-₹{high:.0f}")
                else:
                    ranges.append("N/A")
            result += f"| **52W Range** | {' | '.join(ranges)} |\n"
            
            # Add sector information
            result += "\n**Sector Information:**\n"
            for stock in stocks:
                symbol_clean = stock['symbol'].replace('.NS', '').replace('.BO', '')
                result += f"• **{symbol_clean}:** {stock.get('sector', 'N/A')} - {stock.get('industry', 'N/A')}\n"
            
            # Performance summary
            result += "\n**Performance Summary:**\n"
            best_ytd = max(stocks, key=lambda x: x.get('ytd_return', -float('inf')))
            worst_ytd = min(stocks, key=lambda x: x.get('ytd_return', float('inf')))
            
            result += f"• **Best YTD:** {best_ytd['symbol'].replace('.NS', '')} ({best_ytd.get('ytd_return', 0):.2f}%)\n"
            result += f"• **Worst YTD:** {worst_ytd['symbol'].replace('.NS', '')} ({worst_ytd.get('ytd_return', 0):.2f}%)\n"
            
            # Valuation summary
            pe_stocks = [s for s in stocks if s.get('pe_ratio')]
            if pe_stocks:
                cheapest_pe = min(pe_stocks, key=lambda x: x['pe_ratio'])
                result += f"• **Lowest P/E:** {cheapest_pe['symbol'].replace('.NS', '')} ({cheapest_pe['pe_ratio']:.2f})\n"
            
            return result
            
        except Exception as e:
            return f"❌ Error comparing stocks: {str(e)}"
