from typing import List, Optional, Tuple, Dict
import yfinance as yf
import re
from difflib import SequenceMatcher
import pandas as pd
import os

class SymbolResolver:
    """Service to intelligently resolve stock symbols from company names or partial symbols"""
    
    def __init__(self):
        self._stock_mapping = None
        self._global_mapping = None
        self._load_mappings()
    
    def _load_mappings(self):
        """Load stock mappings from CSV file and global companies"""
        self._load_indian_stocks_from_csv()
        self._load_global_stocks()
    
    def _load_indian_stocks_from_csv(self):
        """Load Indian stock mapping from tickers.csv file"""
        try:
            # Get the current directory path
            current_dir = os.path.dirname(__file__)
            csv_path = os.path.join(current_dir, 'tickers.csv')
            
            # Read the CSV file
            df = pd.read_csv(csv_path)
            
            # Create mapping dictionary with lowercase company names as keys
            self._stock_mapping = {}
            
            for _, row in df.iterrows():
                company_name = str(row['IssuerName']).lower().strip()
                ticker = str(row['SecurityId']).strip()
                
                # Add the full company name
                self._stock_mapping[company_name] = ticker
                
                # Create better variations for matching
                # Remove common suffixes
                clean_name = re.sub(r'\s+(limited|ltd\.?|private|pvt\.?|corporation|corp\.?|company|co\.?)$', '', company_name, flags=re.IGNORECASE)
                if clean_name != company_name and clean_name:
                    self._stock_mapping[clean_name] = ticker
                
                # Remove common prefixes  
                clean_name = re.sub(r'^(the\s+|dr\.?\s+|shri\s+|sri\s+)', '', clean_name, flags=re.IGNORECASE)
                if clean_name not in self._stock_mapping and clean_name:
                    self._stock_mapping[clean_name] = ticker
                
                # Add partial name variations (first 2-3 significant words)
                words = clean_name.split()
                if len(words) >= 2:
                    # Add first two words
                    partial_name = ' '.join(words[:2])
                    if partial_name not in self._stock_mapping:
                        self._stock_mapping[partial_name] = ticker
                    
                    # Add first three words if available
                    if len(words) >= 3:
                        partial_name_3 = ' '.join(words[:3])
                        if partial_name_3 not in self._stock_mapping:
                            self._stock_mapping[partial_name_3] = ticker
                
                # Add acronyms for multi-word companies
                if len(words) > 1:
                    acronym = ''.join(word[0] for word in words if word and word[0].isalpha())
                    if len(acronym) >= 2 and acronym not in self._stock_mapping:
                        self._stock_mapping[acronym] = ticker
            
            print(f"Loaded {len(self._stock_mapping)} Indian stock mappings from CSV")
                        
        except Exception as e:
            print(f"Error loading Indian stocks from CSV: {e}")
            # Fallback to empty mapping
            self._stock_mapping = {}
    
    def _load_global_stocks(self):
        """Load global stock mappings"""
        self._global_mapping = {
            # Global Companies
            'apple': 'AAPL',
            'microsoft': 'MSFT',
            'google': 'GOOGL',
            'alphabet': 'GOOGL',
            'amazon': 'AMZN',
            'tesla': 'TSLA',
            'meta': 'META',
            'facebook': 'META',
            'netflix': 'NFLX',
            'nvidia': 'NVDA',
            'intel': 'INTC',
            'amd': 'AMD',
            'oracle': 'ORCL',
            'salesforce': 'CRM',
            'adobe': 'ADBE',
            'cisco': 'CSCO',
            'ibm': 'IBM',
            'walmart': 'WMT',
            'berkshire hathaway': 'BRK-A',
            'berkshire': 'BRK-A',
            'johnson johnson': 'JNJ',
            'pfizer': 'PFE',
            'coca cola': 'KO',
            'pepsi': 'PEP',
            'visa': 'V',
            'mastercard': 'MA',
            'disney': 'DIS',
            'nike': 'NKE',
            'mcdonalds': 'MCD',
            'starbucks': 'SBUX',
            'boeing': 'BA',
            'caterpillar': 'CAT',
            '3m': 'MMM',
            'general electric': 'GE',
            'ge': 'GE',
            'goldman sachs': 'GS',
            'jpmorgan': 'JPM',
            'jp morgan': 'JPM',
            'bank of america': 'BAC',
            'american express': 'AXP',
            'amex': 'AXP'
        }
    
    @property 
    def stock_mapping(self):
        """Get combined stock mapping (Indian + Global)"""
        if self._stock_mapping is None:
            self._load_mappings()
        
        combined_mapping = {}
        if self._stock_mapping:
            combined_mapping.update(self._stock_mapping)
        if self._global_mapping:
            combined_mapping.update(self._global_mapping)
        
        return combined_mapping
    
    def normalize_input(self, query: str) -> str:
        """Normalize input for better matching"""
        # More thorough normalization
        normalized = query.lower().strip()
        normalized = re.sub(r'\s+(ltd\.?|limited|private|pvt\.?|corp\.?|corporation|company|co\.?)(\s|$)', '', normalized, flags=re.IGNORECASE)
        normalized = re.sub(r'[.,&]+', ' ', normalized)  # Replace punctuation with spaces
        normalized = re.sub(r'\s+', ' ', normalized).strip()  # Normalize whitespace
        return normalized
    
    def similarity(self, a: str, b: str) -> float:
        """Calculate similarity between two strings"""
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()
    
    async def resolve_symbol(self, query: str, prefer_indian: bool = True) -> Tuple[Optional[str], List[Dict], str]:
        """
        Resolve a stock symbol from company name or partial symbol.
        
        Args:
            query: Company name or partial symbol
            prefer_indian: Whether to prefer Indian stocks in results
            
        Returns:
            Tuple of (resolved_symbol, suggestions_list, resolution_message)
        """
        original_query = query
        normalized_query = self.normalize_input(query)
        
        # Step 1: Check if it's already a valid symbol
        try:
            ticker = yf.Ticker(query.upper())
            info = ticker.info
            if info and info.get('symbol'):
                return query.upper(), [], f"✅ Symbol '{query.upper()}' is valid"
        except:
            pass
        
        # Step 2: Check direct mapping for common companies
        stock_mapping = self.stock_mapping
        
        if normalized_query in stock_mapping:
            resolved_symbol = stock_mapping[normalized_query]
            return resolved_symbol, [], f"✅ Resolved '{original_query}' to '{resolved_symbol}'"
            
        # Check exact query without normalization as fallback 
        if query.lower() in stock_mapping:
            resolved_symbol = stock_mapping[query.lower()]
            return resolved_symbol, [], f"✅ Resolved '{original_query}' to '{resolved_symbol}'"
        
        # Step 3: Enhanced partial matching in mapping
        best_match = None
        best_score = 0
        best_match_type = ""
        
        for company_name, symbol in stock_mapping.items():
            # Try different matching strategies
            
            # Strategy 1: Check if query words are all in company name (improved matching)
            query_words = normalized_query.split()
            company_words = company_name.split()
            
            # Check if all query words match company words (exact word match or substring)
            words_matched = 0
            for query_word in query_words:
                for comp_word in company_words:
                    if query_word == comp_word or query_word in comp_word or comp_word.startswith(query_word):
                        words_matched += 1
                        break
            
            if words_matched == len(query_words):
                # All query words found in company name
                word_match_score = 0.95 - (0.05 * (len(company_words) - len(query_words)) / max(len(company_words), 1))  # Prefer shorter matches
                if word_match_score > best_score:
                    best_score = word_match_score
                    best_match = symbol
                    best_match_type = "word_match"
            
            # Strategy 2: Check if company name starts with query
            if company_name.startswith(normalized_query):
                start_match_score = 0.85
                if start_match_score > best_score:
                    best_score = start_match_score
                    best_match = symbol
                    best_match_type = "start_match"
            
            # Strategy 3: Traditional similarity scoring
            similarity_score = self.similarity(normalized_query, company_name)
            if similarity_score > 0.7 and similarity_score > best_score:
                best_score = similarity_score
                best_match = symbol
                best_match_type = "similarity"
        
        if best_match:
            matching_company = [k for k, v in stock_mapping.items() if v == best_match][0]
            return best_match, [], f"✅ Best match for '{original_query}' is '{best_match}' ({matching_company.title()}) [{best_match_type}]"
        
        # Step 4: Use yfinance search for broader search
        try:
            search_results = yf.search(query)
            
            if not search_results:
                return None, [], f"❌ No stocks found matching '{original_query}'. Try a different search term."
            
            # Process and rank results
            suggestions = []
            exact_match = None
            
            for result in search_results[:10]:
                symbol = result.get('symbol', '')
                short_name = result.get('shortname', '')
                long_name = result.get('longname', '')
                exchange = result.get('exchange', '')
                quote_type = result.get('quoteType', '')
                
                # Calculate relevance score
                name_score = max(
                    self.similarity(normalized_query, (short_name or '').lower()),
                    self.similarity(normalized_query, (long_name or '').lower())
                )
                
                # Boost score for Indian stocks if preferred
                is_indian = symbol.endswith('.NS') or symbol.endswith('.BO')
                if prefer_indian and is_indian:
                    name_score *= 1.2
                elif not prefer_indian and not is_indian:
                    name_score *= 1.1
                
                suggestion = {
                    'symbol': symbol,
                    'name': long_name or short_name or 'Unknown',
                    'exchange': exchange,
                    'type': quote_type,
                    'score': name_score,
                    'is_indian': is_indian
                }
                suggestions.append(suggestion)
                
                # Check for very high confidence match
                if name_score > 0.85 and not exact_match:
                    exact_match = symbol
            
            # Sort by score
            suggestions.sort(key=lambda x: x['score'], reverse=True)
            
            # Return exact match if found
            if exact_match:
                best_suggestion = next(s for s in suggestions if s['symbol'] == exact_match)
                return exact_match, suggestions[:5], f"✅ High confidence match for '{original_query}': {exact_match} ({best_suggestion['name'][:50]}{'...' if len(best_suggestion['name']) > 50 else ''})"
            
            # Return top suggestion if score is good enough
            if suggestions and suggestions[0]['score'] > 0.6:
                top_suggestion = suggestions[0]
                return top_suggestion['symbol'], suggestions[:5], f"✅ Best match for '{original_query}': {top_suggestion['symbol']} ({top_suggestion['name'][:50]}{'...' if len(top_suggestion['name']) > 50 else ''})"
            
            # Return suggestions for manual selection
            return None, suggestions[:5], f"🔍 Found {len(suggestions)} possible matches for '{original_query}'. Please review suggestions below:"
            
        except Exception as e:
            return None, [], f"❌ Error searching for '{original_query}': {str(e)}"
    
    def format_suggestions(self, suggestions: List[Dict]) -> str:
        """Format suggestions for display"""
        if not suggestions:
            return ""
        
        result = "\n**🔍 Did you mean:**\n\n"
        result += "| **Symbol** | **Company Name** | **Exchange** | **Confidence** |\n"
        result += "|---|---|---|---|\n"
        
        for suggestion in suggestions:
            symbol = suggestion['symbol']
            name = suggestion['name'][:40] + ('...' if len(suggestion['name']) > 40 else '')
            exchange = suggestion['exchange']
            confidence = f"{suggestion['score']:.0%}"
            
            # Add flag for Indian stocks
            flag = "🇮🇳 " if suggestion['is_indian'] else "🌍 "
            
            result += f"| **{flag}{symbol}** | {name} | {exchange} | {confidence} |\n"
        
        result += "\n**💡 Usage:** Copy the exact symbol (e.g., `RELIANCE.NS`) and use it in your next request.\n"
        return result
    
    async def resolve_multiple_symbols(self, symbols_input: str, prefer_indian: bool = True) -> Tuple[List[str], str]:
        """
        Resolve multiple symbols from a comma-separated string.
        
        Args:
            symbols_input: Comma-separated symbols/company names
            prefer_indian: Whether to prefer Indian stocks
            
        Returns:
            Tuple of (resolved_symbols_list, resolution_message)
        """
        symbols_list = [s.strip() for s in symbols_input.split(',')]
        resolved_symbols = []
        messages = []
        all_suggestions = []
        
        for symbol_query in symbols_list:
            if not symbol_query:
                continue
                
            resolved, suggestions, message = await self.resolve_symbol(symbol_query, prefer_indian)
            
            if resolved:
                resolved_symbols.append(resolved)
                if "✅" in message:  # Successful resolution
                    messages.append(message)
            else:
                # Could not resolve - add to suggestions
                all_suggestions.extend(suggestions)
                messages.append(f"❌ Could not resolve '{symbol_query}'")
        
        # Format final message
        final_message = "\n".join(messages)
        
        if all_suggestions:
            final_message += "\n" + self.format_suggestions(all_suggestions)
        
        return resolved_symbols, final_message
    
    def add_indian_suffix(self, symbol: str) -> str:
        """Add appropriate Indian exchange suffix if missing"""
        symbol = symbol.upper()
        
        # Already has suffix
        if symbol.endswith('.NS') or symbol.endswith('.BO'):
            return symbol
            
        # Check if it's a known Indian stock
        symbol_lower = symbol.lower()
        stock_mapping = self.stock_mapping
        for company, full_symbol in stock_mapping.items():
            if full_symbol.replace('.NS', '').replace('.BO', '').upper() == symbol:
                return full_symbol
        
        # Default to NSE for Indian market
        return f"{symbol}.NS"
    
    async def smart_resolve(self, query: str, context: str = "general") -> Tuple[Optional[str], str]:
        """
        Smart resolution with context awareness.
        
        Args:
            query: Symbol or company name
            context: Context like 'indian', 'global', 'general'
            
        Returns:
            Tuple of (resolved_symbol, formatted_message_with_suggestions)
        """
        prefer_indian = context in ['indian', 'general']
        
        resolved, suggestions, message = await self.resolve_symbol(query, prefer_indian)
        
        if resolved:
            return resolved, message
        else:
            formatted_message = message
            if suggestions:
                formatted_message += "\n" + self.format_suggestions(suggestions)
            return None, formatted_message
