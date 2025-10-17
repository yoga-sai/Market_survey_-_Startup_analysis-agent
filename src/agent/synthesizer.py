# -*- coding: utf-8 -*-
from __future__ import annotations

import os
from typing import List, Dict

from .schemas import Report, ReportSection


def _format_swot(competitors: List[Dict], trends: List[Dict]) -> str:
    strength = "AI-driven approach and semantic retrieval enable grounded insights."
    weakness = "Coverage depends on available indexed data; may miss private info."
    opportunity = "Partnerships with data providers; expand to telehealth or B2B."
    threat = "Incumbents with strong brand and proprietary datasets."
    return (
        f"- Strength: {strength}\n"
        f"- Weakness: {weakness}\n"
        f"- Opportunity: {opportunity}\n"
        f"- Threat: {threat}\n"
    )


def _chart_code(competitor_funding: List[Dict]) -> str:
    return (
        "```python\n"
        "import matplotlib.pyplot as plt\n"
        "data = {}\n".format({c.get("company", "?"): c.get("amount", 0) for c in competitor_funding}) +
        "names = list(data.keys()); values = list(data.values())\n"
        "plt.bar(names, values); plt.xticks(rotation=45, ha=\"right\"); plt.tight_layout(); plt.show()\n"
        "```"
    )


class Synthesizer:
    def __init__(self) -> None:
        self.use_llm = bool(os.getenv("OPENAI_API_KEY"))

    def synthesize(self, parsed, intermediate: Dict) -> Report:
        exec_sum = ReportSection(
            title="Executive Summary",
            content_md=(
                f"This report analyzes a startup in {parsed.businessDomain} targeting {parsed.targetAudience}. "
                f"The core value proposition centers on {parsed.valueProposition}.\n"
            ),
        )

        competitors = intermediate.get("competitors", [])
        comp_md_lines = ["| Company | Similarity | Category |", "|---|---:|---|"]
        for c in competitors:
            comp_md_lines.append(f"| {c.get(\"company\",\"?\")} | {c.get(\"similarity\",0):.3f} | {c.get(\"category\",\"?\")} |")
        competitor_analysis = ReportSection(
            title="Competitor Analysis",
            content_md="\n".join(comp_md_lines) or "No competitors found.",
        )

        funding = intermediate.get("funding", [])
        fund_md_lines = ["| Company | Round | Amount | Date |", "|---|---|---:|---|"]
        for f in funding:
            fund_md_lines.append(f"| {f.get(\"company\",\"?\")} | {f.get(\"round\",\"?\")} | {f.get(\"amount\",\"?\")} | {f.get(\"date\",\"?\")} |")
        funding_landscape = ReportSection(
            title="Funding Landscape",
            content_md="\n".join(fund_md_lines) or "No funding records found.",
        )

        trends = intermediate.get("trends", [])
        trend_lines = []
        for t in trends:
            trend_lines.append(f"- {t.get(\"title\",\"?\")} — {t.get(\"summary\",\"\")} ({t.get(\"source\",\"\")})")
        market_trends = ReportSection(
            title="Market Trends",
            content_md=("\n".join(trend_lines) if trend_lines else "No recent trends found."),
        )

        swot_analysis = ReportSection(
            title="SWOT Analysis",
            content_md=_format_swot(competitors, trends),
        )

        chart_snippet = _chart_code([
            {"company": f.get("company"), "amount": f.get("amount") or 0}
            for f in funding[:6]
        ]) if funding else ""
        if chart_snippet:
            funding_landscape.content_md += "\n\n" + chart_snippet

        return Report(
            executive_summary=exec_sum,
            competitor_analysis=competitor_analysis,
            funding_landscape=funding_landscape,
            swot_analysis=swot_analysis,
            market_trends=market_trends,
            citations=intermediate.get("citations", []),
        )
