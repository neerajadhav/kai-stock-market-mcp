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

TOKEN = os.environ.get("AUTH_TOKEN", "").strip().strip('"')
MY_NUMBER = os.environ.get("MY_NUMBER", "").strip().strip('"')

print(f"Debug: TOKEN loaded: {'Yes' if TOKEN else 'No'}")
print(f"Debug: MY_NUMBER loaded: {'Yes' if MY_NUMBER else 'No'}")

assert TOKEN, "Please set AUTH_TOKEN in your environment variables"
assert MY_NUMBER, "Please set MY_NUMBER in your environment variables"

# --- MCP Server Setup ---
mcp = FastMCP(
    "Stock Market MCP Server",
    auth=SimpleBearerAuthProvider(TOKEN),
)

# --- Tool: validate (required by Puch) ---
@mcp.tool
async def validate() -> str:
    return MY_NUMBER

# Register all tool modules
register_stock_tools(mcp)
register_market_analysis_tools(mcp)
register_chart_tools(mcp)
register_analysis_tools(mcp)
register_screening_tools(mcp)
register_info_tools(mcp)

# --- Run MCP Server ---
async def main():
    try:
        # Railway sets PORT environment variable
        port = int(os.environ.get("PORT", 8087))
        host = "0.0.0.0"
        
        print(f"📈 Starting Stock Market MCP server on http://{host}:{port}")
        print(f"🔧 Using AUTH_TOKEN: {TOKEN[:10]}..." if TOKEN else "🔧 No AUTH_TOKEN")
        print(f"📱 Validation number: {MY_NUMBER}" if MY_NUMBER else "📱 No MY_NUMBER")
        
        await mcp.run_async("streamable-http", host=host, port=port, path="/")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"💥 Server crashed: {e}")
        exit(1)
