"""
intelligent_parser.py
----------------------
Human-friendly, robust parser that transforms a freeform business idea into a
structured JSON schema suitable for a ReAct loop.

What this module does
- Uses an LLM (via `langchain_openai`) to extract four fields:
  - core_idea: One-sentence summary of the idea.
  - domain: Primary domain/industry.
  - key_features: Short list of key features.
  - target_audience: Concise description of the audience.
- Loads configuration from `.env` for API access.
- Enforces schema and normalizes types, returning a clean JSON string.
- Handles common LLM formatting issues (e.g., code fences like ```json ... ```).
- Provides safe fallbacks if parsing or API calls fail.

Environment configuration
- OPENAI_API_KEY: Your API key (required).
- OPENAI_MODEL: The model identifier (recommended; a sensible default is used if not set).
- OPENAI_BASE_URL: Optional custom base URL; auto-detected for OpenRouter keys.

Usage
    from intelligent_parser import parse_business_idea
    json_str = parse_business_idea("My idea...")

Guarantees
- Always returns a JSON string with keys: core_idea, domain, key_features, target_audience.
- On failures, returns a minimal valid JSON string following the schema.
"""

import os
import json
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


# Target schema enforced by the parser
REACT_SCHEMA_KEYS = ("core_idea", "domain", "key_features", "target_audience")

REACT_SCHEMA_DESCRIPTION = {
    "core_idea": "One-sentence core idea.",
    "domain": "Primary domain/industry (e.g., HealthTech).",
    "key_features": "Short list of key features.",
    "target_audience": "Main audience segment as a concise phrase.",
}


def _build_llm() -> ChatOpenAI:
    """Construct a ChatOpenAI client using environment configuration.

    Loads `.env`, reads the API key and model, and optionally sets a base URL
    for providers like OpenRouter when the API key starts with `sk-or-`.

    Returns:
        ChatOpenAI: A configured LLM client ready for invocation.

    Raises:
        RuntimeError: If required environment variables are missing.
    """
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing OPENAI_API_KEY in environment/.env")

    # Use a sensible default if OPENAI_MODEL is not set.
    model = os.getenv("OPENAI_MODEL") or "json-friendly-model"

    base_url = os.getenv("OPENAI_BASE_URL")
    # Auto-detect OpenRouter keys and set base URL accordingly
    if not base_url and api_key.startswith("sk-or-"):
        base_url = "https://openrouter.ai/api/v1"

    return ChatOpenAI(model=model, temperature=0, api_key=api_key, base_url=base_url)


def _ensure_list_of_strings(value: Any) -> List[str]:
    """Normalize a value to a list of strings.

    If `value` is a string, it will be split by commas and trimmed.
    If `value` is a list, non-string items are ignored and strings are trimmed.
    Otherwise, returns an empty list.
    """
    if isinstance(value, str):
        parts = [p.strip() for p in value.split(",")]
        return [p for p in parts if p]
    if isinstance(value, list):
        out: List[str] = []
        for item in value:
            if isinstance(item, str):
                s = item.strip()
                if s:
                    out.append(s)
        return out
    return []


def _fallback_schema() -> Dict[str, Any]:
    """Return a minimal valid schema used when parsing fails."""
    return {
        "core_idea": "",
        "domain": "",
        "key_features": [],
        "target_audience": "",
    }


def _strip_code_fences(text: str) -> str:
    """Remove Markdown code fences from a string if present.

    Handles blocks like ```json ... ``` or ``` ... ``` and returns the inner
    content. If no fences are found, returns the input unchanged.
    """
    import re

    fence_pattern = re.compile(r"```(?:json)?\s*(.*?)\s*```", re.DOTALL | re.IGNORECASE)
    match = fence_pattern.search(text)
    if match:
        return match.group(1).strip()
    return text


def _extract_json_object(text: str) -> Optional[str]:
    """Extract a JSON object substring from arbitrary text.

    Finds the first opening brace and last closing brace and attempts to return
    the substring. Returns None if braces are not found.
    """
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        return text[start : end + 1]
    return None


def parse_business_idea(idea: str) -> str:
    """Parse a freeform business idea into the ReAct loop JSON schema.

    Uses environment configuration and an LLM to extract:
    - core_idea (str): One-sentence summary of the idea.
    - domain (str): Primary domain/industry.
    - key_features (List[str]): Short list of key features.
    - target_audience (str): Concise description of the audience.

    The function enforces a strict JSON schema, performs defensive validation,
    and returns a JSON string. If the LLM invocation or parsing fails, a minimal
    valid JSON string is returned.

    Args:
        idea: The user's freeform description of a business idea.

    Returns:
        A JSON string conforming to the schema with keys: "core_idea",
        "domain", "key_features", "target_audience".
    """
    llm = _build_llm()

    # Build a detailed, humanized prompt within the function.
    system_prompt = (
        "You are an intelligent input parser for a ReAct reasoning loop. "
        "Analyze the user's business idea and return ONLY valid JSON that matches "
        "this exact schema: "
        f"{json.dumps(REACT_SCHEMA_DESCRIPTION)}. "
        "Constraints: \n"
        "- Use these keys exactly: core_idea, domain, key_features, target_audience.\n"
        "- For missing info, use empty string or empty list.\n"
        "- Keep key_features as short, distinct phrases (3–7 items).\n"
        "- Do not include explanations, prose, or extra keys.\n"
        "- Prefer concise, clear phrasing suitable for downstream tools."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": idea},
    ]

    try:
        resp = llm.invoke(messages)
        raw_text = getattr(resp, "content", "{}")

        # Handle markdown code blocks and stray text gracefully
        cleaned = _strip_code_fences(raw_text)
        json_candidate = _extract_json_object(cleaned) or cleaned

        data = json.loads(json_candidate)

        # Ensure we have a dict with all required keys
        if not isinstance(data, dict):
            raise ValueError("Parser did not return a JSON object")
        for key in REACT_SCHEMA_KEYS:
            if key not in data:
                raise ValueError(f"Missing required key: {key}")

        # Normalize types and trim strings
        core_idea = str(data.get("core_idea") or "").strip()
        domain = str(data.get("domain") or "").strip()
        key_features = _ensure_list_of_strings(data.get("key_features"))
        target_audience = str(data.get("target_audience") or "").strip()

        normalized = {
            "core_idea": core_idea,
            "domain": domain,
            "key_features": key_features,
            "target_audience": target_audience,
        }
        return json.dumps(normalized, ensure_ascii=False)

    except Exception:
        # Return a minimal valid schema on any failure
        return json.dumps(_fallback_schema(), ensure_ascii=False)

