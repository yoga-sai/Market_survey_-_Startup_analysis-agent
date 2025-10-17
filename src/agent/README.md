# Market Analyst Agent

A ReAct (Reasoning and Acting) + RAG (Retrieval-Augmented Generation) agent that analyzes startup ideas and generates comprehensive market reports.

## Features

- **Input Parsing**: Extracts structured data from free-text startup ideas
- **Competitor Analysis**: Identifies similar companies with similarity scores
- **Funding Landscape**: Shows funding rounds and amounts for competitors
- **Market Trends**: Gathers recent industry trends
- **SWOT Analysis**: Provides strategic insights
- **Report Generation**: Creates formatted markdown reports

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Agent

```bash
python run_agent.py "Your startup idea description here"
```

### Examples

```bash
# Logistics optimization platform
python run_agent.py "An AI-powered logistics optimization platform for small e-commerce businesses"

# Blockchain supply chain
python run_agent.py "A blockchain-based supply chain transparency platform for pharmaceutical companies"

# Healthcare AI
python run_agent.py "An AI-powered diagnostic tool for early cancer detection in rural clinics"
```

## Output

The agent generates a comprehensive market analysis report including:

- **Executive Summary**: Overview of business domain and value proposition
- **Competitor Analysis**: Table of similar companies with similarity scores
- **Funding Landscape**: Funding rounds and amounts for competitors
- **SWOT Analysis**: Strengths, Weaknesses, Opportunities, and Threats
- **Market Trends**: Recent industry trends and news
- **Citations**: Sources for the information gathered

## Sample Output

```
Market Analyst Agent
==================================================
Analyzing: An AI-powered logistics optimization platform for small e-commerce businesses
==================================================
Parsed: Logistics Tech targeting small e-commerce
ReAct analysis completed
Report generated

==================================================
# Executive Summary

This report analyzes a startup in Logistics Tech targeting small e-commerce. The core value proposition centers on optimization.

## Competitor Analysis

| Company | Similarity | Category |
|---|---:|---|
| ShipEase | 0.850 | Logistics Tech |
| RouteIQ | 0.780 | Logistics Tech |
| Packly | 0.720 | Logistics Tech |

## Funding Landscape

| Company | Round | Amount | Date |
|---|---|---:|---|
| ShipEase | Seed | 2500000 | 2023-06-01 |
| ShipEase | Series A | 12000000 | 2024-02-15 |
| RouteIQ | Seed | 1800000 | 2023-08-20 |

## SWOT Analysis

- Strength: AI-driven approach and semantic retrieval enable grounded insights.
- Weakness: Coverage depends on available indexed data; may miss private info.
- Opportunity: Partnerships with data providers; expand to telehealth or B2B.
- Threat: Incumbents with strong brand and proprietary datasets.

## Market Trends

- Retailers embrace AI for logistics efficiency — SMB e-commerce adopt AI routing tools (TechCrunch)
- Warehouse automation trends 2025 — Vision systems and robotics reduce packing time (TechRadar)

## Citations

- https://example.com/shipease
- https://example.com/routeiq
- https://example.com/news1
```

## Architecture

The agent follows a ReAct (Reasoning and Acting) pattern:

1. **Input Parser**: Extracts structured data from free-text ideas
2. **ReAct Engine**: Performs reasoning and actions to gather data
3. **Synthesizer**: Combines all data into a formatted report

## Current Status

This is a **prototype/demo** version with:
- Hardcoded competitor and funding data (not real-time)
- Mock market trends
- Basic heuristic parsing as fallback
- Empty `tools/` and `rag/` directories (for future expansion)

## Future Enhancements

To make this fully functional, you would need to:
1. Implement real tools in the `tools/` directory
2. Add RAG capabilities in the `rag/` directory
3. Connect to real data sources for competitors and funding
4. Add proper error handling and configuration
5. Integrate with real APIs for market data

## Dependencies

- `pydantic>=2.0.0` - Data validation and settings
- `openai>=1.0.0` - Optional LLM integration for enhanced parsing

## License

This project is for demonstration purposes.
