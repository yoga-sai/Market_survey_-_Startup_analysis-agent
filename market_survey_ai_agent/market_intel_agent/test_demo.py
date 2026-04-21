"""
Demo Test Script for Market Intelligence Research Agent

This script demonstrates the functionality of the Market Intelligence Research Agent
without requiring external dependencies.
"""
import os
import json
from datetime import datetime

def simulate_workflow(idea):
    """Simulate the workflow of the Market Intelligence Research Agent."""
    print(f"Starting Market Intelligence Research Agent with idea: {idea}")
    
    # Simulate parsing input
    print("\n[1] Parsing input...")
    parsed_input = {
        "core_idea": "Menstrual health app with AI prediction",
        "domain": "Health Tech",
        "niche": "Women's Health",
        "key_features": ["AI-driven cycle prediction", "Community features", "Health tracking"],
        "target_audience": "Women of reproductive age"
    }
    print(f"Parsed input: {json.dumps(parsed_input, indent=2)}")
    
    # Simulate reasoning loop
    print("\n[2] Running reasoning loop...")
    print("  - Thought: Need to find competitors in the women's health tech space")
    print("  - Action: Using CompetitorFinder tool")
    print("  - Observation: Found 5 competitors including Flo, Clue, and Eve")
    
    print("  - Thought: Need funding data for these competitors")
    print("  - Action: Using FundingRetriever tool")
    print("  - Observation: Retrieved funding data for all 5 competitors")
    
    print("  - Thought: Need market trends in femtech")
    print("  - Action: Using WebSearchTool")
    print("  - Observation: Found articles about femtech market growth")
    
    print("  - Thought: Need specific information about AI in health apps")
    print("  - Action: Using RAGQueryTool")
    print("  - Observation: Retrieved information about AI in health tech")
    
    # Simulate data collection
    collected_data = {
        "competitors": [
            {"name": "Flo", "features": ["Period tracking", "AI predictions", "Community"], "funding": "$50M"},
            {"name": "Clue", "features": ["Cycle tracking", "Health insights", "Data-driven"], "funding": "$30M"},
            {"name": "Eve", "features": ["Period tracking", "Community", "Content"], "funding": "$12M"},
            {"name": "Glow", "features": ["Fertility", "Period tracking", "Premium features"], "funding": "$23M"},
            {"name": "Ovia", "features": ["Fertility", "Pregnancy", "Parenting"], "funding": "$17M"}
        ],
        "market_trends": [
            "The femtech market is projected to reach $50 billion by 2025",
            "AI-driven health apps show 40% better user retention",
            "Community features increase engagement by 65% in health apps",
            "Privacy concerns are a major factor in women's health app selection",
            "Integration with wearables is becoming a standard feature"
        ],
        "funding_data": {
            "total_funding": "$132M",
            "average_round": "$26.4M",
            "top_investor": "Female Founders Fund"
        }
    }
    
    # Simulate report synthesis
    print("\n[3] Synthesizing report...")
    
    # Create output directory if it doesn't exist
    output_dir = "reports/generated_reports"
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate report filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"health_tech_{timestamp}_report"
    
    # Simulate report generation
    report_md = f"""# Market Intelligence Report: {parsed_input['domain']}

## Executive Summary

This report analyzes the market landscape for a menstrual health app with AI-driven cycle prediction and community features. The femtech market is growing rapidly, with projections reaching $50 billion by 2025. Key competitors include Flo, Clue, and Eve, with total funding in the space exceeding $132M.

## Competitor Landscape

| Company | Key Features | Funding |
|---------|-------------|---------|
| Flo | Period tracking, AI predictions, Community | $50M |
| Clue | Cycle tracking, Health insights, Data-driven | $30M |
| Eve | Period tracking, Community, Content | $12M |
| Glow | Fertility, Period tracking, Premium features | $23M |
| Ovia | Fertility, Pregnancy, Parenting | $17M |

## Funding Analysis

The total funding in the menstrual health app space is approximately $132M, with an average funding round of $26.4M. The top investor in this space is Female Founders Fund.

## SWOT Analysis

### Strengths
- AI-driven prediction offers technological advantage
- Community features increase user engagement
- Focused niche in growing femtech market

### Weaknesses
- Crowded market with established competitors
- High development costs for AI features
- Privacy concerns with sensitive health data

### Opportunities
- Growing femtech market ($50B by 2025)
- Integration with wearable devices
- Expansion into broader women's health

### Threats
- Privacy regulations and compliance
- Competition from well-funded players
- User trust concerns with health data

## Market Trends

1. The femtech market is projected to reach $50 billion by 2025
2. AI-driven health apps show 40% better user retention
3. Community features increase engagement by 65% in health apps
4. Privacy concerns are a major factor in women's health app selection
5. Integration with wearables is becoming a standard feature

## Confidence Appendix

| Information Source | Confidence Score |
|-------------------|------------------|
| Competitor Data | 0.90 |
| Funding Information | 0.85 |
| Market Trends | 0.75 |
| AI Technology Assessment | 0.80 |
"""
    
    # Save report
    with open(os.path.join(output_dir, f"{report_filename}.md"), 'w') as f:
        f.write(report_md)
    
    print(f"\nMarket Intelligence Report generated successfully!")
    print(f"Report saved to: {os.path.abspath(os.path.join(output_dir, f'{report_filename}.md'))}")
    
    return report_filename

if __name__ == "__main__":
    idea = "We are building a menstrual health app with AI-driven cycle prediction and community features."
    report_file = simulate_workflow(idea)