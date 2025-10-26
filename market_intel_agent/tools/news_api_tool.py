import requests
import json
from datetime import datetime, timedelta
import yaml
import os
from typing import Dict, List, Optional, Any

class NewsAPITool:
    """
    Tool for retrieving real-time news using the NewsAPI service.
    Allows querying by keywords, company names, domains, and time ranges.
    """
    
    def __init__(self, api_key: str = None, config_path: str = None):
        """
        Initialize the NewsAPI tool with API key.
        
        Args:
            api_key: NewsAPI API key
            config_path: Path to config file containing API key
        """
        self.base_url = "https://newsapi.org/v2/everything"
        
        # Load API key from config if not provided directly
        if api_key is None and config_path is not None:
            try:
                with open(config_path, 'r') as file:
                    config = yaml.safe_load(file)
                    api_key = config.get('newsapi_key')
            except Exception as e:
                print(f"Error loading NewsAPI key from config: {e}")
        
        self.api_key = api_key
        
        # For testing without API key
        self.mock_mode = api_key is None or api_key == "YOUR_NEWSAPI_KEY"
        if self.mock_mode:
            print("NewsAPI running in mock mode - will return sample data")
    
    def get_news(self, 
                query: str, 
                days: int = 30, 
                language: str = "en", 
                sort_by: str = "relevancy",
                page_size: int = 10) -> Dict[str, Any]:
        """
        Retrieve news articles based on query and parameters.
        
        Args:
            query: Search query (company name, domain, keywords)
            days: Number of days to look back
            language: Language of articles (default: English)
            sort_by: Sorting method (relevancy, popularity, publishedAt)
            page_size: Number of results to return
            
        Returns:
            Dictionary containing news articles and metadata
        """
        if self.mock_mode:
            return self._get_mock_news(query, days)
        
        # Calculate date range
        to_date = datetime.now().strftime('%Y-%m-%d')
        from_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        # Prepare request parameters
        params = {
            'q': query,
            'from': from_date,
            'to': to_date,
            'language': language,
            'sortBy': sort_by,
            'pageSize': page_size,
            'apiKey': self.api_key
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching news: {e}")
            return {
                "status": "error",
                "message": str(e),
                "articles": []
            }
    
    def get_company_news(self, company_name: str, days: int = 30) -> Dict[str, Any]:
        """
        Specialized method to get news about a specific company.
        
        Args:
            company_name: Name of the company
            days: Number of days to look back
            
        Returns:
            Dictionary containing news articles about the company
        """
        # Create a more targeted query for company news
        query = f'"{company_name}" OR "{company_name} company" OR "{company_name} startup"'
        return self.get_news(query, days=days, sort_by="relevancy")
    
    def get_domain_news(self, domain: str, days: int = 30) -> Dict[str, Any]:
        """
        Get news related to a specific business domain or industry.
        
        Args:
            domain: Business domain or industry
            days: Number of days to look back
            
        Returns:
            Dictionary containing news articles about the domain
        """
        # Create a more targeted query for domain news
        query = f'"{domain}" OR "{domain} industry" OR "{domain} market" OR "{domain} trends"'
        return self.get_news(query, days=days, sort_by="relevancy")
    
    def format_news_for_report(self, news_data: Dict[str, Any], max_articles: int = 5) -> List[Dict[str, str]]:
        """
        Format news data for inclusion in the market intelligence report.
        
        Args:
            news_data: News data from the API
            max_articles: Maximum number of articles to include
            
        Returns:
            List of formatted news articles with title, source, date, and URL
        """
        formatted_news = []
        
        if news_data.get("status") == "ok":
            articles = news_data.get("articles", [])
            
            for article in articles[:max_articles]:
                # Parse and format the publication date
                pub_date = article.get("publishedAt", "")
                if pub_date:
                    try:
                        date_obj = datetime.strptime(pub_date, "%Y-%m-%dT%H:%M:%SZ")
                        formatted_date = date_obj.strftime("%b %Y")
                    except ValueError:
                        formatted_date = pub_date
                else:
                    formatted_date = "Unknown date"
                
                formatted_news.append({
                    "title": article.get("title", "Untitled"),
                    "source": article.get("source", {}).get("name", "Unknown source"),
                    "date": formatted_date,
                    "url": article.get("url", "")
                })
        
        return formatted_news
    
    def _get_mock_news(self, query: str, days: int) -> Dict[str, Any]:
        """
        Generate mock news data for testing without API key.
        
        Args:
            query: Search query
            days: Number of days to look back
            
        Returns:
            Mock news data
        """
        # Extract main keywords from query
        keywords = [kw.strip('"') for kw in query.split() if len(kw) > 3]
        main_keyword = keywords[0] if keywords else "startup"
        
        # Generate mock articles based on query
        mock_articles = [
            {
                "source": {"id": "techcrunch", "name": "TechCrunch"},
                "author": "John Smith",
                "title": f"{main_keyword.capitalize()} startup raises $15M in Series A funding",
                "description": f"A promising {main_keyword} startup has secured significant funding to expand operations.",
                "url": "https://techcrunch.com/2025/10/15/startup-funding",
                "urlToImage": "https://example.com/image1.jpg",
                "publishedAt": (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "content": f"The {main_keyword} market is heating up with this latest funding round..."
            },
            {
                "source": {"id": "economic-times", "name": "Economic Times"},
                "author": "Priya Sharma",
                "title": f"Indian {main_keyword} market expected to grow 30% by 2026",
                "description": f"Industry analysts predict significant growth in the {main_keyword} sector over the next year.",
                "url": "https://economictimes.com/2025/10/10/market-growth",
                "urlToImage": "https://example.com/image2.jpg",
                "publishedAt": (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "content": f"The {main_keyword} industry in India is showing remarkable growth potential..."
            },
            {
                "source": {"id": "yourstory", "name": "YourStory"},
                "author": "Rahul Mehta",
                "title": f"Top 5 {main_keyword} startups to watch in 2025",
                "description": f"These innovative {main_keyword} companies are disrupting the market with new technologies.",
                "url": "https://yourstory.com/2025/10/05/top-startups",
                "urlToImage": "https://example.com/image3.jpg",
                "publishedAt": (datetime.now() - timedelta(days=15)).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "content": f"The {main_keyword} landscape is evolving rapidly with these innovative players..."
            },
            {
                "source": {"id": "forbes", "name": "Forbes"},
                "author": "Michael Johnson",
                "title": f"How AI is transforming the {main_keyword} industry",
                "description": f"Artificial intelligence is creating new opportunities in the {main_keyword} sector.",
                "url": "https://forbes.com/2025/09/28/ai-transformation",
                "urlToImage": "https://example.com/image4.jpg",
                "publishedAt": (datetime.now() - timedelta(days=22)).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "content": f"AI technologies are revolutionizing how {main_keyword} companies operate..."
            },
            {
                "source": {"id": "inc42", "name": "Inc42"},
                "author": "Ananya Patel",
                "title": f"Government announces new policies to support {main_keyword} startups",
                "description": f"New regulatory framework aims to boost innovation in the {main_keyword} sector.",
                "url": "https://inc42.com/2025/09/20/government-policy",
                "urlToImage": "https://example.com/image5.jpg",
                "publishedAt": (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "content": f"The new policy framework is expected to significantly benefit {main_keyword} startups..."
            }
        ]
        
        return {
            "status": "ok",
            "totalResults": len(mock_articles),
            "articles": mock_articles
        }