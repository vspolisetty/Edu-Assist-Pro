# Updated: Edu Assist with dynamic Groq model support
import aiohttp
import asyncio
import os
from typing import List, Dict, Any
import json
from urllib.parse import quote_plus

class WebSearchService:
    def __init__(self):
        """
        Initialize web search service
        You can use multiple search APIs here:
        - DuckDuckGo (free, no API key required)
        - Google Custom Search (requires API key)
        - Bing Search (requires API key)
        """
        self.ddg_base_url = "https://api.duckduckgo.com/"
        self.google_api_key = os.getenv("GOOGLE_SEARCH_API_KEY")
        self.google_search_engine_id = os.getenv("GOOGLE_SEARCH_ENGINE_ID")
        self.bing_api_key = os.getenv("BING_SEARCH_API_KEY")
        
    async def search(self, query: str, num_results: int = 5) -> List[Dict[str, Any]]:
        """
        Perform web search and return formatted results
        """
        try:
            # Try different search methods in order of preference
            results = []
            
            # Method 1: Try DuckDuckGo first (free, no API key needed)
            try:
                ddg_results = await self._search_duckduckgo(query, num_results)
                if ddg_results:
                    results.extend(ddg_results[:num_results])
            except Exception as e:
                print(f"DuckDuckGo search failed: {e}")
            
            # Method 2: Google Custom Search (if API key available)
            if len(results) < num_results and self.google_api_key:
                try:
                    google_results = await self._search_google(query, num_results - len(results))
                    results.extend(google_results)
                except Exception as e:
                    print(f"Google search failed: {e}")
            
            # Method 3: Bing Search (if API key available)
            if len(results) < num_results and self.bing_api_key:
                try:
                    bing_results = await self._search_bing(query, num_results - len(results))
                    results.extend(bing_results)
                except Exception as e:
                    print(f"Bing search failed: {e}")
            
            # If no results, return educational fallback
            if not results:
                return self._get_educational_fallback(query)
            
            return results[:num_results]
            
        except Exception as e:
            print(f"Web search error: {e}")
            return self._get_educational_fallback(query)
    
    async def _search_duckduckgo(self, query: str, num_results: int) -> List[Dict[str, Any]]:
        """
        Search using DuckDuckGo Instant Answer API (limited but free)
        """
        try:
            async with aiohttp.ClientSession() as session:
                # DuckDuckGo Instant Answer API
                params = {
                    'q': query,
                    'format': 'json',
                    'no_html': '1',
                    'skip_disambig': '1'
                }
                
                async with session.get(self.ddg_base_url, params=params) as response:
                    data = await response.json()
                    
                    results = []
                    
                    # Check for instant answer
                    if data.get('Abstract'):
                        results.append({
                            'title': data.get('Heading', 'DuckDuckGo Result'),
                            'snippet': data['Abstract'],
                            'url': data.get('AbstractURL', ''),
                            'source': 'DuckDuckGo'
                        })
                    
                    # Check for related topics
                    if data.get('RelatedTopics'):
                        for topic in data['RelatedTopics'][:num_results-len(results)]:
                            if isinstance(topic, dict) and topic.get('Text'):
                                results.append({
                                    'title': topic.get('FirstURL', '').split('/')[-1].replace('_', ' '),
                                    'snippet': topic['Text'],
                                    'url': topic.get('FirstURL', ''),
                                    'source': 'DuckDuckGo'
                                })
                    
                    return results
                    
        except Exception as e:
            print(f"DuckDuckGo search error: {e}")
            return []
    
    async def _search_google(self, query: str, num_results: int) -> List[Dict[str, Any]]:
        """
        Search using Google Custom Search API
        """
        try:
            if not self.google_api_key or not self.google_search_engine_id:
                return []
                
            async with aiohttp.ClientSession() as session:
                url = "https://www.googleapis.com/customsearch/v1"
                params = {
                    'key': self.google_api_key,
                    'cx': self.google_search_engine_id,
                    'q': query,
                    'num': min(num_results, 10)
                }
                
                async with session.get(url, params=params) as response:
                    data = await response.json()
                    
                    results = []
                    for item in data.get('items', []):
                        results.append({
                            'title': item.get('title', ''),
                            'snippet': item.get('snippet', ''),
                            'url': item.get('link', ''),
                            'source': 'Google'
                        })
                    
                    return results
                    
        except Exception as e:
            print(f"Google search error: {e}")
            return []
    
    async def _search_bing(self, query: str, num_results: int) -> List[Dict[str, Any]]:
        """
        Search using Bing Search API
        """
        try:
            if not self.bing_api_key:
                return []
                
            async with aiohttp.ClientSession() as session:
                url = "https://api.bing.microsoft.com/v7.0/search"
                headers = {'Ocp-Apim-Subscription-Key': self.bing_api_key}
                params = {
                    'q': query,
                    'count': min(num_results, 20),
                    'responseFilter': 'webpages'
                }
                
                async with session.get(url, headers=headers, params=params) as response:
                    data = await response.json()
                    
                    results = []
                    for item in data.get('webPages', {}).get('value', []):
                        results.append({
                            'title': item.get('name', ''),
                            'snippet': item.get('snippet', ''),
                            'url': item.get('url', ''),
                            'source': 'Bing'
                        })
                    
                    return results
                    
        except Exception as e:
            print(f"Bing search error: {e}")
            return []
    
    def _get_educational_fallback(self, query: str) -> List[Dict[str, Any]]:
        """
        Return educational resources when search fails
        """
        educational_resources = [
            {
                'title': 'Khan Academy',
                'snippet': f'Free educational content related to: {query}',
                'url': f'https://www.khanacademy.org/search?page_search_query={quote_plus(query)}',
                'source': 'Educational Resource'
            },
            {
                'title': 'Wikipedia',
                'snippet': f'Encyclopedia articles about: {query}',
                'url': f'https://en.wikipedia.org/wiki/Special:Search/{quote_plus(query)}',
                'source': 'Educational Resource'
            },
            {
                'title': 'MIT OpenCourseWare',
                'snippet': f'Free course materials from MIT related to: {query}',
                'url': f'https://ocw.mit.edu/search/?q={quote_plus(query)}',
                'source': 'Educational Resource'
            }
        ]
        
        return educational_resources
    
    async def get_page_content(self, url: str, max_chars: int = 2000) -> str:
        """
        Fetch and extract content from a webpage
        """
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                
                timeout = aiohttp.ClientTimeout(total=10)
                async with session.get(url, headers=headers, timeout=timeout) as response:
                    if response.status == 200:
                        html = await response.text()
                        # Simple text extraction (you might want to use BeautifulSoup for better parsing)
                        import re
                        # Remove scripts and styles
                        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
                        html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
                        # Remove HTML tags
                        text = re.sub(r'<[^>]+>', '', html)
                        # Clean up whitespace
                        text = re.sub(r'\s+', ' ', text).strip()
                        
                        return text[:max_chars] if len(text) > max_chars else text
                    else:
                        return ""
                        
        except Exception as e:
            print(f"Error fetching page content: {e}")
            return ""
    
    async def health_check(self) -> bool:
        """
        Check if web search service is working
        """
        try:
            results = await self.search("test query", num_results=1)
            return len(results) > 0
        except:
            return False
