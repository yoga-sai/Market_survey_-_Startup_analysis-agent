"""
Synthesizer Module for Market Intelligence Research Agent.

This module aggregates collected data and generates a comprehensive market report.
"""
from typing import Dict, List, Any, Optional
import json
import os

class Synthesizer:
    """
    Aggregates working memory data and generates a comprehensive market report.
    Uses LLM to synthesize structured and unstructured data into a coherent analysis.
    """
    
    def __init__(self, llm_api_key: Optional[str] = None):
        """
        Initialize the synthesizer with optional LLM API key.
        
        Args:
            llm_api_key: API key for the language model service (e.g., OpenAI)
        """
        self.llm_api_key = llm_api_key or os.environ.get("LLM_API_KEY")
    
    def synthesize(self, working_memory: Dict[str, Any], parsed_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Synthesize collected data into a comprehensive market report.
        
        Args:
            working_memory: Working memory with collected data
            parsed_input: Original parsed input
            
        Returns:
            Dictionary containing the synthesized report sections
        """
        # Extract relevant data from working memory
        competitors = working_memory["collected_data"]["competitors"]
        funding_data = working_memory["collected_data"]["funding_data"]
        web_search_results = working_memory["collected_data"]["web_search_results"]
        rag_results = working_memory["collected_data"]["rag_results"]
        
        # In a production system, this would call an LLM API with a prompt
        # For now, we'll implement a template-based approach
        
        # Generate report sections
        executive_summary = self._generate_executive_summary(parsed_input, competitors, funding_data)
        competitor_landscape = self._generate_competitor_landscape(competitors)
        funding_analysis = self._generate_funding_analysis(funding_data)
        swot_analysis = self._generate_swot_analysis(parsed_input, competitors, web_search_results)
        market_trends = self._generate_market_trends(web_search_results, rag_results)
        
        # Combine into final report
        report = {
            "executive_summary": executive_summary,
            "competitor_landscape": competitor_landscape,
            "funding_analysis": funding_analysis,
            "swot_analysis": swot_analysis,
            "market_trends": market_trends,
            "confidence_scores": self._generate_confidence_scores(working_memory)
        }
        
        return report
    
    def _generate_executive_summary(self, parsed_input: Dict[str, Any], 
                                   competitors: List[Dict[str, Any]], 
                                   funding_data: Dict[str, Any]) -> str:
        """
        Generate the executive summary section.
        
        Args:
            parsed_input: Original parsed input
            competitors: List of competitor data
            funding_data: Funding data for competitors
            
        Returns:
            Executive summary text
        """
        domain = parsed_input.get("domain", "")
        core_idea = parsed_input.get("core_idea", "")
        num_competitors = len(competitors)
        
        # Simple template-based summary
        summary = f"""
# Executive Summary

This market intelligence report analyzes the viability of a new startup in the {domain} domain. 
The core business idea is: {core_idea}.

Our analysis identified {num_competitors} established competitors in this space, with varying levels of 
funding and market penetration. The overall market shows {self._get_market_health(competitors, funding_data)} 
health, with {self._get_funding_trend(funding_data)} in recent investment activity.

Key opportunities and challenges are highlighted in the SWOT analysis, along with detailed competitor 
profiles and current market trends that may impact the success of this venture.
        """
        
        return summary.strip()
    
    def _generate_competitor_landscape(self, competitors: List[Dict[str, Any]]) -> str:
        """
        Generate the competitor landscape section.
        
        Args:
            competitors: List of competitor data
            
        Returns:
            Competitor landscape text with table
        """
        if not competitors:
            return "# Competitor Landscape\n\nNo direct competitors were identified in this market space."
        
        # Create competitor table
        table_header = "| Company | Key Features | Target Audience | USP |\n| --- | --- | --- | --- |\n"
        table_rows = ""
        
        for comp in competitors:
            name = comp.get("name", "Unknown")
            features = ", ".join(comp.get("features", ["N/A"]))
            audience = comp.get("audience", "N/A")
            usp = comp.get("usp", "N/A")
            
            table_rows += f"| {name} | {features} | {audience} | {usp} |\n"
        
        landscape = f"""
# Competitor Landscape

The following table summarizes the key competitors in this market space:

{table_header}{table_rows}

## Competitive Positioning

Based on the competitor analysis, the market shows {self._get_competition_level(competitors)} 
level of competition with {self._get_differentiation_level(competitors)} differentiation between offerings.
        """
        
        return landscape.strip()
    
    def _generate_funding_analysis(self, funding_data: Dict[str, Any]) -> str:
        """
        Generate the funding analysis section.
        
        Args:
            funding_data: Funding data for competitors
            
        Returns:
            Funding analysis text with visualization code
        """
        if not funding_data:
            return "# Funding Analysis\n\nNo funding data available for competitors in this space."
        
        # In a real implementation, this would include code to generate charts
        # For now, we'll include placeholder code
        
        funding_analysis = """
# Funding Analysis

## Investment Trends

The following chart shows the funding received by key competitors:

```python
import matplotlib.pyplot as plt
import numpy as np

# Sample data - in production this would use actual funding_data
companies = ['CompA', 'CompB', 'CompC', 'CompD']
funding = [5.2, 3.8, 7.1, 2.5]  # in millions USD

plt.figure(figsize=(10, 6))
plt.bar(companies, funding, color='skyblue')
plt.title('Competitor Funding Comparison')
plt.xlabel('Company')
plt.ylabel('Total Funding (Millions USD)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('reports/funding_chart.png')
plt.close()
```

## Funding Rounds Analysis

Recent funding activity suggests investor confidence in this market space, with an average 
of $X million raised across Y funding rounds in the past 24 months.
        """
        
        return funding_analysis.strip()
    
    def _generate_swot_analysis(self, parsed_input: Dict[str, Any],
                               competitors: List[Dict[str, Any]],
                               web_search_results: List[Dict[str, Any]]) -> str:
        """
        Generate the SWOT analysis section.
        
        Args:
            parsed_input: Original parsed input
            competitors: List of competitor data
            web_search_results: Results from web search
            
        Returns:
            SWOT analysis text
        """
        domain = parsed_input.get("domain", "")
        features = parsed_input.get("key_features", [])
        
        # In a production system, this would use an LLM to generate a proper SWOT
        # For now, we'll use a template with some basic logic
        
        swot = f"""
# SWOT Analysis

## Strengths
- {self._get_random_strength(domain, features)}
- Innovative approach to {domain} challenges
- {self._get_random_strength(domain, features)}

## Weaknesses
- New entrant in an established market
- {self._get_random_weakness(domain)}
- Potential scaling challenges in {domain} space

## Opportunities
- {self._get_random_opportunity(domain, web_search_results)}
- Underserved segments within {domain} market
- {self._get_random_opportunity(domain, web_search_results)}

## Threats
- Established competitors with market share
- {self._get_random_threat(domain, competitors)}
- Regulatory changes in {domain} industry
        """
        
        return swot.strip()
    
    def _generate_market_trends(self, web_search_results: List[Dict[str, Any]],
                               rag_results: List[Dict[str, Any]]) -> str:
        """
        Generate the market trends section.
        
        Args:
            web_search_results: Results from web search
            rag_results: Results from RAG queries
            
        Returns:
            Market trends text with citations
        """
        # In a production system, this would synthesize actual search results
        # For now, we'll use a template with placeholders
        
        trends = """
# Market Trends

## Current Trends

1. **Mobile-First Approach**: The market is increasingly shifting towards mobile-first solutions, with over 70% of users preferring mobile access. [Source: Industry Report 2023]

2. **AI Integration**: Competitors are rapidly integrating AI capabilities to enhance user experience and provide personalized recommendations. [Source: TechCrunch]

3. **Subscription Models**: Recurring revenue models are becoming the norm, with freemium offerings to drive initial adoption. [Source: Market Analysis Q2 2023]

## Emerging Opportunities

1. **International Expansion**: Several competitors are focusing on domestic markets, leaving international segments underserved.

2. **Integration Ecosystems**: Building platform capabilities that integrate with existing tools shows promising adoption rates.

3. **Specialized Features**: Niche-specific functionality addressing unique user needs represents a differentiation opportunity.
        """
        
        return trends.strip()
    
    def _generate_confidence_scores(self, working_memory: Dict[str, Any]) -> Dict[str, float]:
        """
        Generate confidence scores for different parts of the analysis.
        
        Args:
            working_memory: Working memory with collected data
            
        Returns:
            Dictionary of confidence scores
        """
        # In a real implementation, this would calculate actual confidence scores
        # For now, we'll use placeholder values
        
        return {
            "competitor_data": 0.85,
            "funding_analysis": 0.75,
            "market_trends": 0.80,
            "swot_analysis": 0.70,
            "overall_confidence": 0.78
        }
    
    # Helper methods for generating text
    
    def _get_market_health(self, competitors: List[Dict[str, Any]], funding_data: Dict[str, Any]) -> str:
        """Determine market health based on competitors and funding."""
        if len(competitors) > 5 and funding_data:
            return "strong"
        elif len(competitors) > 2:
            return "moderate"
        else:
            return "emerging"
    
    def _get_funding_trend(self, funding_data: Dict[str, Any]) -> str:
        """Determine funding trend based on funding data."""
        # Placeholder logic
        return "an upward trend"
    
    def _get_competition_level(self, competitors: List[Dict[str, Any]]) -> str:
        """Determine competition level based on number of competitors."""
        if len(competitors) > 5:
            return "a high"
        elif len(competitors) > 2:
            return "a moderate"
        else:
            return "a low"
    
    def _get_differentiation_level(self, competitors: List[Dict[str, Any]]) -> str:
        """Determine differentiation level based on competitor features."""
        # Placeholder logic
        return "significant"
    
    def _get_random_strength(self, domain: str, features: List[str]) -> str:
        """Generate a random strength based on domain and features."""
        strengths = [
            f"Unique approach to {domain} with focus on user experience",
            f"Innovative integration of {', '.join(features[:2]) if features else domain} technologies",
            f"Strong potential for network effects in {domain} space"
        ]
        import random
        return random.choice(strengths)
    
    def _get_random_weakness(self, domain: str) -> str:
        """Generate a random weakness based on domain."""
        weaknesses = [
            f"Limited initial brand recognition in {domain} market",
            f"Potential high customer acquisition costs in {domain} space",
            f"Technical complexity of implementing all planned features"
        ]
        import random
        return random.choice(weaknesses)
    
    def _get_random_opportunity(self, domain: str, web_results: List[Dict[str, Any]]) -> str:
        """Generate a random opportunity based on domain and web results."""
        opportunities = [
            f"Growing {domain} market with increasing user adoption",
            f"Untapped international markets for {domain} solutions",
            f"Integration possibilities with complementary {domain} services"
        ]
        import random
        return random.choice(opportunities)
    
    def _get_random_threat(self, domain: str, competitors: List[Dict[str, Any]]) -> str:
        """Generate a random threat based on domain and competitors."""
        threats = [
            f"Rapid technological changes in {domain} landscape",
            f"Potential for larger tech companies to enter {domain} space",
            f"Price competition from established players"
        ]
        import random
        return random.choice(threats)