import json
from typing import Dict, Any

from langchain_openai import ChatOpenAI


SCHEMA_DESCRIPTION = {
    "startup_name": "Concise name if provided or inferable.",
    "sector": "Primary sector/industry (e.g., FinTech, HealthTech).",
    "problem": "Core problem the idea addresses (1-2 sentences).",
    "solution": "What the product/service does (1-2 sentences).",
    "target_users": "Main user/customer groups.",
    "features": "Key features as a short list.",
    "region": "Geography focus if mentioned (city/country/region).",
    "keywords": "Short list of topical keywords to aid search.",
}


SYSTEM_PROMPT = (
    "You are an intelligent input parser. "
    "Given a freeform business idea, extract a structured JSON object strictly following this schema: "
    f"{json.dumps(SCHEMA_DESCRIPTION)}. "
    "Return ONLY valid JSON, no commentary. Use empty strings or empty lists when information is missing."
)


def parse_business_idea(llm: ChatOpenAI, idea_text: str) -> Dict[str, Any]:
    """Parse a freeform business idea into a structured JSON dict."""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": idea_text},
    ]
    resp = llm.invoke(messages)
    text = getattr(resp, "content", "{}")
    try:
        data = json.loads(text)
        if not isinstance(data, dict):
            raise ValueError("Parser did not return a JSON object")
    except Exception:
        # Fallback empty structure
        data = {
            "startup_name": "",
            "sector": "",
            "problem": "",
            "solution": "",
            "target_users": [],
            "features": [],
            "region": "",
            "keywords": [],
        }
    return data


# --- ReAct loop schema requested by user ---
REACT_SCHEMA_DESCRIPTION = {
    "core_idea": "One-sentence core idea.",
    "domain": "Primary domain/industry (e.g., HealthTech).",
    "key_features": "Short list of key features.",
    "target_audience": "Main audience segment as a concise phrase.",
}

REACT_SYSTEM_PROMPT = (
    "You are an intelligent input parser for a ReAct loop. "
    "Given a freeform business idea, return ONLY valid JSON exactly matching this schema: "
    f"{json.dumps(REACT_SCHEMA_DESCRIPTION)}. "
    "Do not add extra keys. Use empty string or empty list when missing."
)


def parse_business_idea_react(llm: ChatOpenAI, idea_text: str) -> Dict[str, Any]:
    """Parse a business idea into the ReAct loop JSON schema."""
    messages = [
        {"role": "system", "content": REACT_SYSTEM_PROMPT},
        {"role": "user", "content": idea_text},
    ]
    resp = llm.invoke(messages)
    text = getattr(resp, "content", "{}")
    try:
        data = json.loads(text)
        # Ensure keys exist exactly
        if not isinstance(data, dict):
            raise ValueError("Parser did not return a JSON object")
        for k in ("core_idea", "domain", "key_features", "target_audience"):
            if k not in data:
                raise ValueError("Missing required keys")
    except Exception:
        data = {
            "core_idea": "",
            "domain": "",
            "key_features": [],
            "target_audience": "",
        }
    return data

