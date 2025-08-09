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
        try:
            stock_service = StockService()
            quote = await stock_service.get_stock_quote(symbol)
            
            # Format the response nicely
            change_symbol = "📈" if quote.change >= 0 else "📉"
            change_sign = "+" if quote.change >= 0 else ""
            
            result = f"""📊 **{quote.symbol} Stock Quote**

**Price:** ₹{quote.price:.2f} {change_symbol}
**Change:** {change_sign}{quote.change:.2f} ({change_sign}{quote.change_percent:.2f}%)
**Volume:** {quote.volume:,}"""
            
            if quote.market_cap:
                if quote.market_cap >= 1e12:
                    market_cap_str = f"₹{quote.market_cap/1e12:.2f}T"
                elif quote.market_cap >= 1e9:
                    market_cap_str = f"₹{quote.market_cap/1e9:.2f}B"
                elif quote.market_cap >= 1e7:
                    market_cap_str = f"₹{quote.market_cap/1e7:.2f}Cr"
                else:
                    market_cap_str = f"₹{quote.market_cap:,.0f}"
                result += f"\n**Market Cap:** {market_cap_str}"
            
            return result
            
        except Exception as e:
            return f"❌ Error fetching quote for {symbol.upper()}: {str(e)}"

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
        try:
            stock_service = StockService()
            history = await stock_service.get_stock_history(symbol, period)
            
            # Calculate some basic statistics
            data = history['data']
            if not data:
                return f"❌ No historical data found for {symbol.upper()}"
            
            prices = [record['Close'] for record in data]
            highest = max(prices)
            lowest = min(prices)
            latest = prices[-1]
            first = prices[0]
            total_return = ((latest - first) / first) * 100
            
            result = f"""📈 **{history['symbol']} Historical Data ({period})**

**Period:** {history['start_date']} to {history['end_date']}
**Total Records:** {history['total_records']} days

**Price Summary:**
• **Current:** ₹{latest:.2f}
• **High:** ₹{highest:.2f}
• **Low:** ₹{lowest:.2f}
• **Total Return:** {total_return:+.2f}%

**Sample Recent Data:**"""
            
            # Show last 5 days of data
            recent_data = data[-5:] if len(data) >= 5 else data
            for record in recent_data:
                date_str = record.get('Date', 'N/A')
                if hasattr(date_str, 'strftime'):
                    date_str = date_str.strftime('%Y-%m-%d')
                result += f"\n• {date_str}: Open ₹{record['Open']:.2f}, Close ₹{record['Close']:.2f}, Vol {int(record.get('Volume', 0)):,}"
            
            return result
            
        except Exception as e:
            return f"❌ Error fetching history for {symbol.upper()}: {str(e)}"

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
        try:
            stock_service = StockService()
            info = await stock_service.get_stock_info(symbol)
            
            result = f"""🏢 **{info['name']} ({info['symbol']})**

**Basic Information:**
• **Sector:** {info['sector']}
• **Industry:** {info['industry']}
• **Country:** {info['country']}
• **Exchange:** {info['exchange']}
• **Currency:** {info['currency']}"""

            if info.get('market_cap'):
                market_cap = info['market_cap']
                if market_cap >= 1e12:
                    market_cap_str = f"₹{market_cap/1e12:.2f}T"
                elif market_cap >= 1e9:
                    market_cap_str = f"₹{market_cap/1e9:.2f}B"
                elif market_cap >= 1e7:
                    market_cap_str = f"₹{market_cap/1e7:.2f}Cr"
                else:
                    market_cap_str = f"₹{market_cap:,.0f}"
                result += f"\n• **Market Cap:** {market_cap_str}"

            result += "\n\n**Financial Metrics:**"
            
            if info.get('pe_ratio'):
                result += f"\n• **P/E Ratio:** {info['pe_ratio']:.2f}"
            if info.get('forward_pe'):
                result += f"\n• **Forward P/E:** {info['forward_pe']:.2f}"
            if info.get('peg_ratio'):
                result += f"\n• **PEG Ratio:** {info['peg_ratio']:.2f}"
            if info.get('price_to_book'):
                result += f"\n• **P/B Ratio:** {info['price_to_book']:.2f}"
            if info.get('eps'):
                result += f"\n• **EPS:** ₹{info['eps']:.2f}"
            if info.get('beta'):
                result += f"\n• **Beta:** {info['beta']:.2f}"
            if info.get('dividend_yield'):
                result += f"\n• **Dividend Yield:** {info['dividend_yield']:.2%}"

            result += "\n\n**Price Range (52-week):**"
            if info.get('fifty_two_week_high') and info.get('fifty_two_week_low'):
                result += f"\n• **High:** ₹{info['fifty_two_week_high']:.2f}"
                result += f"\n• **Low:** ₹{info['fifty_two_week_low']:.2f}"

            if info.get('average_volume'):
                result += f"\n\n**Average Volume:** {info['average_volume']:,}"

            if info.get('website'):
                result += f"\n\n**Website:** {info['website']}"

            if info.get('business_summary') and info['business_summary'] != 'N/A':
                summary = info['business_summary']
                if len(summary) > 300:
                    summary = summary[:297] + "..."
                result += f"\n\n**Business Summary:**\n{summary}"

            return result
            
        except Exception as e:
            return f"❌ Error fetching info for {symbol.upper()}: {str(e)}"

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
        try:
            symbol_list = [s.strip().upper() for s in symbols.split(',')]
            stock_service = StockService()
            quotes = await stock_service.get_stock_quotes(symbol_list)
            
            if not quotes:
                return f"❌ No data found for any of the symbols: {', '.join(symbol_list)}"
            
            result = f"📊 **Multiple Stock Quotes ({len(quotes)} stocks)**\n\n"
            
            for quote in quotes:
                change_symbol = "📈" if quote.change >= 0 else "📉"
                change_sign = "+" if quote.change >= 0 else ""
                
                result += f"**{quote.symbol}**\n"
                result += f"• Price: ₹{quote.price:.2f} {change_symbol} {change_sign}{quote.change:.2f} ({change_sign}{quote.change_percent:.2f}%)\n"
                result += f"• Volume: {quote.volume:,}\n"
                
                if quote.market_cap:
                    if quote.market_cap >= 1e12:
                        market_cap_str = f"₹{quote.market_cap/1e12:.2f}T"
                    elif quote.market_cap >= 1e9:
                        market_cap_str = f"₹{quote.market_cap/1e9:.2f}B"
                    elif quote.market_cap >= 1e7:
                        market_cap_str = f"₹{quote.market_cap/1e7:.2f}Cr"
                    else:
                        market_cap_str = f"₹{quote.market_cap:,.0f}"
                    result += f"• Market Cap: {market_cap_str}\n"
                
                result += "\n"
            
            # Add summary statistics
            if len(quotes) > 1:
                gainers = [q for q in quotes if q.change > 0]
                losers = [q for q in quotes if q.change < 0]
                
                result += f"**Summary:** {len(gainers)} gainers, {len(losers)} losers"
            
            return result
            
        except Exception as e:
            return f"❌ Error fetching multiple quotes: {str(e)}"
