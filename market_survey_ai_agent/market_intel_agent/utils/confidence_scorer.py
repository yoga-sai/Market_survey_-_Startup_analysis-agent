"""
Confidence Scorer utility for Market Intelligence Research Agent.

This module provides functionality for scoring the confidence of information sources.
"""
from typing import Dict, List, Any, Optional

class ConfidenceScorer:
    """
    Scores the confidence of information sources used in market intelligence reports.
    """
    
    def __init__(self):
        """Initialize the confidence scorer with default source weights."""
        # Default confidence weights for different source types
        self.source_weights = {
            "dataset": 0.9,  # Structured data from datasets
            "rag": 0.8,      # Information from RAG system
            "web_search": {
                "news": 0.7,      # News articles
                "research": 0.85,  # Research papers/reports
                "blog": 0.6,      # Blog posts
                "forum": 0.5,     # Forum discussions
                "social": 0.4     # Social media
            }
        }
        
    def score_source(self, source_type: str, source_subtype: Optional[str] = None) -> float:
        """
        Score the confidence of a source.
        
        Args:
            source_type: Type of source (dataset, rag, web_search)
            source_subtype: Subtype of source (for web_search)
            
        Returns:
            Confidence score between 0 and 1
        """
        if source_type == "web_search" and source_subtype:
            return self.source_weights.get("web_search", {}).get(source_subtype, 0.5)
        else:
            return self.source_weights.get(source_type, 0.5)
        
    def score_competitor_data(self, competitor_data: Dict[str, Any]) -> float:
        """
        Score the confidence of competitor data.
        
        Args:
            competitor_data: Competitor data dictionary
            
        Returns:
            Confidence score between 0 and 1
        """
        # For now, all dataset-based competitor data has the same confidence
        return self.score_source("dataset")
        
    def score_funding_data(self, funding_data: Dict[str, Any]) -> float:
        """
        Score the confidence of funding data.
        
        Args:
            funding_data: Funding data dictionary
            
        Returns:
            Confidence score between 0 and 1
        """
        # For now, all dataset-based funding data has the same confidence
        return self.score_source("dataset")
        
    def score_web_result(self, web_result: Dict[str, Any]) -> float:
        """
        Score the confidence of a web search result.
        
        Args:
            web_result: Web search result dictionary
            
        Returns:
            Confidence score between 0 and 1
        """
        # Determine the subtype based on URL or content
        url = web_result.get("url", "").lower()
        
        if "news" in url or "article" in url:
            subtype = "news"
        elif "research" in url or "paper" in url or "report" in url:
            subtype = "research"
        elif "blog" in url:
            subtype = "blog"
        elif "forum" in url or "discussion" in url:
            subtype = "forum"
        elif "twitter" in url or "facebook" in url or "linkedin" in url:
            subtype = "social"
        else:
            subtype = "news"  # Default to news
            
        return self.score_source("web_search", subtype)
        
    def score_rag_result(self, rag_result: Dict[str, Any]) -> float:
        """
        Score the confidence of a RAG result.
        
        Args:
            rag_result: RAG result dictionary
            
        Returns:
            Confidence score between 0 and 1
        """
        # Base confidence on RAG similarity score if available
        base_confidence = self.score_source("rag")
        similarity = rag_result.get("similarity", 0.0)
        
        # Adjust confidence based on similarity
        return base_confidence * similarity