import json
from pathlib import Path
from typing import Any, Dict, List, Union


BASE_DIR = Path(__file__).resolve().parent


STARTUPS_PROFILE_FILE = BASE_DIR / "Startups_Profile_Dataset.json"
FUNDING_ROUNDS_FILE = BASE_DIR / "Funding_Rounds_Datasets.json"
MARKET_NEWS_FILE = BASE_DIR / "Market&News_Dataset.json"
GROUND_TRUTH_FILE = BASE_DIR / "Ground_Truth_Evaluation_Datasets.json"


def _load_json_file(path: Path) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"Dataset file not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_startups_profile() -> List[Dict[str, Any]]:
    """Load the startups profile dataset as a list of records."""
    data = _load_json_file(STARTUPS_PROFILE_FILE)
    if isinstance(data, dict):
        # If wrapped under a key, flatten to list when possible
        for key in ("data", "records", "items", "startups"):
            if key in data and isinstance(data[key], list):
                return data[key]
        # Fallback: return values if looks like map of startup entries
        return list(data.values())
    return data  # assume list


def load_funding_rounds() -> List[Dict[str, Any]]:
    """Load the funding rounds dataset as a list of records."""
    data = _load_json_file(FUNDING_ROUNDS_FILE)
    if isinstance(data, dict):
        for key in ("data", "records", "items", "rounds", "funding"):
            if key in data and isinstance(data[key], list):
                return data[key]
        return list(data.values())
    return data


def load_market_news() -> List[Dict[str, Any]]:
    """Load the market & news dataset as a list of records."""
    data = _load_json_file(MARKET_NEWS_FILE)
    if isinstance(data, dict):
        for key in ("data", "records", "items", "news", "articles"):
            if key in data and isinstance(data[key], list):
                return data[key]
        return list(data.values())
    return data


def load_ground_truth() -> List[Dict[str, Any]]:
    """Load ground truth evaluation dataset as a list of records."""
    data = _load_json_file(GROUND_TRUTH_FILE)
    if isinstance(data, dict):
        for key in ("data", "records", "items", "ground_truth"):
            if key in data and isinstance(data[key], list):
                return data[key]
        return list(data.values())
    return data


def find_name(item: Dict[str, Any]) -> str:
    """Best-effort extraction of a startup/company name from a record."""
    for key in ("name", "startup_name", "company", "company_name", "brand"):
        v = item.get(key)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return ""


def get_field(item: Dict[str, Any], keys: List[str], default: Any = None) -> Any:
    """Return first non-empty field from possible keys."""
    for k in keys:
        v = item.get(k)
        if v not in (None, ""):
            return v
    return default

