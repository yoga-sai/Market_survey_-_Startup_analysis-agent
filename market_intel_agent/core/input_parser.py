"""
Input Parser Module for Market Intelligence Research Agent.

This module is responsible for parsing user input (startup idea) into structured JSON format.
"""
import json
import os
from typing import Dict, List, Any, Optional

class IntelligentInputParser:
    """
    Parses plain-English startup idea into structured JSON format.
    Uses semantic parsing to extract key components of the business idea.
    """
    
    def __init__(self, llm_api_key: Optional[str] = None):
        """
        Initialize the parser with optional LLM API key.
        
        Args:
            llm_api_key: API key for the language model service (e.g., OpenAI)
        """
        self.llm_api_key = llm_api_key or os.environ.get("LLM_API_KEY")
        
    def parse(self, idea_text: str) -> Dict[str, Any]:
        """
        Parse the startup idea text into structured JSON.
        
        Args:
            idea_text: Plain-English description of the startup idea
            
        Returns:
            Dict containing structured information about the startup idea
        """
        # In a production system, this would call an LLM API
        # For now, we'll implement a simple rule-based parser
        
        # Example implementation (to be replaced with actual LLM call)
        parsed_data = self._simple_parse(idea_text)
        
        # Validate the parsed data
        self._validate_parsed_data(parsed_data)
        
        return parsed_data
    
    def _simple_parse(self, idea_text: str) -> Dict[str, Any]:
        """
        Simple rule-based parsing for demonstration purposes.
        In production, this would be replaced with an LLM call.
        
        Args:
            idea_text: Plain-English description of the startup idea
            
        Returns:
            Dict containing structured information about the startup idea
        """
        # Default structure
        parsed_data = {
            "core_idea": "",
            "domain": "",
            "niche": "",
            "key_features": [],
            "target_audience": ""
        }
        
        # Extract domain (simple keyword matching)
        domains = {
            "health": ["health", "medical", "wellness", "fitness", "menstrual"],
            "finance": ["finance", "banking", "investment", "money", "payment", "fintech", "stock trading", "trading", "stocks"],
            "education": ["education", "learning", "teaching", "school", "course"],
            "e-commerce": ["e-commerce", "shop", "retail", "store", "marketplace"],
            "social": ["social", "community", "network", "connect", "share"]
        }
        
        # Find domain based on keywords
        for domain, keywords in domains.items():
            if any(keyword in idea_text.lower() for keyword in keywords):
                parsed_data["domain"] = domain
                break
        
        # Extract core idea (first sentence)
        sentences = idea_text.split('.')
        if sentences:
            parsed_data["core_idea"] = sentences[0].strip()
        
        # Extract key features (look for words after "with" or "features")
        if "with" in idea_text:
            features_text = idea_text.split("with")[1]
            features = [f.strip() for f in features_text.split("and")]
            parsed_data["key_features"] = features
        
        # In a real implementation, we would use more sophisticated NLP techniques
        # or call an LLM API for better extraction
        
        return parsed_data
    
    def _validate_parsed_data(self, data: Dict[str, Any]) -> None:
        """
        Validate that the parsed data contains all required fields.
        
        Args:
            data: Parsed data dictionary to validate
            
        Raises:
            ValueError: If required fields are missing
        """
        required_fields = ["core_idea", "domain"]
        
        for field in required_fields:
            if not data.get(field):
                raise ValueError(f"Required field '{field}' is missing or empty")
    
    def to_json(self, parsed_data: Dict[str, Any]) -> str:
        """
        Convert parsed data to JSON string.
        
        Args:
            parsed_data: Dictionary containing parsed data
            
        Returns:
            JSON string representation of the parsed data
        """
        return json.dumps(parsed_data, indent=2)