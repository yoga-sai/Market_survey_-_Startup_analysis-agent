import json
import uuid
from typing import Any, Dict, List, Tuple

from langchain.tools import tool

from pathlib import Path
from data_loader import (
    load_startups_profile,
    load_funding_rounds,
    load_market_news,
    find_name,
    get_field,
)


# Load datasets once at import time
STARTUPS = load_startups_profile()
FUNDING = load_funding_rounds()
NEWS = load_market_news()


def _doc_id(text: str) -> str:
    # Deterministic id based on text content
    return str(uuid.uuid5(uuid.NAMESPACE_URL, text))

BASE_DIR = Path(__file__).resolve().parent


def _find_startup_record(name: str) -> Dict[str, Any]:
    target = name.strip().lower()
    best: Dict[str, Any] = {}
    for item in STARTUPS:
        n = find_name(item).lower()
        if not n:
            continue
        if n == target:
            return item
        # quick contains match
        if target in n and not best:
            best = item
    return best


def _get_record_id(item: Dict[str, Any]) -> str:
    """Best-effort extraction of a unique ID for a startup record."""
    for key in ("id", "uuid", "startup_id", "company_id"):
        v = item.get(key)
        if isinstance(v, (str, int)):
            return str(v)
    return ""


def _find_startup_by_id(identifier: str) -> Dict[str, Any]:
    ident = str(identifier).strip()
    if not ident:
        return {}
    for item in STARTUPS:
        if _get_record_id(item) == ident:
            return item
    return {}


@tool("startup_search")
def startup_search(name: str) -> str:
    """Find a startup profile by name. Returns JSON with key 'profile'."""
    record = _find_startup_record(name)
    if not record:
        return json.dumps({"profile": None, "message": f"No profile found for '{name}'"})

    # Optionally select common fields
    profile = {
        "name": find_name(record),
        "description": get_field(record, ["description", "about", "summary"], None),
        "website": get_field(record, ["website", "url"], None),
        "location": get_field(record, ["location", "hq", "city"], None),
        "sector": get_field(record, ["sector", "industry", "category"], None),
        "competitors": get_field(record, ["competitors"], []),
        "extra": record,
    }

    return json.dumps({"profile": profile})


@tool("competitor_finder")
def competitor_finder(name: str) -> str:
    """Find competitors for a startup by name. Returns JSON list under 'competitors'."""
    record = _find_startup_record(name)
    if not record:
        return json.dumps({"competitors": [], "message": f"No profile found for '{name}'"})

    # Prefer explicit competitors if present
    explicit = record.get("competitors")
    results: List[Dict[str, Any]] = []
    if isinstance(explicit, list) and explicit:
        for comp in explicit:
            results.append({"name": comp, "reason": "Listed as competitor in profile"})

    # Map competitor_ids -> names when available
    comp_ids = record.get("competitor_ids")
    if isinstance(comp_ids, list) and comp_ids:
        for cid in comp_ids:
            other = _find_startup_by_id(cid)
            if other:
                results.append({
                    "name": find_name(other),
                    "reason": "Linked via competitor_ids",
                })

    # Heuristic: same sector/industry/category
    sector = get_field(record, ["sector", "industry", "category"], None)
    if sector:
        for item in STARTUPS:
            if item is record:
                continue
            other_sector = get_field(item, ["sector", "industry", "category"], None)
            if other_sector and str(other_sector).lower() == str(sector).lower():
                results.append({
                    "name": find_name(item),
                    "reason": f"Operates in the same sector: {sector}",
                })

    # Deduplicate by name
    dedup: Dict[str, Dict[str, Any]] = {}
    for r in results:
        n = (r.get("name") or "").strip()
        if n and n not in dedup:
            dedup[n] = r

    return json.dumps({"competitors": list(dedup.values())})


@tool("funding_retriever")
def funding_retriever(name: str) -> str:
    """Retrieve funding rounds for a startup by name. Returns JSON list under 'funding'."""
    target = name.strip().lower()
    rounds: List[Dict[str, Any]] = []
    for item in FUNDING:
        company = get_field(item, ["company", "startup_name", "name"], "").strip().lower()
        if not company:
            continue
        if company == target or target in company:
            rounds.append({
                "round": get_field(item, ["round", "stage"], None),
                "date": get_field(item, ["date", "announced_on"], None),
                "amount": get_field(item, ["amount", "raised", "value"], None),
                "investors": get_field(item, ["investors", "leads"], None),
                "raw": item,
            })

    # Sort by date descending if available
    def _date_key(r: Dict[str, Any]):
        d = r.get("date")
        return str(d) if d is not None else ""

    rounds.sort(key=_date_key, reverse=True)
    return json.dumps({"funding": rounds})


@tool("news_search")
def news_search(query: str) -> str:
    """Lightweight keyword-based news search over the dataset.

    Returns JSON list under 'news' with fields: title, date, source, startup, snippet.
    """
    if not query or not query.strip():
        return json.dumps({"news": [], "message": "Empty query"})

    q = query.strip().lower()
    scored: List[Tuple[int, Dict[str, Any]]] = []
    for item in NEWS:
        title = get_field(item, ["title", "headline", "news_title"], "") or ""
        summary = get_field(item, ["content", "text", "summary", "body"], "") or ""
        date = get_field(item, ["date", "published_at", "time"], None)
        source = get_field(item, ["source", "publisher", "url"], None)
        related = get_field(item, ["startup", "company", "startup_name", "name"], None)

        text = (title + "\n" + summary).lower()
        score = 0
        # crude keyword scoring: occurrences of tokens
        for token in set(q.split()):
            if token and token in text:
                score += 1
        if score:
            scored.append((score, {
                "title": title,
                "date": date,
                "source": source,
                "startup": related,
                "snippet": (title + "\n" + summary)[:400],
            }))

    scored.sort(key=lambda x: x[0], reverse=True)
    items = [entry for _, entry in scored[:5]]
    return json.dumps({"news": items})
