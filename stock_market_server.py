import asyncio
from typing import Annotated
import os
from dotenv import load_dotenv
from fastmcp import FastMCP
from fastmcp.server.auth.providers.bearer import BearerAuthProvider, RSAKeyPair
from mcp import ErrorData, McpError
from mcp.server.auth.provider import AccessToken
from mcp.types import TextContent, ImageContent, INVALID_PARAMS, INTERNAL_ERROR
from pydantic import BaseModel, Field, AnyUrl

from auth import SimpleBearerAuthProvider
from models import RichToolDescription
from services.stock_service import StockService
from services.market_data_service import MarketDataService
from services.chart_service import ChartService
from tools.stock_tools import register_stock_tools
from tools.market_analysis_tools import register_market_analysis_tools
from tools.chart_tools import register_chart_tools
from tools.analysis_tools import register_analysis_tools
from tools.screening_tools import register_screening_tools
from tools.info_tools import register_info_tools

# --- Load environment variables ---
load_dotenv()

TOKEN = os.environ.get("AUTH_TOKEN")
MY_NUMBER = os.environ.get("MY_NUMBER")

assert TOKEN is not None, "Please set AUTH_TOKEN in your .env file"
assert MY_NUMBER is not None, "Please set MY_NUMBER in your .env file"

# --- MCP Server Setup ---
mcp = FastMCP(
    "Stock Market MCP Server",
    auth=SimpleBearerAuthProvider(TOKEN),
)

# --- Tool: validate (required by Puch) ---
@mcp.tool
async def validate() -> str:
    return MY_NUMBER

# --- Health check endpoint ---
@mcp.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Stock Market MCP Server"}

@mcp.get("/")
async def root():
    return {"message": "Stock Market MCP Server", "status": "running"}

# Register all tool modules
register_stock_tools(mcp)
register_market_analysis_tools(mcp)
register_chart_tools(mcp)
register_analysis_tools(mcp)
register_screening_tools(mcp)
register_info_tools(mcp)

# --- Run MCP Server ---
async def main():
    # Railway sets PORT environment variable
    port = int(os.environ.get("PORT", 8087))
    host = "0.0.0.0"
    
    print(f"📈 Starting Stock Market MCP server on http://{host}:{port}")
    await mcp.run_async("streamable-http", host=host, port=port, path="/")

if __name__ == "__main__":
    asyncio.run(main())
