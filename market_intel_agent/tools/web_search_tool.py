"""
Web Search Tool for Market Intelligence Research Agent.

This tool performs web searches using the Serper API.
"""
import os
import json
import requests
from typing import List, Dict, Any, Optional
from utils.logger import AgentLogger

class WebSearchTool:
    """
    Performs web searches using the Serper API.
    """
    
    def __init__(self, api_key: Optional[str] = None, search_engine: str = "serper", logger: AgentLogger = None):
        """
        Initialize the web search tool.
        
        Args:
            api_key: API key for Serper
            search_engine: Should be "serper" (kept for backward compatibility)
            logger: Logger instance
        """
        self.api_key = api_key or os.environ.get("SERPER_API_KEY")
        self.logger = logger if logger else AgentLogger()
        
    def search(self, query: str, num_results: int = 5) -> List[Dict[str, str]]:
        """
        Perform a web search with the given query using Serper API.
        
        Args:
            query: Search query
            num_results: Number of results to return
            
        Returns:
            List of search result dictionaries
        """
        return self._serper_search(query, num_results)
    

    
    def _serper_search(self, query: str, num_results: int) -> List[Dict[str, str]]:
        """
        Perform a real Serper search.
        
        Args:
            query: Search query
            num_results: Number of results to return
            
        Returns:
            List of search result dictionaries
        """
        if not self.api_key:
            raise ValueError("Serper API key is not provided.")

        url = "https://google.serper.dev/search"
        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "q": query,
            "num": num_results
        }

        try:
            self.logger.log_debug(f"Serper API URL: {url}")
            self.logger.log_debug(f"Serper API Headers: {headers}")
            self.logger.log_debug(f"Serper API Payload: {payload}")
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=10
            )
            self.logger.log_debug(f"Serper API Response Status: {response.status_code}")
            response.raise_for_status()
            self.logger.log_debug(f"Serper API Response Body: {response.text}")
            with open("serper_response.json", "w") as f:
                f.write(response.text)
            search_results = response.json()
            
            # Extract relevant information
            results = []
            if "organic_results" in search_results:
                for item in search_results["organic_results"]:
                    results.append({
                        "title": item.get("title", ""),
                        "url": item.get("link", ""),
                        "snippet": item.get("snippet", "")
                    })
            return results
        except requests.exceptions.RequestException as e:
            print(f"Error during Serper API call: {e}")
            return []
    
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