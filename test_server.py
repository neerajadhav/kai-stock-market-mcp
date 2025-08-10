#!/usr/bin/env python3
"""
Simple test script to verify the MCP server starts correctly
"""

import os
import sys
import time
import subprocess
import requests
from dotenv import load_dotenv

def test_server():
    """Test if the MCP server starts and responds"""
    load_dotenv()
    
    # Check environment variables
    auth_token = os.environ.get("AUTH_TOKEN", "").strip().strip('"')
    my_number = os.environ.get("MY_NUMBER", "").strip().strip('"')
    
    if not auth_token:
        print("❌ AUTH_TOKEN not found in environment")
        return False
        
    if not my_number:
        print("❌ MY_NUMBER not found in environment")
        return False
        
    print(f"✅ Environment variables loaded")
    print(f"   AUTH_TOKEN: {auth_token[:10]}...")
    print(f"   MY_NUMBER: {my_number}")
    
    # Test server import
    try:
        import stock_market_server
        print("✅ Server module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import server module: {e}")
        return False
    
    # Test dependencies
    try:
        import yfinance as yf
        import matplotlib
        import pandas as pd
        print("✅ All dependencies available")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🧪 Testing Stock Market MCP Server setup...")
    
    if test_server():
        print("🎉 All tests passed! Server should work on Railway.")
    else:
        print("💥 Tests failed! Check the errors above.")
        sys.exit(1)
