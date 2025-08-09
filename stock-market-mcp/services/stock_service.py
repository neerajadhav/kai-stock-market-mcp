from typing import List
import yfinance as yf
from models import StockQuote, StockAnalysis

class StockService:
    """Service for yfinance-powered stock operations"""
    
    @classmethod
    async def get_stock_quote(cls, symbol: str) -> StockQuote:
        """Get current stock quote for a symbol using yfinance"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            hist = ticker.history(period="2d")
            
            if hist.empty or len(hist) == 0:
                raise ValueError(f"No data available for symbol {symbol}")
            
            current_price = hist['Close'].iloc[-1]
            previous_close = info.get('previousClose', hist['Close'].iloc[-2] if len(hist) > 1 else current_price)
            
            change = current_price - previous_close
            change_percent = (change / previous_close) * 100 if previous_close != 0 else 0
            
            return StockQuote(
                symbol=symbol.upper(),
                price=float(current_price),
                change=float(change),
                change_percent=float(change_percent),
                volume=int(hist['Volume'].iloc[-1]) if not hist['Volume'].iloc[-1] == 0 else 0,
                market_cap=info.get('marketCap')
            )
        except Exception as e:
            raise ValueError(f"Error fetching quote for {symbol}: {str(e)}")
    
    @classmethod
    async def get_stock_quotes(cls, symbols: List[str]) -> List[StockQuote]:
        """Get current stock quotes for multiple symbols using yfinance"""
        quotes = []
        for symbol in symbols:
            try:
                quote = await cls.get_stock_quote(symbol)
                quotes.append(quote)
            except ValueError as e:
                # Continue with other symbols even if one fails
                print(f"Warning: {str(e)}")
                continue
        return quotes
    
    @classmethod
    async def get_stock_history(cls, symbol: str, period: str = "1y") -> dict:
        """Get historical stock price data using yfinance"""
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            
            if hist.empty:
                raise ValueError(f"No historical data available for symbol {symbol}")
            
            # Convert to dictionary format for easy consumption
            return {
                "symbol": symbol.upper(),
                "period": period,
                "data": hist.to_dict('records'),
                "start_date": hist.index[0].strftime('%Y-%m-%d'),
                "end_date": hist.index[-1].strftime('%Y-%m-%d'),
                "total_records": len(hist)
            }
        except Exception as e:
            raise ValueError(f"Error fetching history for {symbol}: {str(e)}")
    
    @classmethod
    async def get_stock_info(cls, symbol: str) -> dict:
        """Get comprehensive stock information using yfinance"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            if not info or len(info) == 0:
                raise ValueError(f"No information available for symbol {symbol}")
            
            # Extract key information
            return {
                "symbol": symbol.upper(),
                "name": info.get('longName', info.get('shortName', 'N/A')),
                "sector": info.get('sector', 'N/A'),
                "industry": info.get('industry', 'N/A'),
                "market_cap": info.get('marketCap'),
                "enterprise_value": info.get('enterpriseValue'),
                "pe_ratio": info.get('trailingPE'),
                "forward_pe": info.get('forwardPE'),
                "peg_ratio": info.get('pegRatio'),
                "price_to_book": info.get('priceToBook'),
                "eps": info.get('trailingEps'),
                "beta": info.get('beta'),
                "dividend_yield": info.get('dividendYield'),
                "ex_dividend_date": info.get('exDividendDate'),
                "fifty_two_week_high": info.get('fiftyTwoWeekHigh'),
                "fifty_two_week_low": info.get('fiftyTwoWeekLow'),
                "average_volume": info.get('averageVolume'),
                "country": info.get('country', 'N/A'),
                "currency": info.get('currency', 'N/A'),
                "exchange": info.get('exchange', 'N/A'),
                "website": info.get('website'),
                "business_summary": info.get('longBusinessSummary', 'N/A')
            }
        except Exception as e:
            raise ValueError(f"Error fetching info for {symbol}: {str(e)}")
