from typing import List
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import yfinance as yf
import base64
import io
from datetime import datetime

class ChartService:
    """Service for generating matplotlib stock charts"""
    
    @classmethod
    async def create_stock_chart(cls, symbol: str, period: str = "1y") -> str:
        """Create a price chart for a single stock using matplotlib"""
        try:
            # Fetch stock data
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            
            if hist.empty:
                raise ValueError(f"No data available for {symbol}")
            
            # Setup chart style
            cls._setup_chart_style()
            
            # Create figure and axis
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), height_ratios=[3, 1])
            
            # Price chart
            ax1.plot(hist.index, hist['Close'], linewidth=2, color='#2E86AB', label='Close Price')
            ax1.fill_between(hist.index, hist['Close'], alpha=0.3, color='#2E86AB')
            
            # Add moving averages
            hist['MA20'] = hist['Close'].rolling(window=20).mean()
            hist['MA50'] = hist['Close'].rolling(window=50).mean()
            
            ax1.plot(hist.index, hist['MA20'], linewidth=1, color='#A23B72', label='MA20', alpha=0.8)
            ax1.plot(hist.index, hist['MA50'], linewidth=1, color='#F18F01', label='MA50', alpha=0.8)
            
            # Format price chart
            ax1.set_title(f'{symbol.upper()} Stock Price ({period.upper()})', fontsize=16, fontweight='bold')
            ax1.set_ylabel('Price (₹)', fontsize=12)
            ax1.legend(loc='upper left')
            ax1.grid(True, alpha=0.3)
            
            # Format x-axis dates
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
            ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
            
            # Volume chart
            colors = ['#FF6B6B' if close < open else '#4ECDC4' for close, open in zip(hist['Close'], hist['Open'])]
            ax2.bar(hist.index, hist['Volume'], color=colors, alpha=0.7)
            ax2.set_ylabel('Volume', fontsize=12)
            ax2.set_xlabel('Date', fontsize=12)
            ax2.grid(True, alpha=0.3)
            
            # Format volume numbers
            ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M' if x >= 1e6 else f'{x/1e3:.0f}K'))
            
            # Format x-axis dates for volume chart
            ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
            ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
            
            plt.tight_layout()
            
            # Convert to base64
            chart_base64 = cls._save_chart_as_base64()
            return chart_base64
            
        except Exception as e:
            raise ValueError(f"Error creating chart for {symbol}: {str(e)}")
    
    @classmethod
    async def create_comparison_chart(cls, symbols: List[str], period: str = "1y") -> str:
        """Create a comparison chart for multiple stocks using matplotlib"""
        try:
            # Setup chart style
            cls._setup_chart_style()
            
            # Create figure
            fig, ax = plt.subplots(figsize=(14, 8))
            
            # Color palette for different stocks
            colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
            
            stock_data = {}
            
            # Fetch and normalize data for each stock
            for i, symbol in enumerate(symbols):
                try:
                    ticker = yf.Ticker(symbol)
                    hist = ticker.history(period=period)
                    
                    if hist.empty:
                        print(f"Warning: No data for {symbol}")
                        continue
                    
                    # Normalize to percentage change from start
                    normalized_prices = ((hist['Close'] / hist['Close'].iloc[0]) - 1) * 100
                    
                    color = colors[i % len(colors)]
                    display_symbol = symbol.replace('.NS', '').replace('.BO', '')
                    
                    ax.plot(hist.index, normalized_prices, linewidth=2.5, 
                           color=color, label=display_symbol, alpha=0.8)
                    
                    stock_data[symbol] = {
                        'data': hist,
                        'normalized': normalized_prices,
                        'color': color,
                        'display_name': display_symbol
                    }
                    
                except Exception as e:
                    print(f"Warning: Error fetching {symbol}: {str(e)}")
                    continue
            
            if not stock_data:
                raise ValueError("No valid stock data available for comparison")
            
            # Format chart
            ax.set_title(f'Stock Performance Comparison ({period.upper()})', 
                        fontsize=16, fontweight='bold', pad=20)
            ax.set_ylabel('Performance (%)', fontsize=12)
            ax.set_xlabel('Date', fontsize=12)
            ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            ax.grid(True, alpha=0.3)
            
            # Add zero line
            ax.axhline(y=0, color='black', linestyle='--', alpha=0.5, linewidth=1)
            
            # Format x-axis dates
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
            ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
            
            # Format y-axis as percentage
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.1f}%'))
            
            # Add performance summary text
            summary_text = "Performance Summary:\n"
            for symbol, data in stock_data.items():
                final_return = data['normalized'].iloc[-1]
                display_name = data['display_name']
                summary_text += f"{display_name}: {final_return:+.1f}%\n"
            
            ax.text(0.02, 0.98, summary_text, transform=ax.transAxes, 
                   verticalalignment='top', bbox=dict(boxstyle='round', 
                   facecolor='white', alpha=0.8), fontsize=9)
            
            plt.tight_layout()
            
            # Convert to base64
            chart_base64 = cls._save_chart_as_base64()
            return chart_base64
            
        except Exception as e:
            raise ValueError(f"Error creating comparison chart: {str(e)}")
    
    @classmethod
    def _setup_chart_style(cls):
        """Setup consistent chart styling"""
        # Use a more widely available style
        try:
            plt.style.use('seaborn-v0_8')
        except OSError:
            try:
                plt.style.use('seaborn')
            except OSError:
                plt.style.use('default')
        
        plt.rcParams['figure.figsize'] = (12, 8)
        plt.rcParams['font.size'] = 10
        plt.rcParams['axes.labelsize'] = 12
        plt.rcParams['axes.titlesize'] = 14
        plt.rcParams['xtick.labelsize'] = 10
        plt.rcParams['ytick.labelsize'] = 10
        plt.rcParams['legend.fontsize'] = 10
        plt.rcParams['figure.facecolor'] = 'white'
        plt.rcParams['axes.facecolor'] = 'white'
    
    @classmethod
    def _save_chart_as_base64(cls) -> str:
        """Convert matplotlib chart to base64 string"""
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        
        graphic = base64.b64encode(image_png)
        graphic = graphic.decode('utf-8')
        plt.close()  # Close the figure to free memory
        return graphic
    
    @classmethod
    async def create_candlestick_chart(cls, symbol: str, period: str = "3mo") -> str:
        """Create a candlestick chart for detailed price action analysis"""
        try:
            # Fetch stock data
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            
            if hist.empty:
                raise ValueError(f"No data available for {symbol}")
            
            # Setup chart style
            cls._setup_chart_style()
            
            # Create figure
            fig, ax = plt.subplots(figsize=(14, 8))
            
            # Create candlestick-like bars
            for i, (date, row) in enumerate(hist.iterrows()):
                open_price, high_price, low_price, close_price = row['Open'], row['High'], row['Low'], row['Close']
                
                # Determine color
                color = '#4ECDC4' if close_price >= open_price else '#FF6B6B'
                
                # Draw the high-low line
                ax.plot([date, date], [low_price, high_price], color='black', linewidth=1, alpha=0.7)
                
                # Draw the open-close rectangle
                height = abs(close_price - open_price)
                bottom = min(open_price, close_price)
                ax.bar(date, height, bottom=bottom, color=color, alpha=0.8, width=pd.Timedelta(days=0.8))
            
            # Format chart
            ax.set_title(f'{symbol.upper()} Candlestick Chart ({period.upper()})', 
                        fontsize=16, fontweight='bold')
            ax.set_ylabel('Price (₹)', fontsize=12)
            ax.set_xlabel('Date', fontsize=12)
            ax.grid(True, alpha=0.3)
            
            # Format x-axis dates
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
            ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
            
            plt.tight_layout()
            
            # Convert to base64
            chart_base64 = cls._save_chart_as_base64()
            return chart_base64
            
        except Exception as e:
            raise ValueError(f"Error creating candlestick chart for {symbol}: {str(e)}")
    
    @classmethod
    async def create_volume_analysis_chart(cls, symbol: str, period: str = "6mo") -> str:
        """Create a volume analysis chart with price overlay"""
        try:
            # Fetch stock data
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            
            if hist.empty:
                raise ValueError(f"No data available for {symbol}")
            
            # Setup chart style
            cls._setup_chart_style()
            
            # Create figure with subplots
            fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 12), height_ratios=[2, 1, 1])
            
            # Price chart with volume-weighted average price (VWAP)
            ax1.plot(hist.index, hist['Close'], linewidth=2, color='#2E86AB', label='Close Price')
            
            # Calculate VWAP
            hist['VWAP'] = (hist['Volume'] * (hist['High'] + hist['Low'] + hist['Close']) / 3).cumsum() / hist['Volume'].cumsum()
            ax1.plot(hist.index, hist['VWAP'], linewidth=2, color='#A23B72', label='VWAP', alpha=0.8)
            
            ax1.set_title(f'{symbol.upper()} Volume Analysis ({period.upper()})', fontsize=16, fontweight='bold')
            ax1.set_ylabel('Price (₹)', fontsize=12)
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            
            # Volume chart with moving average
            ax2.bar(hist.index, hist['Volume'], alpha=0.6, color='#4ECDC4')
            hist['Volume_MA'] = hist['Volume'].rolling(window=20).mean()
            ax2.plot(hist.index, hist['Volume_MA'], color='#FF6B6B', linewidth=2, label='Volume MA20')
            
            ax2.set_ylabel('Volume', fontsize=12)
            ax2.legend()
            ax2.grid(True, alpha=0.3)
            ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M' if x >= 1e6 else f'{x/1e3:.0f}K'))
            
            # Volume-Price Trend (VPT)
            hist['VPT'] = (hist['Volume'] * ((hist['Close'] - hist['Close'].shift(1)) / hist['Close'].shift(1))).cumsum()
            ax3.plot(hist.index, hist['VPT'], linewidth=2, color='#F18F01', label='Volume-Price Trend')
            ax3.axhline(y=0, color='black', linestyle='--', alpha=0.5)
            
            ax3.set_ylabel('VPT', fontsize=12)
            ax3.set_xlabel('Date', fontsize=12)
            ax3.legend()
            ax3.grid(True, alpha=0.3)
            
            # Format x-axis for all subplots
            for ax in [ax1, ax2, ax3]:
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
                ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
            
            plt.tight_layout()
            
            # Convert to base64
            chart_base64 = cls._save_chart_as_base64()
            return chart_base64
            
        except Exception as e:
            raise ValueError(f"Error creating volume analysis chart for {symbol}: {str(e)}")
