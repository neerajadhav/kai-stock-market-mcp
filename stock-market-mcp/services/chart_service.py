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
        # TODO: Implement matplotlib stock chart generation
        pass
    
    @classmethod
    async def create_comparison_chart(cls, symbols: List[str], period: str = "1y") -> str:
        """Create a comparison chart for multiple stocks using matplotlib"""
        # TODO: Implement matplotlib comparison chart generation
        pass
    
    @classmethod
    def _setup_chart_style(cls):
        """Setup consistent chart styling"""
        plt.style.use('seaborn-v0_8')
        plt.rcParams['figure.figsize'] = (12, 8)
        plt.rcParams['font.size'] = 10
    
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
