import os
import re
import time
import argparse
from typing import Dict, List, Tuple

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from tools import startup_search, competitor_finder, funding_retriever, news_search
from intelligent_parser import parse_business_idea
from prompt_template import build_react_agent_prompt_template_v2
from data_loader import load_startups_profile, load_funding_rounds, load_market_news, get_field, find_name


def build_llm() -> ChatOpenAI:
    load_dotenv()
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    # Auto-detect OpenRouter keys and set base URL accordingly
    if not base_url and api_key and api_key.startswith("sk-or-"):
        base_url = "https://openrouter.ai/api/v1"

    llm = ChatOpenAI(model=model, temperature=0, api_key=api_key, base_url=base_url)
    return llm


def _format_tools_for_prompt() -> str:
    """Produce a simple listing of available tools and their docstrings."""
    tools = [startup_search, competitor_finder, funding_retriever, news_search]
    lines = []
    for t in tools:
        # langchain.tools.Tool exposes name/description
        name = getattr(t, "name", "unknown_tool")
        desc = getattr(t, "description", "")
        lines.append(f"- {name}: {desc}")
    return "\n".join(lines)


def _tool_registry() -> Dict[str, object]:
    return {
        getattr(startup_search, "name", "startup_search"): startup_search,
        getattr(competitor_finder, "name", "competitor_finder"): competitor_finder,
        getattr(funding_retriever, "name", "funding_retriever"): funding_retriever,
        getattr(news_search, "name", "news_search"): news_search,
    }


def _extract_action_and_input(text: str) -> Tuple[str, str]:
    """Parse Action and Action Input from model output.

    Returns (action_name, action_input). Empty action_name indicates final answer or no action.
    """
    final_match = re.search(r"Final Answer\s*:\s*(.+)", text, re.DOTALL)
    if final_match:
        return ("", final_match.group(1).strip())

    action_match = re.search(r"Action\s*:\s*(.+)", text)
    input_match = re.search(r"Action Input\s*:\s*(.+)", text, re.DOTALL)
    if action_match and input_match:
        return (action_match.group(1).strip(), input_match.group(1).strip())
    return ("", "")


def _normalize_action_input(action_input: str) -> str:
    """Return a single string argument for tools from action input.

    Accepts JSON like {"query": "..."} or {"name": "..."}, otherwise returns raw string.
    """
    import json
    try:
        obj = json.loads(action_input)
        if isinstance(obj, dict):
            for key in ("query", "name", "input"):
                v = obj.get(key)
                if isinstance(v, str):
                    return v
        if isinstance(obj, list) and obj and isinstance(obj[0], str):
            return obj[0]
    except Exception:
        pass
    return action_input.strip()


def react_generate_report(llm: ChatOpenAI, input_json_str: str) -> str:
    """Run a strict ReAct loop using the V2 prompt and dataset tools.

    The loop enforces tool whitelist, parses Action/Action Input pairs, executes tools,
    records observations, and stops when Final Answer is produced.
    """
    prompt = build_react_agent_prompt_template_v2()
    scratchpad = ""
    tools_str = _format_tools_for_prompt()

    # The template expects {tools}, {input}, {agent_scratchpad}
    system_prompt = (
        prompt
        .replace("{tools}", tools_str)
        .replace("{input}", input_json_str)
        .replace("{agent_scratchpad}", scratchpad)
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Begin. Follow the ReAct protocol. Output Thought, Action, Action Input."},
    ]
    registry = _tool_registry()
    allowed = set(registry.keys())

    # Iterate Thought→Action→Observation until Final Answer
    for _ in range(12):
        try:
            resp = llm.invoke(messages)
        except Exception as e:
            msg = str(e)
            if "Rate limit" in msg or "429" in msg:
                # Backoff and retry
                time.sleep(25)
                resp = llm.invoke(messages)
            else:
                # Record failure and continue loop
                scratchpad += f"\nObservation: LLM error: {msg}\n"
                messages = [
                    {
                        "role": "system",
                        "content": prompt.replace("{tools}", tools_str).replace("{input}", input_json_str).replace("{agent_scratchpad}", scratchpad)
                    },
                    {"role": "user", "content": "Continue. Output Thought, Action, Action Input or Final Answer."},
                ]
                continue
        text = getattr(resp, "content", str(resp))
        action, action_input = _extract_action_and_input(text)

        # If Final Answer detected, return it
        if action == "" and action_input:
            return action_input

        # If no action parsed, append response to scratchpad and continue once
        if not action:
            scratchpad += f"\n{text}\n"
            # Refresh system with updated scratchpad
            messages = [
                {
                    "role": "system",
                    "content": prompt.replace("{tools}", tools_str).replace("{input}", input_json_str).replace("{agent_scratchpad}", scratchpad)
                },
                {"role": "user", "content": "Continue. Output Thought, Action, Action Input."},
            ]
            continue

        # Enforce tool whitelist
        if action not in allowed:
            scratchpad += f"\nObservation: Disallowed tool '{action}'. Allowed: {sorted(allowed)}\n"
            messages = [
                {
                    "role": "system",
                    "content": prompt.replace("{tools}", tools_str).replace("{input}", input_json_str).replace("{agent_scratchpad}", scratchpad)
                },
                {"role": "user", "content": "Tool not allowed. Re-plan. Output Thought, Action, Action Input."},
            ]
            continue

        # Execute tool
        tool_arg = _normalize_action_input(action_input)
        try:
            output = registry[action].run(tool_arg)
        except Exception as e:
            output = f"{{\"error\": \"Tool execution failed: {str(e)}\"}}"

        # Record observation and continue
        scratchpad += f"\nObservation: {output}\n"
        messages = [
            {
                "role": "system",
                "content": prompt.replace("{tools}", tools_str).replace("{input}", input_json_str).replace("{agent_scratchpad}", scratchpad)
            },
            {"role": "user", "content": "Continue. Output Thought, Action, Action Input or Final Answer."},
        ]

    # Fallback if no Final Answer after iterations
    return "Final Answer: Iteration limit reached before the agent produced a final report. Please retry or provide a slightly more specific input, and ensure rate limits are not active."


