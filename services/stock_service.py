from typing import List
import yfinance as yf
import pandas as pd
from models import StockQuote

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

    @classmethod
    async def get_stock_news(cls, symbol: str) -> list:
        """Get latest news for a stock using yfinance"""
        try:
            ticker = yf.Ticker(symbol)
            news = ticker.news
            
            if not news:
                return []
            
            # Format news data
            formatted_news = []
            for article in news:
                formatted_news.append({
                    'title': article.get('title', 'No title'),
                    'publisher': article.get('publisher', 'Unknown'),
                    'link': article.get('link', ''),
                    'publish_time': article.get('providerPublishTime', 'Unknown'),
                    'type': article.get('type', 'Unknown'),
                    'summary': article.get('summary', '')
                })
            
            return formatted_news
        except Exception as e:
            raise ValueError(f"Error fetching news for {symbol}: {str(e)}")

    @classmethod
    async def get_stock_dividends(cls, symbol: str) -> list:
        """Get dividend history for a stock using yfinance"""
        try:
            ticker = yf.Ticker(symbol)
            dividends = ticker.dividends
            
            if dividends.empty:
                return []
            
            # Format dividend data
            dividend_list = []
            for date, amount in dividends.items():
                dividend_list.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'amount': float(amount)
                })
            
            return dividend_list
        except Exception as e:
            raise ValueError(f"Error fetching dividends for {symbol}: {str(e)}")

    @classmethod
    async def get_stock_splits(cls, symbol: str) -> list:
        """Get stock split history using yfinance"""
        try:
            ticker = yf.Ticker(symbol)
            splits = ticker.splits
            
            if splits.empty:
                return []
            
            # Format splits data
            splits_list = []
            for date, ratio in splits.items():
                splits_list.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'ratio': float(ratio)
                })
            
            return splits_list
        except Exception as e:
            raise ValueError(f"Error fetching splits for {symbol}: {str(e)}")

    @classmethod
    async def get_stock_fast_info(cls, symbol: str) -> dict:
        """Get quick stock information using yfinance fast_info"""
        try:
            ticker = yf.Ticker(symbol)
            fast_info = ticker.fast_info
            
            if not fast_info:
                raise ValueError(f"No fast info available for symbol {symbol}")
            
            return {
                "symbol": symbol.upper(),
                "last_price": fast_info.get('lastPrice'),
                "previous_close": fast_info.get('previousClose'),
                "open": fast_info.get('open'),
                "day_high": fast_info.get('dayHigh'),
                "day_low": fast_info.get('dayLow'),
                "year_high": fast_info.get('yearHigh'),
                "year_low": fast_info.get('yearLow'),
                "market_cap": fast_info.get('marketCap'),
                "shares": fast_info.get('shares'),
                "currency": fast_info.get('currency'),
                "timezone": fast_info.get('timezone')
            }
        except Exception as e:
            raise ValueError(f"Error fetching fast info for {symbol}: {str(e)}")

    @classmethod
    async def get_income_statement(cls, symbol: str) -> dict:
        """Get income statement for a stock using yfinance"""
        try:
            ticker = yf.Ticker(symbol)
            income_stmt = ticker.income_stmt
            
            if income_stmt.empty:
                return {}
            
            # Convert to dictionary with periods as keys
            result = {}
            for period in income_stmt.columns:
                period_str = period.strftime('%Y-%m-%d') if hasattr(period, 'strftime') else str(period)
                result[period_str] = income_stmt[period].to_dict()
            
            return result
        except Exception as e:
            raise ValueError(f"Error fetching income statement for {symbol}: {str(e)}")

    @classmethod
    async def get_balance_sheet(cls, symbol: str) -> dict:
        """Get balance sheet for a stock using yfinance"""
        try:
            ticker = yf.Ticker(symbol)
            balance_sheet = ticker.balance_sheet
            
            if balance_sheet.empty:
                return {}
            
            # Convert to dictionary with periods as keys
            result = {}
            for period in balance_sheet.columns:
                period_str = period.strftime('%Y-%m-%d') if hasattr(period, 'strftime') else str(period)
                result[period_str] = balance_sheet[period].to_dict()
            
            return result
        except Exception as e:
            raise ValueError(f"Error fetching balance sheet for {symbol}: {str(e)}")

    @classmethod
    async def get_cashflow_statement(cls, symbol: str) -> dict:
        """Get cash flow statement for a stock using yfinance"""
        try:
            ticker = yf.Ticker(symbol)
            cashflow = ticker.cashflow
            
            if cashflow.empty:
                return {}
            
            # Convert to dictionary with periods as keys
            result = {}
            for period in cashflow.columns:
                period_str = period.strftime('%Y-%m-%d') if hasattr(period, 'strftime') else str(period)
                result[period_str] = cashflow[period].to_dict()
            
            return result
        except Exception as e:
            raise ValueError(f"Error fetching cash flow statement for {symbol}: {str(e)}")

    @classmethod
    async def get_earnings_data(cls, symbol: str) -> dict:
        """Get earnings data for a stock using yfinance"""
        try:
            ticker = yf.Ticker(symbol)
            earnings = ticker.earnings
            quarterly_earnings = ticker.quarterly_earnings
            
            result = {}
            
            # Process yearly earnings
            if not earnings.empty:
                yearly_data = []
                for year, row in earnings.iterrows():
                    yearly_data.append({
                        'year': int(year),
                        'revenue': float(row['Revenue']) if not pd.isna(row['Revenue']) else None,
                        'earnings': float(row['Earnings']) if not pd.isna(row['Earnings']) else None
                    })
                result['yearly'] = yearly_data
            
            # Process quarterly earnings
            if not quarterly_earnings.empty:
                quarterly_data = []
                for quarter, row in quarterly_earnings.iterrows():
                    quarter_str = quarter.strftime('%Y-Q%m') if hasattr(quarter, 'strftime') else str(quarter)
                    quarterly_data.append({
                        'quarter': quarter_str,
                        'revenue': float(row['Revenue']) if not pd.isna(row['Revenue']) else None,
                        'earnings': float(row['Earnings']) if not pd.isna(row['Earnings']) else None
                    })
                result['quarterly'] = quarterly_data
            
            return result
        except Exception as e:
            # Import pandas for NaN checking
            import pandas as pd
            raise ValueError(f"Error fetching earnings data for {symbol}: {str(e)}")

    @classmethod
    async def get_earnings_dates(cls, symbol: str) -> list:
        """Get earnings dates for a stock using yfinance"""
        try:
            ticker = yf.Ticker(symbol)
            earnings_dates = ticker.earnings_dates
            
            if earnings_dates.empty:
                return []
            
            # Process earnings dates
            earnings_list = []
            for date, row in earnings_dates.iterrows():
                earnings_list.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'eps_estimate': float(row['EPS Estimate']) if not pd.isna(row.get('EPS Estimate')) else None,
                    'eps_actual': float(row['Reported EPS']) if not pd.isna(row.get('Reported EPS')) else None,
                    'revenue_estimate': float(row['Revenue Estimate']) if not pd.isna(row.get('Revenue Estimate')) else None,
                    'revenue_actual': float(row['Reported Revenue']) if not pd.isna(row.get('Reported Revenue')) else None
                })
            
            return earnings_list
        except Exception as e:
            import pandas as pd
            raise ValueError(f"Error fetching earnings dates for {symbol}: {str(e)}")

    @classmethod
    async def get_recommendations(cls, symbol: str) -> list:
        """Get analyst recommendations for a stock using yfinance"""
        try:
            ticker = yf.Ticker(symbol)
            recommendations = ticker.recommendations
            
            if recommendations.empty:
                return []
            
            # Process recommendations
            recs_list = []
            for date, row in recommendations.iterrows():
                recs_list.append({
                    'date': date.strftime('%Y-%m-%d') if hasattr(date, 'strftime') else str(date),
                    'firm': row.get('Firm', 'Unknown'),
                    'toGrade': row.get('To Grade', 'N/A'),
                    'fromGrade': row.get('From Grade', ''),
                    'action': row.get('Action', 'N/A')
                })
            
            return recs_list
        except Exception as e:
            raise ValueError(f"Error fetching recommendations for {symbol}: {str(e)}")

    @classmethod
    async def get_analyst_price_targets(cls, symbol: str) -> dict:
        """Get analyst price targets for a stock using yfinance"""
        try:
            ticker = yf.Ticker(symbol)
            price_targets = ticker.analyst_price_targets
            
            # Also get current price
            current_price = None
            try:
                hist = ticker.history(period="1d")
                if not hist.empty:
                    current_price = float(hist['Close'].iloc[-1])
            except:
                pass
            
            if price_targets.empty:
                return {'current_price': current_price, 'targets': {}}
            
            # Process price targets - it's usually a single row with columns
            targets_dict = {}
            if not price_targets.empty:
                row = price_targets.iloc[0]  # Take first row
                targets_dict = {
                    'mean_target': float(row.get('mean', 0)) if not pd.isna(row.get('mean')) else None,
                    'high_target': float(row.get('high', 0)) if not pd.isna(row.get('high')) else None,
                    'low_target': float(row.get('low', 0)) if not pd.isna(row.get('low')) else None,
                    'median_target': float(row.get('median', 0)) if not pd.isna(row.get('median')) else None,
                    'numberOfAnalysts': int(row.get('numberOfAnalysts', 0)) if not pd.isna(row.get('numberOfAnalysts')) else None
                }
            
            return {
                'current_price': current_price,
                'targets': targets_dict
            }
        except Exception as e:
            raise ValueError(f"Error fetching price targets for {symbol}: {str(e)}")

    @classmethod
    async def get_major_holders(cls, symbol: str) -> dict:
        """Get major holders for a stock using yfinance"""
        try:
            ticker = yf.Ticker(symbol)
            major_holders = ticker.major_holders
            institutional_holders = ticker.institutional_holders
            mutualfund_holders = ticker.mutualfund_holders
            
            result = {}
            
            # Process major holders breakdown
            if not major_holders.empty:
                breakdown = []
                for index, row in major_holders.iterrows():
                    breakdown.append({
                        'percentage': float(str(row[0]).replace('%', '')) if '%' in str(row[0]) else row[0],
                        'description': str(row[1])
                    })
                result['ownership_breakdown'] = breakdown
            
            # Process institutional holders
            if not institutional_holders.empty:
                institutional_list = []
                for index, row in institutional_holders.iterrows():
                    institutional_list.append({
                        'holder': row.get('Holder', 'Unknown'),
                        'shares': int(row.get('Shares', 0)) if not pd.isna(row.get('Shares')) else 0,
                        'date_reported': row.get('Date Reported', ''),
                        'percent_held': float(row.get('% Out', 0)) if not pd.isna(row.get('% Out')) else 0,
                        'value': int(row.get('Value', 0)) if not pd.isna(row.get('Value')) else 0
                    })
                result['institutional_holders'] = institutional_list
            
            # Process mutual fund holders
            if not mutualfund_holders.empty:
                mf_list = []
                for index, row in mutualfund_holders.iterrows():
                    mf_list.append({
                        'holder': row.get('Holder', 'Unknown'),
                        'shares': int(row.get('Shares', 0)) if not pd.isna(row.get('Shares')) else 0,
                        'date_reported': row.get('Date Reported', ''),
                        'percent_held': float(row.get('% Out', 0)) if not pd.isna(row.get('% Out')) else 0
                    })
                result['mutual_fund_holders'] = mf_list
            
            return result
        except Exception as e:
            raise ValueError(f"Error fetching major holders for {symbol}: {str(e)}")

    @classmethod
    async def search_stocks(cls, query: str) -> list:
        """Search for stocks using yfinance search"""
        try:
            # Use yfinance search functionality
            search_results = yf.search(query)
            
            if not search_results or len(search_results) == 0:
                return []
            
            # Process search results
            results_list = []
            for result in search_results:
                results_list.append({
                    'symbol': result.get('symbol', ''),
                    'shortname': result.get('shortname', ''),
                    'longname': result.get('longname', ''),
                    'exchange': result.get('exchange', ''),
                    'quoteType': result.get('quoteType', ''),
                    'typeDisp': result.get('typeDisp', ''),
                    'market': result.get('market', ''),
                    'index': result.get('index', ''),
                    'score': result.get('score', 0)
                })
            
            # Sort by score if available
            try:
                results_list.sort(key=lambda x: x.get('score', 0), reverse=True)
            except:
                pass
            
            return results_list
        except Exception as e:
            raise ValueError(f"Error searching for stocks with query '{query}': {str(e)}")

    @classmethod
    async def get_earnings_estimates(cls, symbol: str) -> dict:
        """Get earnings estimates for a stock using yfinance"""
        try:
            ticker = yf.Ticker(symbol)
            earnings_estimate = ticker.earnings_estimate
            
            if earnings_estimate.empty:
                return {}
            
            # Process earnings estimates
            result = {}
            for period in earnings_estimate.columns:
                period_str = str(period)
                estimates_data = earnings_estimate[period]
                
                result[period_str] = {
                    'avg_estimate': float(estimates_data.get('avg', 0)) if not pd.isna(estimates_data.get('avg')) else None,
                    'low_estimate': float(estimates_data.get('low', 0)) if not pd.isna(estimates_data.get('low')) else None,
                    'high_estimate': float(estimates_data.get('high', 0)) if not pd.isna(estimates_data.get('high')) else None,
                    'number_of_analysts': int(estimates_data.get('numberOfAnalysts', 0)) if not pd.isna(estimates_data.get('numberOfAnalysts')) else None,
                }
            
            return result
        except Exception as e:
            raise ValueError(f"Error fetching earnings estimates for {symbol}: {str(e)}")

    @classmethod
    async def get_revenue_estimates(cls, symbol: str) -> dict:
        """Get revenue estimates for a stock using yfinance"""
        try:
            ticker = yf.Ticker(symbol)
            revenue_estimate = ticker.revenue_estimate
            
            if revenue_estimate.empty:
                return {}
            
            # Process revenue estimates
            result = {}
            for period in revenue_estimate.columns:
                period_str = str(period)
                estimates_data = revenue_estimate[period]
                
                result[period_str] = {
                    'avg_estimate': float(estimates_data.get('avg', 0)) if not pd.isna(estimates_data.get('avg')) else None,
                    'low_estimate': float(estimates_data.get('low', 0)) if not pd.isna(estimates_data.get('low')) else None,
                    'high_estimate': float(estimates_data.get('high', 0)) if not pd.isna(estimates_data.get('high')) else None,
                    'number_of_analysts': int(estimates_data.get('numberOfAnalysts', 0)) if not pd.isna(estimates_data.get('numberOfAnalysts')) else None,
                }
            
            return result
        except Exception as e:
            raise ValueError(f"Error fetching revenue estimates for {symbol}: {str(e)}")

    @classmethod
    async def get_institutional_holders(cls, symbol: str) -> list:
        """Get detailed institutional holders for a stock using yfinance"""
        try:
            ticker = yf.Ticker(symbol)
            institutional_holders = ticker.institutional_holders
            
            if institutional_holders.empty:
                return []
            
            # Process institutional holders
            institutional_list = []
            for index, row in institutional_holders.iterrows():
                institutional_list.append({
                    'holder': row.get('Holder', 'Unknown'),
                    'shares': int(row.get('Shares', 0)) if not pd.isna(row.get('Shares')) else 0,
                    'date_reported': str(row.get('Date Reported', '')) if row.get('Date Reported') else '',
                    'percent_held': float(row.get('% Out', 0)) if not pd.isna(row.get('% Out')) else 0,
                    'value': int(row.get('Value', 0)) if not pd.isna(row.get('Value')) else 0
                })
            
            return institutional_list
        except Exception as e:
            raise ValueError(f"Error fetching institutional holders for {symbol}: {str(e)}")
