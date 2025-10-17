# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import json
from typing import Any

from input_parser import InputParser
from react_engine import ReActEngine
from synthesizer import Synthesizer


def main() -> None:
    parser = argparse.ArgumentParser(description="Market Analyst Agent (ReAct + RAG)")
    parser.add_argument("idea", type=str, help="Plain-text description of a startup idea")
    args = parser.parse_args()

    ip = InputParser()
    parsed = ip.parse(args.idea)
    re = ReActEngine()
    intermediate: dict[str, Any] = re.run(parsed)
    sy = Synthesizer()
    report = sy.synthesize(parsed, intermediate)

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
