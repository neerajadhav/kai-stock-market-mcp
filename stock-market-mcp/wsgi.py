#!/usr/bin/env python3
"""
ASGI entry point for the Stock Market MCP Server.
This file is used by Gunicorn with uvicorn workers to serve the MCP server.
"""

import asyncio
import os
from dotenv import load_dotenv
from fastmcp import FastMCP
from auth import SimpleBearerAuthProvider
from services.stock_service import StockService
from services.market_data_service import MarketDataService
from services.chart_service import ChartService
from tools.stock_tools import register_stock_tools
from tools.market_analysis_tools import register_market_analysis_tools
from tools.chart_tools import register_chart_tools

# Load environment variables
load_dotenv()

TOKEN = os.environ.get("AUTH_TOKEN")
MY_NUMBER = os.environ.get("MY_NUMBER")

assert TOKEN is not None, "Please set AUTH_TOKEN in your .env file"
assert MY_NUMBER is not None, "Please set MY_NUMBER in your .env file"

def create_app():
    """Create and configure the MCP application."""
    # Create MCP server instance
    mcp = FastMCP(
        "Stock Market MCP Server",
        auth=SimpleBearerAuthProvider(TOKEN),
    )

    # Register the validation tool
    @mcp.tool
    async def validate() -> str:
        return MY_NUMBER

    # Register all tool modules
    register_stock_tools(mcp)
    register_market_analysis_tools(mcp)
    register_chart_tools(mcp)

    return mcp

# Create the application instance for ASGI
app = create_app()

# For Gunicorn with uvicorn workers, we need to expose the ASGI app
application = app.http_app()

if __name__ == "__main__":
    # For development/testing purposes
    asyncio.run(app.run_async("streamable-http", host="0.0.0.0", port=8087))
