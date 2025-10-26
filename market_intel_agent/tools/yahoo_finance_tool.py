"""
Yahoo Finance Tool for Market Intelligence Research Agent.

Provides stock quotes, company profile, and recent news using yfinance.
"""
from typing import Dict, Any, List, Optional

import yfinance as yf

from utils.logger import AgentLogger


class YahooFinanceTool:
    """
    Fetches finance data for a given ticker using yfinance.
    """

    def __init__(self, logger: Optional[AgentLogger] = None) -> None:
        """
        Initialize the Yahoo Finance tool.

        Args:
            logger: Optional AgentLogger instance
        """
        self.logger = logger if logger else AgentLogger()

    def get_quote(self, ticker: str) -> Dict[str, Any]:
        """
        Get a quick quote for a ticker (price, currency, market cap).

        Args:
            ticker: Stock ticker symbol (e.g., "AAPL")

        Returns:
            Dictionary with basic quote information
        """
        try:
            t = yf.Ticker(ticker)
            fast_info = getattr(t, "fast_info", {}) or {}
            price = fast_info.get("last_price") or fast_info.get("last_trade_price")
            currency = fast_info.get("currency")
            market_cap = fast_info.get("market_cap")

            if price is None:
                hist = t.history(period="1d")
                if not hist.empty:
                    price = float(hist["Close"].iloc[-1])

            data = {
                "symbol": ticker,
                "price": float(price) if price is not None else None,
                "currency": currency,
                "market_cap": market_cap,
            }
            self.logger.log_debug(f"YahooFinanceTool.get_quote({ticker}) -> {data}")
            return data
        except Exception as e:
            self.logger.log_error(f"Error fetching quote for {ticker}: {e}")
            return {}

    def get_company_profile(self, ticker: str) -> Dict[str, Any]:
        """
        Get company profile details (name, sector, industry, website, summary).

        Args:
            ticker: Stock ticker symbol

        Returns:
            Dictionary with company profile information
        """
        try:
            t = yf.Ticker(ticker)
            info: Dict[str, Any] = {}
            try:
                info = t.get_info()  # preferred over .info in newer yfinance
            except Exception as ie:
                self.logger.log_debug(f"get_info failed for {ticker}: {ie}")

            profile = {
                "symbol": ticker,
                "name": info.get("longName") or info.get("shortName"),
                "sector": info.get("sector"),
                "industry": info.get("industry"),
                "website": info.get("website"),
                "summary": info.get("longBusinessSummary"),
            }
            self.logger.log_debug(f"YahooFinanceTool.get_company_profile({ticker}) -> {profile}")
            return profile
        except Exception as e:
            self.logger.log_error(f"Error fetching profile for {ticker}: {e}")
            return {}

    def get_news(self, ticker: str, count: int = 5) -> List[Dict[str, Any]]:
        """
        Get recent news articles for a ticker.

        Args:
            ticker: Stock ticker symbol
            count: Max number of articles to return

        Returns:
            List of news dictionaries with title, publisher, link, and timestamp
        """
        try:
            t = yf.Ticker(ticker)
            news_list = getattr(t, "news", []) or []
            results: List[Dict[str, Any]] = []
            for item in news_list[:count]:
                results.append({
                    "title": item.get("title"),
                    "publisher": item.get("publisher"),
                    "link": item.get("link") or item.get("url"),
                    "published": item.get("providerPublishTime") or item.get("pubDate"),
                })
            self.logger.log_debug(f"YahooFinanceTool.get_news({ticker}, count={count}) -> {len(results)} items")
            return results
        except Exception as e:
            self.logger.log_error(f"Error fetching news for {ticker}: {e}")
            return []