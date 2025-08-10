from typing import Annotated
from pydantic import Field
from models import RichToolDescription

def register_info_tools(mcp):
    """Register information and capability tools"""
    
    GET_MCP_CAPABILITIES_DESCRIPTION = RichToolDescription(
        description="Get comprehensive information about Stock Market MCP capabilities, features, and usage examples",
        use_when="When user asks 'what can you do', 'help', 'capabilities', or wants to understand MCP functionality",
        side_effects="Returns detailed overview of all available tools and features"
    )

    @mcp.tool(description=GET_MCP_CAPABILITIES_DESCRIPTION.model_dump_json())
    async def get_mcp_capabilities() -> str:
        """Get comprehensive overview of Stock Market MCP capabilities and features"""
        
        return """# 📈 Stock Market MCP - Complete Capabilities Guide

## 🎯 **What is Stock Market MCP?**

The Stock Market MCP (Model Context Protocol) is a comprehensive financial data server that provides **real-time stock market data, analysis, and visualization** for both **Indian (NSE/BSE)** and **Global markets**. 

**🚀 Key Advantage:** Supports both **exact symbols** (RELIANCE.NS) AND **company names** (Reliance, Apple, TCS) with **intelligent auto-resolution**!

---

## 🔧 **Core Capabilities**

### 📊 **1. Real-Time Stock Data**
- **Current Prices & Quotes** - Live price, change %, volume, market cap
- **Multiple Stock Quotes** - Compare multiple stocks simultaneously  
- **Historical Price Data** - Price history for any time period
- **Fast Info** - Quick price checks without full details
- **Smart Symbol Resolution** - Use company names instead of exact symbols!

**Examples:**
- `get_stock_quote("Reliance")` → Auto-resolves to RELIANCE.NS
- `get_multiple_stock_quotes("Apple, Microsoft, Google")` 
- `get_stock_history("TCS", "1y")`

### 🏢 **2. Company Information**
- **Detailed Company Profiles** - Sector, industry, business summary
- **Financial Metrics** - P/E ratio, market cap, EPS, beta, dividend yield
- **52-Week Ranges** - High/low prices, trading ranges
- **Company News** - Latest news affecting stock prices
- **Dividend History** - Past dividend payments and yield analysis
- **Stock Splits** - Historical splits and bonus issues

### 📈 **3. Professional Chart Generation**
- **Price Charts** - Beautiful matplotlib charts with moving averages
- **Candlestick Charts** - OHLC technical analysis charts
- **Volume Analysis Charts** - Volume trends with VWAP indicators
- **Comparison Charts** - Side-by-side performance comparisons
- **Multiple Timeframes** - From 1 day to 10+ years

**Chart Types Available:**
- Stock Price Charts (with MA20, MA50)
- Candlestick Charts (OHLC data)
- Volume Analysis (with VWAP, Volume trends)
- Multi-stock Comparison Charts

### 💰 **4. Financial Statement Analysis**
- **Income Statements** - Revenue, profit, expenses analysis
- **Balance Sheets** - Assets, liabilities, equity breakdown
- **Cash Flow Statements** - Operating, investing, financing cash flows
- **Earnings Data** - Quarterly and annual earnings history
- **Earnings Calendar** - Upcoming earnings dates and estimates

### 🔍 **5. Market Analysis & Research**
- **Analyst Recommendations** - Buy/sell/hold ratings from analysts
- **Price Targets** - Analyst price predictions and consensus
- **Earnings Estimates** - EPS and revenue forecasts
- **Major Shareholders** - Institutional and mutual fund holdings
- **Market Indices** - NIFTY 50, SENSEX, sector indices
- **Market Movers** - Top gainers and losers

### 🌍 **6. Market Data & Screening**
- **Indian Market Indices** - NIFTY 50, SENSEX, BANK NIFTY, etc.
- **Market Movers** - Today's top gainers and losers
- **Stock Screening** - Find stocks by various criteria
- **Symbol Search** - Find exact symbols for companies
- **Smart Symbol Resolution** - Auto-convert company names to symbols

---

## 🇮🇳 **Indian Market Specialization**

### **Optimized for NSE/BSE:**
- ✅ **NSE (.NS) and BSE (.BO)** symbol support
- ✅ **Rupee (₹) currency** formatting throughout
- ✅ **Crore/Lakh number** formatting (₹1.5Cr, ₹18.5T)
- ✅ **NIFTY 50 watchlist** for screening and analysis
- ✅ **Indian market hours** and timezone considerations
- ✅ **Popular Indian stocks** pre-loaded in smart resolution

### **Pre-loaded Indian Companies:**
Reliance, TCS, Infosys, HDFC Bank, ICICI Bank, Airtel, ITC, HUL, SBI, Axis Bank, Kotak Bank, Bajaj Finance, Asian Paints, Maruti, Titan, Wipro, HCL Tech, Tech Mahindra, L&T, NTPC, ONGC, Power Grid, Coal India, Tata Steel, JSW Steel, UltraTech, Nestle, Britannia, Dr Reddy's, Sun Pharma, Cipla, Adani stocks, and many more!

---

## 🌐 **Global Market Support**

### **Major Global Stocks:**
Apple (AAPL), Microsoft (MSFT), Google/Alphabet (GOOGL), Amazon (AMZN), Tesla (TSLA), Meta/Facebook (META), Netflix (NFLX), NVIDIA (NVDA), and 50+ other major US/global companies pre-loaded.

---

## 🧠 **Intelligent Features**

### **1. Smart Symbol Resolution**
- **Input:** Company names like "Reliance", "Apple", "TCS"  
- **Output:** Correct symbols like "RELIANCE.NS", "AAPL", "TCS.NS"
- **Fuzzy Matching:** Handles typos and partial names
- **Context Aware:** Prioritizes Indian stocks for Indian users
- **Suggestions:** Shows alternatives when unsure

### **2. Error Handling & Recovery**
- **Invalid Symbols:** Auto-suggests correct symbols
- **Multiple Options:** Shows ranked suggestions with confidence scores
- **Partial Matches:** Finds closest matches using similarity algorithms
- **Fallback Search:** Uses yfinance search when direct mapping fails

### **3. Rich Formatting**
- **Emojis & Symbols:** 📈 📉 🔴 🟢 for visual indicators
- **Tables:** Clean markdown tables for comparisons
- **Currency Formatting:** Proper ₹ symbol and Indian number formatting
- **Color Coding:** Visual indicators for gains/losses

---

## 🛠️ **Available Tools**

### **Stock Data Tools (8 tools):**
1. `get_stock_quote` - Current price and change
2. `get_multiple_stock_quotes` - Multiple stocks at once  
3. `get_stock_info` - Detailed company information
4. `get_stock_history` - Historical price data
5. `get_stock_fast_info` - Quick price check
6. `search_stocks` - Find stocks by name
7. `resolve_symbol` - Convert company names to symbols
8. `get_stock_news` - Latest company news

### **Financial Analysis Tools (10 tools):**
1. `get_income_statement` - Revenue, profit analysis
2. `get_balance_sheet` - Assets, liabilities
3. `get_cashflow_statement` - Cash flow analysis  
4. `get_earnings_data` - Historical earnings
5. `get_earnings_dates` - Upcoming earnings
6. `get_stock_dividends` - Dividend history
7. `get_stock_splits` - Stock splits history
8. `get_recommendations` - Analyst ratings
9. `get_analyst_price_targets` - Price predictions
10. `get_earnings_estimates` - EPS forecasts

### **Market Analysis Tools (8 tools):**
1. `get_market_indices` - NIFTY, SENSEX, etc.
2. `get_market_movers` - Top gainers/losers
3. `compare_stocks` - Side-by-side comparison
4. `get_major_holders` - Institutional ownership
5. `get_institutional_holders` - Detailed holdings
6. `get_revenue_estimates` - Revenue forecasts
7. `get_earnings_estimate` - Earnings predictions
8. `validate` - System validation

### **Chart Generation Tools (5 tools):**
1. `create_stock_chart` - Price charts with moving averages
2. `create_candlestick_chart` - OHLC technical charts
3. `create_comparison_chart` - Multi-stock performance
4. `create_volume_analysis_chart` - Volume and VWAP analysis
5. `create_volume_analysis_chart` - Advanced volume indicators

### **Information Tools (1 tool):**
1. `get_mcp_capabilities` - This comprehensive guide!

---

## 💡 **Usage Examples**

### **Basic Stock Queries:**
```
"What's the current price of Reliance?"
"Show me TCS stock information"  
"Get quotes for Apple, Microsoft, Google"
"What's Infosys trading at?"
```

### **Analysis Queries:**
```
"Compare Reliance and TCS performance"
"Show me HDFC Bank's financial statements"
"What are analysts saying about Apple?"
"When is the next earnings for Microsoft?"
```

### **Chart Requests:**
```
"Create a price chart for Reliance over 6 months"
"Show me a candlestick chart for TCS" 
"Compare Apple vs Microsoft performance"
"Generate volume analysis for Infosys"
```

### **Market Overview:**
```
"What are today's top gainers?"
"Show me Indian market indices"
"Which stocks are moving the most?"
"What's the NIFTY 50 doing?"
```

---

## 🎯 **Perfect For:**

- 📊 **Individual Investors** - Research stocks before investing
- 💼 **Portfolio Managers** - Monitor multiple stocks and performance  
- 📈 **Technical Analysts** - Generate charts and technical indicators
- 🔍 **Financial Researchers** - Access comprehensive financial data
- 🎓 **Students & Educators** - Learn about stock market analysis
- 🤖 **AI Applications** - Integrate real-time market data

---

## 🚀 **Getting Started**

### **Simple Commands:**
1. **For Stock Prices:** Just ask "What's [company name] trading at?"
2. **For Charts:** Say "Show me a chart for [company name]"
3. **For Analysis:** Ask "Compare [company1] vs [company2]"
4. **For Market:** Ask "What are today's top movers?"

### **Pro Tips:**
- ✅ Use company names instead of exact symbols (we'll auto-resolve!)
- ✅ Ask for multiple stocks in one query: "Compare Apple, Microsoft, Google"
- ✅ Request specific time periods: "Show 6 months chart for Reliance"
- ✅ Mix Indian and global stocks: "Compare TCS vs Microsoft"

---

## 📞 **Need Help?**

- **Symbol Issues:** Use `search_stocks` or `resolve_symbol` tools
- **Data Issues:** Try different time periods or check market hours
- **Feature Questions:** Ask "What can you do with [specific topic]?"
- **Examples:** Ask "Show me examples of [specific analysis type]"

---

**📈 Ready to explore the markets? Just ask me anything about stocks, companies, or market data!**"""

    GET_MCP_HELP_DESCRIPTION = RichToolDescription(
        description="Get quick help and common usage examples for Stock Market MCP",
        use_when="When user needs quick help, usage examples, or common commands",
        side_effects="Returns concise help guide with practical examples"
    )

    @mcp.tool(description=GET_MCP_HELP_DESCRIPTION.model_dump_json())
    async def get_mcp_help() -> str:
        """Get quick help and usage examples for Stock Market MCP"""
        
        return """# 🆘 Stock Market MCP - Quick Help

## 🚀 **Most Common Commands**

### **📊 Stock Prices & Info**
```
"What's Reliance trading at?"
"Get Apple stock information"  
"Show me TCS current price"
"Multiple quotes: HDFC, ICICI, Axis"
```

### **📈 Charts & Analysis**  
```
"Create chart for Infosys 6 months"
"Candlestick chart for TCS 3 months"
"Compare Reliance vs TCS performance"
"Volume analysis for Apple"
```

### **🏢 Company Research**
```
"Show me Microsoft financial statements"
"What are analysts saying about Tesla?"
"HDFC Bank earnings history"
"When is next Apple earnings?"
```

### **🌍 Market Overview**
```
"What are today's top gainers?"
"Show Indian market indices"  
"NIFTY 50 current value"
"Top losers today"
```

---

## 🧠 **Smart Features**

✅ **No Need for Exact Symbols!** 
   - Say "Reliance" instead of "RELIANCE.NS"
   - Say "Apple" instead of "AAPL"
   - We auto-resolve company names to correct symbols!

✅ **Mix Indian & Global Stocks:**
   - "Compare TCS vs Microsoft"
   - "Show Apple and Reliance charts"

✅ **Multiple Stocks at Once:**
   - "Get quotes for Apple, Google, Microsoft"
   - "Compare HDFC, ICICI, SBI, Axis Bank"

---

## 🛠️ **Tool Categories**

| **Category** | **What it does** | **Example** |
|---|---|---|
| **📊 Stock Data** | Prices, history, company info | `get_stock_quote("Apple")` |
| **📈 Charts** | Visual price charts & analysis | `create_stock_chart("TCS", "6mo")` |  
| **💰 Financials** | Earnings, balance sheets, cash flow | `get_income_statement("Microsoft")` |
| **🔍 Analysis** | Analyst ratings, price targets | `get_recommendations("HDFC Bank")` |
| **🌍 Market** | Indices, movers, screening | `get_market_movers("gainers")` |

---

## ❓ **Troubleshooting**

**🔴 "Symbol not found" errors:**
- Use `search_stocks("company name")` to find correct symbol
- Try company's full name: "Tata Consultancy Services" 
- Check spelling of company name

**🔴 "No data available":**
- Market might be closed (check timings)
- Try different time period for historical data
- Some data may not be available for all stocks

**🔴 "Multiple matches found":**  
- Use more specific company name
- Check suggestions provided in error message
- Use exact symbol if you know it

---

## 🎯 **Quick Start Commands**

Try these right now:

1. `"What's the current price of Reliance?"`
2. `"Show me Apple vs Microsoft comparison"`
3. `"Create a chart for TCS over 3 months"`  
4. `"What are today's top gainers in Indian market?"`
5. `"Get financial information for HDFC Bank"`

**🚀 Just type any of these naturally - no special syntax needed!**

---

**💡 For complete capabilities, use `get_mcp_capabilities` tool!**"""

    GET_SUPPORTED_STOCKS_DESCRIPTION = RichToolDescription(
        description="Get list of popular Indian and global stocks with their symbols that are pre-loaded in smart resolution",
        use_when="When user wants to know which companies are supported or needs symbol examples",
        side_effects="Returns comprehensive list of supported Indian and global companies with exact symbols"
    )

    @mcp.tool(description=GET_SUPPORTED_STOCKS_DESCRIPTION.model_dump_json())
    async def get_supported_stocks() -> str:
        """Get comprehensive list of popular stocks supported by smart symbol resolution"""
        
        return """# 📋 Supported Stocks - Pre-loaded Companies

## 🇮🇳 **Major Indian Stocks (NSE/BSE)**

### **🏦 Banking & Financial Services**
| **Company** | **Symbol** | **Usage Example** |
|---|---|---|
| HDFC Bank | HDFCBANK.NS | `"HDFC Bank"` or `"HDFC"` |
| ICICI Bank | ICICIBANK.NS | `"ICICI Bank"` or `"ICICI"` |
| State Bank of India | SBIN.NS | `"SBI"` or `"State Bank"` |
| Axis Bank | AXISBANK.NS | `"Axis Bank"` or `"Axis"` |  
| Kotak Mahindra Bank | KOTAKBANK.NS | `"Kotak"` or `"Kotak Mahindra"` |
| Bajaj Finance | BAJFINANCE.NS | `"Bajaj Finance"` |
| Bajaj Finserv | BAJAJFINSV.NS | `"Bajaj Finserv"` |

### **💻 Information Technology**
| **Company** | **Symbol** | **Usage Example** |
|---|---|---|
| Tata Consultancy Services | TCS.NS | `"TCS"` or `"Tata Consultancy"` |
| Infosys | INFY.NS | `"Infosys"` |
| Wipro | WIPRO.NS | `"Wipro"` |
| HCL Technologies | HCLTECH.NS | `"HCL"` or `"HCL Technologies"` |
| Tech Mahindra | TECHM.NS | `"Tech Mahindra"` |

### **⚡ Energy & Utilities**
| **Company** | **Symbol** | **Usage Example** |
|---|---|---|
| Reliance Industries | RELIANCE.NS | `"Reliance"` |
| Oil & Natural Gas Corp | ONGC.NS | `"ONGC"` or `"Oil Natural Gas"` |
| NTPC | NTPC.NS | `"NTPC"` |
| Power Grid Corp | POWERGRID.NS | `"Power Grid"` or `"Powergrid"` |
| Coal India | COALINDIA.NS | `"Coal India"` |

### **🏭 Manufacturing & Industrial**
| **Company** | **Symbol** | **Usage Example** |
|---|---|---|
| Larsen & Toubro | LT.NS | `"L&T"` or `"Larsen Toubro"` |
| Tata Steel | TATASTEEL.NS | `"Tata Steel"` |
| JSW Steel | JSWSTEEL.NS | `"JSW Steel"` |
| UltraTech Cement | ULTRACEMCO.NS | `"UltraTech"` |
| Asian Paints | ASIANPAINT.NS | `"Asian Paints"` |

### **🚗 Automotive**  
| **Company** | **Symbol** | **Usage Example** |
|---|---|---|
| Maruti Suzuki | MARUTI.NS | `"Maruti"` or `"Maruti Suzuki"` |
| Tata Motors | TATAMOTORS.NS | `"Tata Motors"` |
| Mahindra & Mahindra | M&M.NS | `"Mahindra"` |
| Bajaj Auto | BAJAJ-AUTO.NS | `"Bajaj Auto"` |
| Eicher Motors | EICHERMOT.NS | `"Eicher"` |
| Hero MotoCorp | HEROMOTOCO.NS | `"Hero"` |

### **📱 Telecom & Consumer**
| **Company** | **Symbol** | **Usage Example** |
|---|---|---|
| Bharti Airtel | BHARTIARTL.NS | `"Airtel"` or `"Bharti Airtel"` |
| ITC | ITC.NS | `"ITC"` |
| Hindustan Unilever | HINDUNILVR.NS | `"HUL"` or `"Hindustan Unilever"` |
| Titan Company | TITAN.NS | `"Titan"` |
| Nestle India | NESTLEIND.NS | `"Nestle"` |
| Britannia Industries | BRITANNIA.NS | `"Britannia"` |

### **💊 Pharmaceuticals**
| **Company** | **Symbol** | **Usage Example** |
|---|---|---|
| Dr. Reddy's Labs | DRREDDY.NS | `"Dr Reddy"` or `"Dr Reddys"` |
| Sun Pharmaceutical | SUNPHARMA.NS | `"Sun Pharma"` |
| Cipla | CIPLA.NS | `"Cipla"` |
| Divis Laboratories | DIVISLAB.NS | `"Divis Lab"` |

### **🟢 Adani Group**
| **Company** | **Symbol** | **Usage Example** |
|---|---|---|
| Adani Enterprises | ADANIENT.NS | `"Adani Enterprises"` |
| Adani Ports | ADANIPORTS.NS | `"Adani Ports"` |
| Adani Power | ADANIPOWER.NS | `"Adani Power"` |
| Adani Green Energy | ADANIGREEN.NS | `"Adani Green"` |
| Adani Transmission | ADANITRANS.NS | `"Adani Transmission"` |

### **🛒 New Economy**
| **Company** | **Symbol** | **Usage Example** |
|---|---|---|
| Zomato | ZOMATO.NS | `"Zomato"` |
| Paytm (One97 Comm) | PAYTM.NS | `"Paytm"` |
| Nykaa (FSN E-Comm) | NYKAA.NS | `"Nykaa"` |
| DMart (Avenue Supermarts) | DMART.NS | `"DMart"` |
| LIC of India | LICI.NS | `"LIC"` or `"LICI"` |
| IRCTC | IRCTC.NS | `"IRCTC"` |

---

## 🌍 **Major Global Stocks**

### **💻 Technology**
| **Company** | **Symbol** | **Usage Example** |
|---|---|---|
| Apple | AAPL | `"Apple"` |
| Microsoft | MSFT | `"Microsoft"` |
| Alphabet/Google | GOOGL | `"Google"` or `"Alphabet"` |
| Amazon | AMZN | `"Amazon"` |
| Meta/Facebook | META | `"Meta"` or `"Facebook"` |
| Tesla | TSLA | `"Tesla"` |
| Netflix | NFLX | `"Netflix"` |
| NVIDIA | NVDA | `"NVIDIA"` |
| Intel | INTC | `"Intel"` |
| AMD | AMD | `"AMD"` |
| Oracle | ORCL | `"Oracle"` |
| Salesforce | CRM | `"Salesforce"` |
| Adobe | ADBE | `"Adobe"` |
| Cisco | CSCO | `"Cisco"` |
| IBM | IBM | `"IBM"` |

### **🏦 Financial Services**
| **Company** | **Symbol** | **Usage Example** |
|---|---|---|
| Berkshire Hathaway | BRK-A | `"Berkshire"` or `"Berkshire Hathaway"` |
| JPMorgan Chase | JPM | `"JPMorgan"` or `"JP Morgan"` |
| Bank of America | BAC | `"Bank of America"` |
| Goldman Sachs | GS | `"Goldman Sachs"` |
| American Express | AXP | `"American Express"` or `"Amex"` |
| Visa | V | `"Visa"` |
| Mastercard | MA | `"Mastercard"` |

### **🛍️ Consumer & Retail**
| **Company** | **Symbol** | **Usage Example** |
|---|---|---|
| Walmart | WMT | `"Walmart"` |
| Coca-Cola | KO | `"Coca Cola"` |
| PepsiCo | PEP | `"Pepsi"` |
| McDonald's | MCD | `"McDonalds"` |
| Starbucks | SBUX | `"Starbucks"` |
| Nike | NKE | `"Nike"` |
| Disney | DIS | `"Disney"` |

### **🏭 Industrial & Healthcare**  
| **Company** | **Symbol** | **Usage Example** |
|---|---|---|
| Johnson & Johnson | JNJ | `"Johnson Johnson"` |
| Pfizer | PFE | `"Pfizer"` |
| Boeing | BA | `"Boeing"` |
| Caterpillar | CAT | `"Caterpillar"` |
| 3M Company | MMM | `"3M"` |
| General Electric | GE | `"General Electric"` or `"GE"` |

---

## 💡 **Usage Tips**

### **✅ What Works:**
- **Company Names:** `"Reliance"`, `"Apple"`, `"TCS"`
- **Partial Names:** `"HDFC"` (resolves to HDFC Bank)
- **Common Abbreviations:** `"SBI"`, `"L&T"`, `"HUL"`
- **Mixed Case:** `"reliance"`, `"APPLE"`, `"Tcs"` - all work!

### **🎯 Pro Tips:**
1. **Use natural language** - just say the company name
2. **Don't worry about exact symbols** - we'll figure it out
3. **Multiple stocks:** `"Compare Apple, Microsoft, Google"`
4. **Mix markets:** `"TCS vs Microsoft comparison"`

### **🔍 If Not Listed:**
- Use `search_stocks("company name")` to find any stock
- Use `resolve_symbol("company name")` for smart resolution  
- We support **thousands more stocks** via yfinance search!

---

**📈 All these companies can be accessed by just using their common names - no need to remember exact symbols!**"""

    STOCK_MCP_AUTHORS_INFO_DESCRIPTION = RichToolDescription(
        description="Get authors information and resume links for the Stock Market MCP Server",
        use_when="When user asks about 'who made this', 'authors', 'creators', 'developers', or 'resume'",
        side_effects="Returns author name and resume link"
    )

    @mcp.tool(description=STOCK_MCP_AUTHORS_INFO_DESCRIPTION.model_dump_json())
    async def stock_mcp_authors_info() -> str:
        """Get authors information and resume links for the Stock Market MCP Server"""
        
        return """# Puch AI x Stock Market MCP Server - Authors

**Author:** Neeraj Adhav  
**Resume:** https://drive.google.com/drive/folders/1ucLAwjyzFtJ5vS8_UYWD_oz43LtY8L08?usp=drive_link
---
**Author:** Jansty Lewis
**Resume:** https://drive.google.com/file/d/15F2YfGq8m3SoqD_73nmXKzR-u7Iys_mb/view?usp=drivesdk
---
**Author:** Manu Shukla
**Resume:** https://drive.google.com/file/d/1_qFoiw64xWT3EVd6ox2nTcURoG-kWSa2/view?usp=drivesdk"""