def offline_generate_report(input_json_str: str) -> str:
    """Offline fallback: generate a structured Markdown report using only datasets.

    This avoids LLM calls when rate limits are active. It performs simple keyword matching
    against startup profiles, funding rounds, and news to approximate the requested sections.
    """
    import json as _json
    try:
        data = _json.loads(input_json_str)
    except Exception:
        data = {}

    core = (data.get("core_idea") or "").lower()
    domain = (data.get("domain") or "").lower()
    features = data.get("key_features") or []
    audience = data.get("target_audience") or ""
    tokens = set([t for t in (core + " " + domain + " " + " ".join(features)).lower().split() if t])

    startups = load_startups_profile()
    funding = load_funding_rounds()
    news = load_market_news()

    # Match startups by keyword presence in description or tags
    candidates = []
    for item in startups:
        name = find_name(item)
        desc = get_field(item, ["description", "about", "summary"], "") or ""
        tags = get_field(item, ["industry_tags", "tags", "sector"], [])
        text = (desc + " " + (" ".join(tags) if isinstance(tags, list) else str(tags))).lower()
        score = sum(1 for tk in tokens if tk in text)
        if score:
            candidates.append((score, name, item))

    candidates.sort(key=lambda x: x[0], reverse=True)
    top_comps = [
        {"name": c[1], "reason": f"Keyword overlap ({c[0]}) with domain/features"}
        for c in candidates[:5]
    ]

    # Funding summaries for top competitors
    funding_map = {}
    for comp in top_comps:
        comp_name = comp["name"].lower()
        rounds = []
        for fr in funding:
            company = str(get_field(fr, ["company", "startup_name", "name"], "")).lower()
            if comp_name and (company == comp_name or comp_name in company):
                rounds.append({
                    "round": get_field(fr, ["round", "stage"], None),
                    "date": get_field(fr, ["date", "announced_on"], None),
                    "amount": get_field(fr, ["amount", "raised", "value"], None),
                    "investors": get_field(fr, ["investors", "leads"], None),
                })
        funding_map[comp["name"]] = rounds

    # News items via simple keyword matching
    news_hits = []
    for n in news:
        title = get_field(n, ["title", "headline", "news_title"], "") or ""
        summary = get_field(n, ["content", "text", "summary", "body"], "") or ""
        date = get_field(n, ["date", "published_at", "time"], None)
        source = get_field(n, ["source", "publisher", "url"], None)
        text = (title + "\n" + summary).lower()
        score = sum(1 for tk in tokens if tk in text)
        if score:
            news_hits.append((score, {
                "title": title,
                "date": date,
                "source": source,
                "snippet": (title + "\n" + summary)[:400],
            }))
    news_hits.sort(key=lambda x: x[0], reverse=True)
    news_top = [entry for _, entry in news_hits[:5]]

    # Compose Markdown
    lines = []
    lines.append("# Market Intelligence Report")
    lines.append("")
    lines.append("## Idea Summary")
    lines.append(f"- core_idea: {data.get('core_idea', '')}")
    lines.append(f"- domain: {data.get('domain', '')}")
    lines.append("- key_features:")
    for f in features:
        lines.append(f"  - {f}")
    lines.append(f"- target_audience: {audience}")
    lines.append("")
    lines.append("## Market Size & Category")
    lines.append("- Dataset-derived signals only; quantitative TAM/SAM/SOM not available. Qualitative category: sustainable packaging / coffee accessories.")
    lines.append("")
    lines.append("## Competitor Analysis")
    if top_comps:
        for c in top_comps:
            lines.append(f"- {c['name']}: {c['reason']}")
    else:
        lines.append("- No direct competitors found in datasets with keyword matching.")
    lines.append("")
    lines.append("## Funding Landscape")
    if any(funding_map.values()):
        for name, rounds in funding_map.items():
            lines.append(f"- {name}:")
            if rounds:
                for r in rounds[:5]:
                    lines.append(f"  - {r.get('round')} | {r.get('date')} | {r.get('amount')} | investors: {r.get('investors')}")
            else:
                lines.append("  - No funding records found.")
    else:
        lines.append("- No funding records found for matched competitors.")
    lines.append("")
    lines.append("## Recent News Signals")
    if news_top:
        for n in news_top:
            lines.append(f"- {n.get('date')} | {n.get('title')} ({n.get('source')})")
    else:
        lines.append("- No recent relevant news found in datasets via keyword matching.")
    lines.append("")
    lines.append("## Risks & Mitigations")
    lines.append("- Supply chain reliability for biodegradable materials; mitigate via diversified sourcing.")
    lines.append("- Compatibility variability across machine models; mitigate via rigorous testing for top devices.")
    lines.append("- Price sensitivity vs. sustainable premium; mitigate via subscription bundles.")
    lines.append("- Regulatory/standards claims for compostability; mitigate via certification.")
    lines.append("- Brand awareness vs. incumbents; mitigate via partnerships.")
    lines.append("")
    lines.append("## Opportunities & Go-to-Market")
    lines.append("- Partner with eco-conscious coffee brands and retailers.")
    lines.append("- Subscription model with recycling/return incentives.")
    lines.append("- Target workplaces and universities with sustainability initiatives.")
    lines.append("")
    lines.append("## Financial & Traction KPIs to Watch")
    lines.append("- Monthly active subscribers, repeat purchase rate, churn.")
    lines.append("- Gross margin per pod, blended CAC, LTV.")
    lines.append("- Recycling return rate, certification coverage.")
    lines.append("- Distribution partnerships signed.")
    lines.append("- Complaint rate by machine compatibility.")
    lines.append("- Unit economics by channel.")
    lines.append("")
    lines.append("## Final Recommendation")
    lines.append("- Proceed with focused pilot targeting top compatible machines and green retailers; validate pricing and subscription uptake. Expand with certified claims and partnerships.")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Market Survey AI Agent (ReAct)")
    parser.add_argument("--name", type=str, help="Startup name to analyze (non-interactive mode)")
    parser.add_argument("--idea", type=str, help="Freeform business idea to parse and analyze using ReAct")
    parser.add_argument("--idea-json", type=str, help="Already-parsed business idea JSON to analyze using ReAct")
    args = parser.parse_args()

    llm = build_llm()

    if args.idea_json:
        print("Running ReAct with provided idea JSON...\n")
        result = react_generate_report(llm, args.idea_json)
        print("\n===== Market Intelligence Report =====\n")
        print(result)
        print("\n=====================================\n")
        return

    if args.idea:
        print("Parsing idea and running ReAct...\n")
        parsed_json_str = parse_business_idea(args.idea)
        result = react_generate_report(llm, parsed_json_str)
        if result.startswith("Final Answer: Iteration limit"):
            print("\nLLM rate limit or iteration cap reached; running offline dataset-only synthesis...\n")
            result = offline_generate_report(parsed_json_str)
        print("\n===== Market Intelligence Report =====\n")
        print(result)
        print("\n=====================================\n")
        return

    if args.name:
        print("Preparing input JSON and running ReAct...\n")
        # Build a minimal JSON input when only a name is provided
        import json as _json
        minimal = _json.dumps({
            "core_idea": f"Analyze startup: {args.name}",
            "domain": "startup analysis",
            "key_features": [args.name],
            "target_audience": "stakeholders"
        }, ensure_ascii=False)
        result = react_generate_report(llm, minimal)
        print("\n===== Market Intelligence Report =====\n")
        print(result)
        print("\n=====================================\n")
        return

    print("Market Survey AI Agent (ReAct)\n")
    print("Enter a startup name to analyze. Press Ctrl+C to quit.\n")
    try:
        while True:
            name = input("Startup name or paste an idea: ").strip()
            if not name:
                print("Please enter a non-empty name.\n")
                continue
            print("\nRunning ReAct...\n")
            # Detect if input seems like an idea (multi-sentence)
            import json as _json
            if len(name.split()) > 4:
                parsed_json_str = parse_business_idea(name)
                result = react_generate_report(llm, parsed_json_str)
            else:
                minimal = _json.dumps({
                    "core_idea": f"Analyze startup: {name}",
                    "domain": "startup analysis",
                    "key_features": [name],
                    "target_audience": "stakeholders"
                }, ensure_ascii=False)
                result = react_generate_report(llm, minimal)
            print("\n===== Market Intelligence Report =====\n")
            print(result)
            print("\n=====================================\n")
    except KeyboardInterrupt:
        print("\nGoodbye!")


if __name__ == "__main__":
    main()
