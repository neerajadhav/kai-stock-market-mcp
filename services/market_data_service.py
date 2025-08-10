from typing import List
import yfinance as yf
from models import MarketIndex

class MarketDataService:
    """Service for yfinance-powered market data operations with Indian market focus"""
    
    # Major Indian market indices symbols for yfinance
    INDIAN_INDICES = {
        "NIFTY 50": "^NSEI",
        "SENSEX": "^BSESN", 
        "NIFTY BANK": "^NSEBANK",
        "NIFTY IT": "^CNXIT",
        "NIFTY AUTO": "^CNXAUTO"
    }
    
    # Global indices for comparison
    GLOBAL_INDICES = {
        "S&P 500": "^GSPC",
        "NASDAQ": "^IXIC", 
        "DOW": "^DJI"
    }
    
    # NIFTY 50 stocks (major Indian companies)
    NIFTY_50_STOCKS = [
        "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS",
        "HDFC.NS", "ITC.NS", "KOTAKBANK.NS", "HINDUNILVR.NS", "LT.NS",
        "SBIN.NS", "BAJFINANCE.NS", "BHARTIARTL.NS", "ASIANPAINT.NS", "MARUTI.NS",
        "AXISBANK.NS", "HCLTECH.NS", "M&M.NS", "NTPC.NS", "NESTLEIND.NS",
        "WIPRO.NS", "ULTRACEMCO.NS", "SUNPHARMA.NS", "POWERGRID.NS", "TATASTEEL.NS",
        "TITAN.NS", "BAJAJFINSV.NS", "TECHM.NS", "ONGC.NS", "INDUSINDBK.NS"
    ]
    
    @classmethod
    async def get_market_indices(cls) -> List[MarketIndex]:
        """Get major market indices using yfinance"""
        indices = []
        
        # Fetch Indian indices
        for name, symbol in cls.INDIAN_INDICES.items():
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="2d")
                info = ticker.info
                
                if hist.empty or len(hist) == 0:
                    continue
                
                current_value = hist['Close'].iloc[-1]
                previous_close = info.get('previousClose', hist['Close'].iloc[-2] if len(hist) > 1 else current_value)
                
                change = current_value - previous_close
                change_percent = (change / previous_close) * 100 if previous_close != 0 else 0
                
                indices.append(MarketIndex(
                    name=name,
                    symbol=symbol,
                    value=float(current_value),
                    change=float(change),
                    change_percent=float(change_percent)
                ))
            except Exception as e:
                print(f"Warning: Error fetching {name} ({symbol}): {str(e)}")
                continue
        
        return indices
    
    @classmethod
    async def get_market_movers(cls, type: str = "gainers") -> List[dict]:
        """Get market movers from predefined watchlists using yfinance"""
        movers = []
        
        # Use NIFTY 50 stocks as our watchlist
        for symbol in cls.NIFTY_50_STOCKS:
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="2d")
                info = ticker.info
                
                if hist.empty or len(hist) == 0:
                    continue
                
                current_price = hist['Close'].iloc[-1]
                previous_close = info.get('previousClose', hist['Close'].iloc[-2] if len(hist) > 1 else current_price)
                
                change = current_price - previous_close
                change_percent = (change / previous_close) * 100 if previous_close != 0 else 0
                
                movers.append({
                    'symbol': symbol,
                    'name': info.get('longName', info.get('shortName', symbol)),
                    'price': float(current_price),
                    'change': float(change),
                    'change_percent': float(change_percent),
                    'volume': int(hist['Volume'].iloc[-1]) if not hist['Volume'].iloc[-1] == 0 else 0
                })
            except Exception as e:
                print(f"Warning: Error fetching {symbol}: {str(e)}")
                continue
        
        # Sort by change percentage
        if type.lower() == "gainers":
            movers.sort(key=lambda x: x['change_percent'], reverse=True)
        else:  # losers
            movers.sort(key=lambda x: x['change_percent'])
        
        # Return top 10 movers
        return movers[:10]
    
    @classmethod
    async def compare_stocks(cls, symbols: List[str]) -> dict:
        """Compare multiple stocks using yfinance data"""
        comparison_data = []
        
        for symbol in symbols:
            try:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                hist = ticker.history(period="1y")
                
                if hist.empty or len(hist) == 0:
                    continue
                
                current_price = hist['Close'].iloc[-1]
                year_start_price = hist['Close'].iloc[0]
                ytd_return = ((current_price - year_start_price) / year_start_price) * 100
                
                # Calculate volatility (standard deviation of returns)
                returns = hist['Close'].pct_change().dropna()
                volatility = returns.std() * (252 ** 0.5) * 100  # Annualized volatility
                
                stock_data = {
                    'symbol': symbol.upper(),
                    'name': info.get('longName', info.get('shortName', symbol)),
                    'current_price': float(current_price),
                    'market_cap': info.get('marketCap'),
                    'pe_ratio': info.get('trailingPE'),
                    'pb_ratio': info.get('priceToBook'),
                    'eps': info.get('trailingEps'),
                    'dividend_yield': info.get('dividendYield'),
                    'beta': info.get('beta'),
                    'ytd_return': float(ytd_return),
                    'volatility': float(volatility),
                    'volume': int(hist['Volume'].iloc[-1]) if not hist['Volume'].iloc[-1] == 0 else 0,
                    '52w_high': info.get('fiftyTwoWeekHigh'),
                    '52w_low': info.get('fiftyTwoWeekLow'),
                    'sector': info.get('sector', 'N/A'),
                    'industry': info.get('industry', 'N/A')
                }
                
                comparison_data.append(stock_data)
                
            except Exception as e:
                print(f"Warning: Error fetching comparison data for {symbol}: {str(e)}")
                continue
        
        return {
            'stocks': comparison_data,
            'comparison_date': hist.index[-1].strftime('%Y-%m-%d') if not hist.empty else None,
            'total_stocks': len(comparison_data)
        }

    @classmethod
    async def screen_stocks(cls, screener_type: str) -> List[dict]:
        """Screen stocks using yfinance functionality"""
        try:
            # For now, we'll implement basic screening using available data
            # In a full implementation, you would use yfinance.screen() if available
            
            screened_stocks = []
            
            if screener_type in ['most_active', 'gainers', 'losers', 'trending']:
                # Use our NIFTY 50 watchlist for screening
                stocks_data = []
                
                for symbol in cls.NIFTY_50_STOCKS:
                    try:
                        ticker = yf.Ticker(symbol)
                        hist = ticker.history(period="2d")
                        info = ticker.info
                        
                        if hist.empty:
                            continue
                        
                        current_price = hist['Close'].iloc[-1]
                        previous_close = info.get('previousClose', hist['Close'].iloc[-2] if len(hist) > 1 else current_price)
                        change = current_price - previous_close
                        change_percent = (change / previous_close) * 100 if previous_close != 0 else 0
                        volume = hist['Volume'].iloc[-1]
                        
                        stock_data = {
                            'symbol': symbol,
                            'shortName': info.get('shortName', symbol),
                            'longName': info.get('longName', ''),
                            'regularMarketPrice': float(current_price),
                            'regularMarketChange': float(change),
                            'regularMarketChangePercent': float(change_percent),
                            'regularMarketVolume': int(volume) if volume else 0,
                            'marketCap': info.get('marketCap'),
                            'sector': info.get('sector', '')
                        }
                        
                        stocks_data.append(stock_data)
                        
                    except Exception as e:
                        continue
                
                # Apply screening logic
                if screener_type == 'most_active':
                    screened_stocks = sorted(stocks_data, key=lambda x: x['regularMarketVolume'], reverse=True)
                elif screener_type == 'gainers':
                    screened_stocks = sorted(stocks_data, key=lambda x: x['regularMarketChangePercent'], reverse=True)
                elif screener_type == 'losers':
                    screened_stocks = sorted(stocks_data, key=lambda x: x['regularMarketChangePercent'])
                else:  # trending
                    # For trending, we'll combine volume and price change
                    for stock in stocks_data:
                        trend_score = abs(stock['regularMarketChangePercent']) * (stock['regularMarketVolume'] / 1e6)
                        stock['trend_score'] = trend_score
                    screened_stocks = sorted(stocks_data, key=lambda x: x.get('trend_score', 0), reverse=True)
            
            elif screener_type in ['small_cap', 'mid_cap', 'large_cap']:
                # Market cap based screening
                stocks_data = []
                
                for symbol in cls.NIFTY_50_STOCKS:
                    try:
                        ticker = yf.Ticker(symbol)
                        info = ticker.info
                        hist = ticker.history(period="1d")
                        
                        if hist.empty:
                            continue
                        
                        market_cap = info.get('marketCap', 0)
                        
                        # Cap classification (in USD)
                        is_match = False
                        if screener_type == 'small_cap' and market_cap < 2e9:  # < $2B
                            is_match = True
                        elif screener_type == 'mid_cap' and 2e9 <= market_cap <= 10e9:  # $2B - $10B
                            is_match = True
                        elif screener_type == 'large_cap' and market_cap > 10e9:  # > $10B
                            is_match = True
                        
                        if is_match:
                            stock_data = {
                                'symbol': symbol,
                                'shortName': info.get('shortName', symbol),
                                'longName': info.get('longName', ''),
                                'regularMarketPrice': float(hist['Close'].iloc[-1]),
                                'marketCap': market_cap,
                                'sector': info.get('sector', '')
                            }
                            stocks_data.append(stock_data)
                            
                    except Exception as e:
                        continue
                
                # Sort by market cap
                screened_stocks = sorted(stocks_data, key=lambda x: x.get('marketCap', 0), reverse=True)
            
            return screened_stocks
            
        except Exception as e:
            raise ValueError(f"Error screening stocks: {str(e)}")
