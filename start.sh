#!/bin/bash

# Startup script for Stock Market MCP Server
# This ensures proper environment setup before starting the server

echo "🚀 Starting Stock Market MCP Server..."

# Check if required environment variables are set
if [ -z "$AUTH_TOKEN" ]; then
    echo "❌ ERROR: AUTH_TOKEN environment variable is not set"
    exit 1
fi

if [ -z "$MY_NUMBER" ]; then
    echo "❌ ERROR: MY_NUMBER environment variable is not set"
    exit 1
fi

# Set default port if not provided
export PORT=${PORT:-8087}

echo "✅ Environment variables validated"
echo "📊 Starting server on port $PORT"

# Start the Python server
exec python stock_market_server.py
