"""
Web Search Tool for Market Intelligence Research Agent.

This tool performs web searches using external search APIs.
"""
import os
import json
import requests
from typing import List, Dict, Any, Optional

class WebSearchTool:
    """
    Performs web searches using external search APIs (Brave, Bing, or Serper).
    """
    
    def __init__(self, api_key: Optional[str] = None, search_engine: str = "brave"):
        """
        Initialize the web search tool.
        
        Args:
            api_key: API key for the search engine
            search_engine: Search engine to use (brave, bing, or serper)
        """
        self.api_key = api_key or os.environ.get("SEARCH_API_KEY")
        self.search_engine = search_engine.lower()
        
    def search(self, query: str, num_results: int = 5) -> List[Dict[str, str]]:
        """
        Perform a web search with the given query.
        
        Args:
            query: Search query
            num_results: Number of results to return
            
        Returns:
            List of search result dictionaries
        """
        # In a production system, this would call the actual search API
        # For now, we'll return mock results
        
        if self.search_engine == "brave":
            return self._mock_brave_search(query, num_results)
        elif self.search_engine == "bing":
            return self._mock_bing_search(query, num_results)
        elif self.search_engine == "serper":
            return self._mock_serper_search(query, num_results)
        else:
            raise ValueError(f"Unsupported search engine: {self.search_engine}")
    
    def _mock_brave_search(self, query: str, num_results: int) -> List[Dict[str, str]]:
        """
        Mock Brave search results for testing.
        
        Args:
            query: Search query
            num_results: Number of results to return
            
        Returns:
            List of mock search results
        """
        domain = self._extract_domain(query)
        
        mock_results = [
            {
                "title": f"{domain} Market Size, Share & Trends Analysis Report, 2023-2030",
                "url": f"https://www.example.com/reports/{domain.lower()}-market-analysis",
                "snippet": f"The global {domain} market size was valued at USD 5.2 billion in 2022 and is expected to grow at a compound annual growth rate (CAGR) of 15.3% from 2023 to 2030."
            },
            {
                "title": f"Top 10 {domain} Startups to Watch in 2023",
                "url": f"https://www.techcrunch.com/2023/top-{domain.lower()}-startups",
                "snippet": f"These innovative {domain} startups are disrupting the industry with new technologies and business models."
            },
            {
                "title": f"{domain} Industry Trends and Future Outlook",
                "url": f"https://www.industryreports.com/{domain.lower()}-trends",
                "snippet": f"Key trends shaping the {domain} industry include AI integration, mobile-first approaches, and subscription-based revenue models."
            },
            {
                "title": f"Funding Landscape in the {domain} Sector",
                "url": f"https://www.venturecapital.com/{domain.lower()}-funding",
                "snippet": f"Venture capital investments in {domain} startups reached $12.5 billion in 2022, with early-stage funding showing particularly strong growth."
            },
            {
                "title": f"Consumer Behavior Analysis: {domain} Products and Services",
                "url": f"https://www.consumerinsights.com/{domain.lower()}-analysis",
                "snippet": f"A comprehensive analysis of consumer preferences, pain points, and adoption patterns for {domain} products and services."
            }
        ]
        
        return mock_results[:num_results]
    
    def _mock_bing_search(self, query: str, num_results: int) -> List[Dict[str, str]]:
        """
        Mock Bing search results for testing.
        
        Args:
            query: Search query
            num_results: Number of results to return
            
        Returns:
            List of mock search results
        """
        # Similar to Brave but with different URLs and snippets
        return self._mock_brave_search(query, num_results)
    
    def _mock_serper_search(self, query: str, num_results: int) -> List[Dict[str, str]]:
        """
        Mock Serper search results for testing.
        
        Args:
            query: Search query
            num_results: Number of results to return
            
        Returns:
            List of mock search results
        """
        # Similar to Brave but with different URLs and snippets
        return self._mock_brave_search(query, num_results)
    
    def _extract_domain(self, query: str) -> str:
        """
        Extract domain from query for generating relevant mock results.
        
        Args:
            query: Search query
            
        Returns:
            Domain extracted from query
        """
        domains = ["Health", "Finance", "Education", "E-commerce", "Social"]
        
        for domain in domains:
            if domain.lower() in query.lower():
                return domain
        
        # Default domain if none found
        return "Technology"