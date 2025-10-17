# -*- coding: utf-8 -*-
from __future__ import annotations

import os
import re
from typing import List

from pydantic import BaseModel

from .schemas import ParsedInput


class InputParser(BaseModel):
    """Parses free-text startup ideas into structured fields.

    Uses an LLM if configured via OPENAI_API_KEY; otherwise falls back to simple heuristics.
    """

    def parse(self, text: str) -> ParsedInput:
        text_norm = text.strip()
        if not text_norm:
            raise ValueError("Input text is empty")

        if os.getenv("OPENAI_API_KEY"):
            try:
                from openai import OpenAI  # type: ignore
            except Exception:
                # Fallback to heuristic if OpenAI SDK is unavailable
                return self._heuristic_parse(text_norm)
            return self._llm_parse(text_norm)
        return self._heuristic_parse(text_norm)

    def _heuristic_parse(self, text: str) -> ParsedInput:
        # Very lightweight heuristics
        lower = text.lower()
        techs = self._extract_keywords(lower, [
            "ai", "ml", "llm", "nlp", "blockchain", "computer vision", "cv",
            "recommendation", "search", "rag", "agent", "optimization",
        ])
        # Domain guess by pattern
        domain = "Logistics Tech" if any(k in lower for k in ["logistic", "supply chain", "delivery"]) else "General Tech"
        audience = "small e-commerce" if "e-commerce" in lower or "ecommerce" in lower else "B2B/B2C"
        value_prop = "optimization" if "optimiz" in lower else (
            "automation" if "autom" in lower else "insights"
        )
        return ParsedInput(
            businessDomain=domain,
            targetAudience=audience,
            keyTechnologies=techs or ["AI"],
            valueProposition=value_prop,
            originalText=text,
        )

    def _extract_keywords(self, text: str, candidates: List[str]) -> List[str]:
        found: List[str] = []
        for cand in candidates:
            pattern = r"\b" + re.escape(cand) + r"\b"
            if re.search(pattern, text):
                found.append(cand.upper())
        return found

    def _llm_parse(self, text: str) -> ParsedInput:
        from openai import OpenAI  # type: ignore

        client = OpenAI()
        prompt = (
            "Extract businessDomain, targetAudience, keyTechnologies (list), valueProposition from:\n" + text
        )
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
        )
        content = resp.choices[0].message.content
        if not content:
            raise RuntimeError("LLM returned empty content")
        import json
        parsed = json.loads(content)
        return ParsedInput(
            businessDomain=parsed.get("businessDomain", "Unknown"),
            targetAudience=parsed.get("targetAudience", "Unknown"),
            keyTechnologies=parsed.get("keyTechnologies", []) or [],
            valueProposition=parsed.get("valueProposition", "Unknown"),
            originalText=text,
        )
