# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import List, Dict, Any

from .schemas import ParsedInput, ThoughtStep, AgentPlan, ToolResult, ToolContext


class ReActEngine:
    def __init__(self, context: ToolContext | None = None) -> None:
        self.context = context or ToolContext()

    def run(self, parsed: ParsedInput) -> Dict[str, Any]:
        plan = AgentPlan(steps=[])

        # Thought 1: find competitors
        step1 = ThoughtStep(thought="Identify competitors based on the parsed description.")
        step1.action = "CompetitorFinder"
        step1.input = {"description": parsed.originalText}
        step1.observation = {"result": {"competitors": [
            {"company": "ShipEase", "similarity": 0.85, "category": "Logistics Tech"},
            {"company": "RouteIQ", "similarity": 0.78, "category": "Logistics Tech"},
            {"company": "Packly", "similarity": 0.72, "category": "Logistics Tech"}
        ]}}
        plan.steps.append(step1)

        # Thought 2: fetch funding for competitors
        step2 = ThoughtStep(thought="Retrieve funding data for identified competitors.")
        step2.action = "FundingRetriever"
        step2.input = {"company_names": ["ShipEase", "RouteIQ", "Packly"]}
        step2.observation = {"result": {"funding": [
            {"company": "ShipEase", "round": "Seed", "amount": 2500000, "date": "2023-06-01"},
            {"company": "ShipEase", "round": "Series A", "amount": 12000000, "date": "2024-02-15"},
            {"company": "RouteIQ", "round": "Seed", "amount": 1800000, "date": "2023-08-20"}
        ]}}
        plan.steps.append(step2)

        # Thought 3: gather market trends
        step3 = ThoughtStep(thought="Fetch recent market trends relevant to the domain and audience.")
        step3.action = "MarketTrendScraper"
        step3.input = {"query": f"Latest market trends in {parsed.businessDomain} for {parsed.targetAudience}"}
        step3.observation = {"result": {"trends": [
            {"title": "Retailers embrace AI for logistics efficiency", "summary": "SMB e-commerce adopt AI routing tools", "source": "TechCrunch"},
            {"title": "Warehouse automation trends 2025", "summary": "Vision systems and robotics reduce packing time", "source": "TechRadar"}
        ]}}
        plan.steps.append(step3)

        return {
            "plan": plan,
            "competitors": step1.observation["result"]["competitors"],
            "funding": step2.observation["result"]["funding"],
            "trends": step3.observation["result"]["trends"],
            "citations": ["https://example.com/shipease", "https://example.com/routeiq", "https://example.com/news1"],
        }
