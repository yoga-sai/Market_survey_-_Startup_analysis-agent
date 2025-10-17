# -*- coding: utf-8 -*-
"""
Market Analyst Agent - Command Line Interface
Usage: python run_agent.py "Your startup idea description"
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from schemas import ParsedInput, ReportSection, Report

# Simple implementations
class InputParser:
    def parse(self, text: str) -> ParsedInput:
        text_norm = text.strip()
        lower = text.lower()
        
        # Extract technologies
        techs = []
        tech_keywords = {
            "ai": "AI", "artificial intelligence": "AI", "machine learning": "ML", "ml": "ML",
            "blockchain": "Blockchain", "computer vision": "Computer Vision", "cv": "Computer Vision",
            "nlp": "NLP", "natural language processing": "NLP", "llm": "LLM", "large language model": "LLM",
            "deep learning": "Deep Learning", "neural network": "Neural Networks", "gpu": "GPU Computing",
            "quantum": "Quantum Computing", "robotics": "Robotics", "iot": "IoT", "internet of things": "IoT"
        }
        for keyword, tech in tech_keywords.items():
            if keyword in lower and tech not in techs:
                techs.append(tech)
        
        # Determine business domain
        domain = "General Tech"
        domain_keywords = {
            "logistic": "Logistics Tech", "supply chain": "Logistics Tech", "delivery": "Logistics Tech",
            "shipping": "Logistics Tech", "warehouse": "Logistics Tech", "inventory": "Logistics Tech",
            "chip": "Semiconductor Tech", "semiconductor": "Semiconductor Tech", "processor": "Semiconductor Tech",
            "cpu": "Semiconductor Tech", "gpu": "Semiconductor Tech", "asic": "Semiconductor Tech",
            "healthcare": "Healthcare Tech", "medical": "Healthcare Tech", "diagnostic": "Healthcare Tech",
            "pharma": "Pharmaceutical Tech", "drug": "Pharmaceutical Tech", "medicine": "Healthcare Tech",
            "fintech": "FinTech", "financial": "FinTech", "payment": "FinTech", "banking": "FinTech",
            "edtech": "EdTech", "education": "EdTech", "learning": "EdTech", "training": "EdTech",
            "cybersecurity": "Cybersecurity", "security": "Cybersecurity", "privacy": "Cybersecurity",
            "automotive": "Automotive Tech", "autonomous": "Automotive Tech", "self-driving": "Automotive Tech"
        }
        for keyword, domain_name in domain_keywords.items():
            if keyword in lower:
                domain = domain_name
                break
        
        # Determine target audience
        audience = "B2B/B2C"
        if any(k in lower for k in ["small business", "sme", "startup", "e-commerce", "ecommerce"]):
            audience = "Small Business/SME"
        elif any(k in lower for k in ["enterprise", "corporate", "b2b"]):
            audience = "Enterprise/B2B"
        elif any(k in lower for k in ["consumer", "b2c", "individual"]):
            audience = "Consumer/B2C"
        
        # Determine value proposition
        value_prop = "insights"
        if any(k in lower for k in ["optimiz", "efficien", "cost"]):
            value_prop = "optimization"
        elif any(k in lower for k in ["autom", "streamline", "reduce"]):
            value_prop = "automation"
        elif any(k in lower for k in ["security", "protect", "secure"]):
            value_prop = "security"
        elif any(k in lower for k in ["design", "create", "build"]):
            value_prop = "design/creation"
        
        return ParsedInput(
            businessDomain=domain,
            targetAudience=audience,
            keyTechnologies=techs or ["AI"],
            valueProposition=value_prop,
            originalText=text,
        )

class ReActEngine:
    def run(self, parsed: ParsedInput) -> dict:
        domain = parsed.businessDomain
        
        # Domain-specific competitor data
        competitor_data = {
            "Semiconductor Tech": [
                {"company": "Cerebras Systems", "similarity": 0.92, "category": "AI Chip Design"},
                {"company": "Graphcore", "similarity": 0.88, "category": "AI Processors"},
                {"company": "SambaNova", "similarity": 0.85, "category": "AI Hardware"},
                {"company": "Groq", "similarity": 0.82, "category": "AI Inference Chips"}
            ],
            "Logistics Tech": [
                {"company": "ShipEase", "similarity": 0.85, "category": "Logistics Tech"},
                {"company": "RouteIQ", "similarity": 0.78, "category": "Logistics Tech"},
                {"company": "Packly", "similarity": 0.72, "category": "Logistics Tech"}
            ],
            "Healthcare Tech": [
                {"company": "PathAI", "similarity": 0.90, "category": "AI Diagnostics"},
                {"company": "Tempus", "similarity": 0.85, "category": "Precision Medicine"},
                {"company": "Butterfly Network", "similarity": 0.80, "category": "Medical Imaging"}
            ],
            "FinTech": [
                {"company": "Stripe", "similarity": 0.88, "category": "Payment Processing"},
                {"company": "Plaid", "similarity": 0.85, "category": "Financial Data"},
                {"company": "Chime", "similarity": 0.82, "category": "Digital Banking"}
            ]
        }
        
        # Domain-specific funding data
        funding_data = {
            "Semiconductor Tech": [
                {"company": "Cerebras Systems", "round": "Series F", "amount": 250000000, "date": "2023-11-01"},
                {"company": "Graphcore", "round": "Series E", "amount": 222000000, "date": "2022-12-15"},
                {"company": "SambaNova", "round": "Series D", "amount": 676000000, "date": "2021-04-13"},
                {"company": "Groq", "round": "Series C", "amount": 300000000, "date": "2021-10-20"}
            ],
            "Logistics Tech": [
                {"company": "ShipEase", "round": "Seed", "amount": 2500000, "date": "2023-06-01"},
                {"company": "ShipEase", "round": "Series A", "amount": 12000000, "date": "2024-02-15"},
                {"company": "RouteIQ", "round": "Seed", "amount": 1800000, "date": "2023-08-20"}
            ],
            "Healthcare Tech": [
                {"company": "PathAI", "round": "Series C", "amount": 165000000, "date": "2021-09-15"},
                {"company": "Tempus", "round": "Series G", "amount": 200000000, "date": "2022-05-10"},
                {"company": "Butterfly Network", "round": "Series D", "amount": 250000000, "date": "2021-01-20"}
            ],
            "FinTech": [
                {"company": "Stripe", "round": "Series H", "amount": 6000000000, "date": "2021-03-15"},
                {"company": "Plaid", "round": "Series D", "amount": 425000000, "date": "2021-04-07"},
                {"company": "Chime", "round": "Series G", "amount": 1000000000, "date": "2021-08-12"}
            ]
        }
        
        # Domain-specific trends
        trends_data = {
            "Semiconductor Tech": [
                {"title": "AI chip market reaches $50B by 2025", "summary": "Growing demand for specialized AI processors drives semiconductor innovation", "source": "Semiconductor Today"},
                {"title": "Chip design automation with AI", "summary": "Machine learning accelerates chip design and verification processes", "source": "EE Times"},
                {"title": "Edge AI chips for IoT devices", "summary": "Low-power AI processors enable smart edge computing applications", "source": "TechCrunch"}
            ],
            "Logistics Tech": [
                {"title": "Retailers embrace AI for logistics efficiency", "summary": "SMB e-commerce adopt AI routing tools", "source": "TechCrunch"},
                {"title": "Warehouse automation trends 2025", "summary": "Vision systems and robotics reduce packing time", "source": "TechRadar"}
            ],
            "Healthcare Tech": [
                {"title": "AI diagnostics market grows 40% annually", "summary": "Machine learning improves accuracy in medical imaging and pathology", "source": "Healthcare IT News"},
                {"title": "Digital therapeutics gain FDA approval", "summary": "Software-based treatments become mainstream in healthcare", "source": "MedTech Dive"}
            ],
            "FinTech": [
                {"title": "Embedded finance reaches $7T market", "summary": "Financial services integration into non-financial platforms", "source": "FinTech Magazine"},
                {"title": "AI fraud detection saves billions", "summary": "Machine learning prevents financial crimes and reduces false positives", "source": "American Banker"}
            ]
        }
        
        # Get domain-specific data or default to General Tech
        competitors = competitor_data.get(domain, [
            {"company": "TechCorp", "similarity": 0.75, "category": "General Tech"},
            {"company": "InnovateLabs", "similarity": 0.70, "category": "General Tech"}
        ])
        
        funding = funding_data.get(domain, [
            {"company": "TechCorp", "round": "Series A", "amount": 5000000, "date": "2023-01-01"},
            {"company": "InnovateLabs", "round": "Seed", "amount": 2000000, "date": "2023-06-01"}
        ])
        
        trends = trends_data.get(domain, [
            {"title": "AI adoption accelerates across industries", "summary": "Companies invest heavily in AI infrastructure and talent", "source": "TechCrunch"},
            {"title": "Digital transformation trends 2025", "summary": "Cloud-first strategies and automation drive business growth", "source": "Forbes"}
        ])
        
        return {
            "competitors": competitors,
            "funding": funding,
            "trends": trends,
            "citations": [f"https://example.com/{domain.lower().replace(' ', '-')}-market", 
                         f"https://example.com/{domain.lower().replace(' ', '-')}-trends"],
        }

class Synthesizer:
    def synthesize(self, parsed, intermediate: dict) -> Report:
        exec_sum = ReportSection(
            title="Executive Summary",
            content_md=f"This report analyzes a startup in {parsed.businessDomain} targeting {parsed.targetAudience}. The core value proposition centers on {parsed.valueProposition}.\n",
        )

        competitors = intermediate.get("competitors", [])
        comp_md_lines = ["| Company | Similarity | Category |", "|---|---:|---|"]
        for c in competitors:
            comp_md_lines.append(f"| {c.get('company','?')} | {c.get('similarity',0):.3f} | {c.get('category','?')} |")
        competitor_analysis = ReportSection(
            title="Competitor Analysis",
            content_md="\n".join(comp_md_lines) or "No competitors found.",
        )

        funding = intermediate.get("funding", [])
        fund_md_lines = ["| Company | Round | Amount | Date |", "|---|---|---:|---|"]
        for f in funding:
            fund_md_lines.append(f"| {f.get('company','?')} | {f.get('round','?')} | {f.get('amount','?')} | {f.get('date','?')} |")
        funding_landscape = ReportSection(
            title="Funding Landscape",
            content_md="\n".join(fund_md_lines) or "No funding records found.",
        )

        trends = intermediate.get("trends", [])
        trend_lines = []
        for t in trends:
            trend_lines.append(f"- {t.get('title','?')} — {t.get('summary','')} ({t.get('source','')})")
        market_trends = ReportSection(
            title="Market Trends",
            content_md=("\n".join(trend_lines) if trend_lines else "No recent trends found."),
        )

        # Domain-specific SWOT analysis
        swot_content = self._get_domain_swot(parsed.businessDomain, parsed.valueProposition)
        swot_analysis = ReportSection(
            title="SWOT Analysis",
            content_md=swot_content,
        )

        return Report(
            executive_summary=exec_sum,
            competitor_analysis=competitor_analysis,
            funding_landscape=funding_landscape,
            swot_analysis=swot_analysis,
            market_trends=market_trends,
            citations=intermediate.get("citations", []),
        )
    
    def _get_domain_swot(self, domain: str, value_prop: str) -> str:
        swot_data = {
            "Semiconductor Tech": {
                "strength": "AI-driven chip design reduces time-to-market and improves performance optimization",
                "weakness": "High capital requirements and complex manufacturing dependencies",
                "opportunity": "Growing demand for specialized AI chips in edge computing and IoT",
                "threat": "Established players like NVIDIA and Intel with massive R&D budgets"
            },
            "Logistics Tech": {
                "strength": "AI optimization algorithms improve efficiency and reduce costs",
                "weakness": "Integration complexity with existing supply chain systems",
                "opportunity": "E-commerce growth and supply chain digitization trends",
                "threat": "Large logistics companies developing in-house AI solutions"
            },
            "Healthcare Tech": {
                "strength": "AI improves diagnostic accuracy and patient outcomes",
                "weakness": "Regulatory compliance and data privacy requirements",
                "opportunity": "Aging population and increasing healthcare costs drive adoption",
                "threat": "Established medical device companies and regulatory barriers"
            },
            "FinTech": {
                "strength": "AI enables better risk assessment and fraud detection",
                "weakness": "Regulatory compliance and security concerns",
                "opportunity": "Digital banking adoption and embedded finance trends",
                "threat": "Traditional banks investing heavily in digital transformation"
            }
        }
        
        default_swot = {
            "strength": "AI-driven approach provides competitive advantage",
            "weakness": "High development costs and talent acquisition challenges",
            "opportunity": "Growing market demand for AI-powered solutions",
            "threat": "Established competitors with significant resources"
        }
        
        swot = swot_data.get(domain, default_swot)
        
        return (
            f"- Strength: {swot['strength']}\n"
            f"- Weakness: {swot['weakness']}\n"
            f"- Opportunity: {swot['opportunity']}\n"
            f"- Threat: {swot['threat']}\n"
        )

def main():
    if len(sys.argv) != 2:
        print("Usage: python run_agent.py \"Your startup idea description\"")
        print("\nExample:")
        print('python run_agent.py "An AI-powered logistics optimization platform for small e-commerce businesses"')
        sys.exit(1)
    
    idea = sys.argv[1]
    
    print("Market Analyst Agent")
    print("=" * 50)
    print(f"Analyzing: {idea}")
    print("=" * 50)
    
    # Parse input
    ip = InputParser()
    parsed = ip.parse(idea)
    print(f"Parsed: {parsed.businessDomain} targeting {parsed.targetAudience}")
    
    # Run ReAct engine
    re = ReActEngine()
    intermediate = re.run(parsed)
    print("ReAct analysis completed")
    
    # Synthesize report
    sy = Synthesizer()
    report = sy.synthesize(parsed, intermediate)
    print("Report generated")
    print("\n" + "=" * 50)
    
    # Print report
    print(f"# {report.executive_summary.title}\n")
    print(report.executive_summary.content_md)
    print(f"\n## {report.competitor_analysis.title}\n")
    print(report.competitor_analysis.content_md)
    print(f"\n## {report.funding_landscape.title}\n")
    print(report.funding_landscape.content_md)
    print(f"\n## {report.swot_analysis.title}\n")
    print(report.swot_analysis.content_md)
    print(f"\n## {report.market_trends.title}\n")
    print(report.market_trends.content_md)
    if report.citations:
        print("\n## Citations\n")
        for c in report.citations:
            print(f"- {c}")

if __name__ == "__main__":
    main()
