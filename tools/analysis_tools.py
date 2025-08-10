from typing import Annotated
from pydantic import Field
from models import RichToolDescription
from services.stock_service import StockService

def register_analysis_tools(mcp):
    """Register all yfinance-powered analysis tools"""
    
    GET_RECOMMENDATIONS_DESCRIPTION = RichToolDescription(
        description="Get analyst recommendations for a stock using yfinance recommendations API",
        use_when="When user wants to see analyst buy/sell/hold recommendations for Indian or global stocks",
        side_effects="Fetches analyst recommendation data from Yahoo Finance via yfinance API"
    )

    @mcp.tool(description=GET_RECOMMENDATIONS_DESCRIPTION.model_dump_json())
    async def get_analyst_recommendations(
        symbol: Annotated[str, Field(description="Stock symbol (e.g., RELIANCE.NS, TCS.BO for Indian stocks)")]
    ) -> str:
        """Get analyst recommendations for a stock using yfinance"""
        try:
            stock_service = StockService()
            recommendations = await stock_service.get_recommendations(symbol)
            
            if not recommendations:
                return f"📊 No analyst recommendations found for {symbol.upper()}"
            
            result = f"📊 **Analyst Recommendations for {symbol.upper()}**\n\n"
            
            # Show recent recommendations (last 10)
            recent_recommendations = recommendations[-10:] if len(recommendations) > 10 else recommendations
            
            result += "**Recent Recommendations:**\n\n"
            result += "| **Date** | **Firm** | **To Grade** | **From Grade** | **Action** |\n"
            result += "|---|---|---|---|---|\n"
            
            for rec in recent_recommendations:
                date_str = rec.get('date', 'N/A')
                firm = rec.get('firm', 'N/A')[:20] + "..." if len(rec.get('firm', '')) > 20 else rec.get('firm', 'N/A')
                to_grade = rec.get('toGrade', 'N/A')
                from_grade = rec.get('fromGrade', 'N/A') or '-'
                action = rec.get('action', 'N/A')
                
                # Add emoji for action type
                action_emoji = ""
                if 'upgrade' in action.lower():
                    action_emoji = "📈"
                elif 'downgrade' in action.lower():
                    action_emoji = "📉"
                elif 'initiate' in action.lower():
                    action_emoji = "🆕"
                elif 'maintain' in action.lower():
                    action_emoji = "➡️"
                
                result += f"| {date_str} | {firm} | {to_grade} | {from_grade} | {action} {action_emoji} |\n"
            
            # Calculate recommendation summary
            recent_grades = [rec.get('toGrade', '').lower() for rec in recent_recommendations if rec.get('toGrade')]
            
            buy_count = sum(1 for grade in recent_grades if 'buy' in grade or 'strong' in grade)
            hold_count = sum(1 for grade in recent_grades if 'hold' in grade or 'neutral' in grade)
            sell_count = sum(1 for grade in recent_grades if 'sell' in grade)
            
            total_recent = len([g for g in recent_grades if g])
            
            if total_recent > 0:
                result += f"\n**Recent Sentiment Summary (Last {total_recent} recommendations):**\n"
                result += f"• **Buy/Strong Buy:** {buy_count} ({buy_count/total_recent*100:.1f}%)\n"
                result += f"• **Hold/Neutral:** {hold_count} ({hold_count/total_recent*100:.1f}%)\n"
                result += f"• **Sell:** {sell_count} ({sell_count/total_recent*100:.1f}%)\n"
                
                # Overall sentiment
                if buy_count > hold_count + sell_count:
                    sentiment = "🟢 **Bullish** (Most analysts recommend buying)"
                elif sell_count > buy_count + hold_count:
                    sentiment = "🔴 **Bearish** (Most analysts recommend selling)"
                elif hold_count > buy_count + sell_count:
                    sentiment = "🟡 **Neutral** (Most analysts recommend holding)"
                else:
                    sentiment = "🟡 **Mixed** (Analysts have divided opinions)"
                
                result += f"\n**Overall Sentiment:** {sentiment}\n"
            
            return result
            
        except Exception as e:
            return f"❌ Error fetching recommendations for {symbol.upper()}: {str(e)}"

    GET_PRICE_TARGETS_DESCRIPTION = RichToolDescription(
        description="Get analyst price targets for a stock using yfinance analyst_price_targets API",
        use_when="When user wants to see analyst price target consensus for Indian or global stocks",
        side_effects="Fetches analyst price target data from Yahoo Finance via yfinance API"
    )

    @mcp.tool(description=GET_PRICE_TARGETS_DESCRIPTION.model_dump_json())
    async def get_analyst_price_targets(
        symbol: Annotated[str, Field(description="Stock symbol (e.g., RELIANCE.NS, TCS.BO for Indian stocks)")]
    ) -> str:
        """Get analyst price targets for a stock using yfinance"""
        try:
            stock_service = StockService()
            price_targets = await stock_service.get_analyst_price_targets(symbol)
            
            if not price_targets:
                return f"🎯 No analyst price targets found for {symbol.upper()}"
            
            result = f"🎯 **Analyst Price Targets for {symbol.upper()}**\n\n"
            
            # Current price for comparison
            current_price = price_targets.get('current_price')
            if current_price:
                result += f"**Current Price:** ₹{current_price:.2f}\n\n"
            
            # Price target metrics
            targets = price_targets.get('targets', {})
            
            result += "**Price Target Consensus:**\n\n"
            
            if targets.get('mean_target'):
                mean_target = targets['mean_target']
                result += f"• **Mean Target:** ₹{mean_target:.2f}"
                if current_price:
                    upside = ((mean_target - current_price) / current_price) * 100
                    upside_emoji = "📈" if upside > 0 else "📉"
                    result += f" ({upside:+.1f}% upside) {upside_emoji}"
                result += "\n"
            
            if targets.get('high_target'):
                high_target = targets['high_target']
                result += f"• **High Target:** ₹{high_target:.2f}"
                if current_price:
                    high_upside = ((high_target - current_price) / current_price) * 100
                    result += f" ({high_upside:+.1f}% potential upside)"
                result += "\n"
            
            if targets.get('low_target'):
                low_target = targets['low_target']
                result += f"• **Low Target:** ₹{low_target:.2f}"
                if current_price:
                    low_upside = ((low_target - current_price) / current_price) * 100
                    result += f" ({low_upside:+.1f}% potential upside)"
                result += "\n"
            
            if targets.get('median_target'):
                median_target = targets['median_target']
                result += f"• **Median Target:** ₹{median_target:.2f}"
                if current_price:
                    median_upside = ((median_target - current_price) / current_price) * 100
                    result += f" ({median_upside:+.1f}% upside)"
                result += "\n"
            
            # Number of analysts
            num_analysts = targets.get('numberOfAnalysts')
            if num_analysts:
                result += f"\n**Coverage:** {num_analysts} analysts providing targets\n"
            
            # Target range
            if targets.get('high_target') and targets.get('low_target'):
                target_range = targets['high_target'] - targets['low_target']
                mean_price = (targets['high_target'] + targets['low_target']) / 2
                if mean_price > 0:
                    range_percentage = (target_range / mean_price) * 100
                    result += f"**Target Range:** ₹{targets['low_target']:.2f} - ₹{targets['high_target']:.2f} "
                    result += f"({range_percentage:.1f}% spread)\n"
            
            # Interpretation
            if current_price and targets.get('mean_target'):
                upside_pct = ((targets['mean_target'] - current_price) / current_price) * 100
                
                result += f"\n**Interpretation:**\n"
                if upside_pct > 20:
                    result += "🚀 **Strong Buy Signal** - Analysts see significant upside potential\n"
                elif upside_pct > 10:
                    result += "📈 **Buy Signal** - Analysts see good upside potential\n"
                elif upside_pct > 0:
                    result += "🟢 **Moderate Buy** - Analysts see modest upside\n"
                elif upside_pct > -10:
                    result += "🟡 **Hold/Neutral** - Price near target range\n"
                else:
                    result += "🔴 **Potential Overvaluation** - Current price above analyst targets\n"
            
            return result
            
        except Exception as e:
            return f"❌ Error fetching price targets for {symbol.upper()}: {str(e)}"

    GET_MAJOR_HOLDERS_DESCRIPTION = RichToolDescription(
        description="Get major shareholders information for a stock using yfinance major_holders API",
        use_when="When user wants to see major shareholders and institutional ownership for Indian or global stocks",
        side_effects="Fetches major shareholders data from Yahoo Finance via yfinance API"
    )

    @mcp.tool(description=GET_MAJOR_HOLDERS_DESCRIPTION.model_dump_json())
    async def get_major_holders(
        symbol: Annotated[str, Field(description="Stock symbol (e.g., RELIANCE.NS, TCS.BO for Indian stocks)")]
    ) -> str:
        """Get major shareholders for a stock using yfinance"""
        try:
            stock_service = StockService()
            holders = await stock_service.get_major_holders(symbol)
            
            if not holders:
                return f"👥 No major holders data found for {symbol.upper()}"
            
            result = f"👥 **Major Shareholders for {symbol.upper()}**\n\n"
            
            # Ownership breakdown
            if holders.get('ownership_breakdown'):
                breakdown = holders['ownership_breakdown']
                result += "**Ownership Breakdown:**\n\n"
                
                for item in breakdown:
                    percentage = item.get('percentage', 'N/A')
                    description = item.get('description', 'N/A')
                    result += f"• **{description}:** {percentage}%\n"
                result += "\n"
            
            # Top institutional holders
            if holders.get('institutional_holders'):
                institutional = holders['institutional_holders'][:10]  # Top 10
                
                result += "**Top Institutional Holders:**\n\n"
                result += "| **Institution** | **Shares** | **% Held** | **Value** |\n"
                result += "|---|---|---|---|\n"
                
                for holder in institutional:
                    name = holder.get('holder', 'N/A')[:25] + "..." if len(holder.get('holder', '')) > 25 else holder.get('holder', 'N/A')
                    shares = holder.get('shares', 0)
                    percent_held = holder.get('percent_held', 0)
                    value = holder.get('value', 0)
                    
                    # Format numbers
                    if shares >= 1e9:
                        shares_str = f"{shares/1e9:.2f}B"
                    elif shares >= 1e6:
                        shares_str = f"{shares/1e6:.2f}M"
                    elif shares >= 1e3:
                        shares_str = f"{shares/1e3:.2f}K"
                    else:
                        shares_str = f"{shares:,}"
                    
                    percent_str = f"{percent_held:.2f}%" if percent_held else "N/A"
                    
                    if value >= 1e9:
                        value_str = f"₹{value/1e9:.2f}B"
                    elif value >= 1e7:
                        value_str = f"₹{value/1e7:.2f}Cr"
                    elif value >= 1e6:
                        value_str = f"₹{value/1e6:.2f}M"
                    else:
                        value_str = f"₹{value:,.0f}" if value else "N/A"
                    
                    result += f"| {name} | {shares_str} | {percent_str} | {value_str} |\n"
            
            # Top mutual fund holders
            if holders.get('mutual_fund_holders'):
                mutual_funds = holders['mutual_fund_holders'][:5]  # Top 5
                
                result += "\n**Top Mutual Fund Holders:**\n\n"
                result += "| **Fund** | **Shares** | **% Held** |\n"
                result += "|---|---|---|\n"
                
                for holder in mutual_funds:
                    name = holder.get('holder', 'N/A')[:30] + "..." if len(holder.get('holder', '')) > 30 else holder.get('holder', 'N/A')
                    shares = holder.get('shares', 0)
                    percent_held = holder.get('percent_held', 0)
                    
                    # Format numbers
                    if shares >= 1e9:
                        shares_str = f"{shares/1e9:.2f}B"
                    elif shares >= 1e6:
                        shares_str = f"{shares/1e6:.2f}M"
                    elif shares >= 1e3:
                        shares_str = f"{shares/1e3:.2f}K"
                    else:
                        shares_str = f"{shares:,}"
                    
                    percent_str = f"{percent_held:.2f}%" if percent_held else "N/A"
                    
                    result += f"| {name} | {shares_str} | {percent_str} |\n"
            
            # Summary insights
            result += "\n**Ownership Insights:**\n"
            if holders.get('ownership_breakdown'):
                breakdown = holders['ownership_breakdown']
                institutional_pct = next((item['percentage'] for item in breakdown if 'institution' in item.get('description', '').lower()), None)
                insider_pct = next((item['percentage'] for item in breakdown if 'insider' in item.get('description', '').lower()), None)
                
                if institutional_pct is not None:
                    if institutional_pct > 70:
                        result += "• 🏢 **High Institutional Ownership** - Strong institutional confidence\n"
                    elif institutional_pct > 50:
                        result += "• 🏢 **Moderate Institutional Ownership** - Good institutional interest\n"
                    else:
                        result += "• 🏢 **Low Institutional Ownership** - Limited institutional presence\n"
                
                if insider_pct is not None:
                    if insider_pct > 20:
                        result += "• 👨‍💼 **High Insider Ownership** - Management has significant stake\n"
                    elif insider_pct > 5:
                        result += "• 👨‍💼 **Moderate Insider Ownership** - Management has some skin in the game\n"
                    else:
                        result += "• 👨‍💼 **Low Insider Ownership** - Limited management ownership\n"
            
            return result
            
        except Exception as e:
            return f"❌ Error fetching major holders for {symbol.upper()}: {str(e)}"

    GET_EARNINGS_ESTIMATES_DESCRIPTION = RichToolDescription(
        description="Get earnings estimates for a stock using yfinance earnings_estimate API",
        use_when="When user wants to see analyst earnings forecasts and estimates for Indian or global stocks",
        side_effects="Fetches earnings estimates data from Yahoo Finance via yfinance API"
    )

    @mcp.tool(description=GET_EARNINGS_ESTIMATES_DESCRIPTION.model_dump_json())
    async def get_earnings_estimates(
        symbol: Annotated[str, Field(description="Stock symbol (e.g., RELIANCE.NS, TCS.BO for Indian stocks)")]
    ) -> str:
        """Get earnings estimates for a stock using yfinance"""
        try:
            stock_service = StockService()
            estimates = await stock_service.get_earnings_estimates(symbol)
            
            if not estimates:
                return f"📊 No earnings estimates found for {symbol.upper()}"
            
            result = f"📊 **Earnings Estimates for {symbol.upper()}**\n\n"
            
            # Display estimates by period
            periods = ['Current Qtr', 'Next Qtr', 'Current Year', 'Next Year']
            
            result += "**Analyst Earnings Estimates:**\n\n"
            result += "| **Period** | **Avg Estimate** | **Low** | **High** | **# Analysts** |\n"
            result += "|---|---|---|---|---|\n"
            
            for period in periods:
                if period in estimates:
                    data = estimates[period]
                    avg_est = data.get('avg_estimate', 'N/A')
                    low_est = data.get('low_estimate', 'N/A')
                    high_est = data.get('high_estimate', 'N/A')
                    num_analysts = data.get('number_of_analysts', 'N/A')
                    
                    # Format values
                    avg_str = f"₹{avg_est:.2f}" if avg_est != 'N/A' and avg_est is not None else "N/A"
                    low_str = f"₹{low_est:.2f}" if low_est != 'N/A' and low_est is not None else "N/A"
                    high_str = f"₹{high_est:.2f}" if high_est != 'N/A' and high_est is not None else "N/A"
                    analysts_str = str(num_analysts) if num_analysts != 'N/A' else "N/A"
                    
                    result += f"| **{period}** | {avg_str} | {low_str} | {high_str} | {analysts_str} |\n"
            
            # Growth analysis if we have current and next year
            if 'Current Year' in estimates and 'Next Year' in estimates:
                current_est = estimates['Current Year'].get('avg_estimate')
                next_est = estimates['Next Year'].get('avg_estimate')
                
                if current_est and next_est and current_est != 0:
                    growth_rate = ((next_est - current_est) / abs(current_est)) * 100
                    result += f"\n**Expected Earnings Growth:** {growth_rate:+.1f}% (Current Year to Next Year)\n"
            
            # Consensus analysis
            result += f"\n**Consensus Analysis:**\n"
            
            # Look at current quarter estimates
            if 'Current Qtr' in estimates:
                current_qtr = estimates['Current Qtr']
                avg_est = current_qtr.get('avg_estimate')
                low_est = current_qtr.get('low_estimate')
                high_est = current_qtr.get('high_estimate')
                
                if avg_est and low_est and high_est:
                    range_pct = ((high_est - low_est) / avg_est) * 100 if avg_est != 0 else 0
                    result += f"• **Current Quarter Range:** {range_pct:.1f}% spread in estimates\n"
                    
                    if range_pct < 10:
                        result += f"• **Consensus Strength:** 🟢 Strong (Low variance in estimates)\n"
                    elif range_pct < 25:
                        result += f"• **Consensus Strength:** 🟡 Moderate (Some variance in estimates)\n"
                    else:
                        result += f"• **Consensus Strength:** 🔴 Weak (High variance in estimates)\n"
            
            return result
            
        except Exception as e:
            return f"❌ Error fetching earnings estimates for {symbol.upper()}: {str(e)}"

    GET_REVENUE_ESTIMATES_DESCRIPTION = RichToolDescription(
        description="Get revenue estimates for a stock using yfinance revenue_estimate API",
        use_when="When user wants to see analyst revenue forecasts and estimates for Indian or global stocks",
        side_effects="Fetches revenue estimates data from Yahoo Finance via yfinance API"
    )

    @mcp.tool(description=GET_REVENUE_ESTIMATES_DESCRIPTION.model_dump_json())
    async def get_revenue_estimates(
        symbol: Annotated[str, Field(description="Stock symbol (e.g., RELIANCE.NS, TCS.BO for Indian stocks)")]
    ) -> str:
        """Get revenue estimates for a stock using yfinance"""
        try:
            stock_service = StockService()
            estimates = await stock_service.get_revenue_estimates(symbol)
            
            if not estimates:
                return f"📊 No revenue estimates found for {symbol.upper()}"
            
            result = f"📊 **Revenue Estimates for {symbol.upper()}**\n\n"
            
            # Display estimates by period
            periods = ['Current Qtr', 'Next Qtr', 'Current Year', 'Next Year']
            
            result += "**Analyst Revenue Estimates:**\n\n"
            result += "| **Period** | **Avg Estimate** | **Low** | **High** | **# Analysts** |\n"
            result += "|---|---|---|---|---|\n"
            
            for period in periods:
                if period in estimates:
                    data = estimates[period]
                    avg_est = data.get('avg_estimate', 'N/A')
                    low_est = data.get('low_estimate', 'N/A')
                    high_est = data.get('high_estimate', 'N/A')
                    num_analysts = data.get('number_of_analysts', 'N/A')
                    
                    # Format values (revenue is usually in large numbers)
                    def format_revenue(value):
                        if value == 'N/A' or value is None:
                            return "N/A"
                        if abs(value) >= 1e12:
                            return f"₹{value/1e12:.2f}T"
                        elif abs(value) >= 1e9:
                            return f"₹{value/1e9:.2f}B"
                        elif abs(value) >= 1e7:
                            return f"₹{value/1e7:.2f}Cr"
                        elif abs(value) >= 1e6:
                            return f"₹{value/1e6:.2f}M"
                        else:
                            return f"₹{value:,.0f}"
                    
                    avg_str = format_revenue(avg_est)
                    low_str = format_revenue(low_est)
                    high_str = format_revenue(high_est)
                    analysts_str = str(num_analysts) if num_analysts != 'N/A' else "N/A"
                    
                    result += f"| **{period}** | {avg_str} | {low_str} | {high_str} | {analysts_str} |\n"
            
            # Growth analysis
            if 'Current Year' in estimates and 'Next Year' in estimates:
                current_est = estimates['Current Year'].get('avg_estimate')
                next_est = estimates['Next Year'].get('avg_estimate')
                
                if current_est and next_est and current_est != 0:
                    growth_rate = ((next_est - current_est) / current_est) * 100
                    result += f"\n**Expected Revenue Growth:** {growth_rate:+.1f}% (Current Year to Next Year)\n"
                    
                    # Growth interpretation
                    if growth_rate > 20:
                        result += f"• **Growth Outlook:** 🚀 High growth expected\n"
                    elif growth_rate > 10:
                        result += f"• **Growth Outlook:** 📈 Strong growth expected\n"
                    elif growth_rate > 0:
                        result += f"• **Growth Outlook:** 🟢 Moderate growth expected\n"
                    else:
                        result += f"• **Growth Outlook:** 🔴 Revenue decline expected\n"
            
            # Quarter-over-quarter growth
            if 'Current Qtr' in estimates and 'Next Qtr' in estimates:
                current_qtr = estimates['Current Qtr'].get('avg_estimate')
                next_qtr = estimates['Next Qtr'].get('avg_estimate')
                
                if current_qtr and next_qtr and current_qtr != 0:
                    qtr_growth = ((next_qtr - current_qtr) / current_qtr) * 100
                    result += f"**Expected Quarter Growth:** {qtr_growth:+.1f}% (Current to Next Quarter)\n"
            
            return result
            
        except Exception as e:
            return f"❌ Error fetching revenue estimates for {symbol.upper()}: {str(e)}"

    GET_INSTITUTIONAL_HOLDERS_DESCRIPTION = RichToolDescription(
        description="Get detailed institutional holders for a stock using yfinance institutional_holders API",
        use_when="When user wants detailed institutional ownership information for Indian or global stocks",
        side_effects="Fetches detailed institutional holders data from Yahoo Finance via yfinance API"
    )

    @mcp.tool(description=GET_INSTITUTIONAL_HOLDERS_DESCRIPTION.model_dump_json())
    async def get_institutional_holders(
        symbol: Annotated[str, Field(description="Stock symbol (e.g., RELIANCE.NS, TCS.BO for Indian stocks)")]
    ) -> str:
        """Get detailed institutional holders for a stock using yfinance"""
        try:
            stock_service = StockService()
            institutional = await stock_service.get_institutional_holders(symbol)
            
            if not institutional:
                return f"🏢 No institutional holders data found for {symbol.upper()}"
            
            result = f"🏢 **Institutional Holders for {symbol.upper()}**\n\n"
            
            # Top institutional holders
            top_institutions = institutional[:15]  # Show top 15
            
            result += f"**Top {len(top_institutions)} Institutional Holders:**\n\n"
            result += "| **#** | **Institution** | **Shares** | **Value** | **% Outstanding** | **Date** |\n"
            result += "|---|---|---|---|---|---|\n"
            
            total_institutional_value = 0
            total_institutional_shares = 0
            
            for i, holder in enumerate(top_institutions, 1):
                name = holder.get('holder', 'N/A')[:30] + "..." if len(holder.get('holder', '')) > 30 else holder.get('holder', 'N/A')
                shares = holder.get('shares', 0)
                value = holder.get('value', 0)
                percent_out = holder.get('percent_held', 0)
                date_reported = holder.get('date_reported', 'N/A')[:10] if holder.get('date_reported') else 'N/A'
                
                # Format numbers
                if shares >= 1e9:
                    shares_str = f"{shares/1e9:.2f}B"
                elif shares >= 1e6:
                    shares_str = f"{shares/1e6:.2f}M"
                elif shares >= 1e3:
                    shares_str = f"{shares/1e3:.2f}K"
                else:
                    shares_str = f"{shares:,}"
                
                if value >= 1e9:
                    value_str = f"₹{value/1e9:.2f}B"
                elif value >= 1e7:
                    value_str = f"₹{value/1e7:.2f}Cr"
                elif value >= 1e6:
                    value_str = f"₹{value/1e6:.2f}M"
                else:
                    value_str = f"₹{value:,.0f}" if value else "N/A"
                
                percent_str = f"{percent_out:.2f}%" if percent_out else "N/A"
                
                result += f"| {i} | {name} | {shares_str} | {value_str} | {percent_str} | {date_reported} |\n"
                
                total_institutional_value += value if value else 0
                total_institutional_shares += shares if shares else 0
            
            # Summary statistics
            result += f"\n**Institutional Ownership Summary:**\n"
            
            # Total institutional ownership
            if total_institutional_shares > 0:
                if total_institutional_shares >= 1e9:
                    total_shares_str = f"{total_institutional_shares/1e9:.2f}B shares"
                elif total_institutional_shares >= 1e6:
                    total_shares_str = f"{total_institutional_shares/1e6:.2f}M shares"
                else:
                    total_shares_str = f"{total_institutional_shares:,} shares"
                
                result += f"• **Total Institutional Shares:** {total_shares_str}\n"
            
            if total_institutional_value > 0:
                if total_institutional_value >= 1e9:
                    total_value_str = f"₹{total_institutional_value/1e9:.2f}B"
                elif total_institutional_value >= 1e7:
                    total_value_str = f"₹{total_institutional_value/1e7:.2f}Cr"
                else:
                    total_value_str = f"₹{total_institutional_value/1e6:.2f}M"
                
                result += f"• **Total Institutional Value:** {total_value_str}\n"
            
            # Concentration analysis
            if len(top_institutions) >= 5:
                top5_percent = sum(holder.get('percent_held', 0) for holder in top_institutions[:5])
                result += f"• **Top 5 Concentration:** {top5_percent:.2f}% of outstanding shares\n"
                
                if top5_percent > 50:
                    result += f"• **Ownership Pattern:** 🔴 Highly concentrated (Top 5 hold majority)\n"
                elif top5_percent > 30:
                    result += f"• **Ownership Pattern:** 🟡 Moderately concentrated\n"
                else:
                    result += f"• **Ownership Pattern:** 🟢 Well distributed\n"
            
            # Recent changes (if date info available)
            recent_holders = [h for h in top_institutions if h.get('date_reported') and '2024' in str(h.get('date_reported', ''))]
            if recent_holders:
                result += f"\n**Recent Activity:** {len(recent_holders)} institutions reported holdings in 2024\n"
            
            # Investment type analysis
            pension_funds = [h for h in top_institutions if 'pension' in h.get('holder', '').lower()]
            mutual_funds = [h for h in top_institutions if any(word in h.get('holder', '').lower() for word in ['fund', 'investment', 'capital'])]
            insurance = [h for h in top_institutions if 'insurance' in h.get('holder', '').lower()]
            
            if pension_funds or mutual_funds or insurance:
                result += f"\n**Holder Types:**\n"
                if pension_funds:
                    result += f"• **Pension Funds:** {len(pension_funds)} holders\n"
                if mutual_funds:
                    result += f"• **Investment Funds:** {len(mutual_funds)} holders\n"
                if insurance:
                    result += f"• **Insurance Companies:** {len(insurance)} holders\n"
            
            return result
            
        except Exception as e:
            return f"❌ Error fetching institutional holders for {symbol.upper()}: {str(e)}"
