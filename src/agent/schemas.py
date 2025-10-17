# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ParsedInput(BaseModel):
    businessDomain: str
    targetAudience: str
    keyTechnologies: List[str] = Field(default_factory=list)
    valueProposition: str
    originalText: str


class ThoughtStep(BaseModel):
    thought: str
    action: Optional[str] = None
    input: Optional[Dict[str, Any]] = None
    observation: Optional[Dict[str, Any]] = None


class ToolResult(BaseModel):
    name: str
    data: Dict[str, Any]
    citations: List[str] = Field(default_factory=list)


class AgentPlan(BaseModel):
    steps: List[ThoughtStep] = Field(default_factory=list)


class ReportSection(BaseModel):
    title: str
    content_md: str


class Report(BaseModel):
    executive_summary: ReportSection
    competitor_analysis: ReportSection
    funding_landscape: ReportSection
    swot_analysis: ReportSection
    market_trends: ReportSection
    citations: List[str] = Field(default_factory=list)


class ToolContext(BaseModel):
    # Contextual settings shared across tools (e.g., retrievers, vector stores)
    config: Dict[str, Any] = Field(default_factory=dict)
