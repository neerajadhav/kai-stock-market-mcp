from typing import Annotated, List
from pydantic import Field
from models import RichToolDescription
from services.stock_service import StockService
from services.symbol_resolver import SymbolResolver

# Create a global symbol resolver instance
symbol_resolver = SymbolResolver()

def register_stock_tools(mcp):
    """Register all yfinance-powered stock tools"""
    
    GET_STOCK_QUOTE_DESCRIPTION = RichToolDescription(
        description="Get current stock quote with price, change, and volume using yfinance. Supports both exact symbols AND company names with intelligent auto-resolution. Optimized for Indian market (NSE/BSE) but supports global stocks",
        use_when="When user asks for current stock price, quote, or basic stock information using either exact symbols (RELIANCE.NS) OR company names (Reliance, Apple, TCS, etc.)",
        side_effects="Fetches real-time stock data from Yahoo Finance via yfinance. Automatically resolves company names to correct symbols. Indian stocks work best."
    )

    @mcp.tool(description=GET_STOCK_QUOTE_DESCRIPTION.model_dump_json())
    async def get_stock_quote(
        symbol: Annotated[str, Field(description="Stock symbol OR company name (e.g., 'RELIANCE.NS', 'TCS', 'Apple', 'Infosys' - will auto-resolve)")]
    ) -> str:
        """Get current stock quote for Indian or global stocks using yfinance with smart symbol resolution"""
        try:
            # Smart symbol resolution
            resolved_symbol, resolution_message = await symbol_resolver.smart_resolve(symbol, context="indian")
            
            if not resolved_symbol:
                return f"🔍 **Symbol Resolution Failed for '{symbol}'**\n\n{resolution_message}"
            
            # If symbol was resolved differently, show the resolution
            resolution_info = ""
            if resolved_symbol.upper() != symbol.upper():
                resolution_info = f"🔄 *Resolved '{symbol}' → '{resolved_symbol}'*\n\n"
            
            stock_service = StockService()
            quote = await stock_service.get_stock_quote(resolved_symbol)
            
            # Format the response nicely
            change_symbol = "📈" if quote.change >= 0 else "📉"
            change_sign = "+" if quote.change >= 0 else ""
            
            result = f"""{resolution_info}📊 **{quote.symbol} Stock Quote**

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
            return f"❌ Error fetching quote for {symbol}: {str(e)}"

    GET_STOCK_HISTORY_DESCRIPTION = RichToolDescription(
        description="Get historical stock price data using yfinance for technical analysis. Optimized for Indian market (NSE/BSE) stocks",
        use_when="When user wants to see stock price history, charts, or perform technical analysis for Indian or global stocks",
        side_effects="Fetches historical price data from Yahoo Finance via yfinance. Indian stocks should use .NS or .BO suffix"
    )

    @mcp.tool(description=GET_STOCK_HISTORY_DESCRIPTION.model_dump_json())
    async def get_stock_history(
        symbol: Annotated[str, Field(description="Stock symbol OR company name (e.g., 'RELIANCE.NS', 'Reliance', 'Apple' - will auto-resolve)")],
        period: Annotated[str, Field(description="Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)")] = "1y"
    ) -> str:
        """Get historical stock price data for Indian/global stocks using yfinance with smart symbol resolution"""
        try:
            # Smart symbol resolution
            resolved_symbol, resolution_message = await symbol_resolver.smart_resolve(symbol, context="indian")
            
            if not resolved_symbol:
                return f"🔍 **Symbol Resolution Failed for '{symbol}'**\n\n{resolution_message}"
            
            # If symbol was resolved differently, show the resolution
            resolution_info = ""
            if resolved_symbol.upper() != symbol.upper():
                resolution_info = f"🔄 *Resolved '{symbol}' → '{resolved_symbol}'*\n\n"
            
            stock_service = StockService()
            history = await stock_service.get_stock_history(resolved_symbol, period)
            
            # Calculate some basic statistics
            data = history['data']
            if not data:
                return f"❌ No historical data found for {resolved_symbol}"
            
            prices = [record['Close'] for record in data]
            highest = max(prices)
            lowest = min(prices)
            latest = prices[-1]
            first = prices[0]
            total_return = ((latest - first) / first) * 100
            
            result = f"""{resolution_info}📈 **{history['symbol']} Historical Data ({period})**

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
            return f"❌ Error fetching history for {symbol}: {str(e)}"

    GET_STOCK_INFO_DESCRIPTION = RichToolDescription(
        description="Get comprehensive Indian company information and key statistics using yfinance. Primary focus on NSE/BSE listed companies",
        use_when="When user wants detailed Indian company information, market cap, PE ratio, and other fundamentals",
        side_effects="Fetches comprehensive stock information from Yahoo Finance. Best results with Indian stocks using .NS/.BO suffix"
    )

    @mcp.tool(description=GET_STOCK_INFO_DESCRIPTION.model_dump_json())
    async def get_stock_info(
        symbol: Annotated[str, Field(description="Stock symbol OR company name (e.g., 'RELIANCE.NS', 'Reliance', 'Apple', 'TCS' - will auto-resolve)")]
    ) -> str:
        """Get comprehensive Indian/global company information using yfinance with smart symbol resolution"""
        try:
            # Smart symbol resolution
            resolved_symbol, resolution_message = await symbol_resolver.smart_resolve(symbol, context="indian")
            
            if not resolved_symbol:
                return f"🔍 **Symbol Resolution Failed for '{symbol}'**\n\n{resolution_message}"
            
            # If symbol was resolved differently, show the resolution
            resolution_info = ""
            if resolved_symbol.upper() != symbol.upper():
                resolution_info = f"🔄 *Resolved '{symbol}' → '{resolved_symbol}'*\n\n"
            
            stock_service = StockService()
            info = await stock_service.get_stock_info(resolved_symbol)
            
            result = f"""{resolution_info}🏢 **{info['name']} ({info['symbol']})**

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
            return f"❌ Error fetching info for {symbol}: {str(e)}"

    GET_MULTIPLE_QUOTES_DESCRIPTION = RichToolDescription(
        description="Get stock quotes for multiple Indian/global symbols at once using yfinance. Supports both exact symbols AND company names with intelligent auto-resolution. Optimized for NSE/BSE stocks",
        use_when="When user wants to check multiple Indian or global stocks simultaneously using either exact symbols OR company names",
        side_effects="Fetches multiple stock quotes efficiently via yfinance. Automatically resolves company names to correct symbols. Indian stocks prioritized."
    )

    @mcp.tool(description=GET_MULTIPLE_QUOTES_DESCRIPTION.model_dump_json())
    async def get_multiple_stock_quotes(
        symbols: Annotated[str, Field(description="Comma-separated stock symbols OR company names (e.g., 'RELIANCE.NS,TCS,Infosys' or 'Apple,Microsoft,Google' - will auto-resolve all)")]
    ) -> str:
        """Get quotes for multiple Indian/global stocks using yfinance with smart symbol resolution"""
        try:
            # Smart symbol resolution for multiple symbols
            resolved_symbols, resolution_message = await symbol_resolver.resolve_multiple_symbols(symbols, prefer_indian=True)
            
            if not resolved_symbols:
                return f"🔍 **Symbol Resolution Failed**\n\n{resolution_message}"
            
            # Show resolution info if any symbols were resolved
            resolution_info = ""
            original_symbols = [s.strip() for s in symbols.split(',')]
            if len(resolved_symbols) != len(original_symbols) or any(r.upper() != o.upper() for r, o in zip(resolved_symbols, original_symbols)):
                resolution_info = f"🔄 *Auto-resolved: {symbols} → {', '.join(resolved_symbols)}*\n\n"
            
            stock_service = StockService()
            quotes = await stock_service.get_stock_quotes(resolved_symbols)
            
            if not quotes:
                return f"❌ No data found for resolved symbols: {', '.join(resolved_symbols)}"
            
            result = f"{resolution_info}📊 **Multiple Stock Quotes ({len(quotes)} stocks)**\n\n"
            
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
            
            # Add any resolution messages
            if "❌" in resolution_message:
                result += f"\n\n**Note:** {resolution_message}"
            
            return result
            
        except Exception as e:
            return f"❌ Error fetching multiple quotes: {str(e)}"

    GET_STOCK_NEWS_DESCRIPTION = RichToolDescription(
        description="Get latest news for a specific stock using yfinance news API. Optimized for Indian stocks",
        use_when="When user wants to see latest news affecting a specific Indian or global stock",
        side_effects="Fetches latest news articles from Yahoo Finance via yfinance API"
    )

    @mcp.tool(description=GET_STOCK_NEWS_DESCRIPTION.model_dump_json())
    async def get_stock_news(
        symbol: Annotated[str, Field(description="Stock symbol (e.g., RELIANCE.NS, TCS.BO for Indian stocks)")]
    ) -> str:
        """Get latest news for a stock using yfinance"""
        try:
            stock_service = StockService()
            news = await stock_service.get_stock_news(symbol)
            
            if not news:
                return f"📰 No recent news found for {symbol.upper()}"
            
            result = f"📰 **Latest News for {symbol.upper()}**\n\n"
            
            for i, article in enumerate(news[:5], 1):  # Show top 5 articles
                result += f"**{i}. {article['title']}**\n"
                result += f"• **Publisher:** {article.get('publisher', 'Unknown')}\n"
                result += f"• **Published:** {article.get('publish_time', 'Unknown')}\n"
                if article.get('summary'):
                    summary = article['summary'][:200] + "..." if len(article['summary']) > 200 else article['summary']
                    result += f"• **Summary:** {summary}\n"
                if article.get('link'):
                    result += f"• **Link:** {article['link']}\n"
                result += "\n"
            
            return result
            
        except Exception as e:
            return f"❌ Error fetching news for {symbol.upper()}: {str(e)}"

    GET_STOCK_DIVIDENDS_DESCRIPTION = RichToolDescription(
        description="Get dividend history for a stock using yfinance dividends API. Shows dividend payments over time",
        use_when="When user wants to analyze dividend payments and yield history for Indian or global stocks",
        side_effects="Fetches historical dividend data from Yahoo Finance via yfinance API"
    )

    @mcp.tool(description=GET_STOCK_DIVIDENDS_DESCRIPTION.model_dump_json())
    async def get_stock_dividends(
        symbol: Annotated[str, Field(description="Stock symbol (e.g., RELIANCE.NS, TCS.BO for Indian stocks)")]
    ) -> str:
        """Get dividend history for a stock using yfinance"""
        try:
            stock_service = StockService()
            dividends = await stock_service.get_stock_dividends(symbol)
            
            if not dividends or len(dividends) == 0:
                return f"💰 No dividend history found for {symbol.upper()}"
            
            result = f"💰 **Dividend History for {symbol.upper()}**\n\n"
            result += f"**Total Dividend Records:** {len(dividends)}\n\n"
            
            # Calculate total dividends for recent years
            recent_dividends = dividends[-10:] if len(dividends) > 10 else dividends
            total_recent = sum(div['amount'] for div in recent_dividends)
            
            result += f"**Recent Dividend Summary (last {len(recent_dividends)} payments):**\n"
            result += f"• **Total Amount:** ₹{total_recent:.2f}\n"
            result += f"• **Average per Payment:** ₹{total_recent/len(recent_dividends):.2f}\n\n"
            
            result += "**Recent Dividend Payments:**\n"
            for div in recent_dividends:
                result += f"• **{div['date']}:** ₹{div['amount']:.2f}\n"
            
            # Show yearly summary if we have enough data
            if len(dividends) > 5:
                result += "\n**Yearly Summary (approx):**\n"
                yearly_total = sum(div['amount'] for div in dividends[-12:]) if len(dividends) >= 12 else total_recent
                result += f"• **Annual Dividend (estimated):** ₹{yearly_total:.2f}\n"
            
            return result
            
        except Exception as e:
            return f"❌ Error fetching dividends for {symbol.upper()}: {str(e)}"

    GET_STOCK_SPLITS_DESCRIPTION = RichToolDescription(
        description="Get stock split history using yfinance splits API. Shows stock splits and bonus issues",
        use_when="When user wants to see stock split history and bonus share issues for Indian or global stocks",
        side_effects="Fetches historical stock split data from Yahoo Finance via yfinance API"
    )

    @mcp.tool(description=GET_STOCK_SPLITS_DESCRIPTION.model_dump_json())
    async def get_stock_splits(
        symbol: Annotated[str, Field(description="Stock symbol (e.g., RELIANCE.NS, TCS.BO for Indian stocks)")]
    ) -> str:
        """Get stock split history using yfinance"""
        try:
            stock_service = StockService()
            splits = await stock_service.get_stock_splits(symbol)
            
            if not splits or len(splits) == 0:
                return f"📊 No stock split history found for {symbol.upper()}"
            
            result = f"📊 **Stock Split History for {symbol.upper()}**\n\n"
            result += f"**Total Split Records:** {len(splits)}\n\n"
            
            result += "**Split History:**\n"
            for split in splits:
                # Interpret split ratio
                ratio = split['ratio']
                if ratio > 1:
                    split_type = f"Stock Split ({ratio}:1)"
                    impact = "More shares, proportionally lower price"
                elif ratio < 1:
                    ratio_inverse = 1 / ratio
                    split_type = f"Reverse Split (1:{ratio_inverse:.0f})"
                    impact = "Fewer shares, proportionally higher price"
                else:
                    split_type = "Bonus/Other"
                    impact = "Special corporate action"
                
                result += f"• **{split['date']}:** {split_type}\n"
                result += f"  - **Ratio:** {ratio}\n"
                result += f"  - **Impact:** {impact}\n\n"
            
            # Calculate cumulative effect
            total_split_factor = 1.0
            for split in splits:
                total_split_factor *= split['ratio']
            
            result += f"**Cumulative Effect:**\n"
            result += f"• **Total Split Factor:** {total_split_factor:.2f}\n"
            if total_split_factor > 1:
                result += f"• **Meaning:** 1 original share = {total_split_factor:.2f} current shares\n"
            else:
                result += f"• **Meaning:** {1/total_split_factor:.2f} original shares = 1 current share\n"
            
            return result
            
        except Exception as e:
            return f"❌ Error fetching splits for {symbol.upper()}: {str(e)}"

    GET_FAST_INFO_DESCRIPTION = RichToolDescription(
        description="Get quick stock information using yfinance fast_info API for rapid price checks",
        use_when="When user needs quick price and basic data without full company details",
        side_effects="Fetches basic stock info quickly via yfinance fast_info API"
    )

    @mcp.tool(description=GET_FAST_INFO_DESCRIPTION.model_dump_json())
    async def get_stock_fast_info(
        symbol: Annotated[str, Field(description="Stock symbol (e.g., RELIANCE.NS, TCS.BO for Indian stocks)")]
    ) -> str:
        """Get quick stock information using yfinance fast_info"""
        try:
            stock_service = StockService()
            fast_info = await stock_service.get_stock_fast_info(symbol)
            
            result = f"⚡ **Quick Info for {symbol.upper()}**\n\n"
            
            if fast_info.get('last_price'):
                result += f"**Current Price:** ₹{fast_info['last_price']:.2f}\n"
            
            if fast_info.get('previous_close'):
                change = fast_info['last_price'] - fast_info['previous_close']
                change_percent = (change / fast_info['previous_close']) * 100
                change_symbol = "📈" if change >= 0 else "📉"
                change_sign = "+" if change >= 0 else ""
                result += f"**Change:** {change_sign}{change:.2f} ({change_sign}{change_percent:.2f}%) {change_symbol}\n"
            
            if fast_info.get('open'):
                result += f"**Open:** ₹{fast_info['open']:.2f}\n"
            
            if fast_info.get('day_high') and fast_info.get('day_low'):
                result += f"**Day Range:** ₹{fast_info['day_low']:.2f} - ₹{fast_info['day_high']:.2f}\n"
            
            if fast_info.get('year_high') and fast_info.get('year_low'):
                result += f"**52W Range:** ₹{fast_info['year_low']:.2f} - ₹{fast_info['year_high']:.2f}\n"
            
            if fast_info.get('market_cap'):
                market_cap = fast_info['market_cap']
                if market_cap >= 1e12:
                    market_cap_str = f"₹{market_cap/1e12:.2f}T"
                elif market_cap >= 1e9:
                    market_cap_str = f"₹{market_cap/1e9:.2f}B"
                elif market_cap >= 1e7:
                    market_cap_str = f"₹{market_cap/1e7:.2f}Cr"
                else:
                    market_cap_str = f"₹{market_cap:,.0f}"
                result += f"**Market Cap:** {market_cap_str}\n"
            
            if fast_info.get('shares'):
                result += f"**Shares Outstanding:** {fast_info['shares']:,}\n"
            
            if fast_info.get('currency'):
                result += f"**Currency:** {fast_info['currency']}\n"
            
            if fast_info.get('timezone'):
                result += f"**Exchange Timezone:** {fast_info['timezone']}\n"
            
            return result
            
        except Exception as e:
            return f"❌ Error fetching fast info for {symbol.upper()}: {str(e)}"

    GET_INCOME_STATEMENT_DESCRIPTION = RichToolDescription(
        description="Get income statement for a stock using yfinance financial data. Shows revenue, profit, and expenses",
        use_when="When user wants to analyze company's profitability and revenue trends for Indian or global stocks",
        side_effects="Fetches income statement data from Yahoo Finance via yfinance API"
    )

    @mcp.tool(description=GET_INCOME_STATEMENT_DESCRIPTION.model_dump_json())
    async def get_income_statement(
        symbol: Annotated[str, Field(description="Stock symbol (e.g., RELIANCE.NS, TCS.BO for Indian stocks)")]
    ) -> str:
        """Get income statement for a stock using yfinance"""
        try:
            stock_service = StockService()
            income_stmt = await stock_service.get_income_statement(symbol)
            
            if not income_stmt:
                return f"📊 No income statement data found for {symbol.upper()}"
            
            result = f"📊 **Income Statement for {symbol.upper()}**\n\n"
            
            # Show data for latest available periods
            periods = list(income_stmt.keys())[-4:] if len(income_stmt) > 4 else list(income_stmt.keys())
            
            result += "**Key Financial Metrics (in Millions):**\n\n"
            
            # Key metrics to display
            key_metrics = [
                ('Total Revenue', 'Total Revenue'),
                ('Gross Profit', 'Gross Profit'), 
                ('Operating Income', 'Operating Income'),
                ('Net Income', 'Net Income'),
                ('EBITDA', 'EBITDA'),
                ('Basic EPS', 'Basic EPS')
            ]
            
            # Create table format
            result += f"| **Metric** | " + " | ".join([f"**{period}**" for period in periods[-3:]]) + " |\n"
            result += "|" + "---|" * (len(periods[-3:]) + 1) + "\n"
            
            for metric_name, metric_key in key_metrics:
                row_data = []
                for period in periods[-3:]:
                    value = income_stmt.get(period, {}).get(metric_key)
                    if value is not None:
                        if 'EPS' in metric_name:
                            row_data.append(f"₹{value:.2f}")
                        else:
                            # Convert to millions/crores for readability
                            if abs(value) >= 1e9:
                                row_data.append(f"₹{value/1e9:.1f}B")
                            elif abs(value) >= 1e7:
                                row_data.append(f"₹{value/1e7:.1f}Cr")
                            elif abs(value) >= 1e6:
                                row_data.append(f"₹{value/1e6:.1f}M")
                            else:
                                row_data.append(f"₹{value:,.0f}")
                    else:
                        row_data.append("N/A")
                
                result += f"| **{metric_name}** | " + " | ".join(row_data) + " |\n"
            
            # Calculate growth rates if we have multiple periods
            if len(periods) >= 2:
                latest_period = periods[-1]
                previous_period = periods[-2]
                
                latest_revenue = income_stmt.get(latest_period, {}).get('Total Revenue')
                previous_revenue = income_stmt.get(previous_period, {}).get('Total Revenue')
                
                if latest_revenue and previous_revenue:
                    revenue_growth = ((latest_revenue - previous_revenue) / previous_revenue) * 100
                    result += f"\n**Revenue Growth:** {revenue_growth:+.2f}% (YoY)\n"
                
                latest_profit = income_stmt.get(latest_period, {}).get('Net Income')
                previous_profit = income_stmt.get(previous_period, {}).get('Net Income')
                
                if latest_profit and previous_profit and previous_profit != 0:
                    profit_growth = ((latest_profit - previous_profit) / abs(previous_profit)) * 100
                    result += f"**Net Income Growth:** {profit_growth:+.2f}% (YoY)\n"
            
            return result
            
        except Exception as e:
            return f"❌ Error fetching income statement for {symbol.upper()}: {str(e)}"

    GET_BALANCE_SHEET_DESCRIPTION = RichToolDescription(
        description="Get balance sheet for a stock using yfinance financial data. Shows assets, liabilities, and equity",
        use_when="When user wants to analyze company's financial position and leverage for Indian or global stocks",
        side_effects="Fetches balance sheet data from Yahoo Finance via yfinance API"
    )

    @mcp.tool(description=GET_BALANCE_SHEET_DESCRIPTION.model_dump_json())
    async def get_balance_sheet(
        symbol: Annotated[str, Field(description="Stock symbol (e.g., RELIANCE.NS, TCS.BO for Indian stocks)")]
    ) -> str:
        """Get balance sheet for a stock using yfinance"""
        try:
            stock_service = StockService()
            balance_sheet = await stock_service.get_balance_sheet(symbol)
            
            if not balance_sheet:
                return f"📊 No balance sheet data found for {symbol.upper()}"
            
            result = f"📊 **Balance Sheet for {symbol.upper()}**\n\n"
            
            # Show data for latest available periods
            periods = list(balance_sheet.keys())[-3:] if len(balance_sheet) > 3 else list(balance_sheet.keys())
            
            result += "**Key Balance Sheet Items (in Millions):**\n\n"
            
            # Key metrics to display
            key_metrics = [
                ('Total Assets', 'Total Assets'),
                ('Current Assets', 'Current Assets'),
                ('Cash & Equivalents', 'Cash And Cash Equivalents'),
                ('Total Debt', 'Total Debt'),
                ('Current Liabilities', 'Current Liabilities'),
                ('Total Equity', 'Total Equity Gross Minority Interest'),
                ('Retained Earnings', 'Retained Earnings')
            ]
            
            # Create table format
            result += f"| **Item** | " + " | ".join([f"**{period}**" for period in periods]) + " |\n"
            result += "|" + "---|" * (len(periods) + 1) + "\n"
            
            for metric_name, metric_key in key_metrics:
                row_data = []
                for period in periods:
                    value = balance_sheet.get(period, {}).get(metric_key)
                    if value is not None:
                        # Convert to millions/crores for readability
                        if abs(value) >= 1e9:
                            row_data.append(f"₹{value/1e9:.1f}B")
                        elif abs(value) >= 1e7:
                            row_data.append(f"₹{value/1e7:.1f}Cr")
                        elif abs(value) >= 1e6:
                            row_data.append(f"₹{value/1e6:.1f}M")
                        else:
                            row_data.append(f"₹{value:,.0f}")
                    else:
                        row_data.append("N/A")
                
                result += f"| **{metric_name}** | " + " | ".join(row_data) + " |\n"
            
            # Calculate financial ratios
            latest_period = periods[-1] if periods else None
            if latest_period:
                latest_data = balance_sheet[latest_period]
                
                result += f"\n**Key Financial Ratios (Latest Period):**\n"
                
                # Current Ratio
                current_assets = latest_data.get('Current Assets')
                current_liabilities = latest_data.get('Current Liabilities')
                if current_assets and current_liabilities and current_liabilities != 0:
                    current_ratio = current_assets / current_liabilities
                    result += f"• **Current Ratio:** {current_ratio:.2f}\n"
                
                # Debt to Equity Ratio
                total_debt = latest_data.get('Total Debt')
                total_equity = latest_data.get('Total Equity Gross Minority Interest')
                if total_debt and total_equity and total_equity != 0:
                    debt_equity_ratio = total_debt / total_equity
                    result += f"• **Debt-to-Equity:** {debt_equity_ratio:.2f}\n"
                
                # Cash Position
                cash = latest_data.get('Cash And Cash Equivalents')
                total_assets = latest_data.get('Total Assets')
                if cash and total_assets and total_assets != 0:
                    cash_percentage = (cash / total_assets) * 100
                    result += f"• **Cash % of Assets:** {cash_percentage:.1f}%\n"
            
            return result
            
        except Exception as e:
            return f"❌ Error fetching balance sheet for {symbol.upper()}: {str(e)}"

    GET_CASHFLOW_DESCRIPTION = RichToolDescription(
        description="Get cash flow statement for a stock using yfinance financial data. Shows operating, investing, and financing cash flows",
        use_when="When user wants to analyze company's cash generation and usage patterns for Indian or global stocks",
        side_effects="Fetches cash flow statement data from Yahoo Finance via yfinance API"
    )

    @mcp.tool(description=GET_CASHFLOW_DESCRIPTION.model_dump_json())
    async def get_cashflow_statement(
        symbol: Annotated[str, Field(description="Stock symbol (e.g., RELIANCE.NS, TCS.BO for Indian stocks)")]
    ) -> str:
        """Get cash flow statement for a stock using yfinance"""
        try:
            stock_service = StockService()
            cashflow = await stock_service.get_cashflow_statement(symbol)
            
            if not cashflow:
                return f"📊 No cash flow data found for {symbol.upper()}"
            
            result = f"📊 **Cash Flow Statement for {symbol.upper()}**\n\n"
            
            # Show data for latest available periods
            periods = list(cashflow.keys())[-3:] if len(cashflow) > 3 else list(cashflow.keys())
            
            result += "**Cash Flow Summary (in Millions):**\n\n"
            
            # Key metrics to display
            key_metrics = [
                ('Operating Cash Flow', 'Operating Cash Flow'),
                ('Free Cash Flow', 'Free Cash Flow'),
                ('Investing Cash Flow', 'Cash Flow From Continuing Investing Activities'),
                ('Financing Cash Flow', 'Cash Flow From Continuing Financing Activities'),
                ('Capital Expenditure', 'Capital Expenditure'),
                ('Net Change in Cash', 'Changes In Cash')
            ]
            
            # Create table format
            result += f"| **Cash Flow Item** | " + " | ".join([f"**{period}**" for period in periods]) + " |\n"
            result += "|" + "---|" * (len(periods) + 1) + "\n"
            
            for metric_name, metric_key in key_metrics:
                row_data = []
                for period in periods:
                    value = cashflow.get(period, {}).get(metric_key)
                    if value is not None:
                        # Convert to millions/crores for readability
                        if abs(value) >= 1e9:
                            row_data.append(f"₹{value/1e9:.1f}B")
                        elif abs(value) >= 1e7:
                            row_data.append(f"₹{value/1e7:.1f}Cr")
                        elif abs(value) >= 1e6:
                            row_data.append(f"₹{value/1e6:.1f}M")
                        else:
                            row_data.append(f"₹{value:,.0f}")
                    else:
                        row_data.append("N/A")
                
                result += f"| **{metric_name}** | " + " | ".join(row_data) + " |\n"
            
            # Cash flow analysis
            latest_period = periods[-1] if periods else None
            if latest_period:
                latest_data = cashflow[latest_period]
                
                result += f"\n**Cash Flow Analysis (Latest Period):**\n"
                
                operating_cf = latest_data.get('Operating Cash Flow')
                free_cf = latest_data.get('Free Cash Flow')
                capex = latest_data.get('Capital Expenditure')
                
                if operating_cf:
                    cf_millions = operating_cf / 1e6 if abs(operating_cf) >= 1e6 else operating_cf
                    result += f"• **Operating Cash Flow:** Strong cash generation\n" if operating_cf > 0 else f"• **Operating Cash Flow:** Negative cash from operations\n"
                
                if free_cf and operating_cf:
                    result += f"• **Free Cash Flow:** {'Positive' if free_cf > 0 else 'Negative'} (₹{abs(free_cf)/1e7:.1f}Cr)\n"
                
                if capex and operating_cf and capex != 0:
                    capex_ratio = abs(capex) / operating_cf * 100 if operating_cf > 0 else 0
                    result += f"• **CapEx as % of Operating CF:** {capex_ratio:.1f}%\n"
            
            return result
            
        except Exception as e:
            return f"❌ Error fetching cash flow statement for {symbol.upper()}: {str(e)}"

    GET_EARNINGS_DESCRIPTION = RichToolDescription(
        description="Get earnings data for a stock using yfinance earnings API. Shows quarterly and annual earnings",
        use_when="When user wants to analyze company's earnings history and trends for Indian or global stocks",
        side_effects="Fetches earnings data from Yahoo Finance via yfinance API"
    )

    @mcp.tool(description=GET_EARNINGS_DESCRIPTION.model_dump_json())
    async def get_earnings_data(
        symbol: Annotated[str, Field(description="Stock symbol (e.g., RELIANCE.NS, TCS.BO for Indian stocks)")]
    ) -> str:
        """Get earnings data for a stock using yfinance"""
        try:
            stock_service = StockService()
            earnings = await stock_service.get_earnings_data(symbol)
            
            if not earnings:
                return f"📈 No earnings data found for {symbol.upper()}"
            
            result = f"📈 **Earnings Data for {symbol.upper()}**\n\n"
            
            # Show quarterly earnings if available
            if earnings.get('quarterly'):
                quarterly_earnings = earnings['quarterly'][-8:] if len(earnings['quarterly']) > 8 else earnings['quarterly']
                
                result += "**Recent Quarterly Earnings:**\n\n"
                result += "| **Quarter** | **Earnings** | **Revenue** |\n"
                result += "|---|---|---|\n"
                
                for quarter in quarterly_earnings:
                    quarter_str = quarter.get('quarter', 'N/A')
                    earnings_val = quarter.get('earnings', 'N/A')
                    revenue_val = quarter.get('revenue', 'N/A')
                    
                    # Format values
                    if earnings_val != 'N/A' and earnings_val is not None:
                        if abs(earnings_val) >= 1e9:
                            earnings_str = f"₹{earnings_val/1e9:.2f}B"
                        elif abs(earnings_val) >= 1e7:
                            earnings_str = f"₹{earnings_val/1e7:.2f}Cr"
                        else:
                            earnings_str = f"₹{earnings_val/1e6:.1f}M"
                    else:
                        earnings_str = "N/A"
                    
                    if revenue_val != 'N/A' and revenue_val is not None:
                        if abs(revenue_val) >= 1e9:
                            revenue_str = f"₹{revenue_val/1e9:.2f}B"
                        elif abs(revenue_val) >= 1e7:
                            revenue_str = f"₹{revenue_val/1e7:.2f}Cr"
                        else:
                            revenue_str = f"₹{revenue_val/1e6:.1f}M"
                    else:
                        revenue_str = "N/A"
                    
                    result += f"| {quarter_str} | {earnings_str} | {revenue_str} |\n"
            
            # Show annual earnings if available
            if earnings.get('yearly'):
                yearly_earnings = earnings['yearly'][-4:] if len(earnings['yearly']) > 4 else earnings['yearly']
                
                result += "\n**Annual Earnings:**\n\n"
                result += "| **Year** | **Earnings** | **Revenue** |\n"
                result += "|---|---|---|\n"
                
                for year in yearly_earnings:
                    year_str = str(year.get('year', 'N/A'))
                    earnings_val = year.get('earnings', 'N/A')
                    revenue_val = year.get('revenue', 'N/A')
                    
                    # Format values
                    if earnings_val != 'N/A' and earnings_val is not None:
                        if abs(earnings_val) >= 1e9:
                            earnings_str = f"₹{earnings_val/1e9:.2f}B"
                        elif abs(earnings_val) >= 1e7:
                            earnings_str = f"₹{earnings_val/1e7:.2f}Cr"
                        else:
                            earnings_str = f"₹{earnings_val/1e6:.1f}M"
                    else:
                        earnings_str = "N/A"
                    
                    if revenue_val != 'N/A' and revenue_val is not None:
                        if abs(revenue_val) >= 1e9:
                            revenue_str = f"₹{revenue_val/1e9:.2f}B"
                        elif abs(revenue_val) >= 1e7:
                            revenue_str = f"₹{revenue_val/1e7:.2f}Cr"
                        else:
                            revenue_str = f"₹{revenue_val/1e6:.1f}M"
                    else:
                        revenue_str = "N/A"
                    
                    result += f"| {year_str} | {earnings_str} | {revenue_str} |\n"
                
                # Calculate growth if we have multiple years
                if len(yearly_earnings) >= 2:
                    latest_year = yearly_earnings[-1]
                    previous_year = yearly_earnings[-2]
                    
                    if latest_year.get('earnings') and previous_year.get('earnings') and previous_year['earnings'] != 0:
                        earnings_growth = ((latest_year['earnings'] - previous_year['earnings']) / abs(previous_year['earnings'])) * 100
                        result += f"\n**Latest Year Earnings Growth:** {earnings_growth:+.2f}% YoY\n"
                    
                    if latest_year.get('revenue') and previous_year.get('revenue') and previous_year['revenue'] != 0:
                        revenue_growth = ((latest_year['revenue'] - previous_year['revenue']) / previous_year['revenue']) * 100
                        result += f"**Latest Year Revenue Growth:** {revenue_growth:+.2f}% YoY\n"
            
            return result
            
        except Exception as e:
            return f"❌ Error fetching earnings data for {symbol.upper()}: {str(e)}"

    GET_EARNINGS_DATES_DESCRIPTION = RichToolDescription(
        description="Get upcoming earnings dates for a stock using yfinance earnings_dates API",
        use_when="When user wants to see upcoming earnings announcements for Indian or global stocks",
        side_effects="Fetches earnings calendar data from Yahoo Finance via yfinance API"
    )

    @mcp.tool(description=GET_EARNINGS_DATES_DESCRIPTION.model_dump_json())
    async def get_earnings_dates(
        symbol: Annotated[str, Field(description="Stock symbol (e.g., RELIANCE.NS, TCS.BO for Indian stocks)")]
    ) -> str:
        """Get upcoming earnings dates for a stock using yfinance"""
        try:
            stock_service = StockService()
            earnings_dates = await stock_service.get_earnings_dates(symbol)
            
            if not earnings_dates:
                return f"📅 No earnings dates found for {symbol.upper()}"
            
            result = f"📅 **Earnings Calendar for {symbol.upper()}**\n\n"
            
            # Group by upcoming vs past
            upcoming = []
            past = []
            
            from datetime import datetime
            current_date = datetime.now().date()
            
            for earning_date in earnings_dates:
                date_obj = datetime.strptime(earning_date['date'], '%Y-%m-%d').date()
                if date_obj >= current_date:
                    upcoming.append(earning_date)
                else:
                    past.append(earning_date)
            
            # Show upcoming earnings first
            if upcoming:
                result += "**🔜 Upcoming Earnings:**\n\n"
                result += "| **Date** | **EPS Estimate** | **Reported EPS** | **Revenue Estimate** |\n"
                result += "|---|---|---|---|\n"
                
                for earning in upcoming[:5]:  # Show next 5
                    date_str = earning['date']
                    eps_est = f"₹{earning['eps_estimate']:.2f}" if earning.get('eps_estimate') else "N/A"
                    eps_actual = f"₹{earning['eps_actual']:.2f}" if earning.get('eps_actual') else "TBD"
                    revenue_est = earning.get('revenue_estimate', 'N/A')
                    
                    if revenue_est != 'N/A' and revenue_est is not None:
                        if abs(revenue_est) >= 1e9:
                            revenue_str = f"₹{revenue_est/1e9:.2f}B"
                        elif abs(revenue_est) >= 1e7:
                            revenue_str = f"₹{revenue_est/1e7:.2f}Cr"
                        else:
                            revenue_str = f"₹{revenue_est/1e6:.1f}M"
                    else:
                        revenue_str = "N/A"
                    
                    result += f"| {date_str} | {eps_est} | {eps_actual} | {revenue_str} |\n"
            
            # Show recent past earnings
            if past:
                recent_past = past[-3:] if len(past) > 3 else past
                result += "\n**📊 Recent Earnings Results:**\n\n"
                result += "| **Date** | **EPS Estimate** | **Actual EPS** | **Surprise** |\n"
                result += "|---|---|---|---|\n"
                
                for earning in recent_past:
                    date_str = earning['date']
                    eps_est = earning.get('eps_estimate')
                    eps_actual = earning.get('eps_actual')
                    
                    eps_est_str = f"₹{eps_est:.2f}" if eps_est is not None else "N/A"
                    eps_actual_str = f"₹{eps_actual:.2f}" if eps_actual is not None else "N/A"
                    
                    # Calculate surprise
                    if eps_est is not None and eps_actual is not None and eps_est != 0:
                        surprise = ((eps_actual - eps_est) / abs(eps_est)) * 100
                        surprise_str = f"{surprise:+.1f}%"
                        if surprise > 0:
                            surprise_str += " 📈"
                        elif surprise < 0:
                            surprise_str += " 📉"
                    else:
                        surprise_str = "N/A"
                    
                    result += f"| {date_str} | {eps_est_str} | {eps_actual_str} | {surprise_str} |\n"
            
            # Summary
            upcoming_count = len(upcoming)
            if upcoming_count > 0:
                next_earning = upcoming[0]
                result += f"\n**📌 Next Earnings:** {next_earning['date']}"
                if next_earning.get('eps_estimate'):
                    result += f" (Est. EPS: ₹{next_earning['eps_estimate']:.2f})"
            
            return result
            
        except Exception as e:
            return f"❌ Error fetching earnings dates for {symbol.upper()}: {str(e)}"

    SEARCH_STOCKS_DESCRIPTION = RichToolDescription(
        description="Search for stock symbols using yfinance search API. Helpful for finding exact stock symbols from company names or partial queries",
        use_when="When user wants to find stock symbols, search for companies by name, or resolve ambiguous company references",
        side_effects="Searches Yahoo Finance database for matching stocks via yfinance search API"
    )

    @mcp.tool(description=SEARCH_STOCKS_DESCRIPTION.model_dump_json())
    async def search_stocks(
        query: Annotated[str, Field(description="Search query - company name or partial symbol (e.g., 'Reliance', 'TCS', 'Apple')")]
    ) -> str:
        """Search for stock symbols using yfinance search with intelligent suggestions"""
        try:
            # Use the smart resolver for comprehensive search
            resolved_symbol, resolution_message = await symbol_resolver.smart_resolve(query, context="general")
            
            # Always show search results, even if we found a direct match
            stock_service = StockService()
            search_results = await stock_service.search_stocks(query)
            
            result = f"🔍 **Stock Search Results for '{query}'**\n\n"
            
            # If we found a high-confidence match, show it first
            if resolved_symbol and "✅" in resolution_message:
                result += f"**🎯 Best Match:** {resolution_message}\n\n"
            
            if not search_results:
                result += f"❌ No additional stocks found matching '{query}'"
                if resolved_symbol:
                    result += f", but we found: {resolved_symbol}"
                return result
            
            # Show top 10 results
            top_results = search_results[:10] if len(search_results) > 10 else search_results
            
            result += "**All Matching Stocks:**\n\n"
            result += "| **Symbol** | **Company Name** | **Exchange** | **Type** |\n"
            result += "|---|---|---|---|\n"
            
            for stock in top_results:
                symbol = stock.get('symbol', 'N/A')
                name = stock.get('longname', stock.get('shortname', 'N/A'))
                # Truncate long names
                if len(name) > 40:
                    name = name[:37] + "..."
                
                exchange = stock.get('exchange', 'N/A')
                quote_type = stock.get('quoteType', stock.get('typeDisp', 'N/A'))
                
                # Highlight if this is the resolved symbol
                if resolved_symbol and symbol.upper() == resolved_symbol.upper():
                    symbol = f"**⭐ {symbol}**"
                
                result += f"| **{symbol}** | {name} | {exchange} | {quote_type} |\n"
            
            # Add search tips
            result += f"\n**Found {len(search_results)} total results (showing top {len(top_results)})**\n\n"
            result += "**💡 Tips:**\n"
            result += "• For Indian stocks, look for symbols ending with .NS (NSE) or .BO (BSE)\n"
            result += "• Use the exact symbol from the results in other stock tools\n"
            result += "• Try more specific search terms if too many results\n"
            
            # Highlight Indian stocks if any
            indian_stocks = [s for s in top_results if s.get('symbol', '').endswith(('.NS', '.BO'))]
            if indian_stocks:
                result += f"\n**🇮🇳 Indian Stocks Found:** {len(indian_stocks)} results\n"
                for stock in indian_stocks[:5]:  # Show top 5 Indian stocks
                    symbol = stock.get('symbol', '')
                    name = stock.get('longname', stock.get('shortname', ''))
                    result += f"• **{symbol}** - {name[:30]}{'...' if len(name) > 30 else ''}\n"
            
            # Global stocks
            global_stocks = [s for s in top_results if not s.get('symbol', '').endswith(('.NS', '.BO'))]
            if global_stocks:
                result += f"\n**🌍 Global Stocks Found:** {len(global_stocks)} results\n"
                for stock in global_stocks[:3]:  # Show top 3 global stocks
                    symbol = stock.get('symbol', '')
                    name = stock.get('longname', stock.get('shortname', ''))
                    result += f"• **{symbol}** - {name[:30]}{'...' if len(name) > 30 else ''}\n"
            
            return result
            
        except Exception as e:
            return f"❌ Error searching for '{query}': {str(e)}"

    # New dedicated symbol resolution tool
    RESOLVE_SYMBOL_DESCRIPTION = RichToolDescription(
        description="Smart symbol resolution tool that converts company names to exact stock symbols. Handles fuzzy matching and provides suggestions for ambiguous queries",
        use_when="When user provides company names instead of exact symbols, or when stock tools fail due to incorrect symbols",
        side_effects="Uses intelligent matching algorithms and yfinance search to find the most likely stock symbol for a company name"
    )

    @mcp.tool(description=RESOLVE_SYMBOL_DESCRIPTION.model_dump_json())
    async def resolve_symbol(
        query: Annotated[str, Field(description="Company name or partial symbol to resolve (e.g., 'Reliance', 'Tata Consultancy', 'Apple')")],
        prefer_indian: Annotated[bool, Field(description="Whether to prefer Indian stocks in results")] = True
    ) -> str:
        """Intelligently resolve company names to exact stock symbols"""
        try:
            context = "indian" if prefer_indian else "global"
            resolved_symbol, resolution_message = await symbol_resolver.smart_resolve(query, context=context)
            
            result = f"🧠 **Smart Symbol Resolution for '{query}'**\n\n"
            
            if resolved_symbol:
                result += f"✅ **Resolved Symbol:** `{resolved_symbol}`\n\n"
                result += f"**Resolution Details:** {resolution_message}\n\n"
                result += f"**🎯 Use this symbol:** `{resolved_symbol}` in other stock tools\n\n"
                
                # Try to get basic info about the resolved symbol
                try:
                    stock_service = StockService()
                    quote = await stock_service.get_stock_quote(resolved_symbol)
                    result += f"**Quick Verification:**\n"
                    result += f"• **Current Price:** ₹{quote.price:.2f}\n"
                    result += f"• **Symbol:** {quote.symbol}\n"
                except:
                    result += f"**Note:** Symbol resolved but couldn't fetch current price (may be after market hours)\n"
                
            else:
                result += f"❌ **Could not resolve '{query}' to a specific symbol**\n\n"
                result += f"{resolution_message}\n"
            
            return result
            
        except Exception as e:
            return f"❌ Error resolving symbol for '{query}': {str(e)}"
